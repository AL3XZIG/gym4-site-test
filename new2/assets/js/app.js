/*
 * Гимназия № 4 — минимальный скрипт интерфейса.
 * Содержимое страниц от скрипта не зависит: без JS сайт полностью читаем,
 * меню развёрнуто, панель версии для слабовидящих скрыта.
 * Хранилище: localStorage, единственный ключ "gym4-a11y" (размер шрифта и схема).
 */
(function () {
  "use strict";
  var root = document.documentElement;
  var KEY = "gym4-a11y";
  root.classList.add("js");

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* хранилище недоступно */ }
  }

  var state = { fs: "100", scheme: "" };
  var saved = load();
  if (["100", "125", "150"].indexOf(saved.fs) !== -1) state.fs = saved.fs;
  if (["", "bw", "wb"].indexOf(saved.scheme) !== -1) state.scheme = saved.scheme;

  function apply() {
    root.style.fontSize = state.fs + "%";
    if (state.scheme) root.setAttribute("data-scheme", state.scheme);
    else root.removeAttribute("data-scheme");
    document.querySelectorAll("button[data-fs]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-fs") === state.fs));
    });
    document.querySelectorAll("button[data-scheme]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-scheme") === state.scheme));
    });
  }

  // Применяем сохранённые настройки сразу, чтобы избежать мигания оформления.
  if (state.scheme) root.setAttribute("data-scheme", state.scheme);
  root.style.fontSize = state.fs + "%";

  function init() {
    var year = document.getElementById("year");
    if (year) year.textContent = new Date().getFullYear();

    var menuBtn = document.getElementById("menuToggle");
    var nav = document.getElementById("siteNav");
    var a11yBtn = document.getElementById("a11yToggle");
    var panel = document.getElementById("a11yPanel");

    function setMenu(open) {
      if (!menuBtn || !nav) return;
      nav.classList.toggle("open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
    }
    function setPanel(open) {
      if (!panel || !a11yBtn) return;
      panel.hidden = !open;
      a11yBtn.setAttribute("aria-expanded", String(open));
    }
    if (menuBtn) menuBtn.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    if (a11yBtn) a11yBtn.addEventListener("click", function () { setPanel(panel.hidden); });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      if (nav && nav.classList.contains("open")) { setMenu(false); if (menuBtn) menuBtn.focus(); }
      else if (panel && !panel.hidden) { setPanel(false); if (a11yBtn) a11yBtn.focus(); }
    });

    document.querySelectorAll("button[data-fs]").forEach(function (b) {
      b.addEventListener("click", function () { state.fs = b.getAttribute("data-fs"); apply(); save(state); });
    });
    document.querySelectorAll("button[data-scheme]").forEach(function (b) {
      b.addEventListener("click", function () { state.scheme = b.getAttribute("data-scheme"); apply(); save(state); });
    });
    var reset = document.getElementById("a11yReset");
    if (reset) reset.addEventListener("click", function () { state = { fs: "100", scheme: "" }; apply(); save(state); });

    apply();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
