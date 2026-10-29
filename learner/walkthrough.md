# Codex walkthrough prompts

Run each stage in order. Pause after each answer and compare it with source files. Use the CLI, IDE, or Codex desktop app. In the IDE, explicitly add the named files or selected code to the conversation; open tabs alone are not reliable context.

## Stage 1: read-only reconnaissance

> I am onboarding to this unfamiliar booking codebase. Do not edit files. First inspect the repository guidance and test layout, then map the public entry points and the modules they call for quote creation and invoice preview. Return: (1) a text architecture diagram, (2) one call trace for each flow with file paths and function names, (3) duplicated or suspiciously similar logic, (4) what you could not verify, and (5) the smallest next inspection step. Label each statement as verified fact, hypothesis, or open question. Do not infer business policy from function names or comments.

Human check: open every cited file and confirm each arrow. If Codex names a call that is absent, ask it to correct the map and show the evidence.

## Stage 2: dependency and data-flow trace

> Trace how room data moves from `src/api.py:create_quote` to the response, and how invoice preview calculates its total. Do not edit. For every step name the input fields, transformation, function, and returned fields. Identify all callers of each fee helper and report search scope. Distinguish direct call evidence from inference.

Human check: search call sites independently and verify the response shape in tests.

## Stage 3: drift and risk review

> Compare the two fee calculations and `policy/business_rules.md`. Do not edit. List exact disagreements, affected user flows, likely blast radius, tests that currently cover the behavior, and missing tests. Separate policy-backed defects from style concerns. Do not say two implementations are equivalent unless you compare their formulas and rounding points with examples.

Human check: use the supplied rule sheet as intended policy; record code/test divergence rather than quietly treating old tests as policy.

## Stage 4: reconstruct requirements

> Draft a short requirement note for the pricing module using only `policy/business_rules.md`, existing code, and tests. For each requirement, cite the evidence source and confidence. Put conflicts in a separate table. Do not fill gaps with assumptions. Include examples for one room, multiple rooms, rounding, and zero subtotal. Do not edit product code.

Human check: verify each rule against the approved policy and actual test assertions. Codex's explanation is not itself evidence.

## Stage 5: characterize behavior before changing it

> Propose characterization tests for the current booking quote and invoice preview behavior. Do not edit yet. Identify which current behaviors match the approved rule and which encode drift. For drift, propose a test that documents the mismatch without blessing it as desired policy, then propose the acceptance test for the approved behavior. Explain which existing assertions would need an intentional update and why.

Human check: learners decide which assertions are compatibility contracts and which need a policy-approved correction.

## Stage 6: guarded refactor

> Refactor only the duplicated service-fee calculation used by quote and invoice preview into `src/shared/pricing.py`. Follow `policy/business_rules.md`: sum room lines first, calculate 10% once on the subtotal, then round once using the stated rule. Preserve the public `create_quote` and `preview_invoice` signatures and response keys. Do not alter cancellation logic, storage, routes, dependencies, or unrelated formatting. First show a short plan and expected files; wait for review before editing. After approval, implement the smallest change, add focused tests for both callers, run the smallest relevant suite, and report exact commands, results, files changed, and remaining uncertainty.

Human check: inspect the plan and ensure that the business rule is not applied per line or per room.

## Stage 7: compare the explanation with source

> Explain the service-fee behavior after the refactor. Cite the implementation and test evidence for: aggregation point, rate, rounding point, and zero-subtotal behavior. Also inspect cancellation policy. If code comments, tests, and the approved rule sheet disagree, show the disagreement and state which source controls the training policy. Do not infer a cancellation window from a comment alone.

Human check: look for the planted false claim challenge in the instructor packet only after learners have committed their evidence-based answer.
