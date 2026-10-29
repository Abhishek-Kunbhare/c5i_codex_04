# Approved business rule sheet

Version: 1.3 | Owner: Booking Product Operations | Status: approved for this training exercise

- Direct-booking service fee is 10% of the total room subtotal.
- First compute each line as nightly rate × nights × rooms; sum all lines; calculate the fee once on the aggregate subtotal.
- Quote and invoice preview use identical pricing policy.
- Round the fee once to the nearest whole currency unit using Python `round` for the exercise.
- Grand total = subtotal + fee. Zero subtotal means zero fee.
- Cancellation without penalty is allowed until 48 hours before local check-in. The property's local timezone governs this rule.

This document is intended policy for the exercise. Code and tests are evidence of implementation and historical expectations; they can be stale. Record conflicts explicitly.
