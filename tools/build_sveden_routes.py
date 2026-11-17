#!/usr/bin/env python3
"""Generate the official /sveden/<slug>/ subsection URLs from sveden.html."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sveden.html"
OUT = ROOT / "sveden"
ROUTES = [
    ("common", "Основные сведения", "common"),
    ("struct", "Структура и органы управления образовательной организацией", "structure"),
    ("document", "Документы", "documents"),
    ("education", "Образование", "education"),
    ("eduStandarts", "Образовательные стандарты и требования", "standards"),
    ("managers", "Руководство", "management"),
    ("employees", "Педагогический состав", "teachers"),
    ("objects", "Материально-техническое обеспечение и оснащённость образовательного процесса. Доступная среда", "facilities"),
    ("paid_edu", "Платные образовательные услуги", "paid"),
    ("budget", "Финансово-хозяйственная деятельность", "finance"),
    ("vacant", "Вакантные места для приёма (перевода) обучающихся", "vacancies"),
    ("grants", "Стипендии и меры поддержки обучающихся", "grants"),
    ("inter", "Международное сотрудничество", "international"),
    ("catering", "Организация питания в образовательной организации", "food"),
]
ROOT_PAGES = ["index.html", "history.html", "sveden.html", "parents.html", "students.html",
              "news.html", "priem.html", "school-life.html", "election.html", "contacts.html"]

def extract_section(source, section_id):
    match = re.search(r'<section\b(?=[^>]*\bid="' + re.escape(section_id) + r'")[^>]*>', source, re.I)
    if not match:
        raise ValueError("Missing section " + section_id)
    depth = 0
    for tag in re.finditer(r"</?section\b[^>]*>", source[match.start():], re.I):
        if tag.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return source[match.start():match.start() + tag.end()]
        else:
            depth += 1
    raise ValueError("Unclosed section " + section_id)

def fix_links(text, prefix):
    for page in ROOT_PAGES:
        text = text.replace('href="' + page + '"', 'href="' + prefix + page + '"')
    text = text.replace('href="assets/', 'href="' + prefix + 'assets/')
    text = text.replace('src="assets/', 'src="' + prefix + 'assets/')
    return text

def nav(current):
    labels = ["Основные сведения", "Структура и органы управления", "Документы", "Образование",
              "Образовательные стандарты и требования", "Руководство", "Педагогический состав",
              "Материально-техническое обеспечение и доступная среда", "Платные образовательные услуги",
              "Финансово-хозяйственная деятельность", "Вакантные места", "Стипендии и меры поддержки",
              "Международное сотрудничество", "Организация питания"]
    items = []
    for number, route in enumerate(ROUTES):
        slug, label, section_id = route
        active = ' aria-current="page"' if slug == current else ""
        items.append('<li><a href="../' + slug + '/"' + active + '><span>' +
                     str(number + 1).zfill(2) + '</span>' + labels[number] + '</a></li>')
    return ('<aside class="page-aside"><div class="aside-panel"><span class="aside-caption">СВЕДЕНИЯ ОБ ОБРАЗОВАТЕЛЬНОЙ ОРГАНИЗАЦИИ</span>'
            '<nav aria-label="Подразделы сведений"><ul>' + ''.join(items) + '</ul></nav></div>'
            '<div class="aside-help"><span>Нужна помощь?</span><p>Приёмная директора: <a href="tel:+78512500567">(8512) 50-05-67</a>.</p>'
            '<a href="../../contacts.html">Контакты гимназии →</a></div></aside>')

def page(source, slug, title, section_id):
    body = source.index("<body>") + 6
    header_end = source.index("</header>", body) + 9
    header = fix_links(source[body:header_end], "../../")
    header = header.replace('id="a11yToggle"', 'id="a11yToggle" itemprop="copy"')
    footer_start = source.index('<footer class="site-footer">')
    footer_end = source.index("</footer>", footer_start) + 9
    footer = fix_links(source[footer_start:footer_end], "../../")
    head = source[:body].replace('href="assets/', 'href="../../assets/').replace('src="assets/', 'src="../../assets/')
    head = re.sub(r"<title>.*?</title>", "<title>" + title + " — Сведения об образовательной организации</title>", head, flags=re.S)
    section = extract_section(source, section_id)
    for target_slug, _, target_id in ROUTES:
        section = section.replace('href="#' + target_id + '"', 'href="../' + target_slug + '/"')
    hero = ('<section class="inner-hero"><div class="wrap inner-hero__grid"><div>'
            '<nav class="crumbs" aria-label="Навигационная цепочка"><a href="../../index.html">Главная</a>'
            '<span aria-hidden="true"> / </span><a href="../../sveden.html">Сведения об образовательной организации</a>'
            '<span aria-hidden="true"> / </span><span>' + title + '</span></nav>'
            '<p class="eyebrow">Официальная информация</p><h1>' + title + '</h1>'
            '<p class="inner-hero__lead">Обязательные сведения об образовательной организации.</p></div>'
            '<div class="inner-hero__index" aria-hidden="true"><span>ГИМНАЗИЯ</span><strong>04</strong><span>АСТРАХАНЬ</span></div></div></section>')
    main = ('<main id="main" tabindex="-1">' + hero + '<div class="wrap page-main"><div class="page-layout">'
            + nav(slug) + '<div class="page-content"><div class="page-intro"><span class="page-intro__label">ИНФОРМАЦИОННЫЙ РАЗДЕЛ</span>'
            '<p>' + title + '. Информация представлена в текстовом формате и сопровождается ссылками на документы.</p></div>'
            + section + '<div class="page-end"><span>ГИМНАЗИЯ № 4 · АСТРАХАНЬ</span><a href="#main">Вернуться к началу ↑</a></div>'
            '</div></div></div></main>')
    return head + header + main + footer + "</body></html>\n"

def index_page(source):
    body = source.index("<body>") + 6
    header_end = source.index("</header>", body) + 9
    header = fix_links(source[body:header_end], "../")
    header = header.replace('id="a11yToggle"', 'id="a11yToggle" itemprop="copy"')
    footer_start = source.index('<footer class="site-footer">')
    footer_end = source.index("</footer>", footer_start) + 9
    footer = fix_links(source[footer_start:footer_end], "../")
    head = source[:body].replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    head = re.sub(r"<title>.*?</title>", "<title>Сведения об образовательной организации — Гимназия № 4</title>", head, flags=re.S)
    cards = []
    for i, (slug, title, _) in enumerate(ROUTES, 1):
        cards.append('<a class="feature-card" href="' + slug + '/"><span class="feature-kicker">Подраздел ' +
                     str(i).zfill(2) + '</span><h2>' + title + '</h2><span>Открыть сведения →</span></a>')
    hero = ('<section class="inner-hero"><div class="wrap inner-hero__grid"><div>'
            '<nav class="crumbs" aria-label="Навигационная цепочка"><a href="../index.html">Главная</a>'
            '<span aria-hidden="true"> / </span><span>Сведения об образовательной организации</span></nav>'
            '<p class="eyebrow">Официальная информация</p><h1>Сведения об образовательной организации</h1>'
            '<p class="inner-hero__lead">Подразделы официального информационного раздела гимназии.</p></div>'
            '<div class="inner-hero__index" aria-hidden="true"><span>ГИМНАЗИЯ</span><strong>04</strong><span>АСТРАХАНЬ</span></div></div></section>')
    main = ('<main id="main" tabindex="-1">' + hero + '<div class="wrap page-main"><div class="page-content">'
            '<div class="page-intro"><span class="page-intro__label">ИНФОРМАЦИОННЫЙ РАЗДЕЛ</span>'
            '<p>Выберите подраздел. Все страницы доступны без регистрации.</p></div>'
            '<div class="feature-grid feature-grid--2">' + ''.join(cards) + '</div>'
            '<p class="editor-note">Демонстрационная версия. Содержание и документы требуют подтверждения администрацией.</p>'
            '</div></div></main>')
    return head + header + main + footer + "</body></html>\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = SOURCE.read_text(encoding="utf-8")
    generated = {OUT / "index.html": index_page(source)}
    for slug, title, section_id in ROUTES:
        generated[OUT / slug / "index.html"] = page(source, slug, title, section_id)
    stale = []
    for path, content in generated.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("FAIL: stale generated pages:\n" + "\n".join(stale))
        return 1
    print("PASS: generated 14 recommended subsection URLs and the /sveden/ index.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
