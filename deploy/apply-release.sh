#!/usr/bin/env bash
set -Eeuo pipefail

BUNDLE="${1:-}"
if [[ -z "$BUNDLE" || ! -f "$BUNDLE" ]]; then
  echo "Usage: sudo bash deploy/apply-release.sh /path/to/gym4-release.tar.gz" >&2
  exit 2
fi
if [[ "$EUID" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/apply-release.sh $BUNDLE" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"
ENV_FILE="$DEPLOY_DIR/.env"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/gym4-site}"
STAMP="$(date +%Y%m%d-%H%M%S)"
STAGE="$(mktemp -d)"
SOURCE_BACKUP="$BACKUP_DIR/source-$STAMP.tar.gz"
BUNDLE="$(readlink -f "$BUNDLE")"
SUCCESS=0
HEALTH_OK=0

cleanup() { rm -rf "$STAGE"; }
trap cleanup EXIT

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Run the initial installer first." >&2
  exit 1
fi
if [[ ! -d "$ROOT/.git" ]]; then
  echo "The target must be the existing Git clone used by deploy/install.sh." >&2
  exit 1
fi
if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync is required. Install it with: apt-get install -y rsync" >&2
  exit 1
fi

CHECKSUM_FILE="$BUNDLE.sha256"
if [[ ! -f "$CHECKSUM_FILE" ]]; then
  echo "Missing checksum sidecar: $CHECKSUM_FILE" >&2
  exit 1
fi
(
  cd "$(dirname "$BUNDLE")"
  sha256sum --check "$(basename "$CHECKSUM_FILE")"
)

python3 - "$BUNDLE" "$STAGE" <<'PY'
import pathlib
import sys
import tarfile

archive = pathlib.Path(sys.argv[1])
destination = pathlib.Path(sys.argv[2]).resolve()
with tarfile.open(archive, "r:gz") as bundle:
    members = bundle.getmembers()
    for member in members:
        target = (destination / member.name).resolve()
        if target != destination and destination not in target.parents:
            raise SystemExit(f"Unsafe path in release archive: {member.name}")
        if not (member.isfile() or member.isdir()):
            raise SystemExit(f"Unsupported special file in release archive: {member.name}")
    bundle.extractall(destination, members=members)
PY

for required in server/Dockerfile server/manage.py deploy/docker-compose.yml deploy/build-public.sh repo.bundle; do
  if [[ ! -f "$STAGE/$required" ]]; then
    echo "Release bundle is incomplete: missing $required" >&2
    exit 1
  fi
done
if [[ ! -f "$STAGE/RELEASE-MANIFEST.txt" ]]; then
  echo "Release manifest is missing." >&2
  exit 1
fi

echo "Creating database, media and environment backup..."
BACKUP_DIR="$BACKUP_DIR" bash "$DEPLOY_DIR/backup.sh"
mkdir -p "$BACKUP_DIR"
umask 077
tar -czf "$SOURCE_BACKUP" -C "$ROOT" \
  --exclude=.git --exclude=deploy/.env --exclude=var --exclude=public .
chmod 600 "$SOURCE_BACKUP"

rollback() {
  local status=$?
  if [[ "$SUCCESS" -eq 0 ]]; then
    echo "Release failed. Restoring previous application files..." >&2
    if [[ -f "$SOURCE_BACKUP" ]]; then
      mkdir -p "$STAGE/rollback"
      tar -xzf "$SOURCE_BACKUP" -C "$STAGE/rollback"
      rsync -a --delete \
        --exclude='/.git/' \
        --exclude='/deploy/.env' \
        --exclude='/var/' \
        --exclude='/public/' \
        "$STAGE/rollback/" "$ROOT/"
      if ! bash "$DEPLOY_DIR/build-public.sh"; then
        echo "Warning: could not regenerate the public site from restored sources." >&2
      fi
      if [[ -f "$DEPLOY_DIR/.env" ]]; then
        (cd "$DEPLOY_DIR" && docker compose --env-file .env -f docker-compose.yml up -d --build) || true
      fi
    fi
    echo "Database backup is preserved in $BACKUP_DIR; review migrations before restoring it." >&2
  fi
  exit "$status"
}
trap rollback ERR

echo "Applying release files..."
rsync -a --delete \
  --exclude='/.git/' \
  --exclude='/deploy/.env' \
  --exclude='/var/' \
  --exclude='/public/' \
  --exclude='/repo.bundle' \
  "$STAGE/" "$ROOT/"

bash "$DEPLOY_DIR/build-public.sh"
cd "$DEPLOY_DIR"
docker compose --env-file "$ENV_FILE" -f docker-compose.yml config -q
docker compose --env-file "$ENV_FILE" -f docker-compose.yml up -d --build
APP_READY=0
for attempt in $(seq 1 30); do
  if docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec -T web python manage.py check >/dev/null 2>&1; then
    APP_READY=1
    break
  fi
  sleep 2
done
if [[ "$APP_READY" -ne 1 ]]; then
  docker compose --env-file "$ENV_FILE" -f docker-compose.yml logs --tail=100 web >&2 || true
  echo "Django did not become ready." >&2
  false
fi
docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec -T web python manage.py migrate --check
docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec -T web python manage.py showmigrations --plan

# Check the configured virtual host and Django login with the real Host header.
HEALTH_HOST="$(awk -F= '$1 == "ALLOWED_HOSTS" { split($2, hosts, ","); print hosts[1]; exit }' "$ENV_FILE")"
HEALTH_REDIRECT="$(awk -F= '$1 == "SECURE_SSL_REDIRECT" { print $2; exit }' "$ENV_FILE")"
if [[ -z "$HEALTH_HOST" ]]; then
  echo "ALLOWED_HOSTS is empty; cannot perform the deployment health check." >&2
  false
fi
PROXY_PROTO=http
if [[ "$HEALTH_REDIRECT" != "0" ]]; then PROXY_PROTO=https; fi
for attempt in $(seq 1 30); do
  ROOT_STATUS="$(curl --silent --output /dev/null --write-out '%{http_code}' -H "Host: $HEALTH_HOST" http://127.0.0.1/ || true)"
  if [[ "$ROOT_STATUS" =~ ^(200|301|302)$ ]] && \
     curl --fail --silent --show-error --output /dev/null \
       -H "Host: $HEALTH_HOST" \
       -H "X-Forwarded-Proto: $PROXY_PROTO" \
       http://127.0.0.1:8000/portal/login/; then
    HEALTH_OK=1
    break
  fi
  sleep 2
done
if [[ "$HEALTH_OK" -ne 1 ]]; then
  docker compose --env-file "$ENV_FILE" -f docker-compose.yml logs --tail=100 web >&2 || true
  echo "Post-deployment health check failed." >&2
  false
fi

git -C "$ROOT" fetch "$STAGE/repo.bundle" HEAD
git -C "$ROOT" reset --hard FETCH_HEAD
SUCCESS=1
trap - ERR
echo "Release successfully deployed."
echo "Manifest: $ROOT/RELEASE-MANIFEST.txt"
echo "Source rollback archive: $SOURCE_BACKUP"
echo "Database/media/environment backups: $BACKUP_DIR"
echo "Review logs: cd $DEPLOY_DIR && docker compose --env-file .env -f docker-compose.yml logs --tail=100"
