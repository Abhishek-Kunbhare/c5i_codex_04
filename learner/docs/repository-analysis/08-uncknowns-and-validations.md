# Unknowns and validations

This analysis is static. No application code or tests were executed; no packages were installed. Statements about formulas and calls are source observations, while example outputs are static arithmetic or existing test assertions. See [architecture](01-architecture-overview.md) and [contracts](05-api-and-data-contracts.md).

| Question / unknown | Why it remains unknown | Validation needed |
|---|---|---|
| Actual HTTP route, server, deployment entry, and external callers | `api.py` describes an HTTP-facing function but defines no route/server ([api.py:1-7](../../starter/booking_platform/src/api.py#L1-L7)); README only names Python functions ([README:9](../../starter/booking_platform/README.md#L9)). | Inspect deployment/integration repository or service runtime. |
| Runtime Python version and installed library versions | No dependency or interpreter version manifest found; tests use `unittest` ([test_quote.py:1](../../starter/booking_platform/tests/test_quote.py#L1)). | Inspect runtime/build configuration. |
| Database, external API, and background processes in deployed system | No such implementation appears in application source ([module map](02-module-dependency.md)). | Inspect deployment configuration or other services, if any. |
| Real input validation, serialization, currency precision, negative-value behavior | Public functions accept unannotated `rooms` and do arithmetic directly ([pricing.py:3-9](../../starter/booking_platform/src/pricing.py#L3-L9), [invoice.py:3-7](../../starter/booking_platform/src/invoice.py#L3-L7)). | Obtain external contract or run focused inputs in an approved test session. |
| Whether one-shot iterators are supported | Invoice iterates `rooms` twice ([invoice.py:4-6](../../starter/booking_platform/src/invoice.py#L4-L6)); no input type contract or test states iterator support. | Define accepted input type; add focused test if supported. |
| Cancellation timestamp/time-zone processing | Helpers receive only hours and total, and use a 24-hour threshold ([pricing.py:11-15](../../starter/booking_platform/src/pricing.py#L11-L15), [rules.py:2-6](../../starter/booking_platform/src/rules.py#L2-L6)); approved policy requires 48 hours in property local time ([policy:18-20](../../policy/business_rules.md#L18-L20)). | Find upstream calculation/owner and test boundary/time-zone cases. |
| Executed baseline and coverage percentage | Tests were inspected, not run, per task constraint against executing application code without approval. | Run `python -m unittest discover -s tests -v` from `starter/booking_platform` only after approval; use coverage tooling only if already available/approved. |

## Assumptions and boundaries

No production relationship beyond visible imports/calls is assumed. “Python numeric” and “mapping-like” describe operations required by code, not a validated schema. The five flows in [execution flow](06-execution-flow.md) are invocation scenarios visible in tests and source, not claims that five deployed user journeys exist. A repository-wide file inventory and source/test searches found no environment-variable reads, dependency manifests, DB adapters, network clients, or job definitions; absence from this repository does not establish absence from a larger deployment.

## Static validation performed

Inspected all tracked-looking files listed by `rg --files`, the four source modules, four test modules, both policy sheets, README/guidance, and searched for imports, call sites, environment access, database/network/job keywords, and common configuration/dependency filenames. Source paths and line references throughout the documents are the evidence trail. No live behavior was verified.
