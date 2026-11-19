#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"

if [[ -n "${1:-}" ]]; then
  exec bash "$DEPLOY_DIR/apply-release.sh" "$1"
fi

if [[ ! -d "$ROOT/.git" ]]; then
  echo "This update path expects a Git clone. For a portable release archive, pass its path:" >&2
  echo "  sudo bash deploy/update.sh /path/to/gym4-release.tar.gz" >&2
  exit 1
fi

echo "Updating directly from Git (legacy path). Prefer a verified release bundle:"
echo "  bash deploy/package-release.sh"
echo "  sudo bash deploy/update.sh /path/to/gym4-release.tar.gz"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/gym4-site}"
BACKUP_DIR="$BACKUP_DIR" bash "$DEPLOY_DIR/backup.sh"
git -C "$ROOT" pull --ff-only
bash "$DEPLOY_DIR/build-public.sh"
cd "$DEPLOY_DIR"
docker compose --env-file .env -f docker-compose.yml up -d --build
docker compose --env-file .env -f docker-compose.yml exec -T web python manage.py check
docker compose --env-file .env -f docker-compose.yml exec -T web python manage.py migrate --check
curl --fail --silent --output /dev/null http://127.0.0.1/
echo "Update complete. Review: docker compose logs --tail=100 web"
