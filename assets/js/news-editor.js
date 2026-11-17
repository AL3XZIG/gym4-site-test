(function () {
  "use strict";
  var KEY = "gym4-news-editor-v1";
  var posts = [];
  var $ = function (id) { return document.getElementById(id); };

  function localDate() {
    var now = new Date();
    return now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  }
  function createId() {
    var id;
    do { id = "post-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8); }
    while (posts.some(function (post) { return post.id === id; }));
    return id;
  }
  function validDate(value) {
    if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    var date = new Date(value + "T00:00:00Z");
    return !isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
  }
  function safeHttpUrl(value) {
    if (!value) return true;
    try { var url = new URL(value); return url.protocol === "https:" || url.protocol === "http:"; }
    catch (error) { return false; }
  }
  function safeImagePath(value) {
    if (!value) return true;
    if (/^https:\/\//i.test(value)) return safeHttpUrl(value);
    return /^\/?assets\/[a-z0-9_./-]+$/i.test(value) && !value.split("/").some(function (part) { return part === ".."; });
  }
  function validPost(post) {
    return post && typeof post === "object" &&
      typeof post.title === "string" && post.title.trim().length > 0 && post.title.length <= 180 &&
      validDate(post.date) && ["news", "events", "announcements"].indexOf(post.category) >= 0 &&
      safeHttpUrl(String(post.sourceUrl || "")) && safeImagePath(String(post.imageUrl || ""));
  }
  function normalizePosts(value) {
    if (!Array.isArray(value)) throw new Error("В JSON должен быть массив posts");
    var ids = new Set();
    return value.map(function (post) {
      if (!validPost(post)) throw new Error("Некоторые записи имеют неверную дату, заголовок, категорию или ссылку");
      var id = String(post.id || createId());
      if (ids.has(id)) throw new Error("В списке повторяется идентификатор записи: " + id);
      ids.add(id);
      return {
        id: id, title: post.title.trim(), date: post.date, category: post.category,
        sourceName: String(post.sourceName || ""), excerpt: String(post.excerpt || ""),
        body: String(post.body || ""), sourceUrl: String(post.sourceUrl || ""),
        imageUrl: String(post.imageUrl || "")
      };
    });
  }
  function load() {
    var raw = "";
    try { raw = localStorage.getItem(KEY) || ""; } catch (error) {}
    if (raw) {
      try {
        posts = normalizePosts(JSON.parse(raw));
        render();
        $("editorStatus").textContent = "Загружены локальные черновики этого браузера.";
        return;
      } catch (error) {
        $("editorStatus").textContent = "Локальный список повреждён. Загружаем исходные публикации.";
      }
    }
    fetch("assets/data/news.json").then(function (response) {
      if (!response.ok) throw new Error("Не удалось загрузить assets/data/news.json");
      return response.json();
    }).then(function (data) {
      posts = normalizePosts(data.posts || []);
      render();
    }).catch(function (error) {
      posts = [];
      render();
      $("editorStatus").textContent = error.message;
    });
  }
  function persist() {
    try {
      localStorage.setItem(KEY, JSON.stringify(posts));
      $("editorStatus").textContent = "Сохранено локально в этом браузере.";
    } catch (error) {
      $("editorStatus").textContent = "Не удалось сохранить: хранилище браузера недоступно.";
    }
    render();
  }
  function reset() {
    $("newsForm").reset();
    $("postId").value = "";
    $("date").value = localDate();
  }
  function render() {
    var host = $("editorPosts");
    host.textContent = "";
    posts.slice().sort(function (a, b) { return b.date.localeCompare(a.date); }).forEach(function (post) {
      var box = document.createElement("article");
      box.className = "editor-news__item";
      var title = document.createElement("strong");
      title.textContent = post.title;
      var meta = document.createElement("small");
      meta.textContent = post.date + " · " + post.category + (post.sourceName ? " · " + post.sourceName : "");
      var edit = document.createElement("button");
      edit.type = "button";
      edit.textContent = "Изменить";
      edit.addEventListener("click", function () {
        ["postId", "title", "date", "category", "sourceName", "excerpt", "body", "sourceUrl", "imageUrl"].forEach(function (key) {
          $(key).value = post[key === "postId" ? "id" : key] || "";
        });
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
      var del = document.createElement("button");
      del.type = "button";
      del.textContent = "Удалить";
      del.addEventListener("click", function () {
        if (window.confirm("Удалить публикацию из локального списка?")) {
          posts = posts.filter(function (item) { return item.id !== post.id; });
          persist();
        }
      });
      box.append(title, meta, edit, del);
      host.appendChild(box);
    });
    if (!posts.length) {
      var note = document.createElement("p");
      note.textContent = "Публикаций пока нет.";
      host.appendChild(note);
    }
  }
  $("newsForm").addEventListener("submit", function (event) {
    event.preventDefault();
    var date = $("date").value;
    if (!validDate(date)) {
      $("editorStatus").textContent = "Укажите существующую дату публикации.";
      return;
    }
    var id = $("postId").value || createId();
    var post = {
      id: id, title: $("title").value.trim(), date: date, category: $("category").value,
      sourceName: $("sourceName").value.trim(), excerpt: $("excerpt").value.trim(),
      body: $("body").value.trim(), sourceUrl: $("sourceUrl").value.trim(),
      imageUrl: $("imageUrl").value.trim()
    };
    if (!validPost(post)) {
      $("editorStatus").textContent = "Проверьте заголовок (до 180 символов), дату, категорию и безопасный формат ссылок.";
      return;
    }
    var index = posts.findIndex(function (item) { return item.id === id; });
    if (index >= 0) posts[index] = post;
    else posts.push(post);
    persist();
    reset();
  });
  $("resetForm").addEventListener("click", reset);
  $("exportJson").addEventListener("click", function () {
    var blob = new Blob([JSON.stringify({ posts: posts }, null, 2)], { type: "application/json;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = "news.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    $("editorStatus").textContent = "Файл news.json экспортирован. Загрузите его в assets/data/ репозитория.";
  });
  $("importJson").addEventListener("change", function () {
    var file = this.files && this.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var data = JSON.parse(reader.result);
        posts = normalizePosts(data.posts);
        persist();
        $("editorStatus").textContent = "Импортировано записей: " + posts.length;
      } catch (error) {
        $("editorStatus").textContent = "Ошибка импорта: " + error.message;
      } finally {
        $("importJson").value = "";
      }
    };
    reader.onerror = function () { $("editorStatus").textContent = "Не удалось прочитать выбранный файл."; };
    reader.readAsText(file);
  });
  load();
  $("date").value = localDate();
})();
