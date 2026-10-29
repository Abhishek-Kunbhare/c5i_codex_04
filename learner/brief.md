# Business brief

You have joined a team that owns an existing booking platform. Customers can book rooms through the booking flow. An invoice service also calculates totals. The platform has grown over time, some documentation is old, and two modules contain similar fee logic.

## Your assignment

Understand the existing system before changing it. Produce an architecture/call map, identify duplication and drift, reconstruct one module's requirements from available evidence, add characterization tests, and make one guarded refactor that consolidates shared service-fee behavior.

## Learning objective

Demonstrate that Codex can accelerate repository-scale investigation and careful maintenance when given useful scope and evidence requirements. Demonstrate that the human remains responsible for separating observed behavior from intended behavior, validating reconstructed rules, controlling blast radius, and reviewing changes.

## Scope boundary

Only refactor the shared service-fee calculation used by the booking quote and invoice preview. Preserve public function names and return shape unless the design note approves a change. No database, network, payment gateway, UI, dependency, or unrelated cleanup changes.

## Completion evidence

- Architecture map identifies entry points, modules, call paths, data transformations, and tests.
- Drift/risk note distinguishes verified facts, hypotheses, and questions.
- Requirement note cites policy/test/code evidence and marks confidence.
- Characterization tests capture useful current behavior without blessing a policy conflict.
- One focused refactor routes both paths through one shared calculation.
- Tests demonstrate the intended rule and catch an introduced regression.
- Human reviewer records the revision, evidence, residual risk, and decision.
