from pathlib import Path
import json

OUT = Path(__file__).resolve().parent / "site"
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
    <a class="topbar-btn" href="https://pos.gosuslugi.ru/form" target="_blank" rel="noopener">💬 Решаем вместе</a>
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
</div><div class="container footer-bottom"><span>© 2013–<span id="year"></span> МБОУ «Гимназия №4»</span><span>GitHub Pages demo · HTML / CSS / JS</span></div></footer>
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

CSS = '''.placeholder-card{border-style:dashed;background:linear-gradient(145deg,#fffdf8,#f7f0e2)}.placeholder-owner{font-size:.78rem!important;color:#8a641b!important;border-top:1px solid var(--line);padding-top:10px;margin-top:14px}.content-section{margin:30px 0 48px}.table-wrap{overflow-x:auto}.table-wrap table{min-width:560px}.table-wrap .placeholder-owner{margin-bottom:0}
:root{
--ink:#182742;--ink-2:#22355c;--paper:#f5efe3;--surface:#fffcf5;--overlay:#fffdf8;--scrim:rgba(16,29,53,.55);
--line:#e2d6bf;--text:#20293a;--muted:#68718a;--cool:#eef3fb;
--gold:#c9962e;--gold-2:#e8b54a;--blue:#2f6fd0;--electric:#3d8bff;--green:#2e8f66;--red:#c8442e;--amber:#d99a26;
--r:18px;--shadow:0 12px 34px rgba(24,39,66,.10);--serif:"Playfair Display",Georgia,serif;--sans:"Manrope",system-ui,sans-serif;--amb:0deg;--scroll:0}
*{box-sizing:border-box;margin:0}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:112px}
html.no-motion{scroll-behavior:auto}
body{font-family:var(--sans);background:var(--paper);color:var(--text);line-height:1.65;min-height:100vh;overflow-x:hidden}
.ambient{position:fixed;inset:-15%;z-index:-1;pointer-events:none;background:
 radial-gradient(700px 460px at 12% 8%,rgba(201,150,46,.16),transparent 62%),
 radial-gradient(760px 520px at 88% 22%,rgba(47,111,208,.14),transparent 62%),
 radial-gradient(600px 600px at 55% 95%,rgba(46,143,102,.10),transparent 60%);
 filter:hue-rotate(var(--amb));transition:filter 1.2s ease}
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
::placeholder{color:var(--muted);opacity:.85}
code{background:#f3ead9;padding:2px 7px;border-radius:6px;font-size:.85em}
.skip-link{position:fixed;left:16px;top:-60px;z-index:300;background:var(--ink);color:#fff;padding:10px 16px;border-radius:0 0 10px 10px;transition:.2s}
.skip-link:focus{top:0}
.progress{position:fixed;top:0;left:0;height:3px;width:calc(var(--scroll)*100%);background:linear-gradient(90deg,var(--gold),var(--electric),var(--green));z-index:250;box-shadow:0 0 12px rgba(61,139,255,.6)}
.container{width:min(1160px,100% - 40px);margin-inline:auto}
h1,h2,h3,.serif{font-family:var(--serif);color:var(--ink);line-height:1.18}
h2{font-size:clamp(1.5rem,2.6vw,2.1rem);margin:56px 0 18px}
h2::after{content:"";display:block;width:64px;height:4px;background:linear-gradient(90deg,var(--gold),var(--electric));border-radius:99px;margin-top:10px}
h3{font-size:1.22rem;margin-bottom:10px}
p{margin-bottom:10px}
.kicker{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}
.lead{font-size:1.05rem;color:var(--muted);max-width:720px}
.topbar{background:var(--ink);color:#dce6f7;font-size:.84rem;position:relative;z-index:60}
.topbar-in{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:7px 0;flex-wrap:wrap}
.topbar-actions{display:flex;gap:8px;flex-wrap:wrap}
.topbar-btn{color:#fff;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.22);border-radius:99px;padding:4px 13px;font:inherit;font-size:.8rem;cursor:pointer}
.topbar-btn:hover{background:rgba(255,255,255,.14);text-decoration:none}
header{position:sticky;top:0;z-index:55;background:rgba(255,252,245,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);transition:box-shadow .25s}
header.scrolled{box-shadow:0 8px 28px rgba(24,39,66,.12)}
.head-in{display:flex;align-items:center;gap:18px;padding:13px 0}
.logo{display:flex;align-items:center;gap:12px;color:var(--ink)}
.logo:hover{text-decoration:none}
.logo-badge{width:46px;height:46px;border-radius:14px;background:linear-gradient(145deg,var(--ink),var(--blue));color:var(--gold-2);display:grid;place-items:center;font:800 1.7rem var(--serif);box-shadow:inset 0 0 0 1px rgba(232,181,74,.5)}
.logo-text{font:800 1.12rem var(--serif)}
.logo-text small{display:block;font:600 .68rem var(--sans);color:var(--muted);margin-top:2px}
nav{margin-left:auto;display:flex;gap:3px;align-items:center}
nav a{padding:8px 12px;border-radius:10px;color:var(--ink);font-weight:700;font-size:.92rem}
nav a:hover{background:#f0e7d6;text-decoration:none}
nav a.active{background:var(--ink);color:#fff}
nav .nav-mobile-cta{display:none}
.nav-cta{white-space:nowrap}
.burger{display:none;margin-left:auto;background:none;border:0;font-size:1.7rem;cursor:pointer;color:var(--ink)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 22px;border-radius:12px;font-weight:800;font-size:.95rem;border:0;cursor:pointer;transition:.18s;text-decoration:none}
.btn:hover{transform:translateY(-2px);text-decoration:none}
.btn-gold{background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);box-shadow:0 8px 20px rgba(201,150,46,.32)}
.btn-ink{background:var(--ink);color:#fff}
.btn-line{background:transparent;color:var(--ink);border:2px solid var(--line)}
.btn-ghost{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.45)}
.btn-danger{background:var(--red);color:#fff}
.btn-small{padding:8px 15px;font-size:.85rem;border-radius:10px}
.hero{position:relative;overflow:hidden;color:#fff;padding:88px 0 122px;background:
 radial-gradient(700px 380px at 82% 18%,rgba(232,181,74,.3),transparent 62%),
 radial-gradient(760px 460px at 12% 90%,rgba(47,111,208,.42),transparent 60%),
 linear-gradient(135deg,#101d35,#182742 45%,#22355c)}
.hero::after,.page-hero::after{content:"";position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.35'/%3E%3C/svg%3E");opacity:.05;pointer-events:none}
.aurora{position:absolute;inset:0;overflow:hidden;pointer-events:none}
.aurora span{position:absolute;border-radius:50%;filter:blur(60px);opacity:.5;mix-blend-mode:screen}
.aurora .a1{width:420px;height:420px;left:-80px;top:-120px;background:#2f6fd0;animation:drift1 16s ease-in-out infinite alternate}
.aurora .a2{width:360px;height:360px;right:6%;top:10%;background:#c9962e;animation:drift2 20s ease-in-out infinite alternate}
.aurora .a3{width:300px;height:300px;left:38%;bottom:-140px;background:#2e8f66;animation:drift3 24s ease-in-out infinite alternate}
@keyframes drift1{to{transform:translate(70px,50px) scale(1.15)}}
@keyframes drift2{to{transform:translate(-60px,70px) scale(.9)}}
@keyframes drift3{to{transform:translate(50px,-60px) scale(1.2)}}
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
.seal{position:absolute;right:max(20px,calc((100vw - 1160px)/2));top:84px;width:150px;height:150px;opacity:.9;z-index:1}
.seal text{font:700 9.5px var(--sans);letter-spacing:.16em;fill:var(--gold-2)}
.seal .seal-num{font:800 44px var(--serif);letter-spacing:0}
.seal-rot{transform-origin:60px 60px;animation:spin 44s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.ticker{background:var(--ink-2);color:#e7eefc;border-block:1px solid rgba(255,255,255,.12);overflow:hidden;position:relative;z-index:2}
.ticker-track{display:flex;gap:0;width:max-content;animation:marquee 30s linear infinite}
.ticker:hover .ticker-track{animation-play-state:paused}
.ticker span{padding:10px 28px;font-size:.85rem;font-weight:700;letter-spacing:.04em;white-space:nowrap;border-right:1px solid rgba(255,255,255,.12)}
.ticker b{color:var(--gold-2)}
@keyframes marquee{to{transform:translateX(-50%)}}
.page-hero{position:relative;overflow:hidden;color:#fff;padding:44px 0 50px;background:radial-gradient(600px 300px at 85% 20%,rgba(232,181,74,.24),transparent 60%),linear-gradient(130deg,#101d35,#22355c)}
.page-hero h1{color:#fff;font-size:clamp(1.7rem,3.2vw,2.5rem)}
.page-hero .lead{color:#d7e2f5;margin-top:8px}
.crumbs{font-size:.84rem;color:#b9c7de;margin-bottom:12px}
.crumbs a{color:#fff}
main{padding:52px 0 20px;position:relative;z-index:1}
.cards,.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.grid{margin:18px 0}
.overlap{margin-top:-122px;position:relative;z-index:3}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:24px;box-shadow:var(--shadow);color:var(--text);transition:transform .2s,box-shadow .2s,border-color .2s;overflow-wrap:break-word}
a.card:hover,article.card:hover{transform:translateY(-4px);border-color:var(--gold);box-shadow:0 18px 42px rgba(24,39,66,.16);text-decoration:none}
.card .ico{width:46px;height:46px;border-radius:13px;display:grid;place-items:center;font-size:1.5rem;background:linear-gradient(145deg,#f3e6c9,#fff8ea);border:1px solid var(--line);margin-bottom:12px}
.card b{display:block;font-size:1.05rem;margin-bottom:5px;color:var(--ink)}
.card p,.card li,.card>span:not(.badge):not(.ico){font-size:.93rem;color:var(--muted)}
.card ul,.card ol{padding-left:20px}
.news{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}
time{font-size:.78rem;font-weight:800;color:var(--blue)}
.badge{display:inline-block;border-radius:99px;padding:3px 11px;font-size:.74rem;font-weight:800;margin:6px 6px 6px 0}
.badge-blue{background:#e7effc;color:#245a9e}.badge-gold{background:#f7ecd4;color:#8a641b}.badge-green{background:#e2f2ea;color:#226b4c}.badge-red{background:#f9e7e3;color:#963826}
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
.toolbar input[type="search"]{flex:1;min-width:200px;padding:11px 14px;border:1px solid var(--line);border-radius:11px;font:inherit;background:#fff}
.toolbar select{padding:11px 14px;border:1px solid var(--line);border-radius:11px;font:inherit;font-weight:700;background:#fff;color:var(--ink)}
.filter{display:flex;gap:7px;flex-wrap:wrap}
.filter button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:8px 14px;font:inherit;font-size:.86rem;font-weight:800;cursor:pointer;color:var(--ink)}
.filter button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.count{font-size:.85rem;color:var(--muted);font-weight:700}
.steps{counter-reset:s;list-style:none;padding:0;margin:12px 0}
.steps li{position:relative;padding:0 0 18px 48px;color:var(--muted)}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);display:grid;place-items:center;font-weight:800}
.note{background:#fff5df;border:1px solid #ecd39a;border-radius:14px;padding:13px 16px;font-size:.9rem;margin:16px 0;color:#6d541e}
.note-info{background:var(--cool);border-color:#c6d8f5;color:#284f86}
.form label{display:block;font-weight:800;font-size:.9rem;color:var(--ink);margin-bottom:14px}
.form input,.form textarea,.form select{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:12px;font:inherit;margin-top:6px;background:#fff;color:var(--text)}
.form input:focus,.form textarea:focus,.form select:focus{border-color:var(--gold);box-shadow:0 0 0 4px rgba(201,150,46,.15);outline:none}
.form .agree{display:flex;gap:10px;align-items:flex-start;font-size:.85rem;color:var(--muted);font-weight:600}
.form .agree input{width:auto;margin:4px 0 0}
.form-ok{background:#e2f2ea;border:1px solid #a9d6c1;color:#226b4c;border-radius:14px;padding:14px 16px;margin:14px 0;font-weight:700}
.msg-item{display:flex;gap:14px;align-items:flex-start;justify-content:space-between;padding:14px 0;border-bottom:1px solid var(--line)}
.msg-item:last-child{border-bottom:0}
.msg-item b{margin-bottom:2px}
.msg-item p{margin:0;font-size:.88rem}
.msg-meta{font-size:.78rem;color:var(--muted)}
.with-aside{display:grid;grid-template-columns:250px 1fr;gap:26px;align-items:start}
.aside-nav{position:sticky;top:112px;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:var(--shadow)}
.aside-nav p{font-weight:800;color:var(--ink);font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
.aside-nav a{display:block;padding:7px 10px;border-radius:9px;font-size:.88rem;font-weight:700;color:var(--muted)}
.aside-nav a:hover{background:#f0e7d6;text-decoration:none}
.aside-nav a.on{background:var(--ink);color:#fff}
.history{display:grid;grid-template-columns:190px 1fr;gap:26px;align-items:start;margin:18px 0}
.history-pin{position:sticky;top:120px}
.history-pin .serif{font-size:3.4rem;color:var(--gold);line-height:1}
.history-pin p{font-size:.88rem;color:var(--muted)}
.timeline{list-style:none;padding:0;margin:0;border-left:3px solid var(--line)}
.timeline li{position:relative;padding:0 0 26px 26px}
.timeline li::before{content:"";position:absolute;left:-9px;top:4px;width:15px;height:15px;border-radius:50%;background:linear-gradient(135deg,var(--gold-2),var(--blue));box-shadow:0 0 0 4px var(--paper)}
.timeline b{color:var(--ink);display:block}
.timeline span{font-size:.92rem;color:var(--muted)}
.swatch-color{height:84px;border-radius:12px;border:1px solid var(--line);margin-bottom:12px}
.spacing{display:flex;gap:10px;align-items:flex-end;margin-top:14px;flex-wrap:wrap}
.spacing span{display:block;height:26px;background:linear-gradient(135deg,var(--gold-2),var(--blue));border-radius:6px}
footer{background:var(--ink);color:#c3d0e5;margin-top:64px;padding:46px 0 22px;font-size:.9rem;position:relative;z-index:1}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1.2fr;gap:32px}
.footer-logo{font:800 1.4rem var(--serif);color:var(--gold-2);margin-bottom:10px}
.footer-title{font-weight:800;color:#fff;margin-bottom:10px}
.footer-demo{font-size:.8rem;color:#8fa1bd;margin-top:10px}
footer a{display:block;color:#9fc2f0;margin:5px 0}
.footer-bottom{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.14);margin-top:30px;padding-top:16px;font-size:.8rem;color:#8fa1bd}
.cookie{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);width:min(720px,92%);background:var(--overlay);border:1px solid var(--line);border-radius:16px;box-shadow:0 16px 46px var(--scrim);padding:16px 20px;display:flex;gap:16px;align-items:center;z-index:90;font-size:.9rem}
.to-top{position:fixed;right:20px;bottom:20px;width:46px;height:46px;border-radius:50%;border:0;background:linear-gradient(135deg,var(--gold-2),var(--gold));color:var(--ink);font-size:1.3rem;font-weight:800;cursor:pointer;box-shadow:0 10px 26px rgba(201,150,46,.4);opacity:0;visibility:hidden;pointer-events:none;transition:.25s;z-index:80}
.to-top.show{opacity:1;visibility:visible;pointer-events:auto}
.toast{position:fixed;left:50%;bottom:84px;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;padding:11px 16px;border-radius:12px;font-size:.9rem;font-weight:700;opacity:0;pointer-events:none;transition:.25s;z-index:120;box-shadow:0 10px 30px rgba(0,0,0,.3);display:flex;gap:12px;align-items:center}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto}
.toast-action{background:var(--gold-2);color:var(--ink);border:0;border-radius:8px;padding:5px 12px;font-weight:800;cursor:pointer}
.icon-btn{background:none;border:0;font-size:1rem;cursor:pointer;color:var(--ink)}
.a11y-panel{position:fixed;right:18px;top:78px;z-index:110;width:310px;background:var(--overlay);border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 50px rgba(24,39,66,.25);padding:18px}
.a11y-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.a11y-label{font-size:.85rem;font-weight:800;color:var(--ink);margin:10px 0 6px}
.a11y-label.toggle{display:flex;gap:8px;align-items:center;font-weight:700}
.a11y-panel input[type="range"]{width:100%;accent-color:var(--gold)}
.scheme-row{display:flex;gap:8px;margin:8px 0 14px}
.scheme{width:42px;height:42px;border-radius:11px;border:2px solid var(--line);font:800 1rem var(--serif);cursor:pointer;background:var(--surface);color:var(--ink)}
.scheme.on{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,150,46,.25)}
.scheme-bw{background:#fff;color:#000}.scheme-wb{background:#000;color:#fff}.scheme-blue{background:#dceafc;color:#123c69}
body[data-scheme="bw"]{--paper:#fff;--surface:#fff;--overlay:#fff;--text:#000;--muted:#111;--line:#000;--ink:#000;--blue:#000;--cool:#fff}
body[data-scheme="bw"] .hero,body[data-scheme="bw"] .page-hero,body[data-scheme="bw"] footer,body[data-scheme="bw"] .topbar,body[data-scheme="bw"] .ticker{background:#000!important;color:#fff}
body[data-scheme="bw"] .ambient{display:none}
body[data-scheme="bw"] .card,body[data-scheme="bw"] details,body[data-scheme="bw"] .chips a{border-width:2px}
body[data-scheme="wb"]{--paper:#000;--surface:#111;--overlay:#111;--text:#fff;--muted:#ddd;--line:#fff;--ink:#fff;--blue:#fff;--cool:#111}
body[data-scheme="wb"] .hero,body[data-scheme="wb"] .page-hero,body[data-scheme="wb"] footer,body[data-scheme="wb"] .topbar,body[data-scheme="wb"] .ticker{background:#000!important;color:#fff}
body[data-scheme="wb"] header{background:#000;border-color:#fff}
body[data-scheme="wb"] .ambient{display:none}
body[data-scheme="wb"] h1,body[data-scheme="wb"] h2,body[data-scheme="wb"] h3,body[data-scheme="wb"] .logo,body[data-scheme="wb"] nav a{color:#fff}
body[data-scheme="wb"] th{background:#222;color:#fff}
body[data-scheme="wb"] tr:hover td{background:#1a1a1a}
body[data-scheme="wb"] .form input,body[data-scheme="wb"] .form textarea,body[data-scheme="wb"] .form select,body[data-scheme="wb"] .toolbar input,body[data-scheme="wb"] .toolbar select{background:#111;color:#fff;border-color:#fff}
body[data-scheme="wb"] .filter button{background:#111;color:#fff;border-color:#fff}
body[data-scheme="wb"] .note{background:#221a00;color:#ffd;border-color:#aa8}
body[data-scheme="wb"] .btn-gold,body[data-scheme="wb"] .btn-ink{background:#fff;color:#000}
body[data-scheme="wb"] nav a.active,body[data-scheme="wb"] .aside-nav a.on{background:#fff;color:#000}
body[data-scheme="blue"]{--paper:#dceafc;--surface:#eef5ff;--overlay:#eef5ff;--text:#123c69;--muted:#24527e;--line:#7ba7d7;--ink:#123c69;--blue:#123c69;--cool:#d4e5fa}
body[data-scheme="blue"] .hero,body[data-scheme="blue"] .page-hero{background:#123c69!important}
body[data-scheme="blue"] header{background:rgba(238,245,255,.92)}
body[data-scheme="blue"] th{background:#d4e5fa}
.rv{opacity:0;transform:translateY(18px);transition:opacity .55s ease,transform .55s ease}
.rv.in{opacity:1;transform:none}
html.no-motion .rv{opacity:1;transform:none}
html.no-motion .aurora span,html.no-motion .seal-rot,html.no-motion .ticker-track{animation:none}
@media (max-width:980px){
nav{display:none;position:absolute;top:100%;left:0;right:0;background:var(--surface);flex-direction:column;align-items:stretch;padding:14px 20px;border-bottom:1px solid var(--line);box-shadow:0 18px 34px rgba(24,39,66,.15)}
nav.open{display:flex}
.burger{display:block}
.nav-cta{display:none}
nav .nav-mobile-cta{display:flex;margin-top:8px}
nav .nav-mobile-cta:hover{background:linear-gradient(135deg,var(--gold-2),var(--gold))}
.seal{display:none}
.stats{grid-template-columns:repeat(2,1fr)}
.footer-grid{grid-template-columns:1fr 1fr}
.with-aside{grid-template-columns:1fr}
.aside-nav{position:static;display:flex;gap:6px;overflow-x:auto;padding:10px}
.aside-nav p{display:none}
.aside-nav a{white-space:nowrap}
.history{grid-template-columns:1fr}
.history-pin{position:static}
}
@media (max-width:640px){
.container{width:min(100% - 28px,1160px)}
.topbar-name{display:none}
.hero{padding:58px 0 96px}
.overlap{margin-top:-92px}
.footer-grid{grid-template-columns:1fr}
.cookie{flex-direction:column;text-align:center}
.a11y-panel{left:14px;right:14px;width:auto;top:64px}
.toolbar{align-items:stretch}
.toolbar input[type="search"]{min-width:0}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}.rv{opacity:1;transform:none}}
@media print{.topbar,header,.a11y-panel,.cookie,.to-top,.toast,footer,.progress,.ambient,.ticker{display:none!important}body{background:#fff;color:#000}.hero,.page-hero{background:#fff!important;color:#000!important;padding:20px 0}.hero h1,.page-hero h1{color:#000}.card{box-shadow:none;border:1px solid #999}}
'''

JS = '''(() => {
"use strict";
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
const store={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch{return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}};
const root=document.documentElement;
const toastEl=$("#toast"),toastText=$("#toastText"),toastAction=$("#toastAction");
let toastTimer,actionFn=null;
const toast=(msg,actionLabel,fn)=>{if(!toastEl)return;toastText.textContent=msg;actionFn=fn||null;toastAction.hidden=!actionLabel;toastAction.textContent=actionLabel||"";toastEl.classList.add("show");clearTimeout(toastTimer);toastTimer=setTimeout(()=>toastEl.classList.remove("show"),actionLabel?6000:2600)};
if(toastAction)toastAction.onclick=()=>{if(actionFn)actionFn();toastEl.classList.remove("show")};
const year=$("#year");if(year)year.textContent=new Date().getFullYear();

/* scroll: progress, header, parallax */
const header=$("#siteHeader"),toTop=$("#toTop"),parallax=$$("[data-parallax]");
let ticking=false;
const onScroll=()=>{if(ticking)return;ticking=true;requestAnimationFrame(()=>{
 const max=root.scrollHeight-innerHeight;root.style.setProperty("--scroll",max>0?(scrollY/max).toFixed(4):0);
 if(header)header.classList.toggle("scrolled",scrollY>8);
 if(toTop)toTop.classList.toggle("show",scrollY>650);
 if(!root.classList.contains("no-motion"))parallax.forEach(el=>{const sp=+el.dataset.parallax||.12;el.style.transform="translateY("+Math.min(scrollY,700)*sp+"px)"});
 ticking=false})};
addEventListener("scroll",onScroll,{passive:true});onScroll();
if(toTop)toTop.onclick=()=>scrollTo({top:0,behavior:root.classList.contains("no-motion")?"auto":"smooth"});

/* mobile menu */
const burger=$("#burger"),nav=$("#nav");
const setMenu=o=>{if(!burger||!nav)return;nav.classList.toggle("open",o);burger.setAttribute("aria-expanded",String(o));burger.setAttribute("aria-label",o?"Закрыть меню":"Открыть меню");burger.textContent=o?"✕":"☰"};
if(burger)burger.onclick=()=>setMenu(!nav.classList.contains("open"));
if(nav)nav.addEventListener("click",e=>{if(e.target.closest("a"))setMenu(false)});

/* accessibility */
const panel=$("#a11yPanel"),aBtn=$("#a11yBtn"),fsRange=$("#fsRange"),fsValue=$("#fsValue"),motion=$("#motionToggle"),schemes=$$(".scheme");
let a11y=Object.assign({fs:100,scheme:"",motion:true},store.get("gym4-a11y",{}));
const applyA11y=s=>{root.style.fontSize=s.fs+"%";document.body.dataset.scheme=s.scheme||"";root.classList.toggle("no-motion",!s.motion||matchMedia("(prefers-reduced-motion: reduce)").matches);if(fsRange)fsRange.value=s.fs;if(fsValue)fsValue.textContent=s.fs+"%";if(motion)motion.checked=!!s.motion;schemes.forEach(b=>b.classList.toggle("on",(b.dataset.scheme||"")===(s.scheme||"")))};
applyA11y(a11y);
const setPanel=o=>{if(!panel||!aBtn)return;panel.hidden=!o;aBtn.setAttribute("aria-expanded",String(o))};
if(aBtn)aBtn.onclick=()=>setPanel(panel.hidden);
if($("#a11yClose"))$("#a11yClose").onclick=()=>setPanel(false);
if(fsRange)fsRange.oninput=()=>{a11y.fs=+fsRange.value;applyA11y(a11y);store.set("gym4-a11y",a11y)};
schemes.forEach(b=>b.onclick=()=>{a11y.scheme=b.dataset.scheme||"";applyA11y(a11y);store.set("gym4-a11y",a11y)});
if(motion)motion.onchange=()=>{a11y.motion=motion.checked;applyA11y(a11y);store.set("gym4-a11y",a11y)};
if($("#a11yReset"))$("#a11yReset").onclick=()=>{a11y={fs:100,scheme:"",motion:true};applyA11y(a11y);store.set("gym4-a11y",a11y);toast("Обычная версия восстановлена")};
addEventListener("keydown",e=>{if(e.key==="Escape"){setMenu(false);setPanel(false)}});

/* cookie */
const cookie=$("#cookie");
if(cookie&&!store.get("gym4-cookie",false))cookie.hidden=false;
if($("#cookieOk"))$("#cookieOk").onclick=()=>{store.set("gym4-cookie",true);cookie.hidden=true;toast("Настройки сохранены")};

/* reveals + count-up + mood */
const noMotion=()=>root.classList.contains("no-motion");
const targets=$$(".hero .container > *, main h2, main .card, .page-hero .container > *, .timeline li");
if("IntersectionObserver" in window){
 const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}}),{threshold:.12});
 targets.forEach((el,i)=>{el.classList.add("rv");el.style.transitionDelay=(i%5)*55+"ms";io.observe(el)});
 const cio=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting)return;const el=en.target;cio.unobserve(el);const end=+el.dataset.count,suf=el.dataset.suffix||"";if(noMotion()){el.textContent=end+suf;return}
  const t0=performance.now(),dur=1200;const step=t=>{const p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);el.textContent=Math.round(end*e)+suf;if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)}),{threshold:.5});
 $$("[data-count]").forEach(el=>cio.observe(el));
 const moods={gold:"0deg",blue:"38deg",green:"86deg",red:"-28deg"};
 const mio=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)root.style.setProperty("--amb",moods[en.target.dataset.mood]||"0deg")}),{threshold:.35});
 $$("[data-mood]").forEach(el=>mio.observe(el));
}else{targets.forEach(el=>el.classList.add("in"));$$("[data-count]").forEach(el=>el.textContent=el.dataset.count+(el.dataset.suffix||""))}

/* scrollspy for aside */
const aside=$(".aside-nav");
if(aside&&"IntersectionObserver" in window){
 const links=$$("a[href^='#']",aside),map=new Map(links.map(a=>[a.getAttribute("href").slice(1),a]));
 const sio=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){links.forEach(a=>a.classList.remove("on"));const a=map.get(en.target.id);if(a)a.classList.add("on")}}),{rootMargin:"-30% 0px -60% 0px"});
 map.forEach((a,id)=>{const sec=document.getElementById(id);if(sec)sio.observe(sec)});
}

/* news: search + filter + sort */
const list=$("#newsList");
if(list){
 const search=$("#newsSearch"),sort=$("#newsSort"),count=$("#newsCount"),empty=$("#newsEmpty");
 let cat="all";
 const items=$$("#newsList [data-cat]");
 const apply=()=>{const q=(search?.value||"").trim().toLowerCase();
  const sorted=[...items].sort((a,b)=>sort.value==="asc"?a.dataset.date.localeCompare(b.dataset.date):b.dataset.date.localeCompare(a.dataset.date));
  sorted.forEach(el=>list.appendChild(el));let n=0;
  items.forEach(el=>{const ok=(cat==="all"||el.dataset.cat===cat)&&(!q||el.textContent.toLowerCase().includes(q));el.hidden=!ok;if(ok)n++});
  count.textContent="Показано: "+n+" из "+items.length;empty.hidden=n!==0};
 $$("[data-filter]").forEach(b=>b.onclick=()=>{cat=b.dataset.filter;if(!b.closest(".filter")&&search)search.value="";$$(".filter button").forEach(x=>x.classList.toggle("on",x.dataset.filter===cat));apply()});
 if(search)search.oninput=apply;if(sort)sort.onchange=apply;apply();
}

/* Demo form: never transmits or persists user input. */
const form=$("#fbForm");
if(form)form.addEventListener("submit",e=>{e.preventDefault();toast("Демо-режим: данные не отправлены и не сохранены.")});

/* copy hex */
const copy=async t=>{try{await navigator.clipboard.writeText(t)}catch{const ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove()}toast("Скопировано: "+t)};
$$("[data-copy]").forEach(b=>b.onclick=()=>copy(b.dataset.copy));
})();
'''

(OUT / "assets/css/style.css").write_text(CSS, encoding="utf-8")
(OUT / "assets/js/app.js").write_text(JS, encoding="utf-8")
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
