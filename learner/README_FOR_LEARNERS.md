# Learner route

1. Read `policy/business_rules.md` and `brief.md`.
2. Complete `worksheets/reconnaissance.md` before requesting code changes.
3. Use `walkthrough.md` to issue read-only Codex prompts in stages.
4. Complete `worksheets/architecture_and_drift.md` and `worksheets/reconstructed_requirements.md`.
5. Baseline the existing tests. Add characterization tests around the current code, marking which behavior is supported by policy and which is merely observed.
6. Propose one small refactor plan. Do not change behavior outside the chosen rule.
7. Ask Codex to consolidate duplicate fee calculation into the shared component. Inspect the plan and diff; run the relevant tests.
8. Use `worksheets/review_record.md` to record evidence, risks, and human approval.

## Context discipline

For every Codex prompt, state the goal, identify the specific files or directories to inspect, request evidence with paths/symbols, say whether edits are allowed, and name what Codex must not assume. Re-open the source and verify the claims yourself.
