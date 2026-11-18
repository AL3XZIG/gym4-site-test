#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/gym4-site}"
STAMP="${1:-}"

if [[ "$EUID" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/restore.sh YYYYMMDD-HHMMSS" >&2
  exit 1
fi
if [[ ! "$STAMP" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then
  echo "Usage: sudo bash deploy/restore.sh YYYYMMDD-HHMMSS" >&2
  exit 2
fi

DB_BACKUP="$BACKUP_DIR/database-$STAMP.sql.gz"
MEDIA_BACKUP="$BACKUP_DIR/media-$STAMP.tar.gz"
ENV_FILE="$DEPLOY_DIR/.env"
for file in "$DB_BACKUP" "$MEDIA_BACKUP" "$ENV_FILE"; do
  if [[ ! -s "$file" ]]; then
    echo "Required non-empty file not found: $file" >&2
    exit 1
  fi
done
if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required." >&2
  exit 1
fi

# Validate the archive before extracting it. Only relative paths are accepted.
while IFS= read -r entry; do
  case "$entry" in
    /*|..|../*|*/../*|*/..)
      echo "Unsafe path in media archive: $entry" >&2
      exit 1
      ;;
  esac
done < <(tar -tzf "$MEDIA_BACKUP")

echo "WARNING: this replaces the live database and media files."
echo "A safety backup of the current installation will be created first."
read -r -p "Type RESTORE-$STAMP to continue: " confirmation
if [[ "$confirmation" != "RESTORE-$STAMP" ]]; then
  echo "Restore cancelled."
  exit 1
fi

OLD_MEDIA="$ROOT/var/media.pre-restore-$STAMP"
if [[ -e "$OLD_MEDIA" ]]; then
  echo "Refusing to overwrite existing recovery directory: $OLD_MEDIA" >&2
  exit 1
fi
bash "$DEPLOY_DIR/backup.sh"
TEMP_DIR="$(mktemp -d "$ROOT/var/restore.XXXXXX")"
MEDIA_STAGE="$TEMP_DIR/media"
mkdir -p "$MEDIA_STAGE"
cleanup() {
  rm -rf "$TEMP_DIR"
}
web_stopped=0
on_exit() {
  local status=$?
  if [[ "$status" -ne 0 && -d "$OLD_MEDIA" ]]; then
    docker compose --env-file "$ENV_FILE" -f "$DEPLOY_DIR/docker-compose.yml" stop web || true
    if [[ -e "$ROOT/var/media" ]]; then
      mv "$ROOT/var/media" "$ROOT/var/media.failed-$STAMP-$$" || true
    fi
    mv "$OLD_MEDIA" "$ROOT/var/media" || true
  fi
  if [[ "$web_stopped" == "1" ]]; then
    docker compose --env-file "$ENV_FILE" -f "$DEPLOY_DIR/docker-compose.yml" up -d web || true
  fi
  cleanup
  exit "$status"
}
trap on_exit EXIT

tar --no-same-owner --no-same-permissions -xzf "$MEDIA_BACKUP" -C "$MEDIA_STAGE"
mkdir -p "$ROOT/var/media"

cd "$DEPLOY_DIR"
web_stopped=1
docker compose --env-file .env -f docker-compose.yml stop web

docker compose --env-file .env -f docker-compose.yml exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" "$POSTGRES_DB" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'
gunzip -c "$DB_BACKUP" | docker compose --env-file .env -f docker-compose.yml exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" "$POSTGRES_DB"'
mv "$ROOT/var/media" "$OLD_MEDIA"
mv "$MEDIA_STAGE" "$ROOT/var/media"
chown -R 10001:10001 "$ROOT/var/media"
chmod 750 "$ROOT/var/media"
docker compose --env-file .env -f docker-compose.yml up -d web
docker compose --env-file .env -f docker-compose.yml exec -T web python manage.py check
web_stopped=0
echo "Restore completed. Previous media retained at: $OLD_MEDIA"
echo "Run a public-site smoke check and inspect service logs before declaring recovery complete."
