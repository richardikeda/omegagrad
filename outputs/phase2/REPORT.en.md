# Phase 2 — continuum detrending and blind wave

English companion to the [original Portuguese execution report](REPORT.md). The [reference data](results.json) contain the full diagnostics.

## Protocol

The background integrates the logarithmic kernel against the continuum density P/log(uP). Cubic spline interpolation uses 2049 global knots and edge refinement. Gradient sensitivity is measured against 1025 global knots.

The paired regression compares log(lambda) and log(abs(H)) on intervals with one barrier before and after subtraction. Training uses the upper 70%, one embargo row and the lower region for testing. The full potential encodes the targets.

The wave scanner receives the horizon and base primes up to its square root. It brackets gradient sign changes in descending order and refines minima with Brent. Rounded coordinates are scored by a separate evaluator. No modular filter is applied. Steps of 0.05 and 0.025 check candidate stability. The horizon is supplied.

## Blind-wave results

| Bits | Horizon | Precision | Recall | F1 | TP | FP | FN | Stable candidates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 61 | 0.3611 | 0.9286 | 0.5200 | 13 | 23 | 1 | True |
| 8 | 251 | 0.3038 | 1.0000 | 0.4660 | 48 | 110 | 0 | True |
| 10 | 1021 | 0.2355 | 0.9814 | 0.3798 | 158 | 513 | 3 | True |
| 12 | 4093 | 0.1951 | 0.9817 | 0.3255 | 536 | 2211 | 10 | True |

## Paired regression and background sensitivity

| Bits | Before MAE | Before R² | After MAE | After R² | Baseline MAE | Train/test | Gradient sensitivity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 2.5747 | -5.7099 | 1.6778 | -1.7412 | 1.9318 | 11/4 | 0.000742922 |
| 8 | 3.5802 | -5.0175 | 1.9832 | -0.9590 | 2.0333 | 36/15 | 0.00389996 |
| 10 | 4.3860 | -1.7359 | 2.7106 | -0.1737 | 2.9831 | 118/51 | 0.0237357 |
| 12 | 5.3309 | -1.8164 | 3.0214 | -0.0435 | 3.4578 | 393/168 | 0.0232745 |

## Internal-prime removal

Seed 42 removes approximately 10% of internal primes. The midpoint rule proposes coordinates from retained gaps above twice their median. Root shifts and Hessians are stored separately as retrospective diagnostics.

| Bits | Removed | Exact hits | False positives | Missed | F1 |
| --- | --- | --- | --- | --- | --- |
| 6 | 2 | 0 | 0 | 2 | 0.0000 |
| 8 | 5 | 0 | 8 | 5 | 0.0000 |
| 10 | 17 | 0 | 14 | 17 | 0.0000 |
| 12 | 56 | 0 | 79 | 56 | 0.0000 |

The residual model reduces MAE against the training mean at every tested scale while test R² remains negative. Rounded wave minima give high recall with many false positives. The midpoint rule yields zero exact recoveries across the four configurations.

Run `python -m omegagrad.phase2` in a reproduction clone. It writes to the reference output directory.
