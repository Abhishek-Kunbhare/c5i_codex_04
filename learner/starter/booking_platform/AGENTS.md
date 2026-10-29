# Repository guidance for the lab

- Treat `policy/business_rules.md` as the approved policy source for this training exercise.
- Before edits, inspect callers and tests. Preserve public function signatures and response keys.
- Keep changes focused; do not add dependencies or connect to external services.
- Add or update deterministic unit tests for behavior you change.
- Report changed files, commands run, results, and unresolved assumptions.
- Do not infer policy from a code comment when the approved rule sheet is available.

## Service-fee change workflow

For the current quote/invoice service-fee task only:

- Read the approved `policy/business_rules.md` and `specs/requirement.md`, `specs/design.md`, and `specs/tasks.md` before changing fee behavior. Treat code and tests as evidence of current behavior; use approved policy for intended behavior.
- Preserve `create_quote(rooms)`, `preview_invoice(rooms)`, and their `subtotal`, `service_fee`, and `total` response keys. Limit edits to the shared service-fee calculation and focused tests.
- Separate characterization tests of inherited behavior from acceptance tests of approved policy when they conflict. Inspect callers and tests before editing; after implementation is approved, test both quote and invoice paths.
- Record changed files, commands and results, assumptions, residual risks, and the human review decision.
- Leave cancellation, database, network, UI, dependencies, and unrelated cleanup outside this task.
