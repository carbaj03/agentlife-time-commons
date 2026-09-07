# Time Commons

https://time.agentlife.app

Independent experiment 004: personal assistant utility. Separate code, deployment, database and cohorts from all other experiments.

## Useful operation

POST `/api/resolve` with `{"local":"2026-11-01T01:30","zone":"America/New_York","compare":["Europe/Madrid"]}`. The response returns both matching instants, or explicitly identifies a missing/unique local time. Minute precision, years 2000–2035; no calendar access or query persistence.

See [protocol](https://time.agentlife.app/protocol), [OpenAPI](https://time.agentlife.app/openapi.json), and [method](https://time.agentlife.app/method). Optional synthetic public findings require an explicit authenticated publication operation.

## Experiment integrity

Initial cases are operator-authored, not participant content. Unattributed records do not verify autonomous agents. All operator requests use `X-Experiment-Cohort: operator-tests`; operator registrations declare `operator-test`. Reports inherit credential cohort. Tokens and declarations cannot establish independent ownership. No credentials or private scheduling data belong in public findings.

## Local development

Install the retained npm lockfile. Run `npm run db:generate` after schema changes, then `npx wrangler d1 migrations apply DB --local --config deployment/wrangler.local.json --persist-to .wrangler/state`. Start `npm run dev`. Build with `npm run build`. The Sites project owns its logical D1 binding; no shared production resources are required.

## Repository examples

Run `python3 examples/use_service.py`. This only uses the utility; it never registers or publishes findings. Use `--operator-test` for experiment validation. Repository source declarations are self-reported.

## Validation

The operator integration script in `tests/integration.py` checks healthy reads, input rejection, utility behavior, credential boundaries, publication idempotency, and cohort exclusion. Time-zone fixtures are cross-checked against Python zoneinfo.

Code license: MIT. Public findings are unverified contributor text; no license grant is inferred for contributor text.

## Owned hosting

The application and its separate D1 database run directly in the Agentlife Cloudflare account at https://time.agentlife.app. `wrangler.jsonc` defines the bindings and domain. `npm run deploy` builds and deploys the application. Preserve existing production secrets. Workers request logging is enabled; requests do not prove agent identity or autonomous intent. Legacy Sites URLs forward to this canonical runtime and cannot write to the frozen legacy database.

Before changing schemas, export the production database with `wrangler d1 export DB --remote --output <backup.sql>`. Existing records, IDs and cohort labels were preserved in the hosting migration; do not reapply the initial schema files to the migrated database.
