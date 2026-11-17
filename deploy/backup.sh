#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/gym4-site}"
mkdir -p "$BACKUP_DIR"; chmod 700 "$BACKUP_DIR"; umask 077
STAMP="$(date +%Y%m%d-%H%M%S)"
cd "$DEPLOY_DIR"
cp .env "$BACKUP_DIR/environment-$STAMP"
chmod 600 "$BACKUP_DIR/environment-$STAMP"
docker compose --env-file .env -f docker-compose.yml exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$BACKUP_DIR/database-$STAMP.sql.gz"
docker compose --env-file .env -f docker-compose.yml exec -T web tar -czf - -C /app/private_media . > "$BACKUP_DIR/media-$STAMP.tar.gz"
find "$BACKUP_DIR" -type f -mtime +14 -delete
echo "Backup created in $BACKUP_DIR"
