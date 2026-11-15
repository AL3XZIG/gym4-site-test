from pathlib import Path
import json

SOURCE = Path(__file__).resolve().parent
OUT = SOURCE / "site"
for d in ["assets/css", "assets/js"]:
    (OUT / d).mkdir(parents=True, exist_ok=True)

NAV = [("index.html","Главная"),("sveden.html","Сведения"),("parents.html","Родителям"),
       ("students.html","Ученикам"),("news.html","Новости"),("priem.html","Приём"),("contacts.html","Контакты")]

SHELL = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Гимназия №4, Астрахань</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#182742">
<meta property="og:title" content="{title} — Гимназия №4">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{page}">
<div class="ambient" aria-hidden="true"></div>
<div id="progress" class="progress" aria-hidden="true"></div>
<a class="skip-link" href="#main">Перейти к содержимому</a>
<div class="topbar"><div class="container topbar-in">
  <span class="topbar-name">ДЕМОНСТРАЦИОННАЯ ВЕРСИЯ · не официальный сайт · сведения требуют проверки</span>
  <div class="topbar-actions">
    <button id="a11yBtn" class="topbar-btn" aria-expanded="false" aria-controls="a11yPanel">👁 Версия для слабовидящих</button>
    <a class="topbar-btn" href="contacts.html">💬 Обратная связь · демо</a>
  </div>
</div></div>
<div id="a11yPanel" class="a11y-panel" hidden>
  <div class="a11y-head"><b>Настройки доступности</b><button id="a11yClose" class="icon-btn" aria-label="Закрыть">✕</button></div>
  <label class="a11y-label" for="fsRange">Размер шрифта: <span id="fsValue">100%</span></label>
  <input id="fsRange" type="range" min="100" max="160" step="5" value="100">
  <p class="a11y-label">Цветовая схема</p>
  <div class="scheme-row">
    <button class="scheme on" data-scheme="" title="Основная">Ц</button>
    <button class="scheme scheme-bw" data-scheme="bw" title="Чёрным по белому">Ц</button>
    <button class="scheme scheme-wb" data-scheme="wb" title="Белым по чёрному">Ц</button>
    <button class="scheme scheme-blue" data-scheme="blue" title="Синяя">Ц</button>
  </div>
  <label class="a11y-label toggle"><input id="motionToggle" type="checkbox" checked> Анимации и плавная прокрутка</label>
  <button id="a11yReset" class="btn btn-small btn-line">Обычная версия</button>
</div>
<header id="siteHeader"><div class="container head-in">
  <a class="logo" href="index.html"><span class="logo-badge">4</span><span class="logo-text">Гимназия №4<small>Астрахань · макет сайта</small></span></a>
  <button class="burger" id="burger" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">☰</button>
  <nav id="nav" aria-label="Основная навигация">{nav}<a class="btn btn-gold nav-mobile-cta" href="priem.html#first">Приём в 1 класс</a></nav>
  <a class="btn btn-gold nav-cta" href="priem.html#first">Приём</a>
</div></header>
{body}
<footer><div class="container footer-grid">
  <div><p class="footer-logo">Гимназия №4</p><p>Демонстрационный макет информационного сайта образовательной организации.</p><p class="footer-demo">Неофициальная демонстрация интерфейса. Фактические сведения требуют проверки и согласования.</p></div>
  <div><p class="footer-title">Разделы</p><a href="sveden.html">Сведения об ОУ</a><a href="parents.html">Родителям</a><a href="students.html">Ученикам</a><a href="news.html">Новости</a><a href="priem.html">Приём</a><a href="styleguide.html">Дизайн-система</a></div>
  <div><p class="footer-title">Контактная информация</p><p>Адрес, телефон, электронная почта и часы работы будут внесены после проверки администрацией.</p><a href="contacts.html">Открыть раздел контактов</a></div>
</div><div class="container footer-bottom"><span>© <span id="year"></span> Демонстрационный макет</span><span>GitHub Pages demo · HTML / CSS / JS</span></div></footer>
<button id="toTop" class="to-top" aria-label="Наверх">↑</button>
<div class="cookie" id="cookie" hidden><span>Демо-версия использует локальное хранилище только для настроек доступности. Формы ничего не отправляют.</span><button id="cookieOk" class="btn btn-small btn-gold">Принять</button></div>
<div id="toast" class="toast" role="status" aria-live="polite"><span id="toastText"></span><button id="toastAction" class="toast-action" hidden></button></div>
<script src="assets/js/app.js"></script>
</body>
</html>
'''

def hero(title, sub="", kicker="Раздел сайта"):
    return ('<section class="page-hero" data-mood="blue"><div class="container">'
            '<p class="crumbs"><a href="index.html">Главная</a><span> / </span>' + title + '</p>'
            '<p class="kicker">' + kicker + '</p><h1>' + title + '</h1>'
            + ('<p class="lead">' + sub + '</p>' if sub else '') + '</div></section>')

def page(fname, title, desc, body):
    nav = "".join('<a href="' + f + '"' + (' class="active" aria-current="page"' if f == fname else '') + '>' + t + '</a>' for f, t in NAV)
    (OUT / fname).write_text(SHELL.format(title=title, desc=desc, nav=nav, body=body, page=fname.replace(".html", "")), encoding="utf-8")

for relative in ("css/style.css", "js/app.js"):
    source_asset = SOURCE / "assets" / relative
    target_asset = OUT / "assets" / relative
    target_asset.parent.mkdir(parents=True, exist_ok=True)
    target_asset.write_bytes(source_asset.read_bytes())
(OUT / "assets/favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#182742"/><path d="M10 50h44" stroke="#e8b54a" stroke-width="3" stroke-linecap="round"/><text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="38" font-weight="700" fill="#e8b54a">4</text></svg>', encoding="utf-8")

# ---------------- СТРАНИЦЫ ДЕМОНСТРАЦИИ ----------------
def placeholder(title, description="Материал будет добавлен после проверки и согласования администрацией гимназии."):
    return (
        '<section class="card placeholder-card">'
        '<span class="badge badge-gold">ЗАГЛУШКА ДЛЯ ЗАПОЛНЕНИЯ</span>'
        '<h3>' + title + '</h3><p>' + description + '</p>'
        '<p class="placeholder-owner">Ответственный: назначается администрацией · Статус: ожидает заполнения</p>'
        '</section>'
    )

def section(title, intro, items):
    cards = ''.join(placeholder(name, desc) for name, desc in items)
    return '<section class="content-section"><h2>' + title + '</h2><p class="lead">' + intro + '</p><div class="grid">' + cards + '</div></section>'

def table_placeholder(title, columns, rows=3):
    head = ''.join('<th>' + c + '</th>' for c in columns)
    body = ''.join('<tr>' + ''.join('<td><span class="badge badge-gold">Заполнить</span></td>' for _ in columns) + '</tr>' for _ in range(rows))
    return '<section class="content-section"><h2>' + title + '</h2><div class="card table-wrap"><table><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table><p class="placeholder-owner">Таблица-шаблон. Данные не являются фактическими.</p></div></section>'

def layout(title, intro, content, kicker="Информационный раздел"):
    return hero(title, intro, kicker) + '<main id="main" class="container">' + '<div class="note note-info"><b>Демонстрационный макет.</b> Содержимое ниже — структура будущего раздела, а не официальная информация. Перед публикацией требуется проверка и заполнение.</div>' + content + '</main>'

# Главная: демонстрационная витрина разделов, без вымышленных новостей и реквизитов.
home = '''<section class="hero" data-mood="gold"><div class="aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div><div class="container">
<p class="kicker">Демонстрационный макет сайта</p>
<h1>Гимназия №4 — <em>информационный портал</em></h1>
<p class="lead">Современная структура школьного сайта: сведения об образовательной организации, информация для родителей и учеников, новости, документы и приём.</p>
<div class="hero-actions"><a class="btn btn-gold" href="sveden.html">Сведения о гимназии</a><a class="btn btn-ghost" href="priem.html">Раздел приёма</a></div>
<p class="hero-note">Это не официальный сайт. Все поля, отмеченные как заглушки, предназначены для заполнения и согласования.</p>
<div class="stats"><div class="stat"><b>01</b><span>Проверенные сведения</span></div><div class="stat"><b>02</b><span>Новости и объявления</span></div><div class="stat"><b>03</b><span>Документы и материалы</span></div><div class="stat"><b>04</b><span>Информация для семей</span></div></div>
</div></section>
<div class="ticker"><div class="ticker-track"><span><b>ДЕМО</b> · Макет интерфейса</span><span><b>РАЗДЕЛЫ</b> · Навигация работает</span><span><b>КОНТЕНТ</b> · Требует заполнения</span><span><b>БЕЗОПАСНОСТЬ</b> · Формы ничего не отправляют</span><span><b>ДЕМО</b> · Макет интерфейса</span><span><b>РАЗДЕЛЫ</b> · Навигация работает</span><span><b>КОНТЕНТ</b> · Требует заполнения</span><span><b>БЕЗОПАСНОСТЬ</b> · Формы ничего не отправляют</span></div></div>
<main id="main" class="container">
<div class="note note-info"><b>Для просмотра:</b> выберите любой раздел. Внутренние страницы уже имеют общую шапку, навигацию, хлебные крошки, подвал и места для будущего контента.</div>
<h2>Разделы сайта</h2>
<div class="grid">
<a class="card" href="sveden.html"><span class="ico">🏫</span><h3>Сведения об образовательной организации</h3><p>Основные сведения, структура, документы, образование, руководство, педагогический состав и материальная база.</p><span class="badge badge-gold">Открыть раздел →</span></a>
<a class="card" href="parents.html"><span class="ico">👨‍👩‍👧</span><h3>Родителям</h3><p>Памятки, питание, безопасность, школьная жизнь, порядок обращений и полезные материалы.</p><span class="badge badge-gold">Открыть раздел →</span></a>
<a class="card" href="students.html"><span class="ico">🎓</span><h3>Ученикам</h3><p>Расписание, олимпиады, конкурсы, внеурочная деятельность, библиотека и ученическое самоуправление.</p><span class="badge badge-gold">Открыть раздел →</span></a>
<a class="card" href="news.html"><span class="ico">📰</span><h3>Новости и объявления</h3><p>Лента публикаций с датой, категорией, кратким описанием и ссылкой на полный материал.</p><span class="badge badge-gold">Открыть раздел →</span></a>
<a class="card" href="priem.html"><span class="ico">📝</span><h3>Приём в гимназию</h3><p>Порядок приёма, сроки, перечни документов, вакантные места и ответы на вопросы.</p><span class="badge badge-gold">Открыть раздел →</span></a>
<a class="card" href="contacts.html"><span class="ico">📍</span><h3>Контакты</h3><p>Адрес, схема проезда, телефоны, электронная почта, часы работы и способы связи.</p><span class="badge badge-gold">Открыть раздел →</span></a>
</div>
<h2>Что предусмотрено в макете</h2>
<div class="grid">
<section class="card"><span class="ico">♿</span><h3>Доступность</h3><p>Настройка размера шрифта, контрастные схемы, клавиатурный фокус и поддержка reduced motion.</p></section>
<section class="card"><span class="ico">📱</span><h3>Адаптивность</h3><p>Макет перестраивается под мобильные телефоны, планшеты и широкие экраны.</p></section>
<section class="card"><span class="ico">🛠️</span><h3>Передача администратору</h3><p>Разделы подготовлены к наполнению. Архитектура будущей серверной версии описана отдельно.</p></section>
</div>
</main>'''
page("index.html", "Главная", "Демонстрационный макет информационного сайта гимназии.", home)

sveden = section("Основные сведения", "Реквизиты и общая информация об образовательной организации.", [
("Полное и сокращённое наименование", "Официальное наименование, сокращённое название и организационно-правовая форма."),
("Дата создания и история", "Подтверждённая дата основания, историческая справка и архивные материалы."),
("Место нахождения и режим работы", "Юридический и фактический адрес, график работы и часы приёма."),
("Контактные данные", "Телефон, электронная почта и официальные интернет-ресурсы."),
]) + section("Структура и органы управления", "Сведения об органах управления и структурных подразделениях.", [
("Структура управления", "Схема управления, коллегиальные органы и распределение полномочий."),
("Руководство", "ФИО, должности, часы приёма и официальные контакты — после подтверждения."),
("Педагогический состав", "Список педагогов, образование, квалификация и преподаваемые дисциплины."),
]) + section("Образование", "Программы, учебные планы и календарные графики.", [
("Образовательные программы", "Уровни образования, формы обучения, нормативные сроки и языки обучения."),
("Учебные планы", "Утверждённые учебные планы и аннотации рабочих программ."),
("Календарный учебный график", "Актуальный график учебного года и каникул."),
]) + table_placeholder("Материально-техническое обеспечение", ["Объект / ресурс", "Описание", "Доступность"], 4) + section("Документы", "Список локальных актов и обязательных документов с датой и ссылкой на файл.", [
("Устав и лицензия", "Загрузить актуальные документы, проверить сроки и реквизиты."),
("Правила внутреннего распорядка", "Опубликовать утверждённые правила для обучающихся и родителей."),
("Отчёты и предписания", "Добавить документы, подлежащие официальному размещению."),
])
page("sveden.html", "Сведения об образовательной организации", "Структура раздела сведений об образовательной организации.", layout("Сведения об образовательной организации", "Структурированный раздел для обязательных сведений, документов и материалов.", sveden, "Образовательная организация"))

parents = section("Полезная информация", "Материалы для родителей и законных представителей обучающихся.", [
("Организация питания", "Меню, стоимость, льготное питание, поставщик и порядок обратной связи."),
("Безопасность детей", "Памятки по дорожной, пожарной, информационной и антитеррористической безопасности."),
("Психолого-педагогическая помощь", "Порядок записи, часы консультаций и контакты ответственных специалистов."),
("Медицинское сопровождение", "Порядок медицинского обслуживания и согласованные памятки."),
("Школьная форма и принадлежности", "Утверждённые требования и рекомендации, если они действуют."),
("Родительские собрания", "График собраний, повестки и материалы для родителей."),
]) + table_placeholder("Памятки и документы для родителей", ["Название материала", "Дата обновления", "Файл"], 5) + section("Обратная связь", "Здесь будут размещены официальные способы связи и порядок подачи обращений.", [
("Порядок обращения", "Кому и каким способом направлять вопрос; сроки рассмотрения и ответственный."),
("Часто задаваемые вопросы", "Ответы на типовые вопросы после согласования с администрацией."),
])
page("parents.html", "Родителям", "Информационный раздел для родителей и законных представителей.", layout("Родителям", "Материалы, документы и полезные сведения для семей обучающихся.", parents, "Семья и школа"))

students = section("Учебный процесс", "Раздел для обучающихся: актуальная информация и учебные материалы.", [
("Расписание занятий", "Ссылка на утверждённое расписание или подключённую систему расписания."),
("График каникул", "Даты каникул на текущий учебный год после утверждения."),
("Электронный дневник", "Официальная ссылка и инструкция по входу без сбора логинов на демо-сайте."),
("Библиотека и электронные ресурсы", "Каталог, правила пользования и проверенные образовательные ресурсы."),
]) + section("Внеурочная деятельность", "Кружки, секции, проекты и события школьной жизни.", [
("Олимпиады и конкурсы", "Календарь, положения, сроки и результаты — только после публикации организатором."),
("Кружки и секции", "Название, руководитель, возраст, время занятий и порядок записи."),
("Проектная деятельность", "Темы проектов, конференции, требования и архив работ."),
("Ученическое самоуправление", "Органы самоуправления, состав, планы и контакты."),
]) + section("Поддержка ученика", "Справочные материалы и безопасные каналы получения помощи.", [
("Профориентация", "Материалы о выборе профессии, днях открытых дверей и поступлении."),
("Психологическая поддержка", "Контакты и порядок обращения к школьному специалисту."),
("Правила и памятки", "Правила поведения, цифровая безопасность и действия в экстренных ситуациях."),
])
page("students.html", "Ученикам", "Информация для обучающихся гимназии.", layout("Ученикам", "Учебные материалы, расписание, проекты и школьная жизнь.", students, "Обучающимся"))

news = section("Новости гимназии", "В этом блоке будут появляться проверенные публикации с датой, изображением и автором.", [
("Карточка новости №1", "Заглушка публикации. Добавить заголовок, дату, краткий текст, изображение и ссылку на подробную страницу."),
("Карточка новости №2", "Заглушка объявления. Указать срок действия и ответственного за актуальность."),
("Карточка новости №3", "Заглушка события. Добавить подтверждённые сведения и материалы."),
]) + section("Объявления", "Срочные сообщения и важные уведомления с датой публикации и сроком актуальности.", [
("Объявление №1", "Текст объявления и срок действия будут внесены редактором."),
("Объявление №2", "Текст объявления и срок действия будут внесены редактором."),
])
page("news.html", "Новости и объявления", "Шаблон ленты новостей и объявлений гимназии.", layout("Новости и объявления", "Публикации, события и важные сообщения. Сейчас здесь размещены только редакционные заглушки.", news, "Новости"))

priem = section("Поступление в первый класс", "Порядок приёма, сроки и перечень документов должны быть сверены с действующими правилами.", [
("Порядок подачи заявления", "Добавить актуальный порядок, способы подачи заявления и ссылки на официальные сервисы."),
("Сроки приёмной кампании", "Указать даты после утверждения и проверки нормативных документов."),
("Необходимые документы", "Разместить утверждённый перечень документов и требования к копиям."),
]) + section("Перевод и приём в другие классы", "Порядок зачисления при наличии свободных мест.", [
("Наличие свободных мест", "Добавить актуальные сведения по параллелям с датой обновления."),
("Порядок перевода", "Пошаговая инструкция и список документов."),
("Ответы на вопросы", "Ответы приёмной комиссии после согласования."),
]) + table_placeholder("Вакантные места", ["Класс / параллель", "Количество мест", "Дата актуальности"], 5)
page("priem.html", "Приём в гимназию", "Шаблон раздела о приёме и зачислении обучающихся.", layout("Приём в гимназию", "Порядок поступления, документы, сроки и сведения о вакантных местах.", priem, "Поступающим"))

contacts = section("Контактная информация", "Реквизиты и контакты будут внесены только после сверки с администрацией.", [
("Адрес гимназии", "Указать подтверждённый почтовый и фактический адрес."),
("Телефоны", "Указать официальные номера и назначение каждого телефона."),
("Электронная почта", "Указать адреса для общих вопросов и отдельных направлений."),
("Часы работы и приём граждан", "Опубликовать график работы и часы личного приёма."),
]) + section("Как добраться", "Схема проезда, ориентиры и доступность входа будут добавлены после проверки.", [
("Схема расположения", "Добавить карту или схему с проверенными координатами."),
("Общественный транспорт", "Добавить маршруты и остановки после проверки."),
("Доступная среда", "Описать доступность входов и помещений на основании фактической проверки."),
]) + '''<section class="content-section"><h2>Демонстрация формы обращения</h2><div class="card form"><div class="note note-info">Форма показана только для демонстрации интерфейса. Она не отправляет, не сохраняет и не передаёт введённые данные.</div><form id="fbForm"><label for="demoTopic">Тема обращения</label><select id="demoTopic"><option>Выберите тему</option><option>Общий вопрос</option><option>Приём в гимназию</option><option>Документы</option></select><label for="demoMessage">Текст сообщения</label><textarea id="demoMessage" rows="4" placeholder="Поле для демонстрации — не вводите реальные персональные данные"></textarea><button class="btn btn-gold" type="submit">Проверить демонстрацию</button><p class="placeholder-owner">После нажатия появится уведомление, что сообщение не отправлено.</p></form></div></section>'''
page("contacts.html", "Контакты", "Шаблон контактной информации и демонстрация безопасной формы.", layout("Контакты", "Адрес, телефоны, электронная почта и способы связи будут заполнены после проверки.", contacts, "Связь с гимназией"))

style = section("Визуальная система", "Единый набор цветов, типографики и компонентов для дальнейшей разработки.", [
("Цветовая палитра", "Чернильный синий, тёплый светлый фон и золотой акцент."),
("Типографика", "Заголовки с выразительной антиквой, основной текст — нейтральный гротеск."),
("Компоненты", "Карточки, кнопки, таблицы, уведомления и формы с едиными состояниями."),
("Адаптивность и доступность", "Мобильная сетка, контраст, фокус, клавиатура и reduced motion."),
])
page("styleguide.html", "Дизайн-система", "Описание визуальной системы демонстрационного сайта.", layout("Дизайн-система", "Внутренний раздел для разработки и согласования визуального языка.", style, "Для разработчиков"))

notfound = '''<section class="page-hero" data-mood="red"><div class="container"><p class="kicker">Ошибка 404</p><h1>Страница не найдена</h1><p class="lead">Возможно, ссылка устарела или была введена с ошибкой.</p></div></section><main id="main" class="container"><section class="card"><p>Вернитесь на главную или выберите раздел сайта.</p><p><a class="btn btn-gold" href="index.html">На главную</a> <a class="btn btn-line" href="news.html">Новости</a> <a class="btn btn-line" href="contacts.html">Контакты</a></p></section></main>'''
page("404.html", "Страница не найдена", "Ошибка 404 — страница не найдена.", notfound)


# ---------------- СЛУЖЕБНЫЕ ФАЙЛЫ ----------------
(OUT / ".nojekyll").write_text("", encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
(OUT / "site.webmanifest").write_text(json.dumps({
    "name": "Гимназия №4 — демо", "short_name": "Гимназия №4", "start_url": ".",
    "display": "standalone", "background_color": "#f5efe3", "theme_color": "#182742",
    "icons": [{"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]
}, ensure_ascii=False, indent=2), encoding="utf-8")

(OUT / "README.md").write_text("""# Gymnasium No. 4 — static demo

Предварительный редизайн интерфейса. Это не официальный сайт. Новости и сведения в макете демонстрационные либо требуют проверки администрацией.

## Запуск

Нужен Python 3.10+; сторонние Python-пакеты и npm не требуются.

    python build_demo.py
    python -m http.server 8000 --directory site

Откройте http://localhost:8000.

Форма только демонстрирует интерфейс: данные не отправляются и не сохраняются. Перед передачей администрации проверьте адреса, телефоны, ФИО, расписания, документы, ссылки, образовательные сведения и права на изображения.
""", encoding="utf-8")

print(f"Generated {len(list(OUT.glob('*.html')))} HTML pages in {OUT}")
