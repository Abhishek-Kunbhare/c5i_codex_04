# Architecture and drift worksheet

## System context map
Draw modules as boxes and calls/data as arrows. Include external actors, entry points, shared components, and tests. Label each arrow with the function or data passed.

## Call trace
Start with `src/api.py:create_quote` and trace to the returned quote. Then trace `src/invoice.py:preview_invoice`. Record each hop.

| Flow step | File:symbol | Input | Transformation/side effect | Output | Test evidence |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Duplication and drift register
| Item | Evidence | Risk if changed | Confidence | Next safe check |
|---|---|---|---|---|
|  |  |  |  |  |

Use these labels:
- **Fact**: directly visible or reproduced.
- **Hypothesis**: plausible explanation needing evidence.
- **Question**: cannot safely decide from current materials.

## Blast-radius estimate
- Modules directly changed:
- Callers affected:
- Data contracts affected:
- Tests to run:
- Out-of-scope files to keep untouched:
