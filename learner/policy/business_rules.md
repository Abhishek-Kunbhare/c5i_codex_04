# Approved business rule sheet

Version: 1.3 | Owner: Booking Product Operations | Status: approved for this training exercise

## Pricing rules

1. A direct booking has a service fee equal to **10% of the room subtotal**, calculated once after summing all room lines.
2. Room subtotal is the sum of `nightly_rate × nights × rooms` for each room line.
3. The displayed quote and the invoice preview use the same service-fee rule.
4. The fee is rounded to the nearest whole currency unit using Python's `round` behavior for this exercise. This rule applies after calculating 10% of the total room subtotal.
5. The grand total equals room subtotal plus service fee.
6. There is no service fee on a zero subtotal.

## Evidence interpretation

This sheet is the approved source of business intent for service-fee policy in this exercise. Existing code and tests are evidence of current behavior; they may be stale or may encode historical defects. If they conflict with this sheet, record the conflict and follow the sheet for the approved refactor, while preserving a note about behavior change.

## Cancellation rule (used for the confidence challenge)

A direct booking may be cancelled without penalty up to **48 hours before local check-in**. The policy is measured in the property's local time zone. If the booking is within 48 hours of check-in, the standard cancellation fee applies. Do not infer a different window from an old code comment or a generated explanation.
