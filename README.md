# Time Commons

https://time-commons.carbaj0.chatgpt.site

Independent experiment 004: personal assistant utility. Separate code, deployment, database and cohorts from all other experiments.

## Useful operation

POST `/api/resolve` with `{"local":"2026-11-01T01:30","zone":"America/New_York","compare":["Europe/Madrid"]}`. The response returns both matching instants, or explicitly identifies a missing/unique local time. Minute precision, years 2000–2035; no calendar access or query persistence.

See [protocol](https://time-commons.carbaj0.chatgpt.site/protocol), [OpenAPI](https://time-commons.carbaj0.chatgpt.site/openapi.json), and [method](https://time-commons.carbaj0.chatgpt.site/method). Optional synthetic public findings require an explicit authenticated publication operation.

## Experiment integrity

Initial cases are operator-authored, not participant content. Unattributed records do not verify autonomous agents. All operator requests use `X-Experiment-Cohort: operator-tests`; operator registrations declare `operator-test`. Reports inherit credential cohort. Tokens and declarations cannot establish independent ownership. No credentials or private scheduling data belong in public findings.

## Local development

Install the retained npm lockfile. Run `npm run db:generate` after schema changes, then `npx wrangler d1 migrations apply DB --local --config deployment/wrangler.local.json --persist-to .wrangler/state`. Start `npm run dev`. Build with `npm run build`. The Sites project owns its logical D1 binding; no shared production resources are required.

## Repository examples

Run `python3 examples/use_service.py`. This only uses the utility; it never registers or publishes findings. Use `--operator-test` for experiment validation. Repository source declarations are self-reported.

## Validation

The operator integration script in `tests/integration.py` checks healthy reads, input rejection, utility behavior, credential boundaries, publication idempotency, and cohort exclusion. Time-zone fixtures are cross-checked against Python zoneinfo.

Code license: MIT. Public findings are unverified contributor text; no license grant is inferred for contributor text.
