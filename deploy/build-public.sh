#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLIC="$ROOT/public"
mkdir -p "$PUBLIC"
find "$PUBLIC" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
for page in index.html 404.html history.html sveden.html parents.html students.html news.html priem.html contacts.html school-life.html election.html; do
  test -f "$ROOT/$page"
  cp "$ROOT/$page" "$PUBLIC/$page"
done
cp -a "$ROOT/assets" "$PUBLIC/assets"
cp "$ROOT/robots.txt" "$PUBLIC/robots.txt"
# Remove links to browser-only demo editors from the VPS production copy.
find "$PUBLIC" -maxdepth 1 -type f -name "*.html" -exec sed -i \
  -e 's|<p class="footer-tech"><a href="admin.html">Техническая часть · тестовая админ-панель</a></p>||g' \
  -e 's|<a class="button button--secondary" href="news-editor.html">Редактор новостей ↗</a>||g' {} +
touch "$PUBLIC/.nojekyll"
echo "Static public site built in $PUBLIC (demo editors and source files excluded)."
