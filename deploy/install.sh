#!/usr/bin/env bash
set -Eeuo pipefail
DOMAIN="${1:-}"
if [[ ! "$DOMAIN" =~ ^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$ ]] || [[ "$DOMAIN" == *".."* ]]; then
  echo "Usage: sudo bash deploy/install.sh school.example.ru" >&2; exit 2
fi
if [[ "$EUID" -ne 0 ]]; then echo "Run as root: sudo bash deploy/install.sh $DOMAIN" >&2; exit 1; fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT/deploy"
SITE_CONF="/etc/nginx/sites-available/gym4-site"
SITE_LINK="/etc/nginx/sites-enabled/gym4-site"
LIMITS_CONF="/etc/nginx/conf.d/gym4-rate-limits.conf"
BACKUP_SERVICE="/etc/systemd/system/gym4-site-backup.service"
BACKUP_TIMER="/etc/systemd/system/gym4-site-backup.timer"
if ! command -v apt-get >/dev/null 2>&1; then echo "This installer currently supports Debian/Ubuntu (apt)." >&2; exit 1; fi
export DEBIAN_FRONTEND=noninteractive
if ! command -v nginx >/dev/null 2>&1 || ! command -v openssl >/dev/null 2>&1 || ! command -v python3 >/dev/null 2>&1; then apt-get update; apt-get install -y nginx openssl python3; fi
if ! command -v docker >/dev/null 2>&1; then apt-get update; apt-get install -y docker.io; systemctl enable --now docker; fi
if ! docker compose version >/dev/null 2>&1; then
  apt-get update
  if apt-cache show docker-compose-v2 >/dev/null 2>&1; then
    apt-get install -y docker-compose-v2
  elif apt-cache show docker-compose-plugin >/dev/null 2>&1; then
    apt-get install -y docker-compose-plugin
  else
    echo "Could not find a Docker Compose v2 package. Install the Docker Compose plugin and rerun." >&2
    exit 1
  fi
fi
if ! docker compose version >/dev/null 2>&1; then echo "Docker Compose v2 is required. Install the Docker Compose plugin and rerun." >&2; exit 1; fi
systemctl enable --now docker
if [[ -e "$SITE_LINK" ]] && { [[ ! -L "$SITE_LINK" ]] || [[ "$(readlink -f "$SITE_LINK")" != "$SITE_CONF" ]]; }; then echo "$SITE_LINK already exists and points elsewhere. Refusing to replace it." >&2; exit 1; fi
if [[ -e "$SITE_CONF" ]] && ! grep -q "Managed by gym4-site deploy/install.sh" "$SITE_CONF"; then echo "$SITE_CONF already exists and is not managed by this installer. No changes made." >&2; exit 1; fi
if [[ -e "$SITE_CONF" ]] && grep -q "ssl_certificate " "$SITE_CONF"; then echo "HTTPS is already configured in Nginx. Use deploy/update.sh for code updates; do not rerun the installer." >&2; exit 1; fi
if [[ -e "$LIMITS_CONF" ]] && ! grep -q "Managed by gym4-site deploy/install.sh" "$LIMITS_CONF"; then echo "$LIMITS_CONF already exists and is not managed by this installer. No changes made." >&2; exit 1; fi
for unit in "$BACKUP_SERVICE" "$BACKUP_TIMER"; do
  if [[ -e "$unit" ]] && ! grep -q "Managed by gym4-site deploy/install.sh" "$unit"; then
    echo "$unit already exists and is not managed by this installer. No changes made." >&2
    exit 1
  fi
done
mkdir -p "$ROOT/var/media" "$ROOT/var/staticfiles"
chown -R 10001:10001 "$ROOT/var/media" "$ROOT/var/staticfiles"
chmod 750 "$ROOT/var/media" "$ROOT/var/staticfiles"
bash "$DEPLOY_DIR/build-public.sh"
ENV_FILE="$DEPLOY_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  SECRET="$(openssl rand -hex 48)"; DB_PASSWORD="$(openssl rand -hex 32)"
  cat > "$ENV_FILE" <<EOF
DJANGO_SECRET_KEY=$SECRET
DEBUG=0
ALLOWED_HOSTS=$DOMAIN
CSRF_TRUSTED_ORIGINS=https://$DOMAIN
POSTGRES_DB=gym4_elections
POSTGRES_USER=gym4
POSTGRES_PASSWORD=$DB_PASSWORD
SECURE_SSL_REDIRECT=0
EOF
  chmod 600 "$ENV_FILE"
else
  chmod 600 "$ENV_FILE"
  if ! grep -q '^DJANGO_SECRET_KEY=.' "$ENV_FILE" || ! grep -q '^POSTGRES_PASSWORD=.' "$ENV_FILE"; then echo "$ENV_FILE exists but required secrets are missing; refusing to overwrite it." >&2; exit 1; fi
  sed -i "s|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$DOMAIN|" "$ENV_FILE"
  sed -i "s|^CSRF_TRUSTED_ORIGINS=.*|CSRF_TRUSTED_ORIGINS=https://$DOMAIN|" "$ENV_FILE"
  if ! grep -q '^SECURE_SSL_REDIRECT=' "$ENV_FILE"; then printf 'SECURE_SSL_REDIRECT=0\\n' >> "$ENV_FILE"; fi
fi
TMP_CONF="$(mktemp)"
sed -e "s|__DOMAIN__|$DOMAIN|g" -e "s|__ROOT__|$ROOT/public|g" "$DEPLOY_DIR/nginx/gym4-site.conf.template" > "$TMP_CONF"
SITE_LINK_CREATED=0
SITE_BACKUP=""; LIMITS_BACKUP=""
if [[ -f "$SITE_CONF" ]]; then SITE_BACKUP="$SITE_CONF.bak.$(date +%Y%m%d%H%M%S)"; cp -a "$SITE_CONF" "$SITE_BACKUP"; fi
if [[ -f "$LIMITS_CONF" ]]; then LIMITS_BACKUP="$LIMITS_CONF.bak.$(date +%Y%m%d%H%M%S)"; cp -a "$LIMITS_CONF" "$LIMITS_BACKUP"; fi
install -m 644 "$TMP_CONF" "$SITE_CONF"; rm -f "$TMP_CONF"
if [[ ! -e "$SITE_LINK" ]]; then
  ln -s "$SITE_CONF" "$SITE_LINK"
  SITE_LINK_CREATED=1
fi
install -m 644 "$DEPLOY_DIR/nginx/gym4-rate-limits.conf" "$LIMITS_CONF"
if ! nginx -t; then
  echo "Nginx test failed; restoring the previous site configuration." >&2
  if [[ "$SITE_LINK_CREATED" -eq 1 ]]; then rm -f "$SITE_LINK"; fi
  if [[ -n "$SITE_BACKUP" ]]; then cp -a "$SITE_BACKUP" "$SITE_CONF"; else rm -f "$SITE_CONF"; fi
  if [[ -n "$LIMITS_BACKUP" ]]; then cp -a "$LIMITS_BACKUP" "$LIMITS_CONF"; else rm -f "$LIMITS_CONF"; fi
  exit 1
fi
cd "$DEPLOY_DIR"
docker compose --env-file "$ENV_FILE" -f docker-compose.yml up -d --build
systemctl enable --now nginx
nginx -s reload
echo "Waiting for the application to start..."
READY=0
for attempt in $(seq 1 30); do
  if docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec -T web python manage.py check >/dev/null 2>&1; then READY=1; break; fi
  sleep 2
done
if [[ "$READY" -ne 1 ]]; then docker compose --env-file "$ENV_FILE" -f docker-compose.yml logs --tail=100 web; echo "Application did not become ready." >&2; exit 1; fi
if [[ "${ENABLE_TLS:-0}" == "1" ]]; then
  if [[ -z "${CERTBOT_EMAIL:-}" ]]; then echo "Set CERTBOT_EMAIL when ENABLE_TLS=1." >&2; exit 1; fi
  apt-get install -y certbot python3-certbot-nginx
  certbot --nginx --redirect -d "$DOMAIN" --non-interactive --agree-tos -m "$CERTBOT_EMAIL"
  sed -i 's/^SECURE_SSL_REDIRECT=.*/SECURE_SSL_REDIRECT=1/' "$ENV_FILE"
  docker compose --env-file "$ENV_FILE" -f docker-compose.yml up -d --force-recreate web
  TLS_READY=0
  for attempt in $(seq 1 30); do
    if docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec -T web python manage.py check >/dev/null 2>&1; then TLS_READY=1; break; fi
    sleep 2
  done
  if [[ "$TLS_READY" -ne 1 ]]; then echo "Application did not become ready after enabling HTTPS." >&2; exit 1; fi
fi
echo "Create the first organizer account (Django superuser)."
docker compose --env-file "$ENV_FILE" -f docker-compose.yml exec web python manage.py createsuperuser
if [[ "${ENABLE_TLS:-0}" == "1" ]]; then
  echo "Deployment prepared: https://$DOMAIN"
else
  echo "Deployment prepared: http://$DOMAIN (HTTPS is not configured yet)."
  echo "After obtaining a certificate, set SECURE_SSL_REDIRECT=1 in $ENV_FILE and recreate the web service."
  echo "Install Certbot with: apt-get install -y certbot python3-certbot-nginx && certbot --nginx --redirect -d $DOMAIN"
fi
echo "Do not issue candidate passwords until HTTPS is working."
echo "The existing Nginx default site was not removed or modified."
