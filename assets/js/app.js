(function(){
"use strict";var root=document.documentElement,key="gym4-a11y";root.classList.add("js");
function read(){try{return JSON.parse(localStorage.getItem(key))||{}}catch(e){return{}}}function write(v){try{localStorage.setItem(key,JSON.stringify(v))}catch(e){}}
var saved=read(),state={fs:["100","125","150","175","200"].indexOf(saved.fs)>=0?saved.fs:"100",scheme:["","bw","wb"].indexOf(saved.scheme)>=0?saved.scheme:"",spacing:["normal","wide"].indexOf(saved.spacing)>=0?saved.spacing:"normal",images:["show","hide"].indexOf(saved.images)>=0?saved.images:"show",motion:["on","off"].indexOf(saved.motion)>=0?saved.motion:"on"};
function apply(){root.style.fontSize=state.fs+"%";if(state.scheme)root.setAttribute("data-scheme",state.scheme);else root.removeAttribute("data-scheme");root.setAttribute("data-spacing",state.spacing);root.setAttribute("data-images",state.images);root.setAttribute("data-motion",state.motion);document.querySelectorAll("[data-fs],[data-scheme],[data-spacing],[data-images],[data-motion]").forEach(function(b){var k=["fs","scheme","spacing","images","motion"].filter(function(x){return b.hasAttribute("data-"+x)})[0];if(k)b.setAttribute("aria-pressed",String((b.dataset[k]||"")===state[k]))})}apply();
function init(){var year=document.getElementById("year");if(year)year.textContent=new Date().getFullYear();var menu=document.getElementById("menuToggle"),nav=document.getElementById("siteNav"),a11y=document.getElementById("a11yToggle"),panel=document.getElementById("a11yPanel");function setMenu(v){if(!menu||!nav)return;nav.classList.toggle("open",v);menu.setAttribute("aria-expanded",String(v));menu.setAttribute("aria-label",v?"Закрыть меню":"Открыть меню") }function setPanel(v){if(!a11y||!panel)return;panel.hidden=!v;a11y.setAttribute("aria-expanded",String(v))}if(menu)menu.addEventListener("click",function(){setMenu(!nav.classList.contains("open"))});if(nav)nav.addEventListener("click",function(e){if(e.target.closest("a"))setMenu(false)});document.addEventListener("click",function(e){if(menu&&nav&&!menu.contains(e.target)&&!nav.contains(e.target))setMenu(false)});if(a11y)a11y.addEventListener("click",function(){setPanel(panel.hidden)});document.addEventListener("keydown",function(e){if(e.key==="Escape"){setMenu(false);setPanel(false)}});
[["fs","[data-fs]"],["scheme","[data-scheme]"],["spacing","[data-spacing]"],["images","[data-images]"],["motion","[data-motion]"]].forEach(function(pair){document.querySelectorAll(pair[1]).forEach(function(b){b.addEventListener("click",function(){state[pair[0]]=b.dataset[pair[0]]||"";apply();write(state)})})});var reset=document.getElementById("a11yReset");if(reset)reset.addEventListener("click",function(){state={fs:"100",scheme:"",spacing:"normal",images:"show",motion:"on"};apply();write(state)});
var aside=document.querySelector(".aside-panel");if(aside&&"IntersectionObserver"in window){var links=Array.prototype.slice.call(aside.querySelectorAll('a[href^="#"]')),sections=links.map(function(a){return document.getElementById(a.getAttribute("href").slice(1))}).filter(Boolean),observer=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting)links.forEach(function(a){a.classList.toggle("is-active",a.hash==="#"+entry.target.id)})})},{rootMargin:"-20% 0px -68% 0px"});sections.forEach(function(s){observer.observe(s)})}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();})();

/* GYM4 interface enhancements: site search, reading progress and reveal motion. */
(function () {
  "use strict";

  var pages = ["index.html", "history.html", "news.html", "parents.html", "students.html", "priem.html", "contacts.html", "sveden.html", "school-life.html", "election.html"];
  var entries = [
    { title: "Главная", description: "О гимназии, история, направления и новости.", href: "index.html", keywords: "школа гимназия" },
    { title: "История гимназии", description: "История школы № 46 и становление гимназии № 4.", href: "history.html", keywords: "история основание 1964 1997" },
    { title: "Новости и объявления", description: "Публикации, события, объявления и школьная жизнь.", href: "news.html", keywords: "новости мероприятия" },
    { title: "Родителям", description: "Питание, безопасность, поддержка ребёнка и обращения.", href: "parents.html", keywords: "семья питание безопасность" },
    { title: "Обучающимся", description: "Учебный процесс, расписание, проекты, олимпиады и кружки.", href: "students.html", keywords: "ученики расписание олимпиады" },
    { title: "Приём в гимназию", description: "Порядок зачисления, документы и ответы на вопросы.", href: "priem.html", keywords: "поступление зачисление первый класс" },
    { title: "Контакты", description: "Адрес, телефоны, электронная почта и как добраться.", href: "contacts.html", keywords: "адрес телефон почта" },
    { title: "Сведения об образовательной организации", description: "Документы, образование, руководство, питание и материальная база.", href: "sveden.html", keywords: "сведения документы образование устав" },
    { title: "Школьная жизнь", description: "События, достижения, школьные проекты и внеурочная деятельность.", href: "school-life.html", keywords: "календарь мероприятия достижения кружки" },
    { title: "Выборы президента гимназии", description: "Кандидаты, программы, агитационные материалы и ученическое самоуправление.", href: "election.html", keywords: "выборы президент школьное самоуправление кандидат программа голосование" }
  ];
  var indexed = false;
  var searchDialog, searchInput, resultList, searchButton;

  function addEntry(entry) {
    var title = (entry.title || "").trim();
    var href = (entry.href || "").trim();
    if (!title || !href) return;
    var key = href + "|" + title.toLocaleLowerCase("ru");
    if (entries.some(function (item) { return item.key === key || (item.href + "|" + item.title.toLocaleLowerCase("ru")) === key; })) return;
    entries.push({ key: key, title: title, href: href, description: (entry.description || "").replace(/\s+/g, " ").trim().slice(0, 180), keywords: entry.keywords || "" });
  }

  function buildIndex() {
    if (indexed || !("fetch" in window) || !("DOMParser" in window)) return;
    indexed = true;
    pages.forEach(function (path) {
      fetch(path, { credentials: "same-origin" }).then(function (response) {
        if (!response.ok) throw new Error("Page unavailable");
        return response.text();
      }).then(function (source) {
        var doc = new DOMParser().parseFromString(source, "text/html");
        var title = doc.querySelector("title");
        var description = doc.querySelector('meta[name="description"]');
        var pageTitle = title ? title.textContent.replace(/\s*[—|].*$/, "").trim() : path;
        addEntry({ title: pageTitle, href: path, description: description ? description.content : "", keywords: path });
        Array.prototype.forEach.call(doc.querySelectorAll("main h1, main h2, main h3"), function (heading) {
          var label = heading.textContent.replace(/\s+/g, " ").trim();
          if (!label || label === pageTitle) return;
          var target = heading.id ? heading : heading.closest("[id]");
          var scope = heading.closest("section, article") || heading.parentElement;
          addEntry({
            title: label,
            href: path + (target && target.id ? "#" + encodeURIComponent(target.id) : ""),
            description: scope ? scope.textContent : label,
            keywords: path + " " + label
          });
        });
        renderResults();
      }).catch(function () { /* Keep the built-in page index as an offline fallback. */ });
    });
  }

  function renderResults() {
    if (!resultList || !searchInput) return;
    var query = searchInput.value.trim().toLocaleLowerCase("ru");
    var tokens = query.split(/\s+/).filter(Boolean);
    var filtered = entries.map(function (item) {
      var title = item.title.toLocaleLowerCase("ru");
      var text = (item.title + " " + item.description + " " + (item.keywords || "") + " " + item.href).toLocaleLowerCase("ru");
      var match = tokens.every(function (token) { return text.indexOf(token) !== -1; });
      var score = title.indexOf(query) === 0 ? 4 : (title.indexOf(query) !== -1 ? 3 : 1);
      return { item: item, match: match, score: score };
    }).filter(function (item) {
      return tokens.length ? item.match : item.item.href.indexOf("#") === -1;
    }).sort(function (a, b) {
      return b.score - a.score || a.item.title.localeCompare(b.item.title, "ru");
    }).slice(0, 9);

    resultList.textContent = "";
    if (!filtered.length) {
      var empty = document.createElement("p");
      empty.className = "site-search__empty";
      empty.textContent = "Ничего не найдено. Попробуйте другое слово.";
      resultList.appendChild(empty);
      return;
    }

    filtered.forEach(function (result) {
      var link = document.createElement("a");
      link.className = "site-search__result";
      link.href = result.item.href;
      link.setAttribute("role", "listitem");
      var title = document.createElement("strong");
      title.textContent = result.item.title;
      var summary = document.createElement("span");
      summary.textContent = result.item.description || result.item.href;
      link.appendChild(title);
      link.appendChild(summary);
      resultList.appendChild(link);
    });
  }

  function initSearch() {
    var tools = document.querySelector(".header-tools");
    if (!tools) return;

    searchButton = document.createElement("button");
    searchButton.type = "button";
    searchButton.className = "tool-btn search-trigger";
    searchButton.setAttribute("aria-label", "Поиск по сайту");
    searchButton.setAttribute("aria-haspopup", "dialog");
    searchButton.innerHTML = '<span class="search-trigger__mark" aria-hidden="true">⌕</span><span class="search-trigger__label">Поиск</span>';
    tools.insertBefore(searchButton, tools.firstChild);

    searchDialog = document.createElement("dialog");
    searchDialog.className = "site-search-dialog";
    searchDialog.setAttribute("aria-labelledby", "siteSearchTitle");
    searchDialog.innerHTML =
      '<div class="site-search__panel">' +
        '<div class="site-search__top"><div><span class="site-search__eyebrow">БЫСТРАЯ НАВИГАЦИЯ</span><h2 id="siteSearchTitle">Что вы ищете?</h2></div>' +
        '<button class="site-search__close" type="button" aria-label="Закрыть поиск">×</button></div>' +
        '<label class="site-search__input-wrap"><span class="site-search__magnify" aria-hidden="true">⌕</span>' +
        '<input class="site-search__input" type="search" autocomplete="off" placeholder="Например: расписание, питание, документы…" aria-label="Поиск по страницам и разделам"></label>' +
        '<p class="site-search__hint" aria-live="polite">Поиск по разделам сайта</p>' +
        '<div class="site-search__results" role="list" aria-label="Результаты поиска"></div>' +
        '<div class="site-search__foot"><span>Откройте подходящий раздел одним нажатием</span><span><kbd class="site-search__key">Ctrl</kbd> + <kbd class="site-search__key">K</kbd> · <kbd class="site-search__key">Esc</kbd></span></div>' +
      '</div>';
    document.body.appendChild(searchDialog);
    searchInput = searchDialog.querySelector(".site-search__input");
    resultList = searchDialog.querySelector(".site-search__results");

    function open() {
      if (typeof searchDialog.showModal === "function") searchDialog.showModal();
      else searchDialog.setAttribute("open", "");
      searchInput.value = "";
      renderResults();
      searchInput.focus();
      buildIndex();
    }
    function close() {
      if (typeof searchDialog.close === "function" && searchDialog.open) searchDialog.close();
      else searchDialog.removeAttribute("open");
    }

    searchButton.addEventListener("click", open);
    searchDialog.querySelector(".site-search__close").addEventListener("click", close);
    searchDialog.addEventListener("click", function (event) {
      if (event.target === searchDialog) close();
    });
    searchDialog.addEventListener("close", function () { searchButton.focus(); });
    searchInput.addEventListener("input", renderResults);
    searchButton.__openSearch = open;
  }

  function initReadingTools() {
    var progress = document.createElement("div");
    progress.className = "reading-progress";
    progress.setAttribute("role", "progressbar");
    progress.setAttribute("aria-label", "Прогресс чтения страницы");
    progress.setAttribute("aria-valuemin", "0");
    progress.setAttribute("aria-valuemax", "100");
    progress.setAttribute("aria-valuenow", "0");
    progress.innerHTML = '<span class="reading-progress__bar"></span>';
    document.body.appendChild(progress);
    var bar = progress.querySelector(".reading-progress__bar");

    var top = document.createElement("button");
    top.type = "button";
    top.className = "back-to-top";
    top.textContent = "↑ Наверх";
    top.setAttribute("aria-label", "Вернуться к началу страницы");
    top.hidden = true;
    document.body.appendChild(top);
    top.addEventListener("click", function () {
      try { window.scrollTo({ top: 0, behavior: "smooth" }); }
      catch (error) { window.scrollTo(0, 0); }
    });

    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var value = max > 0 ? Math.min(100, Math.max(0, window.scrollY / max * 100)) : 0;
      bar.style.transform = "scaleX(" + (value / 100) + ")";
      progress.setAttribute("aria-valuenow", String(Math.round(value)));
      var visible = window.scrollY > 420;
      top.hidden = !visible;
      top.classList.toggle("is-visible", visible);
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  function initReveal() {
    if (!("IntersectionObserver" in window) || (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
    var nodes = document.querySelectorAll(".quick-card, .school-fact, .home-direction, .feature-card, .data-card, .contact-card, .news-entry");
    if (!nodes.length) return;
    var observer = new IntersectionObserver(function (items) {
      items.forEach(function (item) {
        if (item.isIntersecting) {
          item.target.classList.add("is-visible");
          observer.unobserve(item.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });
    Array.prototype.forEach.call(nodes, function (node) {
      node.classList.add("motion-reveal");
      observer.observe(node);
    });
  }

  function init() {
    initSearch();
    initReadingTools();
    initReveal();
    document.addEventListener("keydown", function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k" && searchButton && searchButton.__openSearch) {
        event.preventDefault();
        searchButton.__openSearch();
      }
      if (event.key === "Escape" && searchDialog && searchDialog.open) searchDialog.close();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

/* Seasonal event themes: automatic calendar + explicit HTML override. */
(function(){
"use strict";
function orthodoxEaster(year){
 var a=year%4,b=year%7,c=year%19,x=(19*c+15)%30,y=(2*a+4*b-x+34)%7;
 var month=Math.floor((x+y+114)/31),day=((x+y+114)%31)+1;
 var result=new Date(Date.UTC(year,month-1,day));
 result.setUTCDate(result.getUTCDate()+(year>=2100?14:13));return result;
}
function chooseTheme(now){
 var y=now.getFullYear(),m=now.getMonth(),d=now.getDate();
 if((m===11&&d>=20)||(m===0&&d<=10))return "new-year";
 if(m===1&&d>=15&&d<=24)return "defender";
 if(m===2&&d>=1&&d<=9)return "women";
 if(m===5&&d>=10&&d<=13)return "russia";
 if(m===9&&d>=1&&d<=7)return "teacher";
 if(m===10&&d>=1&&d<=5)return "unity";
 if(m===11&&d>=10&&d<=13)return "constitution";
 var easter=orthodoxEaster(y),from=new Date(easter),to=new Date(easter);
 from.setUTCDate(from.getUTCDate()-3);to.setUTCDate(to.getUTCDate()+1);
 var today=new Date(Date.UTC(y,m,d));
 if(today>=from&&today<=to)return "easter";
 if(m===4&&d>=1&&d<=10)return "victory";
 if((m===7&&d>=25)||(m===8&&d<=5))return "knowledge";
 if(m===11||m===0||m===1)return "winter";
 if(m>=2&&m<=4)return "spring";
 if(m>=5&&m<=7)return "summer";
 return "autumn";
}
var root=document.documentElement;
window.gym4ChooseSeasonTheme=chooseTheme;
if(!root.hasAttribute("data-season-theme")){root.setAttribute("data-season-theme","autumn");}
})();

/* Theme preference and partner directory */
(function(){
"use strict";
function initSeasonDemo(){
 var select=document.getElementById("seasonDemoSelect"),key="gym4-season-demo",saved="auto";
 try{saved=localStorage.getItem(key)||"auto";}catch(e){}
 function apply(value){
  var mode=value||"auto",theme=mode==="auto"?window.gym4ChooseSeasonTheme(new Date()):mode;
  if(!theme)theme="autumn";
  document.documentElement.setAttribute("data-season-theme",theme);
  if(mode==="auto")document.documentElement.setAttribute("data-season-auto","true");
  else document.documentElement.removeAttribute("data-season-auto");
  if(select)select.value=mode;
  try{localStorage.setItem(key,mode);}catch(e){}
  document.dispatchEvent(new CustomEvent("gym4:seasonchange",{detail:{value:mode,theme:theme}}));
 }
 if(select){
  var options=[["auto","Автоматически по календарю"],["default","Обычная тема"],["winter","Зима"],["spring","Весна"],["summer","Лето"],["autumn","Осень"],["new-year","Новый год"],["defender","23 февраля"],["women","8 марта"],["easter","Пасха"],["victory","9 мая"],["russia","День России"],["knowledge","1 сентября"],["teacher","День учителя"],["unity","День народного единства"],["constitution","День Конституции"]];
  options.forEach(function(pair){if(!select.querySelector('option[value="'+pair[0]+'"]')){var o=document.createElement("option");o.value=pair[0];o.textContent=pair[1];select.appendChild(o);}});
  select.addEventListener("change",function(){apply(select.value);});
 }
 if(["auto","default","winter","spring","summer","autumn","new-year","defender","women","easter","victory","russia","knowledge","teacher","unity","constitution"].indexOf(saved)<0)saved="auto";
 apply(saved);
 window.setInterval(function(){var mode="auto";try{mode=localStorage.getItem(key)||"auto";}catch(e){}if(mode==="auto"&&document.documentElement.getAttribute("data-season-theme")!==window.gym4ChooseSeasonTheme(new Date()))apply("auto");},60000);
}
function initTheme(){var host=document.querySelector(".header-tools");if(!host)return;var b=document.createElement("button");b.type="button";b.className="tool-btn theme-toggle";b.setAttribute("aria-label","Переключить цветовую тему");var mode="light";try{mode=localStorage.getItem("gym4-theme")||"light";}catch(e){}function apply(){document.documentElement.setAttribute("data-theme",mode);b.dataset.mode=mode;b.textContent=mode==="dark"?"Светлая тема":"Тёмная тема";b.setAttribute("aria-label",mode==="dark"?"Включить светлую тему":"Включить тёмную тему");b.setAttribute("aria-pressed",String(mode==="dark"));}b.addEventListener("click",function(){mode=mode==="dark"?"light":"dark";try{localStorage.setItem("gym4-theme",mode);}catch(e){}apply();});host.insertBefore(b,host.firstChild);apply();}
function initPartners(){var list=document.getElementById("friendsList");if(!list)return;fetch("assets/data/partners.json").then(function(r){if(!r.ok)throw Error("partners");return r.json();}).then(function(d){if(!Array.isArray(d.partners)||!d.partners.length)return;list.textContent="";d.partners.forEach(function(p){if(!p.name)return;var href="";try{var u=new URL(String(p.url||""));if(u.protocol==="https:"||u.protocol==="http:")href=u.href;}catch(e){}var el=document.createElement(href?"a":"article");el.className="friend-card";if(href){el.href=href;el.target="_blank";el.rel="noopener noreferrer";}var mark=document.createElement("span"),name=document.createElement("strong"),desc=document.createElement("small");mark.className="friend-card__mark";mark.textContent=p.name.trim().charAt(0).toLocaleUpperCase("ru");name.textContent=p.name;desc.textContent=p.description||"Партнёр гимназии";el.append(mark,name,desc);list.appendChild(el);});}).catch(function(){});}
document.addEventListener("DOMContentLoaded",function(){initTheme();initPartners();initSeasonDemo();});
})();


/* Homepage holiday greetings and restrained seasonal decorations. */
(function(){
"use strict";
var events={
 "new-year":{eyebrow:"С НОВЫМ ГОДОМ",title:"Пусть новый год принесёт открытия!",message:"Желаем ученикам, родителям и педагогам вдохновения, добрых событий, интересных идей и новых достижений.",art:"❄️ ✨ 🎄",ornaments:["❄","✦","❅","✧"],effect:"snow"},
 "defender":{eyebrow:"23 ФЕВРАЛЯ",title:"С Днём защитника Отечества!",message:"Желаем мужества, ответственности, уверенности в своих силах и мирного неба над головой.",art:"★ ✦ ★",ornaments:["★","✦","✧"],effect:"stars"},
 "women":{eyebrow:"8 МАРТА · МЕЖДУНАРОДНЫЙ ЖЕНСКИЙ ДЕНЬ",title:"С Международным женским днём!",message:"Поздравляем с 8 Марта! Желаем весеннего настроения, здоровья, радости, вдохновения и исполнения добрых желаний.",art:"🌷 🌼 🌷",ornaments:["✿","❀","✧","❋"],effect:"petals"},
 "easter":{eyebrow:"СВЕТЛАЯ ПАСХА",title:"С праздником Светлой Пасхи!",message:"Пусть в каждом доме будут мир, тепло, надежда и доброта. Светлых и радостных праздничных дней!",art:"<span class=\"easter-egg easter-egg--blue\">✦</span><span class=\"easter-kulich\"><i></i></span><span class=\"easter-egg easter-egg--pink\">✿</span>",ornaments:["✿","✧","❀","✦"],effect:"easter"},
 "victory":{eyebrow:"9 МАЯ · ДЕНЬ ПОБЕДЫ",title:"Помним. Гордимся. Благодарим.",message:"В этот памятный день мы отдаём дань уважения поколению победителей и сохраняем память о подвиге народа.",art:"✦ ★ ✦",ornaments:["★","✦","✧"],effect:"stars"},
 "russia":{eyebrow:"12 ИЮНЯ · ДЕНЬ РОССИИ",title:"С Днём России!",message:"Желаем мира, единства, созидания и уверенности в будущем. Пусть знания и талант помогают менять мир к лучшему.",art:"🇷🇺 ✦",ornaments:["✦","✧","★"],effect:"ribbons"},
 "knowledge":{eyebrow:"1 СЕНТЯБРЯ",title:"С Днём знаний!",message:"Пусть новый учебный год будет полон интересных задач, смелых вопросов, открытий и достижений!",art:"📚 ✏️ ✨",ornaments:["✦","✧","✎"],effect:"leaves"},
 "teacher":{eyebrow:"5 ОКТЯБРЯ · ДЕНЬ УЧИТЕЛЯ",title:"Спасибо за знания и вдохновение!",message:"Желаем педагогам благодарных учеников, профессиональных успехов, сил и радости от каждого достижения!",art:"📚 🌿 ✨",ornaments:["✦","❧","✧"],effect:"leaves"},
 "unity":{eyebrow:"4 НОЯБРЯ",title:"С Днём народного единства!",message:"Пусть уважение, взаимопонимание и общие добрые дела объединяют людей.",art:"✦ ★ ✦",ornaments:["✦","★","✧"],effect:"ribbons"},
 "constitution":{eyebrow:"12 ДЕКАБРЯ · ДЕНЬ КОНСТИТУЦИИ",title:"День прав и ответственности",message:"Знание законов, уважение к правам человека и ответственность — важная основа гражданского общества.",art:"§ ⚖ ✦",ornaments:["§","✦","✧"],effect:"stars"}
};
function orthodoxEaster(year){
 var a=year%4,b=year%7,c=year%19,x=(19*c+15)%30,y=(2*a+4*b-x+34)%7;
 var month=Math.floor((x+y+114)/31),day=((x+y+114)%31)+1;
 var result=new Date(Date.UTC(year,month-1,day));result.setUTCDate(result.getUTCDate()+(year>=2100?14:13));return result;
}
function render(value){
 var root=document.getElementById("holidayGreeting");if(!root)return;
 var theme=value&&value!=="default"?value:"default";
 var data=events[theme];
 if(!data){root.hidden=true;document.documentElement.removeAttribute("data-holiday-effect");return;}
 document.documentElement.setAttribute("data-holiday-effect",data.effect);
 root.hidden=false;root.setAttribute("data-holiday",theme);
 document.getElementById("holidayEyebrow").textContent=data.eyebrow;
 document.getElementById("holidayTitle").textContent=data.title;
 document.getElementById("holidayMessage").textContent=data.message;
 document.getElementById("holidayArt").innerHTML=data.art;
 var host=document.getElementById("holidayOrnaments");host.textContent="";
 data.ornaments.forEach(function(symbol,i){var el=document.createElement("span");el.textContent=symbol;el.className="holiday-greeting__ornament holiday-greeting__ornament--"+i;host.appendChild(el);});
 var particleSets={snow:["❄","❅","✻"],petals:["✿","❀","✽"],stars:["★","✦","✧"],ribbons:["✦","❋","✧"],leaves:["❧","✿","✦"],easter:["✿","✧","❀","✦"]};
 var particleSymbols=particleSets[data.effect]||[];
 if(particleSymbols.length){
  var total=data.effect==="snow"||data.effect==="petals"?22:14;
  for(var n=0;n<total;n++){
   var particle=document.createElement("span");
   particle.className="holiday-particle holiday-particle--"+data.effect;
   particle.textContent=particleSymbols[n%particleSymbols.length];
   particle.style.left=((n*37)%100)+"%";
   particle.style.animationDelay=(-(n%9)*.8)+"s";
   particle.style.animationDuration=(7+(n%6))+"s";
   particle.style.fontSize=(.65+(n%4)*.22)+"rem";
   host.appendChild(particle);
  }
 }
}
document.addEventListener("DOMContentLoaded",function(){
 var select=document.getElementById("seasonDemoSelect");
 render(select?select.value:"auto");
 document.addEventListener("gym4:seasonchange",function(e){render(e.detail.theme || e.detail.value);});
});
})();


/* Silent animated school mark: the numeral 4 smoothly morphs into learning symbols. */
(function(){
"use strict";
function initSchoolMark(){
 var mark=document.querySelector(".brand-mark");
 if(!mark||mark.dataset.markReady==="true")return;
 var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
 if(reduce||!window.requestAnimationFrame)return;
 var canvas=document.createElement("canvas"),ctx=canvas.getContext&&canvas.getContext("2d");
 if(!ctx)return;
 var off=document.createElement("canvas"),offCtx=null;
 try{offCtx=off.getContext("2d",{willReadFrequently:true});}catch(error){return;}
 if(!offCtx)return;
 canvas.className="brand-mark__canvas";
 canvas.setAttribute("aria-hidden","true");
 mark.appendChild(canvas);
 mark.classList.add("brand-mark--animated");
 mark.dataset.markReady="true";
 var w=0,h=0,dpr=1,particles=[],targets=[],shapeIndex=0,last=0,holdUntil=0,raf=0,visible=true;
 var sequences={
  "default":["4","book","atom","globe","pi","star","cap"],
  winter:["4","snowflake","tree","gift","star"],
  spring:["4","flower","butterfly","dove","book"],
  summer:["4","globe","star","flower","book"],
  autumn:["4","book","pencil","laurel","star"],
  "new-year":["4","snowflake","tree","gift","star"],
  "defender":["4","shield","star","laurel","dove"],
  "women":["4","flower","butterfly","heart","flower"],
  "easter":["4","egg","cross","flower","dove"],
  "victory":["4","star","laurel","ribbon","dove"],
  "russia":["4","flag","globe","star","book"],
  "knowledge":["4","book","pencil","atom","pi"],
  "teacher":["4","book","apple","lightbulb","star"],
  "unity":["4","globe","laurel","heart","book"],
  "constitution":["4","book","scales","column","star"]
 };
 var symbols=sequences[document.documentElement.getAttribute("data-season-theme")]||sequences["default"];
 var colors=["#ffffff","#f6d58a","#cce8f5"];
 function drawShape(key){
  var S=96;off.width=S;off.height=S;offCtx.clearRect(0,0,S,S);
  var c=offCtx;c.save();c.translate(S/2,S/2);c.strokeStyle="#fff";c.fillStyle="#fff";
  c.lineWidth=6;c.lineCap="round";c.lineJoin="round";
  if(key==="4"){
   c.beginPath();c.moveTo(12,-36);c.lineTo(-24,8);c.lineTo(31,8);c.moveTo(15,-36);c.lineTo(15,37);c.stroke();
  }else if(key==="book"){
   c.beginPath();c.moveTo(0,-24);c.bezierCurveTo(-18,-34,-31,-28,-34,-25);c.lineTo(-34,25);c.bezierCurveTo(-20,19,-9,22,0,30);
   c.bezierCurveTo(9,22,20,19,34,25);c.lineTo(34,-25);c.bezierCurveTo(18,-28,8,-34,0,-24);c.stroke();
   c.beginPath();c.moveTo(0,-23);c.lineTo(0,29);c.stroke();
  }else if(key==="atom"){
   c.beginPath();c.arc(0,0,5,0,Math.PI*2);c.fill();
   for(var a=0;a<3;a++){c.save();c.rotate(a*Math.PI/3);c.beginPath();c.ellipse(0,0,37,14,0,0,Math.PI*2);c.stroke();c.restore();}
  }else if(key==="globe"){
   c.beginPath();c.arc(0,0,34,0,Math.PI*2);c.stroke();
   c.beginPath();c.ellipse(0,0,15,34,0,0,Math.PI*2);c.stroke();
   c.beginPath();c.ellipse(0,0,34,13,0,0,Math.PI*2);c.stroke();
   c.beginPath();c.moveTo(-32,0);c.lineTo(32,0);c.stroke();
  }else if(key==="pi"){
   c.font="bold 76px Georgia,serif";c.textAlign="center";c.textBaseline="middle";c.fillText("π",0,2);
  }else if(key==="star"){
   c.beginPath();for(var i=0;i<10;i++){var r=i%2?15:37,a=-Math.PI/2+i*Math.PI/5,x=Math.cos(a)*r,y=Math.sin(a)*r;i?c.lineTo(x,y):c.moveTo(x,y);}c.closePath();c.stroke();
  }else if(key==="snowflake"){
   for(var a=0;a<6;a++){c.save();c.rotate(a*Math.PI/3);c.beginPath();c.moveTo(0,-38);c.lineTo(0,38);c.moveTo(0,-23);c.lineTo(-9,-14);c.moveTo(0,-23);c.lineTo(9,-14);c.moveTo(0,23);c.lineTo(-9,14);c.moveTo(0,23);c.lineTo(9,14);c.stroke();c.restore();}
  }else if(key==="tree"){
   c.beginPath();c.moveTo(0,-39);c.lineTo(-28,-5);c.lineTo(-13,-5);c.lineTo(-34,21);c.lineTo(-11,21);c.lineTo(-11,37);c.lineTo(11,37);c.lineTo(11,21);c.lineTo(34,21);c.lineTo(13,-5);c.lineTo(28,-5);c.closePath();c.stroke();
  }else if(key==="gift"){
   c.strokeRect(-30,-17,60,48);c.beginPath();c.moveTo(-34,-17);c.lineTo(34,-17);c.moveTo(0,-17);c.lineTo(0,31);c.stroke();c.beginPath();c.ellipse(-10,-25,10,7,-.5,0,Math.PI*2);c.ellipse(10,-25,10,7,.5,0,Math.PI*2);c.stroke();
  }else if(key==="shield"){
   c.beginPath();c.moveTo(0,-38);c.lineTo(31,-27);c.lineTo(27,12);c.quadraticCurveTo(17,31,0,39);c.quadraticCurveTo(-17,31,-27,12);c.lineTo(-31,-27);c.closePath();c.stroke();c.beginPath();c.moveTo(0,-24);c.lineTo(0,24);c.moveTo(-17,0);c.lineTo(17,0);c.stroke();
  }else if(key==="laurel"){
   for(var side=-1;side<=1;side+=2){c.save();c.scale(side,1);c.beginPath();c.arc(-7,0,29,-1.2,1.2);c.stroke();for(var k=0;k<5;k++){var yy=-25+k*12;c.beginPath();c.ellipse(-22,yy,7,12,-.7,0,Math.PI*2);c.stroke();}c.restore();}
  }else if(key==="dove"){
   c.beginPath();c.moveTo(-35,8);c.quadraticCurveTo(-8,-4,-2,-30);c.quadraticCurveTo(8,-8,35,-17);c.quadraticCurveTo(21,4,8,11);c.quadraticCurveTo(23,24,32,29);c.quadraticCurveTo(8,31,-5,16);c.quadraticCurveTo(-21,24,-35,8);c.stroke();
  }else if(key==="flower"){
   for(var a=0;a<6;a++){c.save();c.rotate(a*Math.PI/3);c.beginPath();c.ellipse(0,-22,10,17,0,0,Math.PI*2);c.stroke();c.restore();}c.beginPath();c.arc(0,0,8,0,Math.PI*2);c.fill();
  }else if(key==="butterfly"){
   c.beginPath();c.ellipse(-17,-12,15,21,-.5,0,Math.PI*2);c.ellipse(17,-12,15,21,.5,0,Math.PI*2);c.ellipse(-13,17,11,14,.5,0,Math.PI*2);c.ellipse(13,17,11,14,-.5,0,Math.PI*2);c.moveTo(0,-28);c.lineTo(0,30);c.moveTo(0,-25);c.lineTo(-10,-38);c.moveTo(0,-25);c.lineTo(10,-38);c.stroke();
  }else if(key==="heart"){
   c.beginPath();c.moveTo(0,32);c.bezierCurveTo(-48,0,-31,-34,-8,-25);c.quadraticCurveTo(0,-22,0,-12);c.quadraticCurveTo(20,-43,38,-18);c.bezierCurveTo(52,4,20,26,0,32);c.stroke();
  }else if(key==="egg"){
   c.beginPath();c.moveTo(0,-39);c.bezierCurveTo(25,-30,34,4,27,25);c.bezierCurveTo(19,45,-19,45,-27,25);c.bezierCurveTo(-34,4,-25,-30,0,-39);c.stroke();
   c.beginPath();c.moveTo(-23,0);c.quadraticCurveTo(0,-9,23,0);c.moveTo(-25,14);c.quadraticCurveTo(0,5,25,14);c.stroke();
  }else if(key==="cross"){
   c.beginPath();c.moveTo(-7,-36);c.lineTo(7,-36);c.lineTo(7,-8);c.lineTo(30,-8);c.lineTo(30,7);c.lineTo(7,7);c.lineTo(7,36);c.lineTo(-7,36);c.lineTo(-7,7);c.lineTo(-30,7);c.lineTo(-30,-8);c.lineTo(-7,-8);c.closePath();c.stroke();
  }else if(key==="ribbon"){
   c.beginPath();c.arc(0,-8,23,0,Math.PI*2);c.moveTo(-13,12);c.lineTo(-22,38);c.lineTo(-2,27);c.lineTo(9,40);c.lineTo(14,12);c.stroke();
  }else if(key==="flag"){
   c.beginPath();c.moveTo(-28,-37);c.lineTo(-28,37);c.moveTo(-25,-32);c.lineTo(31,-32);c.lineTo(31,8);c.lineTo(-25,8);c.stroke();c.beginPath();c.moveTo(-25,-19);c.lineTo(31,-19);c.moveTo(-25,-6);c.lineTo(31,-6);c.stroke();
  }else if(key==="pencil"){
   c.save();c.rotate(.65);c.strokeRect(-9,-36,18,60);c.beginPath();c.moveTo(-9,24);c.lineTo(0,39);c.lineTo(9,24);c.moveTo(-9,-25);c.lineTo(9,-25);c.stroke();c.restore();
  }else if(key==="apple"){
   c.beginPath();c.moveTo(0,-8);c.bezierCurveTo(-35,-32,-42,15,-20,30);c.quadraticCurveTo(0,42,0,27);c.quadraticCurveTo(0,42,20,30);c.bezierCurveTo(42,15,35,-32,0,-8);c.stroke();c.beginPath();c.moveTo(0,-9);c.lineTo(3,-29);c.quadraticCurveTo(18,-39,25,-28);c.stroke();
  }else if(key==="lightbulb"){
   c.beginPath();c.arc(0,-7,27,Math.PI*1.08,Math.PI*1.92);c.lineTo(15,18);c.lineTo(-15,18);c.closePath();c.stroke();c.beginPath();c.moveTo(-12,25);c.lineTo(12,25);c.moveTo(-9,32);c.lineTo(9,32);c.stroke();
  }else if(key==="scales"){
   c.beginPath();c.moveTo(0,-35);c.lineTo(0,31);c.moveTo(-27,-23);c.lineTo(27,-23);c.moveTo(-27,-23);c.lineTo(-38,7);c.quadraticCurveTo(-27,20,-16,7);c.closePath();c.moveTo(27,-23);c.lineTo(16,7);c.quadraticCurveTo(27,20,38,7);c.closePath();c.moveTo(-20,34);c.lineTo(20,34);c.stroke();
  }else if(key==="column"){
   c.beginPath();c.moveTo(-29,-28);c.lineTo(29,-28);c.lineTo(22,-20);c.lineTo(-22,-20);c.moveTo(-20,-17);c.lineTo(-20,25);c.moveTo(-7,-17);c.lineTo(-7,25);c.moveTo(7,-17);c.lineTo(7,25);c.moveTo(20,-17);c.lineTo(20,25);c.moveTo(-29,29);c.lineTo(29,29);c.moveTo(-35,37);c.lineTo(35,37);c.stroke();
  }else if(key==="cap"){
   c.beginPath();c.moveTo(-39,-8);c.lineTo(0,-28);c.lineTo(39,-8);c.lineTo(0,12);c.closePath();c.stroke();
   c.beginPath();c.moveTo(-23,5);c.lineTo(-23,24);c.quadraticCurveTo(0,37,23,24);c.lineTo(23,5);c.stroke();
   c.beginPath();c.moveTo(39,-8);c.lineTo(39,21);c.stroke();
  }
  c.restore();
  var data=c.getImageData(0,0,S,S).data,pts=[],step=3;
  for(var y=0;y<S;y+=step)for(var x=0;x<S;x+=step){if(data[(y*S+x)*4+3]>100)pts.push({x:x-S/2,y:y-S/2});}
  if(!pts.length)pts.push({x:0,y:0});
  return pts;
 }
 function retarget(key){
  var pts=drawShape(key),scale=Math.min(w,h)*.39;
  for(var i=0;i<particles.length;i++){
   var p=particles[i],t=pts[(i*17)%pts.length];
   p.tx=w/2+t.x*scale/48;p.ty=h/2+t.y*scale/48;
  }
  targets=pts;
 }
 function resize(){
  var r=mark.getBoundingClientRect();w=Math.max(1,r.width);h=Math.max(1,r.height);
  dpr=Math.min(2,window.devicePixelRatio||1);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
  if(!particles.length){for(var i=0;i<125;i++)particles.push({x:w/2,y:h/2,vx:0,vy:0,tx:w/2,ty:h/2,size:.65+Math.random()*.7,phase:Math.random()*6.28});}
  retarget(symbols[shapeIndex]);
 }
 function nextShape(t){
  shapeIndex=(shapeIndex+1)%symbols.length;retarget(symbols[shapeIndex]);holdUntil=t+1750;
 }
 function restoreStaticMark(){
  if(raf)cancelAnimationFrame(raf);
  raf=0;
  if(observer)observer.disconnect();
  if(resizeObserver)resizeObserver.disconnect();
  canvas.remove();
  mark.classList.remove("brand-mark--animated");
  delete mark.dataset.markReady;
 }
 function frame(t){
  raf=0;if(!visible||document.hidden)return;
  try{
   if(!last)last=t;var dt=Math.min(2.2,Math.max(.35,(t-last)/16.67));last=t;
   if(t>holdUntil)nextShape(t);
   ctx.clearRect(0,0,w,h);
   var accent=getComputedStyle(mark).borderBottomColor;
   for(var i=0;i<particles.length;i++){
    var p=particles[i];
    p.vx+=(p.tx-p.x)*.055*dt;p.vy+=(p.ty-p.y)*.055*dt;
    p.vx*=Math.pow(.78,dt);p.vy*=Math.pow(.78,dt);
    p.x+=p.vx*dt;p.y+=p.vy*dt;
    ctx.globalAlpha=.72+Math.sin(t*.002+p.phase)*.22;
    ctx.fillStyle=i%7===0?accent:colors[i%colors.length];
    ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();
   }
   ctx.globalAlpha=1;
   raf=requestAnimationFrame(frame);
  }catch(error){restoreStaticMark();}
 }
 function setSeasonSymbols(theme){
  var next=sequences[theme]||sequences["default"];
  if(next.join("|")===symbols.join("|"))return;
  symbols=next;shapeIndex=0;retarget(symbols[shapeIndex]);holdUntil=0;
 }
 document.addEventListener("gym4:seasonchange",function(e){var detail=e.detail||{},theme=detail.theme||document.documentElement.getAttribute("data-season-theme")||"default";setSeasonSymbols(theme);});
 window.addEventListener("storage",function(e){if(e.key!=="gym4-season-demo")return;var theme=e.newValue==="auto"?(window.gym4ChooseSeasonTheme?window.gym4ChooseSeasonTheme(new Date()):"default"):(e.newValue||"default");document.documentElement.setAttribute("data-season-theme",theme);if(e.newValue==="auto")document.documentElement.setAttribute("data-season-auto","true");else document.documentElement.removeAttribute("data-season-auto");setSeasonSymbols(theme);});
 function start(){if(!raf&&visible&&!document.hidden){last=0;raf=requestAnimationFrame(frame);}}
 function stop(){if(raf){cancelAnimationFrame(raf);raf=0;}}
 var observer=("IntersectionObserver"in window)?new IntersectionObserver(function(entries){visible=entries[0].isIntersecting;if(visible)start();else stop();},{threshold:.01}):null,resizeObserver=null;
 try{
  if(observer)observer.observe(mark);
  if("ResizeObserver"in window){resizeObserver=new ResizeObserver(function(){try{resize();}catch(error){restoreStaticMark();}});resizeObserver.observe(mark);}
  else window.addEventListener("resize",function(){try{resize();}catch(error){restoreStaticMark();}});
  document.addEventListener("visibilitychange",function(){if(document.hidden)stop();else start();});
  resize();start();mark.dataset.markReady="true";
 }catch(error){restoreStaticMark();}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initSchoolMark);else initSchoolMark();
})();


/* Site-wide seasonal atmosphere, navigation polish and accessible motion controls. */
(function () {
  "use strict";
  var root = document.documentElement;
  var storageKey = "gym4-seasonal-effects";
  var layer = null, toggle = null;
  var activeTheme = root.getAttribute("data-season-theme") || "default";
  var paused = false;
  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  var symbols = {
    "new-year": { effect: "snow", items: ["❄", "❅", "✻", "✧"] },
    defender: { effect: "stars", items: ["★", "✦", "✧", "✦"] },
    women: { effect: "petals", items: ["✿", "❀", "✽", "❁"] },
    easter: { effect: "easter", items: ["✿", "✧", "❀", "◌"] },
    victory: { effect: "ribbons", items: ["✦", "❋", "✧", "★"] },
    russia: { effect: "ribbons", items: ["✦", "✧", "★", "❋"] },
    knowledge: { effect: "leaves", items: ["❧", "✿", "✦", "❦"] },
    teacher: { effect: "leaves", items: ["❧", "❦", "✿", "✧"] },
    unity: { effect: "stars", items: ["✦", "★", "✧", "✦"] },
    constitution: { effect: "stars", items: ["§", "✦", "✧", "★"] }
  };
  function readPaused() {
    try { return localStorage.getItem(storageKey) === "off"; }
    catch (error) { return false; }
  }
  function writePaused(value) {
    try { localStorage.setItem(storageKey, value ? "off" : "on"); }
    catch (error) { /* Decorative preference is optional. */ }
  }
  function createLayer() {
    if (layer || !document.body || document.body.classList.contains("editor-body")) return;
    layer = document.createElement("div");
    layer.className = "seasonal-atmosphere";
    layer.setAttribute("aria-hidden", "true");
    layer.setAttribute("data-seasonal-atmosphere", "");
    document.body.insertBefore(layer, document.body.firstChild);
  }
  function createToggle() {
    if (toggle || !document.body || document.body.classList.contains("editor-body")) return;
    toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "seasonal-toggle";
    toggle.setAttribute("aria-pressed", "true");
    toggle.setAttribute("aria-label", "Отключить праздничные эффекты");
    toggle.addEventListener("click", function () {
      paused = !paused;
      writePaused(paused);
      applyState();
    });
    document.body.appendChild(toggle);
  }
  function applyState() {
    var hasSeason = !!symbols[activeTheme];
    if (layer) {
      layer.hidden = !hasSeason || paused || (reducedMotion && reducedMotion.matches);
      layer.setAttribute("data-effect", hasSeason ? symbols[activeTheme].effect : "none");
    }
    if (toggle) {
      toggle.hidden = !hasSeason;
      toggle.textContent = paused ? "Эффекты: выкл." : "Эффекты: вкл.";
      toggle.setAttribute("aria-pressed", String(!paused));
      toggle.setAttribute("aria-label", paused ? "Включить праздничные эффекты" : "Отключить праздничные эффекты");
      if (reducedMotion && reducedMotion.matches) {
        toggle.textContent = "Анимация отключена";
        toggle.setAttribute("aria-label", "Анимация отключена настройками устройства");
        toggle.disabled = true;
      } else {
        toggle.disabled = false;
      }
    }
  }
  function render(theme) {
    activeTheme = theme || root.getAttribute("data-season-theme") || "default";
    var cornerSets = {
      winter:["❄","✦"], spring:["✿","❀"], summer:["☀","✧"], autumn:["🍂","❧"],
      "new-year":["❄","✦"], defender:["★","✦"], women:["✿","❀"], easter:["✿","◌"],
      victory:["★","✦"], russia:["✦","✧"], knowledge:["✎","✦"], teacher:["❧","✦"],
      unity:["✦","★"], constitution:["§","⚖"]
    };
    var cornerHost = document.querySelector(".seasonal-corners");
    if (!cornerHost && document.body && !document.body.classList.contains("editor-body")) {
      cornerHost = document.createElement("div");
      cornerHost.className = "seasonal-corners";
      cornerHost.setAttribute("aria-hidden", "true");
      cornerHost.innerHTML = "<span></span><span></span>";
      document.body.appendChild(cornerHost);
    }
    if (cornerHost) {
      var cornerSet = cornerSets[activeTheme] || null;
      cornerHost.hidden = !cornerSet;
      if (cornerSet) {
        cornerHost.children[0].textContent = cornerSet[0];
        cornerHost.children[1].textContent = cornerSet[1];
      }
    }
    createLayer();
    createToggle();
    if (!layer) return;
    layer.textContent = "";
    var config = symbols[activeTheme];
    if (config) {
      for (var i = 0; i < 14; i += 1) {
        var particle = document.createElement("span");
        particle.className = "seasonal-particle seasonal-particle--" + config.effect;
        particle.textContent = config.items[i % config.items.length];
        particle.style.left = ((i * 37 + 9) % 100) + "%";
        particle.style.animationDelay = (-((i * 7) % 19)) + "s";
        particle.style.animationDuration = (17 + (i % 7) * 2) + "s";
        particle.style.fontSize = (0.65 + (i % 4) * 0.18) + "rem";
        particle.style.setProperty("--season-drift", ((i % 2 ? 1 : -1) * (12 + (i % 5) * 8)) + "px");
        layer.appendChild(particle);
      }
    }
    applyState();
  }
  function initNavigation() {
    var current = window.location.pathname.split("/").pop() || "index.html";
    var navLinks = document.querySelectorAll(".site-nav a[href]");
    Array.prototype.forEach.call(navLinks, function (link) {
      var href = link.getAttribute("href") || "";
      if (/^(https?:|mailto:|tel:|#|\/)/i.test(href)) return;
      var target = href.split("#")[0].split("?")[0] || "index.html";
      if (target === current) {
        link.setAttribute("aria-current", "page");
        link.classList.add("is-current");
      } else {
        link.removeAttribute("aria-current");
        link.classList.remove("is-current");
      }
    });
    var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (connection && connection.saveData) return;
    var prefetched = {};
    function prefetch(link) {
      var href = link.getAttribute("href") || "";
      if (!href || href.charAt(0) === "#" || link.target || link.hasAttribute("download")) return;
      var url;
      try { url = new URL(href, window.location.href); } catch (error) { return; }
      if (url.origin !== window.location.origin || !/\.html?$/i.test(url.pathname) || url.href === window.location.href || prefetched[url.href]) return;
      prefetched[url.href] = true;
      var hint = document.createElement("link");
      hint.rel = "prefetch";
      hint.href = url.href;
      hint.as = "document";
      document.head.appendChild(hint);
    }
    Array.prototype.forEach.call(document.querySelectorAll(".site-nav a[href], .footer-links a[href], .crumbs a[href]"), function (link) {
      link.addEventListener("pointerenter", function () { prefetch(link); }, { once: true, passive: true });
      link.addEventListener("focus", function () { prefetch(link); }, { once: true });
    });
  }
  function init() {
    activeTheme = root.getAttribute("data-season-theme") || "default";
    paused = readPaused();
    createLayer();
    createToggle();
    render(activeTheme);
    initNavigation();
    if (reducedMotion && reducedMotion.addEventListener) reducedMotion.addEventListener("change", applyState);
    document.addEventListener("gym4:seasonchange", function (event) {
      var detail = event.detail || {};
      render(detail.theme || root.getAttribute("data-season-theme") || "default");
    });
    window.addEventListener("storage", function (event) {
      if (event.key === "gym4-season-demo") {
        var next = event.newValue === "auto" ? (window.gym4ChooseSeasonTheme ? window.gym4ChooseSeasonTheme(new Date()) : "default") : (event.newValue || "default");
        root.setAttribute("data-season-theme", next);
        render(next);
      }
      if (event.key === storageKey) {
        paused = event.newValue === "off";
        applyState();
      }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();


/* Manual seasonal demo controls and page-wide seasonal presentation. */
(function () {
  "use strict";
  var labels = {
    "default": "Обычная тема", winter: "Зима", spring: "Весна", summer: "Лето", autumn: "Осень",
    "new-year": "Новый год", defender: "23 февраля", women: "8 марта", easter: "Пасха",
    victory: "9 мая", russia: "День России", knowledge: "1 сентября", teacher: "День учителя",
    unity: "День народного единства", constitution: "День Конституции"
  };
  var seasonalGreetings = {
    winter: { eyebrow: "ЗИМНЯЯ ГИМНАЗИЯ", title: "Время открытий даже в снежную пору", message: "Зимние каникулы, книжные проекты, научные эксперименты и подготовка к новым учебным достижениям.", art: "❄ ✦ ❄", ornaments: ["❄", "✧", "❅", "✦"], effect: "snow" },
    spring: { eyebrow: "ВЕСНА В ГИМНАЗИИ", title: "Весна — время новых идей", message: "Школьные проекты, творческие мастерские, экологические инициативы и подготовка к весенним событиям.", art: "🌷 ✿ 🌱", ornaments: ["✿", "❀", "✧", "❋"], effect: "petals" },
    summer: { eyebrow: "ЛЕТО И КАНИКУЛЫ", title: "Время открытий за пределами класса", message: "Летнее чтение, исследовательские задания, спортивные активности и яркие впечатления школьного сообщества.", art: "☀ ✦ 🌿", ornaments: ["☀", "✦", "❋", "✧"], effect: "stars" },
    autumn: { eyebrow: "ОСЕНЬ В ГИМНАЗИИ", title: "Новый учебный год — новые возможности", message: "Встречи после каникул, День знаний, школьные проекты, олимпиады и первые достижения учебного года.", art: "🍂 📚 🍁", ornaments: ["🍂", "✧", "❧", "✦"], effect: "leaves" }
  };
  var root = document.documentElement;
  var select, button, panel, panelSelect;
  function currentSeason() { return root.getAttribute("data-season-theme") || "autumn"; }
  function updateButton() {
    if (button) button.textContent = "🎨 Сезон: " + (labels[currentSeason()] || "Оформление");
  }
  function renderSeasonGreeting(theme) {
    var data = seasonalGreetings[theme], box = document.getElementById("holidayGreeting");
    if (!box) return;
    if (!data) return;
    root.setAttribute("data-holiday-effect", data.effect);
    box.hidden = false;
    box.setAttribute("data-holiday", theme);
    var eyebrow = document.getElementById("holidayEyebrow");
    var title = document.getElementById("holidayTitle");
    var message = document.getElementById("holidayMessage");
    var art = document.getElementById("holidayArt");
    var ornaments = document.getElementById("holidayOrnaments");
    if (eyebrow) eyebrow.textContent = data.eyebrow;
    if (title) title.textContent = data.title;
    if (message) message.textContent = data.message;
    if (art) art.textContent = data.art;
    if (ornaments) {
      ornaments.textContent = "";
      data.ornaments.forEach(function (symbol, index) {
        var item = document.createElement("span");
        item.className = "holiday-greeting__ornament holiday-greeting__ornament--" + index;
        item.textContent = symbol;
        ornaments.appendChild(item);
      });
    }
  }
  function applySeasonDecor(value) {
    var theme = value === "auto" ? (window.gym4ChooseSeasonTheme ? window.gym4ChooseSeasonTheme(new Date()) : "autumn") : value;
    if (!labels[theme]) theme = "autumn";
    root.setAttribute("data-season-theme", theme);
    if (value === "auto") root.setAttribute("data-season-auto", "true");
    else root.removeAttribute("data-season-auto");
    try { localStorage.setItem("gym4-season-demo", value); } catch (error) {}
    renderSeasonGreeting(theme);
    updateButton();
  }
  document.addEventListener("gym4:seasonchange", function (event) {
    var theme = event.detail && event.detail.theme || currentSeason();
    root.setAttribute("data-season-theme", theme);
    renderSeasonGreeting(theme);
    var mode = event.detail && event.detail.value || theme;
    if (select) select.value = mode;
    if (panelSelect) panelSelect.value = mode;
    updateButton();
  });
  window.addEventListener("storage", function (event) {
    if (event.key !== "gym4-season-demo" || !event.newValue) return;
    var mode = event.newValue;
    var theme = mode === "auto" ? (window.gym4ChooseSeasonTheme ? window.gym4ChooseSeasonTheme(new Date()) : "autumn") : mode;
    if (!labels[theme]) return;
    root.setAttribute("data-season-theme", theme);
    if (mode === "auto") root.setAttribute("data-season-auto", "true"); else root.removeAttribute("data-season-auto");
    renderSeasonGreeting(theme);
    if (select) select.value = mode;
    if (panelSelect) panelSelect.value = mode;
    updateButton();
  });
  function openPanel() {
    if (!panel) return;
    panel.hidden = false;
    button.setAttribute("aria-expanded", "true");
    panelSelect.focus();
  }
  function closePanel() {
    if (!panel) return;
    panel.hidden = true;
    button.setAttribute("aria-expanded", "false");
  }
  document.addEventListener("DOMContentLoaded", function () {
    select = document.getElementById("seasonDemoSelect");
    if (!select) {
      select = document.createElement("select");
      select.id = "seasonDemoSelect";
      select.hidden = true;
      select.setAttribute("aria-hidden", "true");
      document.body.appendChild(select);
    }
    var allOptions = [["auto","Автоматически по календарю"]];
    Object.keys(labels).forEach(function (value) { allOptions.push([value, labels[value]]); });
    allOptions.forEach(function (pair) {
      if (!select.querySelector('option[value="' + pair[0] + '"]')) {
        var option = document.createElement("option");
        option.value = pair[0];
        option.textContent = pair[1];
        select.appendChild(option);
      }
    });
    var saved = "auto";
    try { saved = localStorage.getItem("gym4-season-demo") || "auto"; } catch (error) {}
    if (!labels[saved] && saved !== "auto") saved = "auto";
    select.value = saved;
    if (select.value !== saved) saved = "auto";
    select.value = saved;
    applySeasonDecor(saved);
    select.addEventListener("change", function () {
      applySeasonDecor(select.value);
      document.dispatchEvent(new CustomEvent("gym4:seasonchange", {detail:{value:select.value,theme:root.getAttribute("data-season-theme")}}));
    });

    button = document.createElement("button");
    button.type = "button";
    button.className = "seasonal-toggle";
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", "seasonDemoPopover");
    button.setAttribute("aria-label", "Открыть ручной выбор сезонного оформления");
    panel = document.createElement("div");
    panel.className = "season-demo-popover";
    panel.id = "seasonDemoPopover";
    panel.hidden = true;
    var label = document.createElement("label");
    label.textContent = "Ручной выбор оформления";
    label.htmlFor = "seasonDemoQuickSelect";
    panelSelect = select.cloneNode(true);
    panelSelect.id = "seasonDemoQuickSelect";
    panelSelect.removeAttribute("aria-label");
    panel.append(label, panelSelect);
    document.body.append(button, panel);
    panelSelect.value = select.value;
    panelSelect.addEventListener("change", function () {
      select.value = panelSelect.value;
      select.dispatchEvent(new Event("change", { bubbles: true }));
    });
    button.addEventListener("click", function () {
      if (panel.hidden) openPanel(); else closePanel();
    });
    document.addEventListener("click", function (event) {
      if (!panel.hidden && !panel.contains(event.target) && event.target !== button) closePanel();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !panel.hidden) { closePanel(); button.focus(); }
    });
    document.addEventListener("gym4:seasonchange", function (event) {
      var detail = event.detail || {}, value = detail.value || detail.theme || currentSeason();
      panelSelect.value = value;
      if (select) select.value = value;
      updateButton();
    });
    updateButton();
  });
})();
