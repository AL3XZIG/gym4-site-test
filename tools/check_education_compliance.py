#!/usr/bin/env python3
"""Structural and accessibility checks for the education-organization demo.

This is a project quality gate, not a legal certification or a content-truth checker.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "sveden.html"
ROUTES_DIR = ROOT / "sveden"
APP_JS = ROOT / "assets" / "js" / "app.js"
CSS = ROOT / "assets" / "css" / "style.css"
PUBLIC_PAGES = [
    "index.html", "history.html", "sveden.html", "parents.html",
    "students.html", "news.html", "priem.html", "school-life.html",
    "election.html", "contacts.html",
]
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
    "fullName", "shortName", "regDate", "nameUchred", "uchredLaw",
    "addressUchred", "telUchred", "mailUchred", "websiteUchred",
    "address", "workTime", "telephone", "email", "licenseDocLink",
    "structOrgUprav", "rucovodstvo", "rucovodstvoZam",
    "eduAccred", "eduOp", "eduName", "eduLevel", "eduProf",
    "eduForm", "learningTerm", "eduPrac", "eduPred", "opMain",
    "educationPlan", "educationShedule", "educationRpd", "methodology", "accreditationDocLink", "eduFedDoc",
    "teachingStaff", "purposeFacil", "purposeFacilOvz", "purposeSport", "ovz",
    "hostelInfo", "interInfo", "hostelNum", "interNum",
    "hostelNumOvz", "interNumOvz", "objName", "objAddress", "objOvz",
    "meals", "health", "grant", "support", "paidEdu", "paidDog", "comNet", "erList", "techOvz", "hostelInterOvz",
    "finPlanDocLink", "vacant", "numberBFVacant", "numberBRVacant",
    "numberBMVacant", "numberPVacant",
}
KNOWN_PENDING_MICRODATA = {
    "languageEl", "eduPred", "educationRpd", "methodology", "paidSt", "purposeCab", "purposePrac", "purposeLibr", "comNetOvz", "erListOvz",
    "finBFVolume", "finBRVolume", "finBMVolume", "finPVolume",
    "volume", "internationalDog",
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
        self.images_without_alt = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            section_id = attrs.get("id")
            if section_id:
                if self.section_stack:
                    self.nesting_errors.append(
                        f"Вложенная секция #{section_id} внутри #{self.section_stack[-1]}"
                    )
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
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
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


def fail_if(condition, message, errors):
    if condition:
        errors.append(message)


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
        errors.append(
            f"Заголовок #{section_id}: ожидалось {expected_title!r}, получено {actual!r}"
        )

for itemprop in sorted(CORE_MICRODATA - parser.itemprops):
    errors.append(f"Нет обязательной/используемой микроразметки itemprop={itemprop}")

pending_microdata = sorted(KNOWN_PENDING_MICRODATA - parser.itemprops)

for url in sorted(MINISTRY_URLS - parser.links):
    errors.append(f"Нет обязательной ссылки на {url}")

if parser.section_stack:
    errors.append(f"Не закрыты секции: {parser.section_stack}")
errors.extend(parser.nesting_errors)
if parser.images_without_alt:
    errors.append(f"Изображений без атрибута alt: {parser.images_without_alt}")
if not parser.demo_banner or "Демонстрационная версия" not in source:
    errors.append("Должна сохраняться явная маркировка демонстрационной версии")

# Verify the whole public site exposes both 200% text scaling and a way to stop motion.
for page_name in PUBLIC_PAGES:
    path = ROOT / page_name
    if not path.is_file():
        errors.append(f"Не найдена публичная страница {page_name}")
        continue
    page = path.read_text(encoding="utf-8")
    if 'data-fs="200"' not in page:
        errors.append(f"{page_name}: нет управления масштабом текста до 200%")
    if 'data-motion="off"' not in page:
        errors.append(f"{page_name}: нет управления отключением анимации")
    if 'id="a11yPanel"' not in page or 'id="a11yToggle"' not in page:
        errors.append(f"{page_name}: отсутствует панель доступности")
    if 'name="viewport"' not in page:
        errors.append(f"{page_name}: отсутствует meta viewport")
    if '<title>' not in page:
        errors.append(f"{page_name}: отсутствует title страницы")

if not APP_JS.is_file() or 'data-font-scale' not in APP_JS.read_text(encoding="utf-8"):
    errors.append("app.js: нет синхронизации состояния масштаба текста")
if not APP_JS.is_file() or 'data-motion' not in APP_JS.read_text(encoding="utf-8"):
    errors.append("app.js: нет управления режимом анимации")
if not CSS.is_file() or 'html[data-font-scale="200"]' not in CSS.read_text(encoding="utf-8"):
    errors.append("style.css: нет правил перестроения интерфейса при масштабе 200%")
if not CSS.is_file() or 'html[data-motion="off"]' not in CSS.read_text(encoding="utf-8"):
    errors.append("style.css: нет глобального отключения анимации")

# A placeholder is not a valid email address and must not be exposed as email microdata.
if 'itemprop="email">Требуется подтвердить' in source:
    errors.append("Плейсхолдер ошибочно размечен как itemprop=email")


# Validate all separately addressable Sveden pages generated from the single source.
ROUTE_MAP = {
    "common": ("common", "Основные сведения"),
    "struct": ("structure", "Структура и органы управления образовательной организацией"),
    "document": ("documents", "Документы"),
    "education": ("education", "Образование"),
    "eduStandarts": ("standards", "Образовательные стандарты и требования"),
    "managers": ("management", "Руководство"),
    "employees": ("teachers", "Педагогический состав"),
    "objects": ("facilities", "Материально-техническое обеспечение и оснащённость образовательного процесса. Доступная среда"),
    "paid_edu": ("paid", "Платные образовательные услуги"),
    "budget": ("finance", "Финансово-хозяйственная деятельность"),
    "vacant": ("vacancies", "Вакантные места для приёма (перевода) обучающихся"),
    "grants": ("grants", "Стипендии и меры поддержки обучающихся"),
    "inter": ("international", "Международное сотрудничество"),
    "catering": ("food", "Организация питания в образовательной организации"),
}
if not (ROUTES_DIR / "index.html").is_file():
    errors.append("Нет индексной страницы /sveden/")
for slug, (section_id, expected_title) in ROUTE_MAP.items():
    route = ROUTES_DIR / slug / "index.html"
    if not route.is_file():
        errors.append(f"Нет страницы /sveden/{slug}/")
        continue
    route_source = route.read_text(encoding="utf-8")
    route_parser = AuditParser()
    route_parser.feed(route_source)
    if section_id not in route_parser.section_ids:
        errors.append(f"/sveden/{slug}/: отсутствует секция #{section_id}")
    if route_parser.headings.get(section_id) != expected_title:
        errors.append(f"/sveden/{slug}/: заголовок подраздела не совпадает")
    if 'itemprop="copy"' not in route_source:
        errors.append(f"/sveden/{slug}/: отсутствует itemprop=copy")
    if 'aria-label="Подразделы сведений"' not in route_source:
        errors.append(f"/sveden/{slug}/: отсутствует общая навигация")
    for required in ('data-fs="200"', 'data-motion="off"', 'name="viewport"', '<title>'):
        if required not in route_source:
            errors.append(f"/sveden/{slug}/: отсутствует {required}")

if errors:
    print("FAIL: структурная/доступностная проверка демо-сайта")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"PASS: {len(REQUIRED)} подразделов, навигация, расширенная микроразметка, "
    f"{len(PUBLIC_PAGES)} публичных страниц, масштаб 200% и отключение анимации."
)
if pending_microdata:
    print("WARN: следующие сведения требуют отдельных подписанных документов или подтверждения:")
    for itemprop in pending_microdata:
        print(f"- itemprop={itemprop}")
print(
    "NOTE: проверка не сертифицирует соответствие постановлению № 102. "
    "Нужны реальные тесты клавиатурой/экранным диктором, reflow при 200%, "
    "контрастности и доступности PDF."
)
print(
    "NOTE: полнота и достоверность школьных документов, кадровых/финансовых "
    "данных, питания и вакансий подтверждаются только администрацией."
)
