# Function and argument inventory

All six production functions are listed. Types below are **inferred from operations**, because source has no annotations or runtime validation. No function declares a default parameter. “Caller” means an in-repository caller; external consumers are unknown. Full call edges are in [call graph](04-function-call-graph.md).

| Function / source | Purpose | Inputs, types, defaults | Calls / in-repo caller | Return / output | Errors and side effects |
|---|---|---|---|---|---|
| [`api.create_quote`](../../starter/booking_platform/src/api.py#L4-L7) | Produce quote response body | `rooms`: iterable of mapping-like room lines; required, no default | Calls `pricing.calculate_quote`; called by `test_quote` and `test_baseline_contracts` ([tests](../../starter/booking_platform/tests/test_quote.py#L2-L10)) | `dict` with `subtotal`, `service_fee`, `total` copied from pricing result | No handler; propagates pricing errors or `KeyError` if result keys absent. No storage/network/state change. |
| [`pricing.room_subtotal`](../../starter/booking_platform/src/pricing.py#L3-L4) | Sum room line amounts | `rooms`: iterable; each line needs numeric `nightly_rate`, `nights`; optional numeric `rooms` multiplicity defaults to `1` | Calls built-in `sum`, mapping `get`; called by `calculate_quote` | Numeric sum; empty iterable yields integer `0` | Missing required keys can raise `KeyError`; bad mapping/operands can raise `TypeError`; arithmetic may raise other operand-defined exceptions. No external side effect; consumes iterator. |
| [`pricing.calculate_quote`](../../starter/booking_platform/src/pricing.py#L6-L9) | Compute quote subtotal, 10% fee, total | `rooms`: same shape as `room_subtotal`; required | Calls `room_subtotal`, built-in `round`; called by `api.create_quote` | `dict` with numeric subtotal/total and `round` result as fee | No handler; propagates input/arithmetic errors. No external side effect. |
| [`pricing.cancellation_fee`](../../starter/booking_platform/src/pricing.py#L11-L15) | Legacy 24-hour cancellation fee calculation | `hours_before_checkin`: comparable number; `booking_total`: numeric; both required | Calls built-in `round` below threshold; no in-repo caller found | `0` when hours ≥ 24; otherwise `round(booking_total * 0.50)` | No handler; incompatible inputs can raise `TypeError` or operand-defined exceptions. No external side effect. |
| [`invoice.preview_invoice`](../../starter/booking_platform/src/invoice.py#L3-L7) | Compute invoice preview using its own subtotal and 12% fee | `rooms`: re-iterable collection of mapping-like room lines; same required/optional fields; no parameter default | Calls built-ins `sum`, `round`; called by `test_invoice`, `test_baseline_contracts` | `dict` with `subtotal`, `service_fee`, `total` | No handler; same key/type risks as subtotal. Iterates `rooms` twice, so a one-shot iterator can yield a wrong fee. No external side effect beyond consuming input. |
| [`rules.cancellation_fee_due`](../../starter/booking_platform/src/rules.py#L2-L6) | Separate legacy 24-hour cancellation fee helper | `hours_before_checkin`: comparable number; `booking_total`: numeric; both required | Calls built-in `round` below threshold; called by `test_rules` | `0` when hours ≥ 24; otherwise `round(booking_total * 0.50)` | No handler; incompatible inputs can raise `TypeError` or operand-defined exceptions. No external side effect. |

## Test methods as callers

| Test method | Calls / assertion | Evidence |
|---|---|---|
| `QuoteTests.test_one_room_quote` | `create_quote`, exact one-room result | [`test_quote.py:5-7`](../../starter/booking_platform/tests/test_quote.py#L5-L7) |
| `QuoteTests.test_quote_response_keys` | `create_quote([])`, key set | [`test_quote.py:9-10`](../../starter/booking_platform/tests/test_quote.py#L9-L10) |
| `InvoiceTests.test_legacy_invoice_example` | `preview_invoice`, historical 12% result | [`test_invoice.py:5-8`](../../starter/booking_platform/tests/test_invoice.py#L5-L8) |
| `BaselineContracts.test_empty_inputs_preserve_numeric_shape` | Both public functions with empty lists | [`test_baseline_contracts.py:6-10`](../../starter/booking_platform/tests/test_baseline_contracts.py#L6-L10) |
| `RuleTests.test_legacy_cancellation_boundary` | `cancellation_fee_due` at 24 and 23 hours | [`test_rules.py:5-7`](../../starter/booking_platform/tests/test_rules.py#L5-L7) |

No classes or API handlers are defined in production source; test classes inherit `unittest.TestCase` ([test_quote.py:1-4](../../starter/booking_platform/tests/test_quote.py#L1-L4)).
