# Shared service-fee implementation tasks

Status: **planning checklist; implementation has not started**. Follow the reviewed [requirements](requirement.md#numbered-requirements) and [design](design.md#shared-helper-contract-and-calculation-order). Run commands below **only after implementation approval**, from `starter/booking_platform/`; no command in this document has been run as part of writing it. The approved policy requires 10% of the aggregate room subtotal, rounded once ([local policy:5-9](../policy/business_rules.md#L5-L9), [root policy:7-12](../../../policy/business_rules.md#L7-L12)). Keep the brief's exclusions and public contract ([brief:13-15](../../../brief.md#L13-L15), [AGENTS.md:3-8](../AGENTS.md#L3-L8)).

## Ordered checklist

### 1. Characterize inherited behavior before production edits

- [ ] Add a focused quote test with two lines, one explicit `rooms: 2` and one omitted count, expecting `{"subtotal": 450, "service_fee": 45, "total": 495}`. Keep the existing one-room and response-key assertions ([test_quote.py:5-10](../tests/test_quote.py#L5-L10), [pricing.py:3-9](../src/pricing.py#L3-L9)).
- [ ] Add an invoice multi-line test asserting subtotal `450`, the three-key shape, and `total == subtotal + service_fee`, without asserting that 12% is desired. Retain the existing `200/24/224` fixture **temporarily** and label it historical/current behavior, as it already is ([test_invoice.py:5-8](../tests/test_invoice.py#L5-L8), [invoice.py:3-7](../src/invoice.py#L3-L7)). Record the observed legacy result in the review evidence before changing it.

**Files expected to change:** `tests/test_quote.py`, `tests/test_invoice.py`. **Requirements:** REQ-01, REQ-04, REQ-06; the legacy result documents the REQ-02 conflict. **Completion evidence:** both added characterization cases pass against pre-refactor source; the review notes distinguish the 12% invoice result from approved policy. **Smallest check after approval:** `python -m unittest tests.test_quote tests.test_invoice -v`. **Human review point:** confirm that the historical assertion is evidence of current behavior only, consistent with the policy's evidence rule ([root policy:14-16](../../../policy/business_rules.md#L14-L16)).

### 2. Add policy acceptance tests before the code change

- [ ] Add tests that call **both** `create_quote(rooms)` and `preview_invoice(rooms)` for the examples in [requirements:34-43](requirement.md#acceptance-examples-for-the-approved-rule): one line `200/20/220`, two lines with explicit/omitted room counts `450/45/495`, two lines of `5` each `10/1/11`, and `[]` as `0/0/0`.
- [ ] Assert the exact response key set `{subtotal, service_fee, total}` for both public paths. Keep the aggregate-rounding case as an explicit regression guard: `round((5 + 5) * .10) == 1`, while separately rounding the two half-unit fees gives `0` ([root policy:7-10](../../../policy/business_rules.md#L7-L10)).

**Files expected to change:** new `tests/test_policy_pricing.py` (or one equivalently focused existing test file, if review prefers). **Requirements:** REQ-01 through REQ-06. **Completion evidence:** the test code contains the four exact fixtures and checks both entry points; before production changes, quote cases pass and invoice cases that distinguish 12% from 10% fail for the **expected policy conflict**, with the failure recorded rather than treated as approval of 12%. **Smallest check after approval:** `python -m unittest tests.test_policy_pricing -v` (expected red for the invoice's 200 and 450 subtotal cases before the refactor). **Human review point:** confirm expected values against the approved policy and explicitly accept the intentional invoice correction before implementation continues.

### 3. Add the shared fee helper

- [ ] Add `src/shared/pricing.py` with the reviewed signature `calculate_service_fee(subtotal)` returning `round(subtotal * 0.10)`. It accepts an already aggregated subtotal, not room lines, and does not add validation or dependencies ([design](design.md#shared-helper-contract-and-calculation-order), [root policy:7-10](../../../policy/business_rules.md#L7-L10)).
- [ ] Add an empty `src/shared/__init__.py` **only if** the reviewer chooses an explicit package; the current `src` package has an [`__init__.py`](../src/__init__.py).

**Files expected to change:** `src/shared/pricing.py`; possibly `src/shared/__init__.py`. **Requirements:** REQ-02, REQ-03, REQ-05, REQ-07. **Completion evidence:** static inspection shows exactly one `0.10` fee formula and one `round` in the new helper, taking `subtotal` as its only argument; the helper does not iterate lines. **Smallest check:** inspect `src/shared/pricing.py` and search fee expressions with `rg -n '0\.10|0\.12|calculate_service_fee' src` (the old caller expressions may still appear until Task 4). **Human review point:** accept the helper name/signature and package-file choice before wiring callers.

### 4. Route both public paths through the helper

- [ ] In `src/pricing.py`, keep `room_subtotal(rooms)` and `calculate_quote(rooms)` signatures; replace `calculate_quote`'s inline fee expression with `calculate_service_fee(subtotal)` ([pricing.py:3-9](../src/pricing.py#L3-L9)).
- [ ] In `src/invoice.py`, keep `preview_invoice(rooms)` and its subtotal expression; replace its second `rooms` traversal and 12% fee expression with `calculate_service_fee(subtotal)` ([invoice.py:3-7](../src/invoice.py#L3-L7)). Keep both result dictionaries and `api.create_quote(rooms)` unchanged ([api.py:4-7](../src/api.py#L4-L7)).

**Files expected to change:** `src/pricing.py`, `src/invoice.py`. **Requirements:** REQ-01 through REQ-07. **Completion evidence:** both source paths import/call the same helper with their aggregate subtotal; no 12% or second invoice traversal remains; public signatures and three response keys match the originals. **Smallest check after approval:** `python -m unittest tests.test_policy_pricing -v`, plus `rg -n 'calculate_service_fee|0\.12|0\.10|^def ' src`. The old invoice test is expected to fail until Task 5. **Human review point:** acknowledge the invoice's rate correction and reduced traversal of `rooms`; one-shot iterator support was not specified as an existing contract ([design](design.md#subtotal-placement-and-scope-decision)).

### 5. Replace the stale invoice assertion deliberately

- [ ] Update `test_legacy_invoice_example` to expect `{"subtotal": 200, "service_fee": 20, "total": 220}`; rename/reword it to express the approved invoice result. Retain the earlier `200/24/224` observation in the requirement/design/review evidence, rather than as a permanent acceptance assertion ([test_invoice.py:5-8](../tests/test_invoice.py#L5-L8), [requirement conflict](requirement.md#conflict-register)).

**Files expected to change:** `tests/test_invoice.py`. **Requirements:** REQ-02, REQ-03, REQ-04, REQ-07. **Completion evidence:** the diff shows an intentional `24 → 20` and `224 → 220` update with a policy explanation; the updated invoice test and policy tests pass. **Smallest check after approval:** `python -m unittest tests.test_invoice tests.test_policy_pricing -v`. **Human review point:** sign off on the changed historical expectation; the approved policy expressly takes precedence over stale tests ([root policy:14-16](../../../policy/business_rules.md#L14-L16)).

### 6. Prove the aggregate-rounding guard catches a regression

- [ ] After the correct tests pass, use a **disposable branch/copy** (or first have a reviewer approve a demonstration plan). Temporarily replace one caller's aggregate helper call with a sum of individually rounded 10% line fees. Do not alter the sole working copy. The helper accepts only `subtotal`, so the faulty per-line behavior must be demonstrated outside its contract ([design](design.md#test-plan-observed-behavior-versus-approved-behavior)).
- [ ] Run the two-line `5 + 5` test for that caller: document that the faulty version returns fee `0` and fails against expected fee `1`. Restore the correct code, rerun the same test successfully, and confirm no faulty diff remains.

**Files expected to change:** only temporary disposable-copy versions of `src/pricing.py` or `src/invoice.py`; no faulty change in the final working implementation. **Requirements:** REQ-02, REQ-03, REQ-07. **Completion evidence:** recorded failing assertion on the faulty copy, passing assertion after restoration, and final diff without per-line rounding. **Smallest check after approval:** `python -m unittest tests.test_policy_pricing -v` on the disposable copy and again on the restored implementation; inspect the temporary diff. **Human review point:** approve the disposable location/plan and inspect proof that the regression was removed. The brief explicitly requests a test that catches an introduced regression ([brief:23-24](../../../brief.md#L23-L24)).

### 7. Run final verification and inspect the change boundary

- [ ] Run the focused quote, invoice, baseline, and policy tests, then the repository's existing `unittest` discovery command. Record exact commands, outputs, failures, and final revision ([README:3-7](../README.md#L3-L7), [AGENTS.md:4-7](../AGENTS.md#L4-L7)).
- [ ] Inspect the complete final diff, including new files, to confirm both paths call the helper, signatures/keys remain stable, the old invoice assertion is intentionally updated, and cancellation/dependencies/unrelated files are untouched. Record residual risks: unsupported numeric/invalid inputs, external callers, and the unconfirmed iterator contract ([requirements:53-59](requirement.md#open-questions-for-review)).

**Files expected to change:** no new application files; implementation evidence/review record and checked task boxes only. **Requirements:** REQ-01 through REQ-07. **Completion evidence:** clean relevant suite, exact final diff review, and an explicit list of unresolved issues. **Smallest checks after approval:** `python -m unittest tests.test_quote tests.test_invoice tests.test_baseline_contracts tests.test_policy_pricing -v`, then `python -m unittest discover -s tests -v`; inspect `git diff -- src tests` and separately inspect any untracked new files. **Human review point:** review the final diff and test results before accepting the change.

### 8. Record the human decision

- [ ] Have the human reviewer record the revision reviewed, policy/requirement IDs, commands and results, regression demonstration, residual risks, and decision (`approve`, `request changes`, or `comment`) in the review record template ([review_record.md:1-23](../../../worksheets/review_record.md#L1-L23), [brief:25](../../../brief.md#L25)). Do not claim human approval merely because tests pass.

**Files expected to change:** `worksheets/review_record.md` at repository root, or another reviewer-chosen record; this task checklist may be checked off. **Requirements:** REQ-01 through REQ-07 as review scope. **Completion evidence:** named reviewer, revision, evidence, residual risk, and explicit decision. **Smallest static check:** open the completed review record and match its revision to the final diff/test evidence. **Human review point:** the reviewer makes and records the decision; any requested changes return to the relevant task and are reverified.

## Decisions required before implementation

1. Approve the proposed `calculate_service_fee(subtotal)` contract in `src/shared/pricing.py` and choose whether `src/shared/__init__.py` is needed ([design checklist](design.md#design-review-checklist)).
2. Accept keeping the existing subtotal expressions in their paths and the invoice's resulting single traversal of `rooms`; do not assert a broader one-shot iterator contract without evidence ([design](design.md#subtotal-placement-and-scope-decision)).
3. Approve the invoice behavior change from 12% to 10% and the corresponding `200/24/224 → 200/20/220` test update ([requirement conflict](requirement.md#conflict-register), [root policy:7-16](../../../policy/business_rules.md#L7-L16)).
4. Choose a disposable location or approve a concrete plan for the regression demonstration, and identify who will record the final review decision ([design](design.md#test-plan-observed-behavior-versus-approved-behavior), [review template](../../../worksheets/review_record.md#L1-L23)).

No source/test edit or application execution is part of creating this task list.
