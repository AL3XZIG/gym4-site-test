(function () {
  "use strict";
  var baseKey = "gym4-election-demo-v1";
  var candidateHost = document.getElementById("electionCandidates");
  var voteForm = document.getElementById("electionVoteForm");
  var voteOptions = document.getElementById("electionVoteOptions");
  var voteStatus = document.getElementById("electionVoteStatus");
  if (!candidateHost || !voteForm || !voteOptions || !voteStatus) return;

  function text(value) { return typeof value === "string" ? value : ""; }
  function safeAssetPath(value) {
    var path = text(value).trim();
    return /^assets\\/[A-Za-z0-9_./-]+$/.test(path) && !path.split("/").some(function (part) { return part === ".."; });
  }
  function safeMaterialUrl(value) {
    var url = text(value).trim();
    if (!url) return false;
    if (safeAssetPath(url)) return true;
    try {
      var parsed = new URL(url);
      return parsed.protocol === "https:" || parsed.protocol === "http:";
    } catch (error) { return false; }
  }
  function make(tag, className, content) {
    var element = document.createElement(tag);
    if (className) element.className = className;
    if (content) element.textContent = content;
    return element;
  }
  function addMaterials(host, materials) {
    if (!Array.isArray(materials) || !materials.length) return;
    var list = make("ul", "election-materials");
    materials.forEach(function (material) {
      if (!material || !safeMaterialUrl(material.url) || !text(material.title).trim()) return;
      var item = document.createElement("li");
      var link = make("a", "", text(material.title).trim());
      link.href = material.url;
      if (/^https?:/i.test(material.url)) {
        link.target = "_blank";
        link.rel = "noopener noreferrer";
      }
      item.appendChild(link);
      list.appendChild(item);
    });
    if (list.children.length) host.appendChild(list);
  }
  function renderCandidate(candidate, index) {
    var card = make("article", "election-candidate");
    var header = make("div", "election-candidate__header");
    var mark = make("span", "election-candidate__mark", String(index + 1).padStart(2, "0"));
    mark.setAttribute("aria-hidden", "true");
    var identity = make("div", "election-candidate__identity");
    identity.appendChild(make("span", "election-candidate__kicker", "ДЕМО-ПРИМЕР"));
    identity.appendChild(make("h3", "", text(candidate.name)));
    if (text(candidate.class).trim()) identity.appendChild(make("span", "election-candidate__class", text(candidate.class)));
    header.append(mark, identity);
    card.appendChild(header);
    if (safeAssetPath(candidate.poster)) {
      var poster = make("img", "election-candidate__poster");
      poster.src = candidate.poster;
      poster.alt = "Демонстрационный агитационный плакат: " + text(candidate.name);
      poster.loading = "lazy";
      poster.decoding = "async";
      card.appendChild(poster);
    }
    if (text(candidate.slogan).trim()) card.appendChild(make("p", "election-candidate__slogan", "«" + text(candidate.slogan).trim() + "»"));
    if (text(candidate.bio).trim()) card.appendChild(make("p", "election-candidate__bio", text(candidate.bio).trim()));
    if (Array.isArray(candidate.program) && candidate.program.length) {
      card.appendChild(make("h4", "election-candidate__subhead", "Ключевые пункты программы"));
      var program = make("ul", "election-program");
      candidate.program.forEach(function (point) {
        if (text(point).trim()) program.appendChild(make("li", "", text(point).trim()));
      });
      card.appendChild(program);
    }
    addMaterials(card, candidate.materials);
    return card;
  }
  function render(data) {
    if (!data || data.mode !== "demo" || data.demoOnly !== true) {
      candidateHost.textContent = "Демонстрационный режим не настроен.";
      voteStatus.textContent = "Настоящее электронное голосование не подключено.";
      return;
    }
    var candidates = Array.isArray(data.candidates) ? data.candidates.filter(function (candidate) {
      return candidate && typeof candidate.id === "string" && candidate.id && text(candidate.name).trim();
    }) : [];
    candidateHost.textContent = "";
    if (!candidates.length) {
      candidateHost.appendChild(make("p", "election-loading", "Список кандидатов пока не опубликован."));
    } else {
      candidates.forEach(function (candidate, index) { candidateHost.appendChild(renderCandidate(candidate, index)); });
    }
    if (!data.votingEnabled || !candidates.length) {
      voteStatus.textContent = "Демонстрационное голосование сейчас не открыто.";
      return;
    }
    var storageKey = baseKey + ":" + (text(data.electionId) || "preview");
    var storage;
    try { storage = { available: true, value: localStorage.getItem(storageKey) }; }
    catch (error) { storage = { available: false, value: null }; }
    if (!storage.available) {
      voteStatus.textContent = "Хранилище браузера недоступно. Тестовый выбор не сохранён.";
      return;
    }
    if (storage.value) {
      voteStatus.textContent = "В этом браузере уже сохранён демонстрационный выбор. Он не отправлялся и не учитывается в результатах.";
      return;
    }
    voteOptions.textContent = "";
    candidates.forEach(function (candidate) {
      var label = make("label", "election-vote-option");
      var radio = document.createElement("input");
      radio.type = "radio";
      radio.name = "electionCandidate";
      radio.value = candidate.id;
      radio.required = true;
      label.append(radio, make("span", "", text(candidate.name)));
      voteOptions.appendChild(label);
    });
    voteForm.hidden = false;
    voteForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var selected = voteForm.querySelector('input[name="electionCandidate"]:checked');
      if (!selected || !candidates.some(function (candidate) { return candidate.id === selected.value; })) {
        voteStatus.textContent = "Сначала выберите одного кандидата.";
        return;
      }
      try {
        localStorage.setItem(storageKey, selected.value);
        voteForm.hidden = true;
        voteStatus.textContent = "Тестовый выбор сохранён только в этом браузере. Он не отправлен организаторам и не является голосом на выборах.";
      } catch (error) {
        voteStatus.textContent = "Не удалось сохранить тестовый выбор: хранилище браузера недоступно.";
      }
    });
  }
  fetch("assets/data/election.json").then(function (response) {
    if (!response.ok) throw new Error("Не удалось загрузить данные выборов.");
    return response.json();
  }).then(render).catch(function () {
    candidateHost.textContent = "Не удалось загрузить демонстрационные данные. Проверьте assets/data/election.json.";
    voteStatus.textContent = "Голосование недоступно: данные не загружены.";
  });
})();
