# API and data contracts

These are Python function contracts visible in source, not HTTP endpoint contracts. No route, request parser, status code, serialization layer, or schema is defined ([api.py:1-7](../../starter/booking_platform/src/api.py#L1-L7)).

| Contract | Current implementation | Evidence / status |
|---|---|---|
| Quote entry | `create_quote(rooms)` returns exactly `subtotal`, `service_fee`, `total`; it copies those keys from `calculate_quote` | [`api.py:4-7`](../../starter/booking_platform/src/api.py#L4-L7), [`test_quote.py:9-10`](../../starter/booking_platform/tests/test_quote.py#L9-L10) — verified |
| Invoice entry | `preview_invoice(rooms)` returns same three keys | [`invoice.py:3-7`](../../starter/booking_platform/src/invoice.py#L3-L7) — verified |
| Room line | Required `nightly_rate`, `nights`; optional `rooms`, default `1`. Arithmetic expects compatible numeric values | [`pricing.py:3-4`](../../starter/booking_platform/src/pricing.py#L3-L4), [`invoice.py:4-6`](../../starter/booking_platform/src/invoice.py#L4-L6) — inferred type, verified keys/default |
| Quote fee | `round(subtotal * 0.10)` after room subtotal is summed | [`pricing.py:6-9`](../../starter/booking_platform/src/pricing.py#L6-L9) — verified |
| Invoice fee | `round(sum(each line amount * 0.12))`; input iterated twice | [`invoice.py:4-7`](../../starter/booking_platform/src/invoice.py#L4-L7) — verified |
| Empty list | Both calculate zero subtotal, zero fee, zero total from formulas; test asserts subtotal/total zero and integer fee | [`pricing.py:3-9`](../../starter/booking_platform/src/pricing.py#L3-L9), [`invoice.py:3-7`](../../starter/booking_platform/src/invoice.py#L3-L7), [`test_baseline_contracts.py:6-10`](../../starter/booking_platform/tests/test_baseline_contracts.py#L6-L10) — verified by static derivation and asserted shape; tests not run here |
| Error response | No validation or `try/except` in either public function | [`api.py:4-7`](../../starter/booking_platform/src/api.py#L4-L7), [`invoice.py:3-7`](../../starter/booking_platform/src/invoice.py#L3-L7) — verified; exact exception depends on input |

## Policy comparison

Approved policy specifies line subtotal = `nightly_rate × nights × rooms`, service fee = 10% of **aggregate** subtotal, `round` once, and total = subtotal + fee ([root policy:5-12](../../policy/business_rules.md#L5-L12)). Quote implements that formula; invoice's 12% conflicts ([invoice.py:6](../../starter/booking_platform/src/invoice.py#L6)). For a 200 subtotal, quote returns fee 20 and invoice fee 24; both examples are encoded in tests ([test_quote.py:5-7](../../starter/booking_platform/tests/test_quote.py#L5-L7), [test_invoice.py:5-8](../../starter/booking_platform/tests/test_invoice.py#L5-L8)). This is a code/policy conflict, not an assumption about a live service.

Cancellation policy is 48 hours before **local check-in**, measured in the property's local time zone ([root policy:18-20](../../policy/business_rules.md#L18-L20)). Both helpers use a numeric `hours_before_checkin >= 24` comparison and do not receive a time zone or check-in timestamp ([pricing.py:11-15](../../starter/booking_platform/src/pricing.py#L11-L15), [rules.py:2-6](../../starter/booking_platform/src/rules.py#L2-L6)). Their 24-hour behavior is historical implementation, not approved policy.

No currency type, decimal precision, negative-value rule, allowed input schema, or externally published HTTP contract is specified in source or policy. See [unknowns](08-uncknowns-and-validations.md).
