# Facilitator activity: inject a refactor regression

After the shared helper exists and the correct acceptance tests pass, demonstrate a faulty alternative: calculate and round the 10% fee independently for each room line, then add the rounded fees. Keep the approved rule's “sum first, round once” contract.

Choose a fixture that differentiates the behaviors, such as two room lines with subtotal 5 each: round(0.5) + round(0.5) = 0 + 0 under Python's ties-to-even behavior, while round(10 × 0.10) = 1. Use the rule sheet and actual runtime semantics. Learners should first predict, then add/run a test, observe the failure, and restore the correct aggregate calculation.

Do not make this alteration in a learner's only copy. Use a disposable branch or ask Codex to show the proposed bad change without applying it, then apply it only in the disposable demo copy.
