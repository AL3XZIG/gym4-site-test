#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLIC="$ROOT/public"
mkdir -p "$PUBLIC"
python3 "$ROOT/tools/build_sveden_routes.py"
find "$PUBLIC" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
for page in index.html 404.html history.html sveden.html parents.html students.html news.html priem.html contacts.html school-life.html election.html; do
  test -f "$ROOT/$page"
  cp "$ROOT/$page" "$PUBLIC/$page"
done
cp -a "$ROOT/assets" "$PUBLIC/assets"
cp -a "$ROOT/sveden" "$PUBLIC/sveden"
rm -f "$PUBLIC/assets/js/admin-demo.js" "$PUBLIC/assets/js/news-editor.js" "$PUBLIC/assets/js/content-review.js" "$PUBLIC/assets/css/admin.css"
cp "$ROOT/robots.txt" "$PUBLIC/robots.txt"
# Production pages must not expose demo editors, demo labels, or demo election ballots.
python3 - "$PUBLIC" <<'PY'
from pathlib import Path
import re
import sys

public = Path(sys.argv[1])
for page in public.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    html = re.sub(r'<div class="demo-strip"[^>]*>.*?</div>', "", html, flags=re.S)
    html = re.sub(r'<a\b[^>]*href="admin\.html"[^>]*>.*?</a>', "", html, flags=re.S)
    html = re.sub(r'<a\b[^>]*href="news-editor\.html"[^>]*>.*?</a>', "", html, flags=re.S)
    html = html.replace("Демонстрационная версия сайта.", "Информация на сайте требует актуализации ответственными сотрудниками.")
    html = html.replace("Демонстрационный проект", "Информационный сайт гимназии № 4")
    html = html.replace("демонстрационный режим голосования", "информация о кампании и кандидатах")
    html = html.replace("Здесь можно разместить даты кампании, порядок встреч с кандидатами, правила агитации и официальные объявления организаторов. Неутверждённые даты и условия не публикуются.", "Информация о сроках кампании, встречах и правилах публикуется организаторами после утверждения.")
    html = html.replace("Если JavaScript отключён, интерактивная демонстрация голосования недоступна.", "Информация о голосовании появится после утверждения процедуры.")
    html = html.replace("Это рекомендации для макета, а не утверждённый регламент гимназии. Официальные правила, возрастные ограничения и порядок подсчёта должны определить организаторы.", "Официальный регламент выборов будет опубликован организаторами после утверждения.")
    html = html.replace("Демонстрационная версия сайта. Содержание и документы требуют согласования.", "Информация и документы требуют актуализации ответственными сотрудниками.")
    html = html.replace("Демонстрационная версия сайта. Сведения не являются официальными и не внесены.", "Информация на сайте требует актуализации ответственными сотрудниками.")
    html = html.replace("Демонстрационная версия. Исторические сведения собраны по официальным материалам гимназии и требуют итогового согласования.", "Исторические сведения требуют актуализации ответственными сотрудниками.")
    html = html.replace("Демо не принимает и не сохраняет обращения.", "Порядок обращений указан в разделе «Контакты».")
    html = html.replace("Настройки доступности хранятся в браузере посетителя. Сайт не отправляет формы и не собирает данные через эту демонстрационную версию.", "Настройки доступности хранятся в браузере посетителя.")
    html = html.replace("Демонстрационная версия. Расписание и события требуют подтверждения администрацией.", "Расписание и события публикуются после подтверждения администрацией.")
    html = html.replace("Кандидаты, программы и демонстрация голосования", "Кандидаты, программы и ход кампании")
    html = html.replace("Демонстрационный раздел", "Информация о кампании")
    html = html.replace("Сейчас на странице показан пример оформления. Указанные кандидаты и их программы условные и не относятся к реальным участникам выборов.", "Здесь публикуются карточки и материалы, одобренные организаторами выборов.")
    html = html.replace("В демоверсии показаны условные профили; на сервере отображаются только одобренные материалы.", "На странице размещаются только материалы, одобренные организаторами.")
    html = html.replace("Только демонстрация — не официальный бюллетень", "Электронное голосование не запущено")
    html = html.replace("Тестовый выбор сохраняется локально в этом браузере. Он не отправляется организаторам, не учитывается в итогах и не подтверждает личность избирателя.", "Сейчас сервер публикует только материалы кампании. Официальный бюллетень появится после утверждения правил и отдельной технической проверки.")
    html = html.replace("Тестирование интерфейса", "Голосование")
    html = html.replace("Демонстрационный режим голосования.", "Информация о кампании и кандидатах.")
    html = html.replace("</head>", '<style>.demo-strip,.footer-season{display:none!important}</style></head>')
    page.write_text(html, encoding="utf-8")

data_dir = public / "assets" / "data"
data_dir.mkdir(parents=True, exist_ok=True)
(data_dir / "election.json").write_text(
    '{"mode":"demo","demoOnly":true,"votingEnabled":false,"candidates":[]}\n',
    encoding="utf-8",
)
(data_dir / "news.json").write_text('{"posts":[]}\n', encoding="utf-8")
PY
touch "$PUBLIC/.nojekyll"
echo "Static VPS site built in $PUBLIC; demo editors, demo ballots and sample data are excluded."
