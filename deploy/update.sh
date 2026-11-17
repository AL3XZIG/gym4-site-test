#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"
if [[ ! -d "$ROOT/.git" ]]; then echo "This update script expects a git clone of the repository." >&2; exit 1; fi
"$DEPLOY_DIR/backup.sh"
git -C "$ROOT" pull --ff-only
bash "$DEPLOY_DIR/build-public.sh"
cd "$DEPLOY_DIR"
docker compose --env-file .env -f docker-compose.yml up -d --build
docker compose --env-file .env -f docker-compose.yml exec -T web python manage.py check
echo "Update complete. Review: docker compose logs --tail=100 web"
