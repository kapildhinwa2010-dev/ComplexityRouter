# ComplexityRouter

ComplexityRouter is a small Python library for routing numeric vectors to registered expert entries using a heuristic complexity score. The current implementation is version `0.1.0`; it provides the scoring and selection logic, but does not connect to or execute external models.

## What it implements

- `complexity_score(vector)` converts its input to a flattened `float64` NumPy array and combines its L2 norm with the normalized entropy of the absolute-value distribution.
- `ComplexityRouter.add_expert(name, capacity, cost=1.0)` registers an expert with a score capacity and a caller-supplied cost.
- `ComplexityRouter.route(vector)` selects an expert whose capacity covers the score, choosing the lowest cost and then the lower capacity as a tie-breaker. It returns the `Expert` object.
- `ComplexityRouter.route_and_handle(vector)` applies the selected expert's local handler. That handler only increments a call counter and returns a text string; it does not run a model or process the vector.
- `usage_report()` returns per-expert call counts.

Empty vectors, missing registered experts, and vectors for which no expert has sufficient capacity raise `ValueError`.

## Requirements and installation

The package metadata requires Python 3.9 or later and NumPy 1.24 or later. Install the project from its source directory with:

```bash
python -m pip install .
```

To install the development/test dependencies listed by this repository instead:

```bash
python -m pip install -r requirements.txt
```

## Example

```python
import numpy as np
from complexityrouter import ComplexityRouter

router = ComplexityRouter()
router.add_expert("small", capacity=1.0, cost=0.1)
router.add_expert("large", capacity=100.0, cost=10.0)

vector = np.array([0.1, 0.1, 0.1, 0.1])
selected = router.route(vector)
print(selected.name)

result = router.route_and_handle(vector)
print(result)  # For example: "handled by small"
print(router.usage_report())
```

Capacities and costs are user-provided values; the library does not estimate real model cost or validate capacity against model capabilities.

## Tests and CI

On the repository's cloned commit `3b11fad6c04bed49bc7a17ed758fd4e911fea9e0`, `python3 -m pytest -q` was run locally with Python 3.12.3 and completed with **12 passed**. The repository's GitHub Actions CI workflow is configured to run tests and a compile/import smoke check on Python 3.10, 3.11, and 3.12. This README draft does not assert the status of any hosted workflow run.

Run the tests with:

```bash
python -m pytest -q
```

## Scope and limitations

This is a minimal routing primitive, not a model-serving system. Experts are in-memory objects with a capacity, a cost, and a counter; there are no model adapters, network calls, persistence, configuration files, or adaptive routing. The score is a heuristic based on vector magnitude and the entropy of normalized absolute values, not a validated measure of task difficulty or resource use. A nonzero vector with only one element also encounters a zero `log(vector.size)` denominator in the entropy calculation; single-element nonzero inputs are therefore not safely supported by the current scoring implementation. No benchmark or performance measurements are included in the repository.

## License

The repository includes an MIT License. See [LICENSE](LICENSE) for its terms and copyright notice.
