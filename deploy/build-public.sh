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
touch "$PUBLIC/.nojekyll"
echo "Static public site built in $PUBLIC (demo editors and source files excluded)."
