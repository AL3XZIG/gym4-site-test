(function(){
"use strict";var root=document.documentElement,key="gym4-a11y";root.classList.add("js");
function read(){try{return JSON.parse(localStorage.getItem(key))||{}}catch(e){return{}}}function write(v){try{localStorage.setItem(key,JSON.stringify(v))}catch(e){}}
var saved=read(),state={fs:["100","125","150","175","200"].indexOf(saved.fs)>=0?saved.fs:"100",scheme:["","bw","wb"].indexOf(saved.scheme)>=0?saved.scheme:"",spacing:["normal","wide"].indexOf(saved.spacing)>=0?saved.spacing:"normal",images:["show","hide"].indexOf(saved.images)>=0?saved.images:"show"};
function apply(){root.style.fontSize=state.fs+"%";if(state.scheme)root.setAttribute("data-scheme",state.scheme);else root.removeAttribute("data-scheme");root.setAttribute("data-spacing",state.spacing);root.setAttribute("data-images",state.images);document.querySelectorAll("[data-fs],[data-scheme],[data-spacing],[data-images]").forEach(function(b){var k=["fs","scheme","spacing","images"].filter(function(x){return b.hasAttribute("data-"+x)})[0];if(k)b.setAttribute("aria-pressed",String((b.dataset[k]||"")===state[k]))})}apply();
function init(){var year=document.getElementById("year");if(year)year.textContent=new Date().getFullYear();var menu=document.getElementById("menuToggle"),nav=document.getElementById("siteNav"),a11y=document.getElementById("a11yToggle"),panel=document.getElementById("a11yPanel");function setMenu(v){if(!menu||!nav)return;nav.classList.toggle("open",v);menu.setAttribute("aria-expanded",String(v))}function setPanel(v){if(!a11y||!panel)return;panel.hidden=!v;a11y.setAttribute("aria-expanded",String(v))}if(menu)menu.addEventListener("click",function(){setMenu(!nav.classList.contains("open"))});if(nav)nav.addEventListener("click",function(e){if(e.target.closest("a"))setMenu(false)});if(a11y)a11y.addEventListener("click",function(){setPanel(panel.hidden)});document.addEventListener("keydown",function(e){if(e.key==="Escape"){setMenu(false);setPanel(false)}});
[["fs","[data-fs]"],["scheme","[data-scheme]"],["spacing","[data-spacing]"],["images","[data-images]"]].forEach(function(pair){document.querySelectorAll(pair[1]).forEach(function(b){b.addEventListener("click",function(){state[pair[0]]=b.dataset[pair[0]]||"";apply();write(state)})})});var reset=document.getElementById("a11yReset");if(reset)reset.addEventListener("click",function(){state={fs:"100",scheme:"",spacing:"normal",images:"show"};apply();write(state)});
var search=document.getElementById("newsSearch"),sort=document.getElementById("newsSort"),list=document.getElementById("newsList"),count=document.getElementById("newsCount"),empty=document.getElementById("newsEmpty");if(list&&search&&sort){var buttons=Array.prototype.slice.call(document.querySelectorAll("[data-filter]")),items=Array.prototype.slice.call(list.querySelectorAll("[data-cat]")),active="all";function update(){var q=search.value.trim().toLocaleLowerCase("ru"),ordered=items.slice().sort(function(a,b){return sort.value==="asc"?a.dataset.date.localeCompare(b.dataset.date):b.dataset.date.localeCompare(a.dataset.date)}),shown=0;ordered.forEach(function(item){list.appendChild(item);var ok=(active==="all"||item.dataset.cat===active)&&(!q||item.textContent.toLocaleLowerCase("ru").indexOf(q)!==-1);item.hidden=!ok;if(ok)shown++});if(count)count.textContent=shown?"Показано публикаций: "+shown:"Публикаций по заданным условиям не найдено.";if(empty)empty.hidden=shown!==0}buttons.forEach(function(b){b.addEventListener("click",function(){active=b.dataset.filter;buttons.forEach(function(x){var on=x===b;x.classList.toggle("is-active",on);x.setAttribute("aria-pressed",String(on))});update()})});search.addEventListener("input",update);sort.addEventListener("change",update);update()}
var aside=document.querySelector(".aside-panel");if(aside&&"IntersectionObserver"in window){var links=Array.prototype.slice.call(aside.querySelectorAll('a[href^="#"]')),sections=links.map(function(a){return document.getElementById(a.getAttribute("href").slice(1))}).filter(Boolean),observer=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting)links.forEach(function(a){a.classList.toggle("is-active",a.hash==="#"+entry.target.id)})})},{rootMargin:"-20% 0px -68% 0px"});sections.forEach(function(s){observer.observe(s)})}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();})();

/* GYM4 interface enhancements: site search, reading progress and reveal motion. */
(function () {
  "use strict";

  var pages = ["index.html", "news.html", "parents.html", "students.html", "priem.html", "contacts.html", "sveden.html"];
  var entries = [
    { title: "Главная", description: "О гимназии, история, направления и новости.", href: "index.html", keywords: "школа гимназия" },
    { title: "Новости и объявления", description: "Публикации, события, объявления и школьная жизнь.", href: "news.html", keywords: "новости мероприятия" },
    { title: "Родителям", description: "Питание, безопасность, поддержка ребёнка и обращения.", href: "parents.html", keywords: "семья питание безопасность" },
    { title: "Обучающимся", description: "Учебный процесс, расписание, проекты, олимпиады и кружки.", href: "students.html", keywords: "ученики расписание олимпиады" },
    { title: "Приём в гимназию", description: "Порядок зачисления, документы и ответы на вопросы.", href: "priem.html", keywords: "поступление зачисление первый класс" },
    { title: "Контакты", description: "Адрес, телефоны, электронная почта и как добраться.", href: "contacts.html", keywords: "адрес телефон почта" },
    { title: "Сведения об образовательной организации", description: "Документы, образование, руководство, питание и материальная база.", href: "sveden.html", keywords: "сведения документы образование устав" }
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
    if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
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
