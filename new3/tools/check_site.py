#!/usr/bin/env python3
"""Проверка статического сайта: ссылки, якоря, id, заголовки, внешние ресурсы.

Только стандартная библиотека Python. Для работы самого сайта Python не нужен;
скрипт используется в GitHub Actions и вручную перед публикацией:

    python3 tools/check_site.py            # проверить корень репозитория
    python3 tools/check_site.py _site      # проверить указанный каталог
"""
import re, sys, pathlib
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REQUIRED = ["index.html", "404.html", "assets/css/style.css", "assets/js/app.js", "assets/img/favicon.svg"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
errors = []

def err(f, msg): errors.append(f"{f}: {msg}")

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.refs = []; self.h1 = 0; self.title = False
        self.has_title = False; self.lang = None; self.main = 0; self.skip = False; self.imgs = []
    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a: self.ids.append(a["id"])
        if tag == "html": self.lang = a.get("lang")
        if tag == "h1": self.h1 += 1
        if tag == "title": self.title = True
        if tag == "main": self.main += 1
        if tag == "img" and not a.get("alt") and a.get("alt") != "": self.imgs.append(a.get("src"))
        if tag == "a" and a.get("class") == "skip-link": self.skip = True
        for k in ("href", "src"):
            if k in a and tag in ("a", "link", "script", "img"): self.refs.append((tag, a[k]))
    def handle_endtag(self, tag):
        if tag == "title": self.title = False
    def handle_data(self, d):
        if self.title and d.strip(): self.has_title = True

for r in REQUIRED:
    if not (ROOT / r).is_file(): errors.append(f"отсутствует обязательный файл {r}")

pages = sorted(ROOT.glob("*.html"))
parsed = {}
for f in pages:
    txt = f.read_text(encoding="utf-8"); p = P(); p.feed(txt); parsed[f.name] = p
    if p.lang != "ru": err(f.name, "нет lang=\"ru\"")
    if not p.has_title: err(f.name, "пустой <title>")
    if p.h1 != 1: err(f.name, f"ожидался один <h1>, найдено {p.h1}")
    if p.main != 1: err(f.name, f"ожидался один <main>, найдено {p.main}")
    if not p.skip: err(f.name, "нет ссылки «Перейти к основному содержанию»")
    for s in p.imgs: err(f.name, f"изображение без alt: {s}")
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: err(f.name, f"повторяющиеся id: {sorted(dup)}")
    if EMOJI.search(txt): err(f.name, "найден эмодзи или декоративный символ")
    if "fonts.googleapis" in txt or re.search(r'<(script|link|img)[^>]+(src|href)="https?://', txt):
        err(f.name, "внешний ресурс (шрифт, скрипт или изображение с другого домена)")

for name, p in parsed.items():
    for tag, ref in p.refs:
        u = urlparse(ref)
        if u.scheme in ("mailto", "tel", "http", "https") or ref.startswith("//"):
            continue
        target = name if not u.path else u.path
        t = (ROOT / unquote(target)).resolve()
        if not t.exists(): err(name, f"битая ссылка: {ref}"); continue
        if u.fragment and t.suffix == ".html":
            ids = parsed.get(t.name).ids if t.name in parsed else []
            if u.fragment not in ids: err(name, f"нет якоря #{u.fragment} в {t.name}")

for f in ROOT.glob("assets/css/*.css"):
    for m in re.finditer(r"url\(([^)]+)\)", f.read_text(encoding="utf-8")):
        u = m.group(1).strip("'\" ")
        if u.startswith(("http", "//")): err(str(f.relative_to(ROOT)), f"внешний url(): {u}")
        elif not u.startswith("data:") and not (f.parent / u).exists(): err(str(f.relative_to(ROOT)), f"нет файла url(): {u}")

if errors:
    print("Найдены проблемы:"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"OK: проверено страниц — {len(pages)}, проблем не найдено.")
