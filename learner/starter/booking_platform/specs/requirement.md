# Shared service-fee requirements

Status: **draft for human review**. Scope is the direct-booking quote and invoice-preview calculations exposed by `src.api.create_quote(rooms)` and `src.invoice.preview_invoice(rooms)` ([README](../README.md#L9), [business brief](../../../brief.md#L3-L15)). This document reconstructs requirements from the approved rule sheets, current code, and tests. It does not claim that the code currently satisfies every requirement.

## Scope and boundaries

The task is to consolidate the service-fee behavior used by the quote and invoice preview while preserving both public function names, their `rooms` argument, and their three response keys. The business brief excludes database, network, payment gateway, UI, dependency, and unrelated cleanup changes ([brief:13-15](../../../brief.md#L13-L15)); repository guidance also requires focused changes and preservation of public signatures and response keys ([AGENTS.md:3-8](../AGENTS.md#L3-L8)). Cancellation is outside this change.

## Evidence and confidence

**Approved policy** means the version 1.3 rule sheets state the intended behavior ([root policy:3-16](../../../policy/business_rules.md#L3-L16), [local policy:3-12](../policy/business_rules.md#L3-L12)). **Observed implementation** means source or an existing test records current behavior, which may conflict with policy. **Unresolved** means neither policy nor the public contract defines the answer. The [repository analysis](../../../docs/repository-analysis/05-api-and-data-contracts.md) was used as an investigation lead; the citations below point to policy, source, tests, or brief.

## Numbered requirements

| ID | Requirement | Current behavior | Intended behavior | Confidence and evidence |
|---|---|---|---|---|
| REQ-01 | For each room line, calculate its amount as `nightly_rate * nights * rooms`, using `1` when that line omits `rooms`; sum all line amounts for the room subtotal. | Both paths use this expression and the `rooms` field default of `1`. | Preserve this subtotal formula for both paths. | **Approved policy** for formula ([root policy:7-8](../../../policy/business_rules.md#L7-L8), [local policy:5-6](../policy/business_rules.md#L5-L6)); **observed implementation** for omitted-field default ([pricing.py:3-4](../src/pricing.py#L3-L4), [invoice.py:3-4](../src/invoice.py#L3-L4)). |
| REQ-02 | Calculate the direct-booking service fee as 10% of the **aggregate** room subtotal, after summing all lines. | Quote uses `round(subtotal * 0.10)`; invoice separately sums line amounts at `0.12` and rounds that sum. | Both paths calculate 10% from the same aggregate subtotal. | **Approved policy** ([root policy:7-10](../../../policy/business_rules.md#L7-L10), [local policy:5-8](../policy/business_rules.md#L5-L8)); current drift is **observed implementation** ([pricing.py:6-8](../src/pricing.py#L6-L8), [invoice.py:3-6](../src/invoice.py#L3-L6)). |
| REQ-03 | Round the calculated fee **once**, after applying 10% to the aggregate subtotal, using Python `round` to a whole currency unit. | Quote rounds once after its subtotal. Invoice rounds once after summing 12% line calculations; it does not use the approved rate. | Both paths round the same aggregate 10% calculation once; do not round each room line separately. | **Approved policy** ([root policy:10](../../../policy/business_rules.md#L10), [local policy:6-8](../policy/business_rules.md#L6-L8)); **observed implementation** ([pricing.py:8](../src/pricing.py#L8), [invoice.py:6](../src/invoice.py#L6)). |
| REQ-04 | Calculate `total = subtotal + service_fee`. | Both paths do so. | Preserve the same calculation. | **Approved policy** ([root policy:11](../../../policy/business_rules.md#L11), [local policy:9](../policy/business_rules.md#L9)); **observed implementation** ([pricing.py:9](../src/pricing.py#L9), [invoice.py:7](../src/invoice.py#L7)). |
| REQ-05 | A zero subtotal must have zero service fee. | Empty input produces a zero subtotal and fee by the current formulas; the baseline test checks zero subtotal/total and integer fee. | Both paths return zero subtotal, zero fee, and zero total for an empty room list. | **Approved policy** ([root policy:12](../../../policy/business_rules.md#L12), [local policy:9](../policy/business_rules.md#L9)); **observed implementation/test** ([pricing.py:3-9](../src/pricing.py#L3-L9), [invoice.py:3-7](../src/invoice.py#L3-L7), [test_baseline_contracts.py:6-10](../tests/test_baseline_contracts.py#L6-L10)). |
| REQ-06 | Preserve `create_quote(rooms)` and `preview_invoice(rooms)` as the public Python function signatures and preserve the returned keys `subtotal`, `service_fee`, `total`. | Both functions take one required `rooms` argument and return these keys. Quote explicitly copies all three pricing-result keys. | Names, argument shape, and keys remain stable across the focused refactor. | **Observed contract** ([api.py:4-7](../src/api.py#L4-L7), [invoice.py:3-7](../src/invoice.py#L3-L7), [test_quote.py:9-10](../tests/test_quote.py#L9-L10)); **scope direction** ([brief:13-15](../../../brief.md#L13-L15), [README:9](../README.md#L9)). |
| REQ-07 | Use one shared service-fee calculation for both public paths. | Quote calculates in `src.pricing`; invoice has a separate formula. | Both paths use one shared rule so they cannot retain different fee percentages or rounding points. | **Task requirement** ([brief:5-7](../../../brief.md#L5-L7), [brief:21-24](../../../brief.md#L21-L24)); **observed duplication** ([pricing.py:6-9](../src/pricing.py#L6-L9), [invoice.py:3-7](../src/invoice.py#L3-L7)). The helper's location/signature belongs in design, not this requirement. |

## Input and output contract

| Item | Verified contract or limit | Evidence |
|---|---|---|
| Function argument | Each public function has one required `rooms` parameter and no declared default or type annotation. | [api.py:4](../src/api.py#L4), [invoice.py:3](../src/invoice.py#L3) |
| Room line fields | `nightly_rate` and `nights` are accessed as required keys; per-line `rooms` is read with default `1`. The operators imply compatible numeric values and mapping-like room lines, but no validation/schema is declared. | [pricing.py:3-4](../src/pricing.py#L3-L4), [invoice.py:4-6](../src/invoice.py#L4-L6) |
| Response | Dictionary with `subtotal`, `service_fee`, and `total`. The fee is the result of `round` with no `ndigits` argument. | [api.py:6-7](../src/api.py#L6-L7), [pricing.py:8-9](../src/pricing.py#L8-L9), [invoice.py:6-7](../src/invoice.py#L6-L7) |
| Errors | No input validation or error handling is defined in these functions; missing keys or incompatible operands propagate Python exceptions. Exact accepted types and error contract are unresolved. | [api.py:4-7](../src/api.py#L4-L7), [pricing.py:3-9](../src/pricing.py#L3-L9), [invoice.py:3-7](../src/invoice.py#L3-L7) |

## Acceptance examples for the approved rule

These are expected results derived from the policy formula, **not test-run results**. Apply each fixture to both public functions and expect the same dictionary.

| Example | `rooms` input | Subtotal calculation | Expected `subtotal` / `service_fee` / `total` | Rule evidence |
|---|---|---|---|---|
| One line, omitted count | `[{"nightly_rate": 100, "nights": 2}]` | `100 * 2 * 1 = 200` | `200 / 20 / 220` | [policy:7-11](../../../policy/business_rules.md#L7-L11); quote example [test_quote.py:5-7](../tests/test_quote.py#L5-L7) |
| Multiple lines and explicit room count | `[{"nightly_rate": 100, "nights": 2, "rooms": 2}, {"nightly_rate": 50, "nights": 1}]` | `400 + 50 = 450` | `450 / 45 / 495` | [policy:7-11](../../../policy/business_rules.md#L7-L11); default in [pricing.py:4](../src/pricing.py#L4) |
| Aggregate-rounding edge | `[{"nightly_rate": 5, "nights": 1}, {"nightly_rate": 5, "nights": 1}]` | `5 + 5 = 10` | `10 / 1 / 11` | [policy:7-10](../../../policy/business_rules.md#L7-L10). This distinguishes `round(10 * .10) = 1` from rounding each line separately. |
| Zero subtotal | `[]` | `0` | `0 / 0 / 0` | [policy:11-12](../../../policy/business_rules.md#L11-L12), [test_baseline_contracts.py:6-10](../tests/test_baseline_contracts.py#L6-L10) |

## Conflict register

| Conflict | Current code/test evidence | Approved intent and disposition |
|---|---|---|
| Invoice rate differs from quote and policy. | Invoice applies `0.12` ([invoice.py:6](../src/invoice.py#L6)); the historical test expects fee `24` and total `224` on subtotal `200` and explicitly labels that expectation historical ([test_invoice.py:5-8](../tests/test_invoice.py#L5-L8)). Quote applies `0.10` and its analogous test expects `20` and `220` ([pricing.py:8](../src/pricing.py#L8), [test_quote.py:5-7](../tests/test_quote.py#L5-L7)). | Policy requires 10% for both paths ([root policy:7-10](../../../policy/business_rules.md#L7-L10)). The invoice test documents inherited behavior; it is **not** authority for intended policy, because the approved rule sheet explicitly says code/tests may be stale ([root policy:14-16](../../../policy/business_rules.md#L14-L16)). Preserve that distinction when later changing tests. |
| Fee logic is duplicated. | Quote calculates from `subtotal`; invoice calculates its own 12% fee inline ([pricing.py:6-9](../src/pricing.py#L6-L9), [invoice.py:3-7](../src/invoice.py#L3-L7)). | Task calls for one shared service-fee calculation ([brief:5-7](../../../brief.md#L5-L7), [brief:21-24](../../../brief.md#L21-L24)). The implementation approach belongs in design. |
| Cancellation boundary is stale, but outside this task. | Two helpers use `>= 24`; a test asserts that boundary ([pricing.py:11-15](../src/pricing.py#L11-L15), [rules.py:2-6](../src/rules.py#L2-L6), [test_rules.py:5-7](../tests/test_rules.py#L5-L7)). | Approved policy says 48 hours before local check-in ([root policy:18-20](../../../policy/business_rules.md#L18-L20)). Record as drift only; make no cancellation change under this service-fee requirement. |

## Open questions for review

| Question | Why unresolved | Decision needed before implementation? |
|---|---|---|
| Must `rooms` support one-shot iterators, or only reusable collections? | Invoice iterates the object twice ([invoice.py:4-6](../src/invoice.py#L4-L6)); no schema or test establishes iterator support. | Decide only if the proposed design changes iteration behavior; avoid claiming iterator support as an existing contract. |
| What numeric types, currency precision, negative values, and invalid-input errors are supported? | Source has arithmetic but no annotations or validation ([pricing.py:3-9](../src/pricing.py#L3-L9), [invoice.py:3-7](../src/invoice.py#L3-L7)); policy specifies only whole-unit fee rounding ([root policy:10](../../../policy/business_rules.md#L10)). | Do not expand validation or numeric behavior as part of this focused refactor without a separate requirement. |
| Are there production callers beyond the functions and tests in this repository? | README names public Python functions ([README:9](../README.md#L9)); this repository defines no route registration or external consumer ([api.py:1-7](../src/api.py#L1-L7)). | Review integration contracts if available before release; preserve the known signature/keys now. |

## Review gate

A human reviewer should confirm the policy citations, accept the intentional invoice behavior change from 12% to 10%, and resolve any open question that would change the design. This document authorizes no code or test change by itself ([brief:9-11](../../../brief.md#L9-L11)).
