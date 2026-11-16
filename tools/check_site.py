#!/usr/bin/env python3
"""Release checks for the static Gymnasium No. 4 demonstration site."""
import datetime as dt
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PUBLISHED_HTML = [
    "index.html", "404.html", "history.html", "sveden.html", "parents.html",
    "students.html", "news.html", "news-editor.html", "priem.html",
    "contacts.html", "school-life.html", "admin.html",
]
REQUIRED = PUBLISHED_HTML + [
    "assets/css/style.css", "assets/js/app.js", "assets/img/favicon.svg",
    "assets/js/news.js", "assets/js/news-editor.js", "assets/js/school-life.js",
    "assets/js/admin-demo.js", "assets/js/content-review.js",
    "assets/data/news.json", "assets/data/partners.json",
    "assets/data/school-life.json", "robots.txt", ".nojekyll",
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
errors = []


def err(file_name, message):
    errors.append(f"{file_name}: {message}")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.idrefs = []
        self.h1 = 0
        self.in_title = False
        self.has_title = False
        self.lang = None
        self.main = 0
        self.has_skip_link = False
        self.has_viewport = False
        self.images_without_alt = []
        self.external_blank_without_rel = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.in_title = True
        if tag == "main":
            self.main += 1
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src", "(без src)"))
        if tag == "a":
            if "skip-link" in attrs.get("class", "").split():
                self.has_skip_link = True
            if attrs.get("target") == "_blank":
                rel = set(attrs.get("rel", "").lower().split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.external_blank_without_rel.append(attrs.get("href", "(без href)"))
        for attr in ("aria-controls", "aria-labelledby", "aria-describedby", "for"):
            if attrs.get(attr):
                self.idrefs.extend((tag, attr, token) for token in attrs[attr].split())
        if tag in ("a", "link", "script", "img"):
            for key in ("href", "src"):
                if key in attrs:
                    self.refs.append((tag, key, attrs[key]))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.has_title = True


for required_file in REQUIRED:
    if not (ROOT / required_file).is_file():
        err(required_file, "отсутствует обязательный файл")

if (ROOT / "tools" / "check_site.py").is_file():
    if not (ROOT / ".github" / "workflows" / "pages.yml").is_file():
        err(".github/workflows/pages.yml", "нет workflow проверки и публикации")

actual_root_html = {p.name for p in ROOT.glob("*.html")}
allowed_root_html = set(PUBLISHED_HTML)
for extra in sorted(actual_root_html - allowed_root_html):
    err(extra, "не входит в список опубликованных страниц")
for missing in sorted(allowed_root_html - actual_root_html):
    err(missing, "страница из списка публикации отсутствует")

pages = [ROOT / name for name in PUBLISHED_HTML if (ROOT / name).is_file()]
parsed = {}
for page in pages:
    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    parsed[page.name] = parser

    if parser.lang != "ru":
        err(page.name, 'нет lang="ru"')
    if not parser.has_title:
        err(page.name, "пустой <title>")
    if parser.h1 != 1:
        err(page.name, f"ожидался один <h1>, найдено {parser.h1}")
    if parser.main != 1:
        err(page.name, f"ожидался один <main>, найдено {parser.main}")
    if not parser.has_viewport:
        err(page.name, "нет meta viewport для мобильных устройств")
    if not parser.has_skip_link:
        err(page.name, "нет ссылки перехода к основному содержимому")
    for image_src in parser.images_without_alt:
        err(page.name, f"изображение без alt: {image_src}")
    for reference in parser.external_blank_without_rel:
        err(page.name, f'target="_blank" без rel="noopener noreferrer": {reference}')
    duplicates = {item for item in parser.ids if parser.ids.count(item) > 1}
    if duplicates:
        err(page.name, f"повторяющиеся id: {sorted(duplicates)}")
    if EMOJI.search(source):
        err(page.name, "найден декоративный emoji-символ; используйте согласованный SVG/CSS")

for page_name, parser in parsed.items():
    known_ids = set(parser.ids)
    for tag, attr, token in parser.idrefs:
        if token not in known_ids:
            err(page_name, f"{tag}[{attr}] ссылается на отсутствующий id: {token}")
    for tag, key, reference in parser.refs:
        url = urlparse(reference)
        if url.scheme.lower() in ("javascript", "vbscript"):
            err(page_name, f"небезопасная схема URL в {tag}[{key}]: {reference}")
            continue
        if url.scheme == "data":
            if tag in ("script", "a"):
                err(page_name, f"data URI не разрешён для {tag}: {reference[:60]}")
            continue
        if tag == "a" and (url.scheme in ("mailto", "tel", "http", "https") or reference.startswith("//")):
            continue
        if url.scheme in ("http", "https") or reference.startswith("//"):
            err(page_name, f"внешний ресурс запрещён для {tag}: {reference}")
            continue
        if url.scheme:
            err(page_name, f"неподдерживаемая схема URL в {tag}[{key}]: {reference}")
            continue
        target_name = page_name if not url.path else unquote(url.path).lstrip("/")
        target = (ROOT / target_name).resolve()
        if not target.exists():
            err(page_name, f"битая ссылка или ресурс: {reference}")
            continue
        if url.fragment and target.suffix == ".html":
            target_parser = parsed.get(target.name)
            target_ids = target_parser.ids if target_parser else []
            if url.fragment not in target_ids:
                err(page_name, f"нет якоря #{url.fragment} в {target.name}")

for css_file in (ROOT / "assets" / "css").glob("*.css"):
    css_source = css_file.read_text(encoding="utf-8")
    if css_source.count("{") != css_source.count("}"):
        err(str(css_file.relative_to(ROOT)), "несбалансированные фигурные скобки CSS")
    for match in re.finditer(r"url\(([^)]+)\)", css_source):
        value = match.group(1).strip("'\" ")
        if value.startswith(("http", "//")):
            err(str(css_file.relative_to(ROOT)), f"внешний url(): {value}")
        elif not value.startswith("data:") and not (css_file.parent / value).exists():
            err(str(css_file.relative_to(ROOT)), f"нет файла url(): {value}")

def load_json(relative):
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err(relative, f"не удалось прочитать JSON: {exc}")
        return {}

news = load_json("assets/data/news.json")
if not isinstance(news.get("posts"), list):
    err("assets/data/news.json", "ожидается массив posts")
else:
    for index, post in enumerate(news["posts"], 1):
        label = f"assets/data/news.json: posts[{index}]"
        if not isinstance(post, dict) or not str(post.get("title", "")).strip():
            err(label, "нет заголовка")
            continue
        try:
            dt.date.fromisoformat(post.get("date", ""))
        except (TypeError, ValueError):
            err(label, "некорректная дата YYYY-MM-DD")
        if post.get("category") not in ("news", "events", "announcements"):
            err(label, "неизвестная категория")
        source = post.get("sourceUrl", "")
        if source and urlparse(source).scheme not in ("http", "https"):
            err(label, "sourceUrl должен использовать HTTP(S)")
        image = post.get("imageUrl", "")
        if image:
            parsed_image = urlparse(image)
            if parsed_image.scheme not in ("", "http", "https") or image.startswith("//"):
                err(label, "imageUrl должен быть HTTPS или локальным путём")
            elif not parsed_image.scheme and not (ROOT / image.lstrip("/")).is_file():
                err(label, f"локальное изображение не найдено: {image}")

partners = load_json("assets/data/partners.json")
if not isinstance(partners.get("partners"), list):
    err("assets/data/partners.json", "ожидается массив partners")
else:
    for index, partner in enumerate(partners["partners"], 1):
        if not isinstance(partner, dict) or not str(partner.get("name", "")).strip():
            err(f"assets/data/partners.json: partners[{index}]", "нет названия")

life = load_json("assets/data/school-life.json")
for field in ("events", "bellTimes", "achievements"):
    if not isinstance(life.get(field, []), list):
        err("assets/data/school-life.json", f"{field} должен быть массивом")
if not isinstance(life.get("classes", {}), dict):
    err("assets/data/school-life.json", "classes должен быть объектом")

if errors:
    print("Найдены проблемы:")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print(f"OK: проверено страниц — {len(pages)}, локальных ресурсов, JSON и ссылок; проблем не найдено.")
