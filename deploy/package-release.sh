#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/releases}"
mkdir -p "$OUT_DIR"

if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Run this script inside a Git clone." >&2
  exit 1
fi
if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit the changes before packaging a release." >&2
  exit 1
fi

COMMIT="$(git -C "$ROOT" rev-parse --short=12 HEAD)"
BRANCH="$(git -C "$ROOT" branch --show-current)"
STAMP="$(date -u +%Y%m%d-%H%M%S)"
NAME="gym4-release-$STAMP-$COMMIT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git -C "$ROOT" archive --format=tar HEAD | tar -xf - -C "$TMP"
git -C "$ROOT" bundle create "$TMP/repo.bundle" HEAD
cat > "$TMP/RELEASE-MANIFEST.txt" <<EOF
Gym4 release bundle
Commit: $COMMIT
Branch: $BRANCH
Created UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Source: git archive HEAD
EOF

tar -czf "$OUT_DIR/$NAME.tar.gz" -C "$TMP" .
(
  cd "$OUT_DIR"
  sha256sum "$NAME.tar.gz" > "$NAME.tar.gz.sha256"
)

echo "Release bundle created:"
echo "  $OUT_DIR/$NAME.tar.gz"
echo "  $OUT_DIR/$NAME.tar.gz.sha256"
echo
echo "Upload both files to the VPS, then run:"
echo "  sudo bash /path/to/gym4-site/deploy/apply-release.sh /path/to/$NAME.tar.gz"
