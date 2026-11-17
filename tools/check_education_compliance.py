#!/usr/bin/env python3
"""Structural checks for the education-organization disclosure section.

This is a project quality gate, not a legal certification or a content-truth checker.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "sveden.html"
REQUIRED = {
    "common": "Основные сведения",
    "structure": "Структура и органы управления образовательной организацией",
    "documents": "Документы",
    "education": "Образование",
    "standards": "Образовательные стандарты и требования",
    "management": "Руководство",
    "teachers": "Педагогический состав",
    "facilities": "Материально-техническое обеспечение и оснащённость образовательного процесса. Доступная среда",
    "paid": "Платные образовательные услуги",
    "finance": "Финансово-хозяйственная деятельность",
    "vacancies": "Вакантные места для приёма (перевода) обучающихся",
    "grants": "Стипендии и меры поддержки обучающихся",
    "international": "Международное сотрудничество",
    "food": "Организация питания в образовательной организации",
}
CORE_MICRODATA = {
    "fullName", "shortName", "nameUchred", "uchredLaw",
    "address", "workTime", "telephone", "email",
    "structOrgUprav", "rucovodstvo", "rucovodstvoZam",
}
MINISTRY_URLS = {"https://edu.gov.ru/", "https://minobrnauki.gov.ru/"}


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_stack = []
        self.section_ids = set()
        self.section_links = set()
        self.itemprops = set()
        self.headings = {}
        self.current_h2 = None
        self.h2_text = []
        self.links = set()
        self.demo_banner = False
        self.nesting_errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            section_id = attrs.get("id")
            if section_id:
                if self.section_stack:
                    self.nesting_errors.append(f"Вложенная секция #{section_id} внутри #{self.section_stack[-1]}")
                self.section_ids.add(section_id)
                self.section_stack.append(section_id)
            else:
                self.section_stack.append("(без id)")
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.section_links.add(attrs["href"][1:])
        if tag == "a" and attrs.get("href"):
            self.links.add(attrs["href"])
        if attrs.get("itemprop"):
            self.itemprops.add(attrs["itemprop"])
        if tag == "h2":
            self.current_h2 = self.section_stack[-1] if self.section_stack else None
            self.h2_text = []
        if "demo-strip" in attrs.get("class", "").split():
            self.demo_banner = True

    def handle_endtag(self, tag):
        if tag == "h2" and self.current_h2:
            self.headings[self.current_h2] = "".join(self.h2_text).strip()
            self.current_h2 = None
            self.h2_text = []
        if tag == "section":
            if not self.section_stack:
                self.nesting_errors.append("Лишний закрывающий </section>")
            else:
                self.section_stack.pop()

    def handle_data(self, data):
        if self.current_h2:
            self.h2_text.append(data)


if not PAGE.is_file():
    print("FAIL: sveden.html не найден", file=sys.stderr)
    raise SystemExit(1)

source = PAGE.read_text(encoding="utf-8")
parser = AuditParser()
parser.feed(source)
errors = []

for section_id, expected_title in REQUIRED.items():
    if section_id not in parser.section_ids:
        errors.append(f"Нет обязательной секции #{section_id}")
    if section_id not in parser.section_links:
        errors.append(f"Нет навигационной ссылки на #{section_id}")
    actual = parser.headings.get(section_id, "")
    if actual != expected_title:
        errors.append(f"Заголовок #{section_id}: ожидалось {expected_title!r}, получено {actual!r}")

for itemprop in sorted(CORE_MICRODATA - parser.itemprops):
    errors.append(f"Нет базовой микроразметки itemprop={itemprop}")

for url in sorted(MINISTRY_URLS - parser.links):
    errors.append(f"Нет обязательной ссылки на {url}")

if parser.section_stack:
    errors.append(f"Не закрыты секции: {parser.section_stack}")
errors.extend(parser.nesting_errors)
if not parser.demo_banner or "Демонстрационная версия" not in source:
    errors.append("Должна сохраняться явная маркировка демонстрационной версии")

if errors:
    print("FAIL: проверка структуры раздела «Сведения об образовательной организации»")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PASS: {len(REQUIRED)} обязательных/условных подразделов, навигация, базовая микроразметка и ссылки на федеральные органы.")
print("NOTE: это структурная проверка; полнота и достоверность документов/сведений проверяются отдельно.")
