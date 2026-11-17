(function () {
  "use strict";
  var baseKey = "gym4-election-demo-v1";
  var candidateHost = document.getElementById("electionCandidates");
  var voteForm = document.getElementById("electionVoteForm");
  var voteOptions = document.getElementById("electionVoteOptions");
  var voteStatus = document.getElementById("electionVoteStatus");
  var portalLink = document.getElementById("electionPortalLink");
  if (!candidateHost || !voteForm || !voteOptions || !voteStatus) return;

  function text(value) { return typeof value === "string" ? value : ""; }
  function safeAssetPath(value) {
    var path = text(value).trim();
    return /^assets\/[A-Za-z0-9_./-]+$/.test(path) && !path.split("/").some(function (part) { return part === ".."; });
  }
  function safeMaterialUrl(value) {
    var url = text(value).trim();
    if (!url) return false;
    if (safeAssetPath(url)) return true;
    try {
      var parsed = new URL(url, window.location.href);
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
  function renderCandidate(candidate, index, live) {
    var card = make("article", "election-candidate");
    var header = make("div", "election-candidate__header");
    var mark = make("span", "election-candidate__mark", String(index + 1).padStart(2, "0"));
    mark.setAttribute("aria-hidden", "true");
    var identity = make("div", "election-candidate__identity");
    identity.appendChild(make("span", "election-candidate__kicker", live ? "КАНДИДАТ" : "ДЕМО-ПРИМЕР"));
    identity.appendChild(make("h3", "", text(candidate.name)));
    if (text(candidate.class).trim()) identity.appendChild(make("span", "election-candidate__class", text(candidate.class)));
    header.append(mark, identity);
    card.appendChild(header);
    if (safeMaterialUrl(candidate.poster)) {
      var poster = make("img", "election-candidate__poster");
      poster.src = candidate.poster;
      poster.alt = (live ? "Агитационный плакат: " : "Демонстрационный плакат: ") + text(candidate.name);
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
  function render(data, live) {
    var candidates = Array.isArray(data.candidates) ? data.candidates.filter(function (candidate) {
      return candidate && typeof candidate.id === "string" && candidate.id && text(candidate.name).trim();
    }) : [];
    candidateHost.textContent = "";
    if (!candidates.length) {
      candidateHost.appendChild(make("p", "election-loading", live ? "Организаторы пока не опубликовали карточки кандидатов." : "Демонстрационные карточки не найдены."));
    } else {
      candidates.forEach(function (candidate, index) {
        candidateHost.appendChild(renderCandidate(candidate, index, live));
      });
    }
    if (live) {
      voteForm.hidden = true;
      voteStatus.textContent = "Публикация материалов работает. Электронное голосование пока не запущено.";
      if (portalLink) portalLink.hidden = false;
      var campaign = data.campaign || {};
      var aboutLead = document.querySelector("#about .section-lead");
      if (aboutLead && text(campaign.intro).trim()) aboutLead.textContent = campaign.intro;
      var callout = document.querySelector(".election-callout");
      if (callout) {
        var calloutTitle = callout.querySelector("strong");
        var calloutText = callout.querySelector("p");
        if (calloutTitle) calloutTitle.textContent = "Информация о кампании";
        if (calloutText) calloutText.textContent = text(campaign.intro).trim() || "Здесь публикуются карточки и материалы, одобренные организаторами выборов.";
      }
      var pageIntro = document.querySelector(".page-intro p");
      if (pageIntro) pageIntro.textContent = "Информация о кандидатах и ходе кампании публикуется на равных условиях. На странице размещаются только материалы, одобренные организаторами.";
      var voteNotice = document.querySelector(".election-demo-notice");
      if (voteNotice) {
        var noticeTitle = voteNotice.querySelector("strong");
        var noticeText = voteNotice.querySelector("p");
        if (noticeTitle) noticeTitle.textContent = "Электронное голосование не запущено";
        if (noticeText) noticeText.textContent = "Сейчас сервер публикует только материалы кампании. Официальный бюллетень появится после утверждения правил и отдельной технической проверки.";
      }
      var rulesNote = document.querySelector("#rules .source-note");
      if (rulesNote) rulesNote.textContent = text(campaign.rules).trim() || "Официальный регламент выборов пока не опубликован организаторами.";
      return;
    }
    if (!data || data.mode !== "demo" || data.demoOnly !== true) {
      voteForm.hidden = true;
      voteStatus.textContent = "Демонстрационный режим не настроен. Настоящее голосование не подключено.";
      return;
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
  fetch("/api/v1/public/election/").then(function (response) {
    if (!response.ok) throw new Error("Live API unavailable");
    return response.json();
  }).then(function (data) {
    if (!data || data.mode !== "live" || data.demoOnly !== false) throw new Error("Not a live election API");
    render(data, true);
  }).catch(function () {
    fetch("assets/data/election.json").then(function (response) {
      if (!response.ok) throw new Error("Не удалось загрузить демонстрационные данные.");
      return response.json();
    }).then(function (data) {
      render(data, false);
    }).catch(function () {
      candidateHost.textContent = "Не удалось загрузить карточки. Проверьте подключение к данным выборов.";
      voteStatus.textContent = "Голосование недоступно: данные не загружены.";
    });
  });
})();
