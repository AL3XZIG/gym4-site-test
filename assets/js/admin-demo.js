(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var frame = $("siteFrame");
  var page = $("pageSelect");\n  var themeSelect = $("seasonThemeSelect");
  var status = $("editorStatus");
  var form = $("elementForm");
  var textField = $("elementText");
  var imageFields = $("imageFields");
  var linkFields = $("linkFields");
  var imageUrl = $("imageUrl");
  var imageAlt = $("imageAlt");
  var linkUrl = $("linkUrl");

  var current = null;
  var currentDoc = null;
  var history = [];
  var future = [];
  var editMode = true;
  var pendingDraft = null;
  var draftKey = "gym4-site-editor-v2";
  var maxHistory = 40;
  var selectable = "img,a,h1,h2,h3,h4,p,li,button,figcaption,blockquote,td,th,span,strong";

  function say(message) {
    status.textContent = message;
  }

  function readDrafts() {
    try {
      return JSON.parse(localStorage.getItem(draftKey) || "{}");
    } catch (error) {
      return {};
    }
  }

  function cleanHTML() {
    var doc = frame.contentDocument;
    if (!doc || !doc.documentElement) return "";
    var clone = doc.documentElement.cloneNode(true);
    clone.querySelectorAll("[data-editor-selected]").forEach(function (el) {
      el.removeAttribute("data-editor-selected");
    });
    clone.querySelectorAll("[data-editor-hover]").forEach(function (el) {
      el.removeAttribute("data-editor-hover");
    });
    var overlay = clone.querySelector("#editorOverlayStyle");
    if (overlay) overlay.remove();
    clone.querySelectorAll("[contenteditable]").forEach(function (el) {
      el.removeAttribute("contenteditable");
    });
    return "<!doctype html>\\n" + clone.outerHTML;
  }

  function updateHistoryButtons() {
    $("undoBtn").disabled = history.length === 0;
    $("redoBtn").disabled = future.length === 0;
  }

  function snapshot() {
    var html = cleanHTML();
    if (!html) return;
    history.push(html);
    if (history.length > maxHistory) history.shift();
    future = [];
    updateHistoryButtons();
  }

  function showEmpty() {
    $("emptyInspector").hidden = false;
    form.hidden = true;
    textField.disabled = false;
    $("selectionInfo").textContent = "Элемент не выбран";
    $("inspectorDescription").textContent = "Выберите текст, изображение или ссылку в макете.";
  }

  function clearSelection() {
    if (current) current.removeAttribute("data-editor-selected");
    current = null;
    showEmpty();
  }

  function elementLabel(el) {
    return el.tagName.toLowerCase() +
      (el.id ? "#" + el.id : "") +
      (el.classList && el.classList.length ? "." + Array.from(el.classList).slice(0, 2).join(".") : "");
  }

  function selectElement(el) {
    if (!el || /^(HTML|BODY|SCRIPT|STYLE|LINK|META|HEAD|NAV|HEADER|FOOTER)$/.test(el.tagName)) return;

    if (current) current.removeAttribute("data-editor-selected");
    current = el;
    el.setAttribute("data-editor-selected", "true");

    var isImage = el.tagName === "IMG";
    var isLink = el.tagName === "A";
    $("emptyInspector").hidden = true;
    form.hidden = false;

    textField.disabled = isImage;
    textField.value = isImage ? "" : (el.innerText || el.textContent || "").trim();
    imageFields.hidden = !isImage;
    linkFields.hidden = !isLink;

    if (isImage) {
      imageUrl.value = el.getAttribute("src") || "";
      imageAlt.value = el.getAttribute("alt") || "";
    }
    if (isLink) linkUrl.value = el.getAttribute("href") || "";

    $("selectionInfo").textContent = "Выбрано: " + elementLabel(el);
    $("inspectorDescription").textContent =
      "Тег " + el.tagName.toLowerCase() + " · изменения применяются к предпросмотру.";
  }

  function attachEditor() {
    var doc = frame.contentDocument;
    if (!doc) return;
    currentDoc = doc;

    if (!doc.getElementById("editorOverlayStyle")) {
      var style = doc.createElement("style");
      style.id = "editorOverlayStyle";
      style.textContent = "[data-editor-selected] { outline: 2px solid #bd8b3b !important; outline-offset: 2px !important; } [data-editor-hover] { cursor: crosshair !important; }";
      (doc.head || doc.documentElement).appendChild(style);
    }

    if (doc.__gym4EditorAttached) return;
    doc.__gym4EditorAttached = true;

    doc.addEventListener("click", function (event) {
      if (!editMode || !event.target || !event.target.closest) return;
      var el = event.target.closest(selectable);
      if (!el) return;
      event.preventDefault();
      event.stopPropagation();
      selectElement(el);
    }, true);

    doc.addEventListener("mouseover", function (event) {
      if (!editMode || !event.target || !event.target.closest) return;
      var el = event.target.closest(selectable);
      if (el && !el.hasAttribute("data-editor-selected")) {
        el.setAttribute("data-editor-hover", "true");
      }
    }, true);

    doc.addEventListener("mouseout", function (event) {
      if (!event.target || !event.target.closest) return;
      var el = event.target.closest("[data-editor-hover]");
      if (el) el.removeAttribute("data-editor-hover");
    }, true);

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape") clearSelection();
    });

    $("canvasHint").textContent = editMode
      ? "Нажмите на элемент, который хотите изменить"
      : "Режим выбора отключён";
    say("Страница загружена");
  }

  function restore(html) {
    var doc = frame.contentDocument;
    if (!doc || !html) return;
    doc.__gym4EditorAttached = false;
    doc.open();
    doc.write(html);
    doc.close();
    current = null;
    attachEditor();
    showEmpty();
    updateHistoryButtons();
  }

  function loadPage(value) {
    var selected = page.options[page.selectedIndex];
    $("currentPageName").textContent = selected ? selected.text : value;
    current = null;
    currentDoc = null;
    history = [];
    future = [];
    updateHistoryButtons();
    showEmpty();

    var draft = readDrafts()[value];
    pendingDraft = draft && draft.html ? { page: value, html: draft.html } : null;
    frame.src = value;
    say("Загрузка страницы…");
  }

  frame.addEventListener("load", function () {
    attachEditor();
    if (pendingDraft && pendingDraft.page === page.value) {
      var draft = pendingDraft;
      pendingDraft = null;
      if (window.confirm("Для этой страницы найден локальный черновик. Восстановить его?")) {
        restore(draft.html);
        say("Локальный черновик восстановлен");
      }
    }
  });

  page.addEventListener("change", function () {
    loadPage(page.value);
  });

  $("editModeBtn").addEventListener("click", function () {
    editMode = !editMode;
    this.classList.toggle("is-active", editMode);
    this.textContent = editMode ? "↖ Режим выбора" : "⏸ Выбор отключён";
    $("canvasHint").textContent = editMode
      ? "Нажмите на элемент, который хотите изменить"
      : "Режим выбора отключён";
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!current || !currentDoc) return;

    snapshot();
    if (current.tagName === "IMG") {
      current.setAttribute("src", imageUrl.value.trim());
      current.setAttribute("alt", imageAlt.value.trim());
    } else {
      // Do not replace an image nested inside a link with plain text.
      if (!(current.tagName === "A" && current.querySelector("img"))) {
        current.textContent = textField.value;
      }
    }
    if (current.tagName === "A") current.setAttribute("href", linkUrl.value.trim());

    say("Изменение применено · сохраните черновик или экспортируйте HTML");
    selectElement(current);
  });

  $("undoBtn").addEventListener("click", function () {
    if (!history.length) return;
    var previous = history.pop();
    future.push(cleanHTML());
    restore(previous);
    say("Действие отменено");
  });

  $("redoBtn").addEventListener("click", function () {
    if (!future.length) return;
    var next = future.pop();
    history.push(cleanHTML());
    restore(next);
    say("Действие восстановлено");
  });

  $("reloadBtn").addEventListener("click", function () {
    if (window.confirm("Перезагрузить страницу и потерять несохранённые изменения?")) {
      pendingDraft = null;
      frame.src = page.value;
      clearSelection();
      history = [];
      future = [];
      updateHistoryButtons();
    }
  });

  $("clearSelectionBtn").addEventListener("click", clearSelection);

  $("saveDraftBtn").addEventListener("click", function () {
    try {
      var html = cleanHTML();
      if (!html) throw new Error("Страница ещё не загружена");
      var all = readDrafts();
      all[page.value] = { html: html, savedAt: new Date().toISOString() };
      localStorage.setItem(draftKey, JSON.stringify(all));
      say("Черновик сохранён в этом браузере");
    } catch (error) {
      say("Не удалось сохранить черновик: " + error.message);
    }
  });

  $("exportBtn").addEventListener("click", function () {
    var html = cleanHTML();
    if (!html) {
      say("Страница ещё не загружена");
      return;
    }
    var blob = new Blob([html], { type: "text/html;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = page.value.split("/").pop() || "page.html";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    say("HTML экспортирован · проверьте файл перед публикацией");
  });

  loadPage(page.value);
})();