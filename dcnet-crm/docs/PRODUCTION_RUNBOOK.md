# DCNET CRM Production Runbook

## Release gates

All commands must pass from the `dcnet-crm` repository before deployment:

```bash
npm ci
npm test
python -m compileall -q dcnet_crm
python scripts/check-backend-safety.py
bench --site staging.local set-config allow_tests true
bench --site staging.local run-tests --app dcnet_crm --module dcnet_crm.tests.test_api
```

Do not deploy a dirty working tree. Release only an immutable Git commit/tag
that passed the `Quality` workflow.

## Required site configuration

```json
{
  "developer_mode": 0,
  "live_reload": false,
  "allow_tests": false,
  "dcnet_crm_show_unready_features": 0
}
```

Production must also use HTTPS at the reverse proxy, authenticated Redis,
restricted MariaDB access, encrypted off-host backups, and secrets supplied by
the deployment environment rather than committed files.

## Deploy

```bash
bench --site <site> backup --with-files
bench build --app dcnet_crm
bench --site <site> migrate
bench --site <site> clear-cache
bench --site <site> clear-website-cache
```

Restart web, queue and socket.io processes using the production process
manager. Verify scheduler and workers:

```bash
bench --site <site> scheduler status
bench doctor
```

## Smoke test

Test using Sales User, Sales Manager and System Manager accounts:

1. CRM page and native sidebar load over HTTPS.
2. List/detail/create/edit for Lead, Contact, Customer and Opportunity.
3. Quotation and Sales Order remain valid ERPNext drafts.
4. Sales Order actions create linked request tasks only.
5. Activity access respects owner/share rules.
6. File upload/download respects document permissions.
7. No placeholder controls appear when `dcnet_crm_show_unready_features = 0`.
8. Error Log, web error log and worker error log remain clean.

## Rollback

1. Put the site in maintenance mode.
2. Restore the pre-deploy database and files backup.
3. Deploy the previous immutable app tag.
4. Run migrate and clear caches.
5. Re-run smoke tests before reopening traffic.

