#!/usr/bin/env python3
"""Проверка статического сайта: ссылки, якоря, id, заголовки и ресурсы.

Python нужен только для этого инструмента, а не для работы сайта.
"""
import re
import sys
import pathlib
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REQUIRED = [
    "index.html", "404.html", "assets/css/style.css", "assets/js/app.js",
    "assets/img/favicon.svg", ".nojekyll",
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
        self.h1 = 0
        self.in_title = False
        self.has_title = False
        self.lang = None
        self.main = 0
        self.has_skip_link = False
        self.images_without_alt = []

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
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src", "(без src)"))
        if tag == "a" and "skip-link" in attrs.get("class", "").split():
            self.has_skip_link = True
        if tag in ("a", "link", "script", "img"):
            for key in ("href", "src"):
                if key in attrs:
                    self.refs.append((tag, attrs[key]))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.has_title = True


for required_file in REQUIRED:
    if not (ROOT / required_file).is_file():
        err(required_file, "отсутствует обязательный файл")

# Workflow обязателен в корне репозитория, но не входит в опубликованный _site.
if (ROOT / "tools" / "check_site.py").is_file():
    if not (ROOT / ".github" / "workflows" / "pages.yml").is_file():
        err(".github/workflows/pages.yml", "нет workflow проверки и публикации")

pages = sorted(ROOT.glob("*.html"))
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
    if not parser.has_skip_link:
        err(page.name, "нет ссылки перехода к основному содержанию")
    for image_src in parser.images_without_alt:
        err(page.name, f"изображение без alt: {image_src}")
    duplicates = {item for item in parser.ids if parser.ids.count(item) > 1}
    if duplicates:
        err(page.name, f"повторяющиеся id: {sorted(duplicates)}")
    if EMOJI.search(source):
        err(page.name, "найден эмодзи или декоративный символ")
    if "fonts.googleapis" in source or re.search(
        r'<(script|link|img)[^>]+(src|href)="https?://', source
    ):
        err(page.name, "внешний шрифт, скрипт или изображение")

for page_name, parser in parsed.items():
    for tag, reference in parser.refs:
        url = urlparse(reference)
        if url.scheme in ("mailto", "tel", "http", "https") or reference.startswith("//"):
            continue
        target_name = page_name if not url.path else url.path
        target = (ROOT / unquote(target_name)).resolve()
        if not target.exists():
            err(page_name, f"битая ссылка: {reference}")
            continue
        if url.fragment and target.suffix == ".html":
            target_parser = parsed.get(target.name)
            target_ids = target_parser.ids if target_parser else []
            if url.fragment not in target_ids:
                err(page_name, f"нет якоря #{url.fragment} в {target.name}")

for css_file in (ROOT / "assets" / "css").glob("*.css"):
    css_source = css_file.read_text(encoding="utf-8")
    for match in re.finditer(r"url\(([^)]+)\)", css_source):
        value = match.group(1).strip("'\" ")
        if value.startswith(("http", "//")):
            err(str(css_file.relative_to(ROOT)), f"внешний url(): {value}")
        elif not value.startswith("data:") and not (css_file.parent / value).exists():
            err(str(css_file.relative_to(ROOT)), f"нет файла url(): {value}")

if errors:
    print("Найдены проблемы:")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print(f"OK: проверено страниц — {len(pages)}, проблем не найдено.")
