# Gym4 production restore runbook

This procedure restores the Django elections service database and private media from a matching backup created by deploy/backup.sh.

## Before starting

1. Confirm the incident owner approved a destructive restore.
2. Identify the exact backup timestamp (YYYYMMDD-HHMMSS).
3. Confirm the database and media archives are non-empty and readable.
4. Ensure sufficient free disk space for a safety backup and temporary media extraction.
5. Keep the current deploy/.env. The environment file from the backup is retained for reference and is not automatically applied.

## Restore

From the repository root:

```bash
sudo BACKUP_DIR=/var/backups/gym4-site bash deploy/restore.sh 20261118-120000
```

The script:
- requires explicit confirmation using RESTORE-<timestamp>;
- creates a safety backup of the current installation first;
- validates media archive paths before extraction;
- stops the web container during the restore;
- restores the PostgreSQL dump and replaces private media;
- retains the previous media directory as var/media.pre-restore-<timestamp>;
- starts the web service and runs Django's system check.

## After restore

1. Inspect docker compose logs --tail=100 web.
2. Verify the expected records and approved media with an authorized operator.
3. Verify public routes, login and moderation workflows.
4. Verify file permissions and that private media is not directly exposed by Nginx.
5. Record the backup timestamp, operator, incident and verification outcome.

## Important limitations

- The script does not restore the Docker image, Nginx configuration, DNS, TLS certificates or host-level secrets.
- Database restore is destructive. It should only be run against the intended deployment after approval.
- A successful Django check is not proof that all content is correct; restore must be tested periodically on a separate staging host.
- Do not treat the presence of a backup file as proof that recovery works.
