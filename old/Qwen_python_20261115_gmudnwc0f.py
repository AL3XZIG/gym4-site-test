from pathlib import Path

OUT = Path("gym4-project")
(OUT / "assets/css").mkdir(parents=True, exist_ok=True)
(OUT / "assets/js").mkdir(parents=True, exist_ok=True)

NAV = [("index.html", "Главная"), ("sveden.html", "Сведения об ОУ"), ("parents.html", "Родителям"),
       ("students.html", "Ученикам"), ("news.html", "Новости"), ("contacts.html", "Контакты")]

SHELL = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Гимназия №4, Астрахань</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{page}">
<a class="skip-link" href="#main">Перейти к содержимому</a>
<div class="topbar"><div class="container topbar-in">
  <span class="topbar-name">МБОУ г. Астрахани «Гимназия №4»</span>
  <div class="topbar-actions">
    <button id="a11yBtn" class="topbar-btn" aria-expanded="false" aria-controls="a11yPanel">👁 Версия для слабовидящих</button>
    <a class="topbar-btn" href="https://pos.gosuslugi.ru/form" target="_blank" rel="noopener">💬 Решаем вместе</a>
  </div>
</div></div>

<div id="a11yPanel" class="a11y-panel" hidden>
  <div class="a11y-head"><b>Настройки доступности</b><button id="a11yClose" class="icon-btn" aria-label="Закрыть">✕</button></div>
  <label class="a11y-label" for="fsRange">Размер шрифта: <span id="fsValue">100%</span></label>
  <input id="fsRange" type="range" min="100" max="160" step="5" value="100">
  <p class="a11y-label">Цветовая схема</p>
  <div class="scheme-row">
    <button class="scheme on" data-scheme="">Ц</button>
    <button class="scheme scheme-bw" data-scheme="bw">Ц</button>
    <button class="scheme scheme-wb" data-scheme="wb">Ц</button>
    <button class="scheme scheme-blue" data-scheme="blue">Ц</button>
  </div>
  <button id="a11yReset" class="btn btn-small btn-line">Обычная версия</button>
</div>

<header id="siteHeader"><div class="container head-in">
  <a class="logo" href="index.html"><span class="logo-badge">4</span><span class="logo-text">Гимназия №4<small>Астрахань · школа ЮНЕСКО · с 1964 года</small></span></a>
  <button class="burger" id="burger" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">☰</button>
  <nav id="nav" aria-label="Основная навигация">{nav}</nav>
  <a class="btn btn-gold nav-cta" href="priem.html">Приём</a>
</div></header>

{body}

<footer><div class="container footer-grid">
  <div><p class="footer-logo">Гимназия №4</p><p>Ассоциированная школа ЮНЕСКО. Углублённое изучение английского языка. Входит в топ-100 образовательных учреждений России.</p></div>
  <div><p class="footer-title">Разделы</p><a href="sveden.html">Сведения об ОУ</a><a href="parents.html">Родителям</a><a href="students.html">Ученикам</a><a href="news.html">Новости</a><a href="priem.html">Приём</a></div>
  <div><p class="footer-title">Контакты</p><p>414024, г. Астрахань,<br>ул. Б. Хмельницкого, 16, корп. 1</p><a href="tel:+78512500567">(8512) 50-05-67</a><a href="mailto:gimn4@obr.astrobl.ru">gimn4@obr.astrobl.ru</a><a class="footer-guide" href="styleguide.html">🎨 Дизайн-система проекта</a></div>
</div><div class="container footer-bottom"><span>© 2013–<span id="year"></span> МБОУ «Гимназия №4»</span><span>Учебный проект · демонстрационный редизайн</span></div></footer>

<button id="toTop" class="to-top" aria-label="Наверх">↑</button>
<div class="cookie" id="cookie" hidden><span>Мы используем файлы cookie, чтобы сайт работал корректно и удобно.</span><button id="cookieOk" class="btn btn-small btn-gold">Принять</button></div>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script src="assets/js/app.js"></script>
</body>
</html>
'''

def hero(title, sub="", kicker="Раздел сайта"):
    return ('<section class="page-hero"><div class="container">'
            '<p class="crumbs"><a href="index.html">Главная</a><span> / </span>' + title + '</p>'
            '<p class="kicker">' + kicker + '</p><h1>' + title + '</h1><p class="lead">' + sub + '</p></div></section>')

def page(fname, title, desc, body):
    nav = "".join('<a href="' + f + '"' + (' class="active" aria-current="page"' if f == fname else '') + '>' + t + '</a>' for f, t in NAV)
    (OUT / fname).write_text(SHELL.format(title=title, desc=desc, nav=nav, body=body, page=fname.replace(".html", "")), encoding="utf-8")

CSS = '''/* ============================================================
   Гимназия №4 — дизайн-система учебного проекта
   Палитра: чернильный синий + тёплая бумага + золото наград
   ============================================================ */
:root{
  --ink:#182742; --ink-2:#22355c; --paper:#f5efe3; --surface:#fffcf5;
  --line:#e2d6bf; --text:#20293a; --muted:#68718a;
  --gold:#c9962e; --gold-2:#e8b54a; --blue:#2f6fd0;
  --green:#2e8f66; --red:#c8442e; --amber:#d99a26;
  --r:18px; --shadow:0 12px 34px rgba(24,39,66,.10);
  --serif:"Playfair Display",Georgia,serif; --sans:"Manrope",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:110px}
body{font-family:var(--sans);background:
  radial-gradient(900px 500px at 8% -5%,rgba(201,150,46,.10),transparent 60%),
  radial-gradient(800px 520px at 95% 12%,rgba(47,111,208,.08),transparent 60%),
  var(--paper);color:var(--text);line-height:1.65;min-height:100vh}
::selection{background:var(--gold);color:var(--ink)}
*{scrollbar-width:thin;scrollbar-color:var(--gold) var(--paper)}
::-webkit-scrollbar{width:12px;height:12px}
::-webkit-scrollbar-track{background:var(--paper)}
::-webkit-scrollbar-thumb{background:linear-gradient(var(--gold),var(--blue));border:3px solid var(--paper);border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:var(--ink)}
img,svg{max-width:100%}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
::placeholder{color:var(--muted);opacity:.8}
code{background:#f3ead9;padding:2px 7px;border-radius:6px;font-size:.85em}
.skip-link{position:fixed;left:16px;top:-60px;z-index:200;background:var(--ink);color:#fff;padding:10px 16px;border-radius:0 0 10px 10px;transition:.2s}
.skip-link:focus{top:0}
.container{width:min(1160px,100% - 40px);margin-inline:auto}
h1,h2,h3,.serif{font-family:var(--serif);color:var(--ink);line-height:1.18}
h2{font-size:clamp(1.5rem,2.6vw,2.1rem);margin:52px 0 18px;position:relative}
h2::after{content:"";display:block;width:64px;height:4px;background:linear-gradient(90deg,var(--gold),var(--blue));border-radius:99px;margin-top:10px}
h3{font-size:1.22rem;margin-bottom:10px}
p{margin-bottom:10px}
.kicker{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}
.lead{font-size:1.05rem;color:var(--muted);max-width:720px}
/* верхняя панель */
.topbar{background:var(--ink);color:#dce6f7;font-size:.84rem;position:relative;z-index:60}
.topbar-in{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:7px 0;flex-wrap:wrap}
.topbar-actions{display:flex;gap:8px;flex-wrap:wrap}
.topbar-btn{color:#fff;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.22);border-radius:99px;padding:4px 13px;font:inherit;font-size:.8rem;cursor:pointer}
.topbar-btn:hover{background:rgba(255,255,255,.14);text-decoration:none}
/* шапка */
header{position:sticky;top:0;z-index:55;background:rgba(255,252,245,.90);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);transition:box-shadow .25s}
header.scrolled{box-shadow:0 8px 28px rgba(24,39,66,.12)}
.head-in{display:flex;align-items:center;gap:18px;padding:13px 0}
.logo{display:flex;align-items:center;gap:12px;color:var(--ink)}
.logo:hover{text-decoration:none}
.logo-badge{width:46px;height:46px;border-radius:14px;background:linear-gradient(145deg,var(--ink),var(--blue));color:var(--gold-2);display:grid;place-items:center;font:800 1.7rem var(--serif);box-shadow:inset 0 0 0 1px rgba(232,181,74,.5)}
.logo-text{font:800 1.12rem var(--serif)}
.logo-text small{display:block;font:600 .68rem var(--sans);letter-spacing:.02em;color:var(--muted);margin-top:2px}
nav{margin-left:auto;display:flex;gap:3px;align-items:center}
nav a{padding:8px 12px;border-radius:10px;color:var(--ink);font-weight:700;font-size:.92rem}
nav a:hover{background:#f0e7d6;text-decoration:none}
nav a.active{background:var(--ink);color:#fff}
.nav-cta{white-space:nowrap}
.burger{display:none;margin-left:auto;background:none;border:0;font-size:1.7rem;cursor:pointer;color:var(--ink)}
/* кнопки */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 22px;border-radius:12px;font-weight:800;font-size:.95rem;border:0;cursor:pointer;transition:.18s;text-decoration:none}
.btn:hover{transform:translateY(-2px);text-decoration:none}
.btn-gold{background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);box-shadow:0 8px 20px rgba(201,150,46,.32)}
.btn-ink{background:var(--ink);color:#fff}
.btn-line{background:transparent;color:var(--ink);border:2px solid var(--line)}
.btn-ghost{background:rgba(255,255,255,.10);color:#fff;border:1px solid rgba(255,255,255,.45)}
.btn-small{padding:8px 15px;font-size:.85rem;border-radius:10px}
/* hero */
.hero{position:relative;overflow:hidden;color:#fff;padding:84px 0 118px;background:
  radial-gradient(700px 380px at 82% 18%,rgba(232,181,74,.30),transparent 62%),
  radial-gradient(760px 460px at 12% 90%,rgba(47,111,208,.42),transparent 60%),
  linear-gradient(135deg,#101d35,#182742 45%,#22355c)}
.hero::after,.page-hero::after{content:"";position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.35'/%3E%3C/svg%3E");opacity:.05;pointer-events:none}
.hero .container,.page-hero .container{position:relative;z-index:1}
.hero h1{color:#fff;font-size:clamp(2.1rem,4.6vw,3.7rem);max-width:760px}
.hero h1 em{font-style:normal;color:var(--gold-2)}
.hero .lead{color:#d7e2f5;margin:18px 0 30px;font-size:1.08rem}
.hero-actions{display:flex;gap:12px;flex-wrap:wrap}
.hero-note{margin-top:18px;color:#b9c7de;font-size:.88rem}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:46px}
.stat{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:var(--r);padding:16px 18px;backdrop-filter:blur(6px)}
.stat b{font:800 1.7rem var(--serif);color:var(--gold-2);display:block}
.stat span{font-size:.86rem;color:#d7e2f5}
.seal{position:absolute;right:max(20px,calc((100vw - 1160px)/2));top:78px;width:150px;height:150px;opacity:.9}
.seal text{font:700 9.5px var(--sans);letter-spacing:.16em;fill:var(--gold-2)}
.seal .seal-num{font:800 44px var(--serif);letter-spacing:0}
.seal-rot{transform-origin:60px 60px;animation:spin 44s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
/* hero подстраниц */
.page-hero{position:relative;overflow:hidden;color:#fff;padding:42px 0 48px;background:
  radial-gradient(600px 300px at 85% 20%,rgba(232,181,74,.24),transparent 60%),
  linear-gradient(130deg,#101d35,#22355c)}
.page-hero h1{color:#fff;font-size:clamp(1.7rem,3.2vw,2.5rem)}
.page-hero .lead{color:#d7e2f5;margin-top:8px}
.crumbs{font-size:.84rem;color:#b9c7de;margin-bottom:12px}
.crumbs a{color:#fff}
/* контент */
main{padding:52px 0 20px;position:relative;z-index:1}
.cards,.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.grid{margin:18px 0}
.overlap{margin-top:-122px;position:relative;z-index:3}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:24px;box-shadow:var(--shadow);color:var(--text);transition:transform .2s,box-shadow .2s,border-color .2s;overflow-wrap:break-word}
a.card:hover{transform:translateY(-5px);border-color:var(--gold);box-shadow:0 18px 42px rgba(24,39,66,.16);text-decoration:none}
.card .ico{width:46px;height:46px;border-radius:13px;display:grid;place-items:center;font-size:1.5rem;background:linear-gradient(145deg,#f3e6c9,#fff8ea);border:1px solid var(--line);margin-bottom:12px}
.card b{display:block;font-size:1.05rem;margin-bottom:5px;color:var(--ink)}
.card span,.card p,.card li{font-size:.93rem;color:var(--muted)}
.card ul,.card ol{padding-left:20px}
.card table{margin-top:6px}
.news{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}
time{font-size:.78rem;font-weight:800;color:var(--blue);letter-spacing:.02em}
.badge{display:inline-block;border-radius:99px;padding:3px 11px;font-size:.74rem;font-weight:800;margin:6px 6px 6px 0}
.badge-blue{background:#e7effc;color:#245a9e}.badge-gold{background:#f7ecd4;color:#8a641b}
.badge-green{background:#e2f2ea;color:#226b4c}.badge-red{background:#f9e7e3;color:#963826}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chips a,.chips span{background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:8px 16px;font-size:.9rem;font-weight:700;color:var(--ink)}
.chips a:hover{border-color:var(--gold);background:#fff7e8;text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:.92rem}
td,th{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;overflow-wrap:break-word}
th{color:var(--muted);font-size:.76rem;text-transform:uppercase;letter-spacing:.06em;background:#f7f0e2}
.kv td:first-child{color:var(--muted);font-weight:700;width:36%}
tr:hover td{background:#fbf6ec}
details{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:15px 18px;margin:10px 0;box-shadow:0 5px 18px rgba(24,39,66,.05)}
summary{font-weight:800;cursor:pointer;color:var(--ink);list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--gold);font-size:1.3rem;line-height:1}
details[open] summary::after{content:"–"}
details p{margin-top:10px}
.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:18px 0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:14px}
.toolbar input[type="search"]{flex:1;min-width:220px;padding:11px 14px;border:1px solid var(--line);border-radius:11px;font:inherit;background:#fff}
.filter{display:flex;gap:7px;flex-wrap:wrap}
.filter button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:8px 14px;font:inherit;font-size:.86rem;font-weight:800;cursor:pointer;color:var(--ink)}
.filter button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.count{font-size:.85rem;color:var(--muted);font-weight:700}
.steps{counter-reset:s;list-style:none;padding:0;margin:12px 0}
.steps li{position:relative;padding:0 0 18px 48px;color:var(--muted)}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);display:grid;place-items:center;font-weight:800}
.note{background:#fff5df;border:1px solid #ecd39a;border-radius:14px;padding:13px 16px;font-size:.9rem;margin:16px 0;color:#6d541e}
.note-info{background:#eaf1fd;border-color:#c6d8f5;color:#284f86}
.form label{display:block;font-weight:800;font-size:.9rem;color:var(--ink);margin-bottom:14px}
.form input,.form textarea,.form select{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:12px;font:inherit;margin-top:6px;background:#fff;color:var(--text)}
.form input:focus,.form textarea:focus,.form select:focus{border-color:var(--gold);box-shadow:0 0 0 4px rgba(201,150,46,.15);outline:none}
.form .agree{display:flex;gap:10px;align-items:flex-start;font-size:.85rem;color:var(--muted);font-weight:600}
.form .agree input{width:auto;margin:4px 0 0}
.form-ok{background:#e2f2ea;border:1px solid #a9d6c1;color:#226b4c;border-radius:14px;padding:14px 16px;margin-top:14px;font-weight:700}
.swatch-color{height:84px;border-radius:12px;border:1px solid var(--line);margin-bottom:12px}
.spacing{display:flex;gap:10px;align-items:flex-end;margin-top:14px;flex-wrap:wrap}
.spacing span{display:block;height:26px;background:linear-gradient(135deg,var(--gold-2),var(--blue));border-radius:6px}
/* подвал */
footer{background:var(--ink);color:#c3d0e5;margin-top:64px;padding:46px 0 22px;font-size:.9rem;position:relative;z-index:1}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1.2fr;gap:32px}
.footer-logo{font:800 1.4rem var(--serif);color:var(--gold-2);margin-bottom:10px}
.footer-title{font-weight:800;color:#fff;margin-bottom:10px}
footer a{display:block;color:#9fc2f0;margin:5px 0}
.footer-guide{margin-top:14px!important;color:var(--gold-2)!important}
.footer-bottom{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.14);margin-top:30px;padding-top:16px;font-size:.8rem;color:#8fa1bd}
/* cookie / toast / наверх */
.cookie{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);width:min(700px,92%);background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:0 16px 46px rgba(0,0,0,.28);padding:16px 20px;display:flex;gap:16px;align-items:center;z-index:90;font-size:.9rem}
.to-top{position:fixed;right:20px;bottom:20px;width:46px;height:46px;border-radius:50%;border:0;background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);font-size:1.3rem;font-weight:800;cursor:pointer;box-shadow:0 10px 26px rgba(201,150,46,.4);opacity:0;visibility:hidden;pointer-events:none;transition:.25s;z-index:80}
.to-top.show{opacity:1;visibility:visible;pointer-events:auto}
.toast{position:fixed;left:50%;bottom:84px;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;padding:11px 18px;border-radius:12px;font-size:.9rem;font-weight:700;opacity:0;pointer-events:none;transition:.25s;z-index:120;box-shadow:0 10px 30px rgba(0,0,0,.3)}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.icon-btn{background:none;border:0;font-size:1rem;cursor:pointer;color:var(--ink)}
/* панель доступности */
.a11y-panel{position:fixed;right:18px;top:78px;z-index:110;width:300px;background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 50px rgba(24,39,66,.25);padding:18px}
.a11y-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.a11y-label{font-size:.85rem;font-weight:800;color:var(--ink);margin:10px 0 6px}
.a11y-panel input[type="range"]{width:100%;accent-color:var(--gold)}
.scheme-row{display:flex;gap:8px;margin:8px 0 14px}
.scheme{width:42px;height:42px;border-radius:11px;border:2px solid var(--line);font:800 1rem var(--serif);cursor:pointer;background:var(--surface);color:var(--ink)}
.scheme.on{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,150,46,.25)}
.scheme-bw{background:#fff;color:#000}.scheme-wb{background:#000;color:#fff}.scheme-blue{background:#dceafc;color:#123c69}
/* схемы доступности */
body[data-scheme="bw"]{--paper:#fff;--surface:#fff;--text:#000;--muted:#111;--line:#000;--ink:#000;--blue:#000}
body[data-scheme="bw"] .hero,body[data-scheme="bw"] .page-hero,body[data-scheme="bw"] footer,body[data-scheme="bw"] .topbar{background:#000!important;color:#fff}
body[data-scheme="bw"] .card,body[data-scheme="bw"] details,body[data-scheme="bw"] .chips a{border-width:2px}
body[data-scheme="bw"] h1,body[data-scheme="bw"] h2,body[data-scheme="bw"] h3{color:#000}
body[data-scheme="wb"]{--paper:#000;--surface:#111;--text:#fff;--muted:#ddd;--line:#fff;--ink:#fff;--blue:#fff}
body[data-scheme="wb"] .hero,body[data-scheme="wb"] .page-hero,body[data-scheme="wb"] footer,body[data-scheme="wb"] .topbar{background:#000!important;color:#fff}
body[data-scheme="wb"] header{background:#000;border-color:#fff}
body[data-scheme="wb"] h1,body[data-scheme="wb"] h2,body[data-scheme="wb"] h3,body[data-scheme="wb"] .logo,body[data-scheme="wb"] nav a{color:#fff}
body[data-scheme="wb"] nav a:hover{background:#222}
body[data-scheme="wb"] th{background:#222;color:#fff}
body[data-scheme="wb"] tr:hover td{background:#1a1a1a}
body[data-scheme="wb"] .form input,body[data-scheme="wb"] .form textarea,body[data-scheme="wb"] .form select,body[data-scheme="wb"] .toolbar input{background:#111;color:#fff;border-color:#fff}
body[data-scheme="wb"] .filter button{background:#111;color:#fff;border-color:#fff}
body[data-scheme="wb"] .note{background:#221a00;color:#ffd;border-color:#aa8}
body[data-scheme="wb"] .btn-gold,body[data-scheme="wb"] .btn-ink{background:#fff;color:#000}
body[data-scheme="wb"] nav a.active{background:#fff;color:#000}
body[data-scheme="blue"]{--paper:#dceafc;--surface:#eef5ff;--text:#123c69;--muted:#24527e;--line:#7ba7d7;--ink:#123c69;--blue:#123c69}
body[data-scheme="blue"] .hero,body[data-scheme="blue"] .page-hero{background:#123c69!important}
body[data-scheme="blue"] header{background:rgba(238,245,255,.92)}
body[data-scheme="blue"] th{background:#d4e5fa}
/* появление при скролле */
.rv{opacity:0;transform:translateY(18px);transition:opacity .55s ease,transform .55s ease}
.rv.in{opacity:1;transform:none}
/* адаптив */
@media (max-width:980px){
  nav{display:none;position:absolute;top:100%;left:0;right:0;background:var(--surface);flex-direction:column;align-items:stretch;padding:14px 20px;border-bottom:1px solid var(--line);box-shadow:0 18px 34px rgba(24,39,66,.15)}
  nav.open{display:flex}
  .burger{display:block}
  .nav-cta{display:none}
  .seal{display:none}
  .stats{grid-template-columns:repeat(2,1fr)}
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .container{width:min(100% - 28px,1160px)}
  .topbar-name{display:none}
  .hero{padding:58px 0 96px}
  .overlap{margin-top:-92px}
  .stats{grid-template-columns:1fr 1fr}
  .footer-grid{grid-template-columns:1fr}
  .cookie{flex-direction:column;text-align:center}
  .a11y-panel{left:14px;right:14px;width:auto;top:64px}
  .toolbar{align-items:stretch}
  .toolbar input[type="search"]{min-width:0}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}
  .rv{opacity:1;transform:none}
}
@media print{
  .topbar,header,.a11y-panel,.cookie,.to-top,.toast,footer{display:none!important}
  body{background:#fff;color:#000}
  .hero,.page-hero{background:#fff!important;color:#000!important;padding:20px 0}
  .hero h1,.page-hero h1{color:#000}
  .card{box-shadow:none;border:1px solid #999}
}
'''

JS = '''/* Гимназия №4 — interactions */
(() => {
"use strict";
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
};
const toastEl = $("#toast");
let toastTimer;
const toast = (msg) => {
  if (!toastEl) return;
  toastEl.textContent = msg; toastEl.classList.add("show");
  clearTimeout(toastTimer); toastTimer = setTimeout(() => toastEl.classList.remove("show"), 2400);
};

/* год, шапка, наверх */
const year = $("#year"); if (year) year.textContent = new Date().getFullYear();
const header = $("#siteHeader"), toTop = $("#toTop");
const onScroll = () => {
  if (header) header.classList.toggle("scrolled", scrollY > 8);
  if (toTop) toTop.classList.toggle("show", scrollY > 650);
};
addEventListener("scroll", onScroll, { passive: true }); onScroll();
if (toTop) toTop.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

/* мобильное меню */
const burger = $("#burger"), nav = $("#nav");
const setMenu = (open) => {
  if (!burger || !nav) return;
  nav.classList.toggle("open", open);
  burger.setAttribute("aria-expanded", String(open));
  burger.textContent = open ? "✕" : "☰";
};
if (burger) burger.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
if (nav) nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });

/* доступность */
const panel = $("#a11yPanel"), aBtn = $("#a11yBtn"), fsRange = $("#fsRange"), fsValue = $("#fsValue");
const schemes = $$(".scheme");
const applyA11y = (state) => {
  document.documentElement.style.fontSize = state.fs + "%";
  document.body.dataset.scheme = state.scheme || "";
  if (fsRange) fsRange.value = state.fs;
  if (fsValue) fsValue.textContent = state.fs + "%";
  schemes.forEach(b => b.classList.toggle("on", (b.dataset.scheme || "") === (state.scheme || "")));
};
let a11y = store.get("gym4-a11y", { fs: 100, scheme: "" });
applyA11y(a11y);
const setPanel = (open) => {
  if (!panel || !aBtn) return;
  panel.hidden = !open; aBtn.setAttribute("aria-expanded", String(open));
};
if (aBtn) aBtn.addEventListener("click", () => setPanel(panel.hidden));
if ($("#a11yClose")) $("#a11yClose").addEventListener("click", () => setPanel(false));
if (fsRange) fsRange.addEventListener("input", () => { a11y.fs = +fsRange.value; applyA11y(a11y); store.set("gym4-a11y", a11y); });
schemes.forEach(b => b.addEventListener("click", () => { a11y.scheme = b.dataset.scheme || ""; applyA11y(a11y); store.set("gym4-a11y", a11y); }));
if ($("#a11yReset")) $("#a11yReset").addEventListener("click", () => { a11y = { fs: 100, scheme: "" }; applyA11y(a11y); store.set("gym4-a11y", a11y); toast("Обычная версия восстановлена"); });
addEventListener("keydown", (e) => { if (e.key === "Escape") { setMenu(false); setPanel(false); } });

/* cookie */
const cookie = $("#cookie");
if (cookie && !store.get("gym4-cookie", false)) cookie.hidden = false;
if ($("#cookieOk")) $("#cookieOk").addEventListener("click", () => { store.set("gym4-cookie", true); cookie.hidden = true; toast("Настройки сохранены"); });

/* появление блоков */
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const targets = $$(".hero .container > *, main h2, main .card, .page-hero .container > *");
if (!reduce && "IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  }), { threshold: .12 });
  targets.forEach((el, i) => { el.classList.add("rv"); el.style.transitionDelay = (i % 5) * 55 + "ms"; io.observe(el); });
} else targets.forEach(el => el.classList.add("in"));

/* новости: поиск + фильтр */
const search = $("#newsSearch"), cards = $$("#newsList [data-cat]"), count = $("#newsCount"), empty = $("#newsEmpty");
let activeCat = "all";
const filterNews = () => {
  const q = (search?.value || "").trim().toLowerCase();
  let shown = 0;
  cards.forEach(c => {
    const okCat = activeCat === "all" || c.dataset.cat === activeCat;
    const okQ = !q || c.textContent.toLowerCase().includes(q);
    const show = okCat && okQ; c.hidden = !show; if (show) shown++;
  });
  if (count) count.textContent = "Показано: " + shown;
  if (empty) empty.hidden = shown !== 0;
};
$$("[data-filter]").forEach(b => b.addEventListener("click", () => {
  activeCat = b.dataset.filter;
  $$(".filter button").forEach(x => x.classList.toggle("on", x.dataset.filter === activeCat));
  filterNews();
}));
if (search) search.addEventListener("input", filterNews);
if (cards.length) filterNews();

/* форма контактов */
const form = $("#fbForm"), formOk = $("#formOk");
if (form) form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!form.checkValidity()) { form.reportValidity(); return; }
  const data = Object.fromEntries(new FormData(form).entries());
  const msgs = store.get("gym4-messages", []); msgs.push({ ...data, at: new Date().toISOString() });
  store.set("gym4-messages", msgs);
  form.reset(); if (formOk) formOk.hidden = false;
  toast("Сообщение сохранено локально");
});

/* копирование цветов (дизайн-система) */
const copy = async (t) => {
  try { await navigator.clipboard.writeText(t); }
  catch {
    const ta = document.createElement("textarea"); ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove();
  }
  toast("Скопировано: " + t);
};
$$("[data-copy]").forEach(b => b.addEventListener("click", () => copy(b.dataset.copy)));
})();
'''

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#182742"/><path d="M10 50h44" stroke="#e8b54a" stroke-width="3" stroke-linecap="round"/><text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="38" font-weight="700" fill="#e8b54a">4</text></svg>'''

README = '''# Сайт МБОУ «Гимназия №4» — учебный проект

**Тема:** редизайн официального сайта школы (gym4.net) с сохранением обязательных разделов и требований доступности.

**Автор:** ____________________ (ФИО, класс/группа)  
**Дата:** ноябрь 2026

## Цель
Создать современную, быструю и доступную версию школьного сайта: понятная навигация, читаемая типографика, адаптивность под телефоны и компьютеры, версия для слабовидящих.

## Как запустить
1. Распаковать/скопировать папку проекта.
2. Открыть `index.html` в браузере.
3. Либо запустить локальный сервер: `python -m http.server 8000` → открыть `http://localhost:8000`.

## Структура
- `index.html` — главная;
- `sveden.html` — сведения об образовательной организации;
- `parents.html` — родителям (питание, безопасность, FAQ);
- `students.html` — ученикам (ГИА, сочинение, кружки, телефон доверия);
- `news.html` — новости с поиском и фильтром;
- `contacts.html` — контакты и форма обратной связи;
- `priem.html` — приём в 1 класс и перевод в гимназию;
- `styleguide.html` — дизайн-система: палитра, типографика, компоненты;
- `assets/css/style.css` — единая дизайн-система и стили;
- `assets/js/app.js` — меню, доступность, фильтр новостей, форма, анимации;
- `assets/favicon.svg` — иконка сайта.

## Реализовано
- 8 страниц с единой шапкой, подвалом, навигацией и активным пунктом меню;
- Sticky-навигация, мобильное меню, хлебные крошки, якорные переходы;
- Панель доступности: размер шрифта 100–160%, четыре цветовые схемы, сохранение настроек;
- Поиск и фильтрация новостей, счётчик результатов и пустое состояние;
- Форма обратной связи с валидацией и сохранением сообщений в браузере (демо);
- Дизайн-система с копированием HEX-кодов цветов;
- Адаптивная сетка, печатная версия, поддержка prefers-reduced-motion;
- Кастомные скроллбары, анимации появления, кнопка «наверх».

## Данные и достоверность
Реальные сведения взяты с официальных страниц gym4.net: адрес, телефоны, e-mail, директор, учредитель, лицензия, аккредитация, кружки, платные услуги. Новости и меню столовой — учебные демонстрационные материалы, явно помечены на страницах. Проект не является официальным сайтом гимназии.

## Технологии
HTML5, CSS3 (переменные, Grid, Flexbox, clamp(), градиенты), ванильный JavaScript (localStorage, IntersectionObserver, FormData), SVG. Без сборщиков и сторонних JS-библиотек.

## Что можно развить
Перенос в тему WordPress, подключение реальной отправки формы на сервер, замена демо-новостей реальными, расширение раздела документов.
'''

(OUT / "assets/css/style.css").write_text(CSS, encoding="utf-8")
(OUT / "assets/js/app.js").write_text(JS, encoding="utf-8")
(OUT / "assets/favicon.svg").write_text(FAVICON, encoding="utf-8")
(OUT / "README.md").write_text(README, encoding="utf-8")

# ---------------- ГЛАВНАЯ ----------------
page("index.html", "Главная", "Современный школьный сайт: сведения, родителям, ученикам, новости, контакты и приём.", '''
<section class="hero">
  <svg class="seal" viewBox="0 0 120 120" aria-hidden="true">
    <defs><path id="sealPath" d="M60,60 m-45,0 a45,45 0 1,1 90,0 a45,45 0 1,1 -90,0"/></defs>
    <g class="seal-rot"><circle cx="60" cy="60" r="56" fill="none" stroke="#e8b54a" stroke-opacity=".45"/><circle cx="60" cy="60" r="34" fill="none" stroke="#e8b54a" stroke-opacity=".25"/><text><textPath href="#sealPath">ГИМНАЗИЯ №4 • АСТРАХАНЬ • ЮНЕСКО • 1964 • </textPath></text></g>
    <text class="seal-num" x="60" y="75" text-anchor="middle" fill="#e8b54a">4</text>
  </svg>
  <div class="container">
    <p class="kicker">Ассоциированная школа ЮНЕСКО</p>
    <h1>Гимназия №4 — <em>школа с историей</em> и будущим</h1>
    <p class="lead">Углублённое изучение английского языка, сильная подготовка к экзаменам и насыщенная школьная жизнь. Входит в топ-100 образовательных учреждений России по итогам 2023–2024 учебного года.</p>
    <div class="hero-actions"><a class="btn btn-gold" href="priem.html#first">Приём в 1 класс</a><a class="btn btn-ghost" href="sveden.html">Сведения об ОУ</a><a class="btn btn-ghost" href="contacts.html#feedback">Задать вопрос</a></div>
    <p class="hero-note">🏅 Победитель конкурса инновационных программ · 🌍 Сеть школ ЮНЕСКО · 🦅 Флагман проекта «Орлята России»</p>
    <div class="stats">
      <div class="stat"><b>1450+</b><span>учеников 1–11 классов</span></div>
      <div class="stat"><b>73</b><span>педагога и наставника</span></div>
      <div class="stat"><b>ТОП-100</b><span>школ России</span></div>
      <div class="stat"><b>60+</b><span>лет истории</span></div>
    </div>
  </div>
</section>
<main id="main" class="container">
  <section class="cards overlap">
    <a class="card" href="parents.html#food"><span class="ico">🍎</span><b>Ежедневное меню</b><span>Горячее питание и здоровый рацион</span></a>
    <a class="card" href="students.html#gia"><span class="ico">📝</span><b>ГИА-9 и ГИА-11</b><span>Регламенты, расписание, подготовка</span></a>
    <a class="card" href="students.html#clubs"><span class="ico">⚽</span><b>Кружки и секции</b><span>Спорт, театр, музыка и шахматы</span></a>
    <a class="card" href="students.html#essay"><span class="ico">✍️</span><b>Итоговое сочинение</b><span>Сроки, темы и материалы</span></a>
    <a class="card" href="students.html#help"><span class="ico">🛡️</span><b>Телефон доверия</b><span>Помощь и психологическая поддержка</span></a>
    <a class="card" href="parents.html#faq"><span class="ico">❓</span><b>Частые вопросы</b><span>Ответы для родителей и учеников</span></a>
  </section>
  <h2>Новости</h2>
  <section class="news">
    <a class="card" href="news.html"><time>Демо · 12 ноября 2026</time><b>Школьный этап ВсОШ</b><span>Приглашаем учеников 4–11 классов. Победители проходят на муниципальный этап.</span></a>
    <a class="card" href="news.html"><time>Демо · 8 ноября 2026</time><b>«Орлята России»: новый сезон</b><span>Гимназия — флагманская школа федерального проекта.</span></a>
    <a class="card" href="news.html"><time>Демо · 5 ноября 2026</time><b>Английский театр</b><span>Студия открыла новый сезон для 5–8 классов.</span></a>
  </section>
  <p style="margin-top:16px"><a class="btn btn-line btn-small" href="news.html">Все новости →</a></p>
  <h2>Официальная информация</h2>
  <div class="chips">
    <a href="sveden.html#basic">Основные сведения</a><a href="sveden.html#docs">Документы</a><a href="sveden.html#edu">Образование</a>
    <a href="sveden.html#staff">Руководство и педсостав</a><a href="sveden.html#objects">Материальное обеспечение</a>
    <a href="sveden.html#budget">Финансы</a><a href="sveden.html#vacant">Вакантные места</a><a href="sveden.html#intl">ЮНЕСКО</a>
  </div>
  <h2>Почему выбирают гимназию</h2>
  <div class="grid">
    <section class="card"><span class="ico">🇬🇧</span><h3>Сильный английский</h3><p>Углублённое изучение языка, спецкурсы перевода и зарубежной литературы, английский театр и Cambridge English.</p></section>
    <section class="card"><span class="ico">🏛️</span><h3>Традиции с 1964 года</h3><p>Гимназия создана в 1996 году на базе школы №46. Выпускники поступают в ведущие вузы страны.</p></section>
    <section class="card"><span class="ico">🌊</span><h3>Комфортная среда</h3><p>Бассейн, два спортзала, четыре спортплощадки, два компьютерных класса, библиотечно-информационный центр.</p></section>
  </div>
</main>
''')

# ---------------- СВЕДЕНИЯ ----------------
page("sveden.html", "Сведения об ОУ", "Официальные сведения, документы, образование, руководство, питание и материальная база гимназии.",
hero("Сведения об образовательной организации", "Структура раздела соответствует требованиям к официальным сайтам образовательных организаций.", "Официальный раздел") + '''
<main id="main" class="container">
  <div class="note note-info">Раздел собран по образцу обязательных подразделов. Документы на этой странице ведут на действующие страницы оригинального сайта, чтобы не потерять первоисточники.</div>
  <div class="grid">
    <section class="card" id="basic"><span class="ico">📌</span><h3>Основные сведения</h3>
      <table class="kv">
        <tr><td>Полное наименование</td><td>МБОУ г. Астрахани «Гимназия №4»</td></tr>
        <tr><td>Дата создания</td><td>1996 г. на базе школы №46 (основана в 1964 г.)</td></tr>
        <tr><td>Учредитель</td><td>МО «Городской округ город Астрахань»</td></tr>
        <tr><td>Адрес</td><td>414024, г. Астрахань, ул. Б. Хмельницкого, 16, корп. 1</td></tr>
        <tr><td>Режим работы</td><td>пн–сб 07:30–18:30, выходной — воскресенье</td></tr>
        <tr><td>Лицензия</td><td>№ Л035-01261-30/00372950 от 05.11.2015</td></tr>
        <tr><td>Аккредитация</td><td>№ А007-01261-30/01134763 от 27.11.2015</td></tr>
      </table>
    </section>
    <section class="card" id="struct"><span class="ico">🏛️</span><h3>Структура и органы управления</h3><p>Филиалов и структурных подразделений нет. Управление — по Уставу: общее собрание работников, педагогический совет, управляющий совет.</p><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/struct/">Подробнее</a></section>
    <section class="card" id="docs"><span class="ico">📄</span><h3>Документы</h3><ul><li>Устав гимназии</li><li>Лицензия и аккредитация</li><li>Локальные нормативные акты</li><li>Публичный доклад и самообследование</li></ul><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/document/">Открыть документы</a></section>
    <section class="card" id="edu"><span class="ico">🎓</span><h3>Образование</h3><ul><li>Начальное общее: 1–4 классы</li><li>Основное общее: 5–9 классы</li><li>Среднее общее: 10–11 классы</li><li>Углублённый английский и спецкурсы перевода</li><li>≈1450 обучающихся, 73 педагога</li></ul><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/education/">Образовательные программы</a></section>
    <section class="card" id="standards"><span class="ico">📚</span><h3>Образовательные стандарты</h3><p>Реализуются ФГОС начального, основного и среднего общего образования.</p><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/edustandarts/">Стандарты и требования</a></section>
    <section class="card" id="staff"><span class="ico">👩‍🏫</span><h3>Руководство. Педагогический состав</h3><table class="kv"><tr><td>Директор</td><td>Лендова Татьяна Викторовна</td></tr><tr><td>Приёмный день</td><td>среда, 14:00–18:00</td></tr><tr><td>Приёмная</td><td><a href="tel:+78512500567">(8512) 50-05-67</a></td></tr></table><p>73 педагога: Заслуженные учителя России, Почётные работники образования, Отличники просвещения.</p><a class="btn btn-small btn-ink" href="https://gym4.net/pedagogicheskij-sostav/">Педагогический состав</a></section>
    <section class="card" id="objects"><span class="ico">🏊</span><h3>Материально-техническое обеспечение</h3><ul><li>Два спортивных зала и бассейн</li><li>Четыре оборудованные спортплощадки</li><li>Два компьютерных класса</li><li>Библиотечно-информационный центр и английская библиотека</li><li>Столовая с горячим питанием и буфет</li></ul></section>
    <section class="card" id="paid"><span class="ico">💼</span><h3>Платные образовательные услуги</h3><div class="chips"><span>Подготовка дошкольников</span><span>Бальные танцы</span><span>Основы правоведения</span><span>Русская словесность</span><span>Happy kids</span><span>Cambridge English</span></div><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/paid_edu/">Условия и стоимость</a></section>
    <section class="card" id="budget"><span class="ico">💰</span><h3>Финансово-хозяйственная деятельность</h3><p>План ФХД, отчёты о поступлениях и расходах, независимая оценка качества.</p><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/budget/">Документы</a> <a class="btn btn-small btn-line" href="https://bus.gov.ru/pub/info-card/33692">bus.gov.ru</a></section>
    <section class="card" id="vacant"><span class="ico">🪑</span><h3>Вакантные места</h3><p>Актуальное количество свободных мест по классам — в разделе и в приёмной гимназии.</p><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/vacant/">Вакантные места</a></section>
    <section class="card" id="grants"><span class="ico">🤝</span><h3>Стипендии и меры поддержки</h3><p>Меры социальной поддержки обучающихся, льготное питание.</p><a class="btn btn-small btn-ink" href="https://gym4.net/sveden/grants/">Подробнее</a></section>
    <section class="card" id="intl"><span class="ico">🌍</span><h3>Международное сотрудничество</h3><p>Гимназия входит в сеть ассоциированных школ ЮНЕСКО.</p><a class="btn btn-small btn-ink" href="https://gym4.net/mezhdunarodnoe-sotrudnichestvo/">Подробнее</a></section>
    <section class="card" id="food"><span class="ico">🍎</span><h3>Организация питания</h3><p>Ежедневное меню, здоровое питание, контроль с участием родителей.</p><a class="btn btn-small btn-ink" href="parents.html#food">Питание на сайте</a></section>
  </div>
</main>
''')

# ---------------- РОДИТЕЛЯМ ----------------
page("parents.html", "Родителям", "Приём, питание, льготы, безопасность и ответы на частые вопросы для родителей.",
hero("Родителям", "Приём и перевод, питание, льготы, безопасность и ответы на частые вопросы.", "Для семьи") + '''
<main id="main" class="container">
  <div class="grid">
    <a class="card" href="priem.html#first"><span class="ico">🎒</span><b>Приём в 1 класс</b><span>Сроки, документы, подача через Госуслуги</span></a>
    <a class="card" href="priem.html#gym"><span class="ico">🏫</span><b>Приём / перевод в гимназию</b><span>5 класс и вакантные места</span></a>
    <a class="card" href="https://gym4.net/klassy-i-klassnye-rukovoditeli/"><span class="ico">👥</span><b>Классы и руководители</b><span>Список классов и классные руководители</span></a>
  </div>
  <h2 id="food">Организация питания</h2>
  <p class="lead">В гимназии организовано горячее питание, работает буфет. Ученики 1–4 классов обеспечиваются бесплатным горячим питанием. Контроль качества ведётся с участием родителей.</p>
  <div class="note">Меню ниже — учебный демонстрационный пример. Актуальное ежедневное меню публикуется на <a href="https://gym4.net/food/">gym4.net/food</a>.</div>
  <div class="card"><table><tr><th>День</th><th>Завтрак</th><th>Обед</th></tr><tr><td>Понедельник</td><td>Каша овсяная, какао, бутерброд с сыром</td><td>Щи, куриная котлета с гарниром, компот</td></tr><tr><td>Вторник</td><td>Запеканка творожная, чай с молоком</td><td>Суп гороховый, рыба запечённая с рисом, кисель</td></tr><tr><td>Среда</td><td>Каша рисовая, чай, выпечка</td><td>Борщ, гуляш с гречей, компот</td></tr><tr><td>Четверг</td><td>Омлет, какао, бутерброд</td><td>Суп-лапша, тефтели с макаронами, компот</td></tr><tr><td>Пятница</td><td>Каша пшённая, чай, сырник</td><td>Рассольник, плов, фруктовый сок</td></tr></table></div>
  <div class="chips" style="margin-top:14px"><a href="https://gym4.net/perechen-lgot/">Перечень льгот</a><a href="https://gym4.net/zdorovoe-pitanie/">Здоровое питание</a><a href="https://gym4.net/informaciya-po-rezultatam-kontrolnyx-meropriyatij-s-uchastiem-roditelej/">Результаты проверок питания</a></div>
  <h2 id="safety">Безопасность и права ребёнка</h2>
  <div class="grid">
    <a class="card" href="https://gym4.net/prava-rebenka/"><span class="ico">⚖️</span><b>Права ребёнка</b><span>Основные документы и памятки</span></a>
    <a class="card" href="https://gym4.net/dlya-roditelej-3/budte-bditelny/"><span class="ico">👀</span><b>Будьте бдительны</b><span>Профилактика и безопасность детей</span></a>
    <a class="card" href="https://gym4.net/pamyatka-po-profilaktike-prestuplenij-protiv-polovoj-neprikosnovennosti-nesovershennoletnix/"><span class="ico">🛡️</span><b>Памятка по профилактике</b><span>Защита несовершеннолетних</span></a>
    <a class="card" href="https://gym4.net/o-svyazi-obraza-zhizni-detej-s-ix-zdorovem-v-tom-chisle-immunitetom/"><span class="ico">🩺</span><b>Медицинская профилактика</b><span>Образ жизни и здоровье детей</span></a>
  </div>
  <h2 id="faq">Часто задаваемые вопросы</h2>
  <details><summary>Как записать ребёнка в 1 класс?</summary><p>Заявление подаётся через Госуслуги или лично в гимназию. Кампания для закреплённой территории начинается 1 апреля. Подробности — <a href="priem.html#first">в разделе «Приём»</a>.</p></details>
  <details><summary>Какие документы нужны для перевода в гимназию?</summary><p>Заявление, паспорт родителя, свидетельство о рождении ребёнка, личное дело и выписка оценок. Наличие свободных мест уточняйте в приёмной: <a href="tel:+78512500567">(8512) 50-05-67</a>.</p></details>
  <details><summary>Питание платное?</summary><p>Ученики 1–4 классов получают бесплатное горячее питание. Для остальных категорий действуют льготы — см. <a href="https://gym4.net/perechen-lgot/">перечень льгот</a>.</p></details>
  <details><summary>Где посмотреть ежедневное меню?</summary><p>В разделе «Питание» выше и на странице <a href="https://gym4.net/food/">ежедневного меню</a> действующего сайта.</p></details>
</main>
''')

# ---------------- УЧЕНИКАМ ----------------
page("students.html", "Ученикам", "ГИА, итоговое сочинение, кружки и секции, телефон доверия и правила безопасности.",
hero("Ученикам", "Экзамены, олимпиады, кружки и секции, помощь и безопасность.", "Школьная жизнь") + '''
<main id="main" class="container">
  <h2 id="gia">Государственная итоговая аттестация</h2>
  <div class="grid">
    <section class="card"><span class="ico">9</span><h3>ГИА-9</h3><p>Русский язык и математика + два предмета по выбору. Допуск — при отсутствии задолженностей и с результатом «зачёт» за итоговое собеседование по русскому языку.</p><a class="btn btn-small btn-ink" href="https://gym4.net/gia-9/">Регламенты и расписание</a></section>
    <section class="card"><span class="ico">11</span><h3>ГИА-11</h3><p>Для аттестата — русский язык и математика (базовая или профильная). Предметы по выбору — для поступления в вуз. Допуск — «зачёт» за итоговое сочинение.</p><a class="btn btn-small btn-ink" href="https://gym4.net/gia-11-2/">Регламенты и расписание</a></section>
  </div>
  <h2 id="essay">Итоговое сочинение</h2>
  <section class="card"><p>Пишется в первую среду декабря, оценивается по системе «зачёт / незачёт» и является условием допуска к ГИА-11. Темы и структура — в материалах гимназии.</p><a class="btn btn-small btn-ink" href="https://gym4.net/itogovoe-sochinenie/">Материалы и сроки</a></section>
  <h2 id="clubs">Кружки и секции</h2>
  <div class="chips"><span>🏊 «Золотая рыбка» (плавание)</span><span>🎤 «Звонкие голоса»</span><span>🎭 «Фабрика идей»</span><span>⚽ «Кожаный мяч»</span><span>🏐 «Олимпийские резервы»</span><span>🏀 Баскетбол</span><span>🇬🇧 Английский театр</span><span>💃 Ритмика</span><span>🤸 ОФП</span><span>♟️ Шахматы</span><span>🌟 Школа личностного роста</span><span>🤝 Республика «Содружество»</span></div>
  <div class="note note-info">Ученики гимназии ежегодно становятся победителями и призёрами районных, городских, областных, всероссийских и международных олимпиад. Выпускники — студенты ведущих вузов России по версии RAEX.</div>
  <h2 id="help">Нужна помощь?</h2>
  <section class="card"><h3>Детский телефон доверия: <a href="tel:88002000122">8-800-2000-122</a></h3><p>Бесплатно, анонимно, круглосуточно. Психологическая служба гимназии также готова помочь.</p><a class="btn btn-small btn-ink" href="https://gym4.net/telefon-doveriya/">Все контакты помощи</a></section>
  <h2 id="safety">Безопасность</h2>
  <div class="grid">
    <a class="card" href="https://gym4.net/pravila-dorozhnogo-dvizheniya-dlya-peshexodov/"><span class="ico">🚦</span><b>ПДД для пешеходов</b><span>Безопасный путь в школу</span></a>
    <a class="card" href="https://gym4.net/pravila-povedeniya-v-obshhestvennom-transporte-i-na-mestax-posadki-passazhirov/"><span class="ico">🚌</span><b>Правила в транспорте</b><span>Общественный транспорт и посадки</span></a>
    <a class="card" href="https://gym4.net/kak-ne-stat-zhertvoj-telefonnogo-moshennichestva/"><span class="ico">📵</span><b>Телефонные мошенники</b><span>Как не стать жертвой</span></a>
    <a class="card" href="https://gym4.net/raspisanie-dvizheniya-prigorodnyx-poezdov/"><span class="ico">🚆</span><b>Пригородные поезда</b><span>Расписание движения</span></a>
  </div>
</main>
''')

# ---------------- НОВОСТИ ----------------
page("news.html", "Новости", "Новости гимназии: олимпиады, проекты, спорт и учебные события.",
hero("Новости гимназии", "Поиск по заголовкам и текстам, фильтр по категориям, живое обновление списка.", "События") + '''
<main id="main" class="container">
  <div class="note">Это учебные демонстрационные новости. В рабочей версии сайта они подключаются к ленте WordPress или школьной CMS.</div>
  <div class="toolbar">
    <input id="newsSearch" type="search" placeholder="Поиск по новостям…" aria-label="Поиск по новостям">
    <div class="filter" role="group" aria-label="Фильтр новостей">
      <button class="on" data-filter="all">Все</button><button data-filter="study">Учёба</button><button data-filter="olimp">Олимпиады</button><button data-filter="project">Проекты</button><button data-filter="sport">Спорт</button>
    </div>
    <span id="newsCount" class="count" aria-live="polite"></span>
  </div>
  <section id="newsList" class="news">
    <article class="card" data-cat="olimp"><time>12 ноября 2026</time><span class="badge badge-blue">Олимпиады</span><b>Школьный этап ВсОШ</b><span>Приглашаем учеников 4–11 классов. Победители пройдут на муниципальный этап.</span><p><span class="badge badge-gold">Демо</span></p></article>
    <article class="card" data-cat="sport"><time>10 ноября 2026</time><span class="badge badge-green">Спорт</span><b>Турнир «Кожаный мяч»</b><span>Сборная гимназии вышла в финал городских соревнований по футболу.</span><p><span class="badge badge-gold">Демо</span></p></article>
    <article class="card" data-cat="project"><time>8 ноября 2026</time><span class="badge badge-red">Проекты</span><b>«Орлята России»: новый сезон</b><span>Гимназия — флагманская школа федерального проекта социальной активности младших школьников.</span><p><span class="badge badge-gold">Демо</span></p></article>
    <article class="card" data-cat="study"><time>5 ноября 2026</time><span class="badge badge-blue">Учёба</span><b>Английский театр открыл сезон</b><span>Студия приглашает учеников 5–8 классов. Постановки готовятся на английском языке.</span><p><span class="badge badge-gold">Демо</span></p></article>
    <article class="card" data-cat="study"><time>1 ноября 2026</time><span class="badge badge-blue">Учёба</span><b>Родительские собрания по ГИА</b><span>В 9-х и 11-х классах прошли собрания о порядке проведения экзаменов.</span><p><span class="badge badge-gold">Демо</span></p></article>
    <article class="card" data-cat="olimp"><time>28 октября 2026</time><span class="badge badge-blue">Олимпиады</span><b>Победы на муниципальных олимпиадах</b><span>Ученики гимназии завоевали призовые места по английскому языку и математике.</span><p><span class="badge badge-gold">Демо</span></p></article>
  </section>
  <div id="newsEmpty" class="note" hidden>Ничего не найдено. Попробуйте изменить запрос или выбрать категорию «Все». <button class="btn btn-small btn-line" data-filter="all" style="margin-left:8px">Сбросить</button></div>
</main>
''')

# ---------------- КОНТАКТЫ ----------------
page("contacts.html", "Контакты", "Адрес, телефоны, e-mail, график работы и форма обратной связи гимназии №4 Астрахани.",
hero("Контакты", "Адрес, телефоны, электронная почта, график работы и обратная связь.", "Связь со школой") + '''
<main id="main" class="container">
  <div class="grid">
    <section class="card"><span class="ico">📍</span><h3>Адрес</h3><p>414024, г. Астрахань, Советский район,<br>ул. Б. Хмельницкого, д. 16, корп. 1</p><a class="btn btn-small btn-ink" href="https://yandex.ru/maps/?text=Астрахань,+улица+Богдана+Хмельницкого,+16к1" target="_blank" rel="noopener">Открыть в Яндекс.Картах</a></section>
    <section class="card"><span class="ico">📞</span><h3>Телефоны</h3><table class="kv"><tr><td>Приёмная директора</td><td><a href="tel:+78512500567">(8512) 50-05-67</a></td></tr><tr><td>Учительская / библиотека</td><td><a href="tel:+78512243404">(8512) 24-34-04</a></td></tr><tr><td>Медицинский кабинет</td><td><a href="tel:+78512336222">(8512) 33-62-22</a></td></tr></table></section>
    <section class="card"><span class="ico">✉️</span><h3>Электронная почта</h3><p><a href="mailto:gimn4@obr.astrobl.ru">gimn4@obr.astrobl.ru</a><br><a href="mailto:gum4ast@30gorod.ru">gum4ast@30gorod.ru</a></p></section>
    <section class="card"><span class="ico">🕗</span><h3>График работы</h3><table class="kv"><tr><td>Понедельник–суббота</td><td>07:30–18:30</td></tr><tr><td>Выходной</td><td>воскресенье</td></tr><tr><td>Приёмный день директора</td><td>среда, 14:00–18:00</td></tr><tr><td>Директор</td><td>Лендова Татьяна Викторовна</td></tr></table></section>
  </div>
  <h2 id="founder">Учредитель</h2>
  <section class="card"><p><b>Управление образования администрации МО «Городской округ город Астрахань»</b><br>Начальник — Фролов Сергей Сергеевич<br>414000, г. Астрахань, ул. Никольская/Ульяновых, д. 10/14<br>тел./факс: <a href="tel:+78512515727">(8512) 51-57-27</a> · <a href="mailto:uprav.obr@30gorod.ru">uprav.obr@30gorod.ru</a><br>График: пн–пт 08:30–17:30, перерыв 13:00–14:00.</p></section>
  <h2 id="feedback">Написать нам</h2>
  <section class="card form">
    <div class="note note-info">Форма учебная: сообщение сохраняется локально в браузере и не отправляется на сервер. Для реальной связи используйте почту или телефон.</div>
    <form id="fbForm">
      <label>Ваше имя<input required name="name" autocomplete="name" placeholder="Как к вам обращаться"></label>
      <label>E-mail<input required type="email" name="email" autocomplete="email" placeholder="you@example.ru"></label>
      <label>Тема<select name="topic"><option>Приём и перевод</option><option>Питание</option><option>Учебный процесс</option><option>Другое</option></select></label>
      <label>Сообщение<textarea required name="message" rows="5" placeholder="Опишите вопрос"></textarea></label>
      <label class="agree"><input required type="checkbox" name="agree">Нажимая «Отправить», я соглашаюсь на обработку персональных данных</label>
      <button class="btn btn-gold" type="submit">Отправить</button>
    </form>
    <div id="formOk" class="form-ok" hidden>✓ Сообщение сохранено. В рабочей версии оно было бы отправлено администрации сайта.</div>
  </section>
</main>
''')

# ---------------- ПРИЁМ ----------------
page("priem.html", "Приём", "Приём в 1 класс и перевод в гимназию: сроки, документы и порядок подачи заявления.",
hero("Приём в гимназию", "Порядок приёма в 1 класс и перевода в гимназию, сроки и документы.", "Поступление") + '''
<main id="main" class="container">
  <div class="note">Сроки указаны по федеральному порядку приёма. Актуальные даты кампании и закреплённые территории уточняйте в приёмной: <a href="tel:+78512500567">(8512) 50-05-67</a>.</div>
  <div class="grid">
    <section class="card" id="first"><span class="ico">🎒</span><h3>Приём в 1 класс</h3><p>Возраст ребёнка на 1 сентября: от 6,5 до 8 лет.</p><ol class="steps"><li><b>1 апреля — 30 июня</b> — заявления от детей на закреплённой территории и льготных категорий.</li><li><b>6 июля — 5 сентября</b> — заявления на оставшиеся свободные места.</li><li><b>Распорядительный акт</b> о зачислении издаётся в течение 5 рабочих дней после завершения приёма.</li></ol><p><b>Документы:</b> паспорт родителя, свидетельство о рождении ребёнка, документ о регистрации по месту жительства.</p><a class="btn btn-small btn-gold" href="https://www.gosuslugi.ru/" target="_blank" rel="noopener">Подать через Госуслуги</a> <a class="btn btn-small btn-line" href="https://gym4.net/priem-v-1-klass/">Подробности</a></section>
    <section class="card" id="gym"><span class="ico">🏫</span><h3>Приём / перевод в 5 класс</h3><p>Гимназия реализует программы повышенного уровня с углублённым изучением английского языка и спецкурсами перевода и зарубежной литературы.</p><p><b>Документы:</b> заявление, паспорт родителя, свидетельство о рождении, личное дело обучающегося и выписка оценок.</p><p>Наличие вакантных мест — <a href="sveden.html#vacant">в разделе «Вакантные места»</a> и в приёмной.</p><a class="btn btn-small btn-ink" href="https://gym4.net/priem-v-5-klass/">Условия приёма</a></section>
  </div>
  <h2>Коротко о главном</h2>
  <div class="grid">
    <section class="card"><span class="ico">📅</span><h3>Когда подавать</h3><p>Основная волна — с 1 апреля. Если остались места, продолжается с 6 июля.</p></section>
    <section class="card"><span class="ico">🧾</span><h3>Что подготовить</h3><p>Паспорт родителя, свидетельство о рождении ребёнка и подтверждение регистрации.</p></section>
    <section class="card"><span class="ico">☎️</span><h3>Куда звонить</h3><p>Приёмная директора: <a href="tel:+78512500567">(8512) 50-05-67</a>. Приёмный день — среда, 14:00–18:00.</p></section>
  </div>
</main>
''')

# ---------------- ДИЗАЙН-СИСТЕМА ----------------
page("styleguide.html", "Дизайн-система", "Палитра, типографика, компоненты и принципы дизайна учебного проекта.",
hero("Дизайн-система проекта", "Единый стиль для всех страниц: палитра, типографика, компоненты, сетка и принципы.", "Для проверки проекта") + '''
<main id="main" class="container">
  <h2>Идея стиля</h2>
  <div class="grid">
    <section class="card"><span class="ico">🖋️</span><h3>Академичность</h3><p>Глубокий чернильный синий, тёплая бумага и золото наград передают атмосферу гимназии: традиция, знание, достоинство.</p></section>
    <section class="card"><span class="ico">🌍</span><h3>Открытость миру</h3><p>Электрический синий напоминает о статусе школы ЮНЕСКО и международном профиле гимназии.</p></section>
    <section class="card"><span class="ico">♿</span><h3>Доступность</h3><p>Контрастные пары, версия для слабовидящих, фокусные состояния и уменьшение анимаций по системной настройке.</p></section>
  </div>
  <h2>Палитра</h2>
  <p class="lead">Нажмите на образец, чтобы скопировать HEX-код.</p>
  <div class="grid">
    <section class="card swatch"><div class="swatch-color" style="background:#182742"></div><h3>Чернильный</h3><p><code>#182742</code> · фон шапки, подвала, hero</p><button class="btn btn-small btn-line" data-copy="#182742">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#f5efe3"></div><h3>Бумага</h3><p><code>#F5EFE3</code> · основной фон страниц</p><button class="btn btn-small btn-line" data-copy="#F5EFE3">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#c9962e"></div><h3>Золото</h3><p><code>#C9962E</code> · главные кнопки и акценты</p><button class="btn btn-small btn-line" data-copy="#C9962E">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#2f6fd0"></div><h3>Синий ЮНЕСКО</h3><p><code>#2F6FD0</code> · ссылки и информационные акценты</p><button class="btn btn-small btn-line" data-copy="#2F6FD0">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#2e8f66"></div><h3>Успех</h3><p><code>#2E8F66</code> · подтверждения и спорт</p><button class="btn btn-small btn-line" data-copy="#2E8F66">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#c8442e"></div><h3>Важное</h3><p><code>#C8442E</code> · предупреждения и проекты</p><button class="btn btn-small btn-line" data-copy="#C8442E">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#fffcf5"></div><h3>Поверхность</h3><p><code>#FFFCF5</code> · карточки и панели</p><button class="btn btn-small btn-line" data-copy="#FFFCF5">Копировать</button></section>
    <section class="card swatch"><div class="swatch-color" style="background:#e2d6bf"></div><h3>Линия</h3><p><code>#E2D6BF</code> · границы и разделители</p><button class="btn btn-small btn-line" data-copy="#E2D6BF">Копировать</button></section>
  </div>
  <h2>Типографика</h2>
  <section class="card">
    <p class="kicker">Заголовки · Playfair Display</p>
    <p class="serif" style="font-size:2.6rem;margin:8px 0 18px">Гимназия №4 — школа с историей</p>
    <h3 style="font-size:1.5rem">Подзаголовок раздела и название карточки</h3>
    <p class="kicker" style="margin-top:22px">Основной текст · Manrope</p>
    <p>Основной шрифт хорошо читается на экранах любого размера. Используется в меню, кнопках, таблицах, формах и длинных текстах.</p>
    <p class="lead">Лид-абзац выделяет главное перед содержимым раздела. Он чуть крупнее обычного текста и задаёт спокойный тон страницы.</p>
    <p style="color:var(--muted);font-size:.88rem">Второстепенный текст: подписи, даты, технические пометки и сноски.</p>
  </section>
  <h2>Компоненты</h2>
  <div class="grid">
    <section class="card"><h3>Кнопки</h3><p><a class="btn btn-gold" href="#components">Главная</a> <a class="btn btn-ink" href="#components">Обычная</a> <a class="btn btn-line" href="#components">Контурная</a></p><p style="margin-top:12px"><a class="btn btn-small btn-gold" href="#components">Малая</a> <a class="btn btn-small btn-line" href="#components">Малая контурная</a></p></section>
    <section class="card"><h3>Бейджи</h3><p><span class="badge badge-blue">Информация</span><span class="badge badge-gold">Демо</span><span class="badge badge-green">Успех</span><span class="badge badge-red">Важное</span></p><p>Цвета кодируют смысл и всегда дублируются текстом.</p></section>
    <section class="card"><h3>Карточка-ссылка</h3><a class="card" href="#components" style="display:block"><span class="ico">📚</span><b>Пример карточки</b><span>Карточки ведут к разделам и дают мягкий отклик при наведении.</span></a></section>
    <section class="card"><h3>Формы</h3><label>Поле ввода<input placeholder="Введите текст"></label><label class="agree"><input type="checkbox">Согласие на обработку данных</label></section>
    <section class="card"><h3>Аккордеон</h3><details><summary>Как работает аккордеон?</summary><p>Используется нативный HTML-элемент details: он доступен с клавиатуры и не требует JavaScript.</p></details></section>
    <section class="card"><h3>Таблица</h3><table class="kv"><tr><td>Приёмная</td><td>(8512) 50-05-67</td></tr><tr><td>Учительская</td><td>(8512) 24-34-04</td></tr><tr><td>Медкабинет</td><td>(8512) 33-62-22</td></tr></table></section>
  </div>
  <h2 id="components">Сетка и состояния</h2>
  <section class="card">
    <p><b>Контейнер:</b> максимальная ширина 1160px, внешние поля 20px. <b>Сетка:</b> CSS Grid auto-fit, минимальная ширина колонки 260–270px.</p>
    <p><b>Радиусы:</b> карточки 18px, кнопки 12px, чипы 99px. <b>Отступы:</b> 8 / 12 / 16 / 18 / 24 / 32 / 52px.</p>
    <p><b>Состояния:</b> hover — подъём карточки и золотая граница; focus — золотое кольцо 3px; active — чернильная заливка; disabled/hidden — скрытие без потери доступности.</p>
    <div class="spacing"><span style="width:8px"></span><span style="width:12px"></span><span style="width:16px"></span><span style="width:18px"></span><span style="width:24px"></span><span style="width:32px"></span><span style="width:52px"></span></div>
  </section>
  <h2>Правила использования</h2>
  <div class="grid">
    <section class="card"><h3>Можно</h3><ul><li>Использовать золото только для главных действий</li><li>Сохранять тёплый фон и чернильные заголовки</li><li>Оставлять много воздуха вокруг текста</li><li>Помечать демонстрационные материалы</li></ul></section>
    <section class="card"><h3>Нельзя</h3><ul><li>Ставить золотой текст на светлом фоне без проверки контраста</li><li>Делать все карточки одинаковыми по цвету</li><li>Прятать важные контакты за дополнительным кликом</li><li>Убирать фокусные состояния у интерактивных элементов</li></ul></section>
  </div>
</main>
''')

print("Готово! Проект собран в папке:", OUT.resolve())
print("Открой gym4-project/index.html в браузере.")
print("Для учителя: README.md (пояснительная записка) и styleguide.html (дизайн-система).")