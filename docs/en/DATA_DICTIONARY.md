# Data dictionary

**Richard Ikeda — Author & Lead Investigator**

| Artifact | Meaning |
|---|---|
| Phase-1 summary.csv | Horizon, epsilon, minima/barrier counts, coverage across seeds, root checks and elapsed time |
| Phase-1 gaps.csv | Consecutive prime pair, integer gap, barrier count/location, asymmetry and next-lower target gap |
| Phase-1 basins.csv | Minimum, associated nearest prime, integer displacement, limits, widths and curvature |
| stationary_points.csv | Coordinate, minimum/maximum classification, residual, Hessian, bracket width, local Newton error estimate |
| trajectory_seedN.csv | Iteration, coordinate, potential, gradient and descent/escape phase |
| Phase-2 results.json | Original/residual roots, paired regressions, blind candidates/minima, holdout targets and measured shifts |
| Phase-2 neighbor_changes.csv | Retained-prime association and before/after minimum location and Hessian |
| Phase-3 features.csv | Candidate integer n, stationary coordinate x, energy, Hessian and fractional distance |
| Phase-3 radar.json | Thresholds, candidates, raw phase-locked/filter/hybrid scores, modular counts and timings |
| Phase-3 geometry.json | Accepted barriers, missing brackets, relative widths, feature rows and regression metrics |
| Phase-3 results.json | Radar results, refined and initial geometry, KS distances, tensor validation and execution metadata |
| Phase-3 summary.csv | Filter/hybrid metrics, two modular-call baselines and wall times |

Normalized z and width_z are dimensionless; integer gaps and displacements use the original arithmetic scale. Epsilon is squared normalized distance in the logarithmic prime potential, while the harmonic wave uses its separately configured regularization.

JSON null and empty CSV cells represent missing or nonfinite values, not zero. `nearest_prime` is a descriptive association, not a navigation capture guarantee. Phase-3 feature rows are [log(lambda), log(abs(H)), displacement in integer units, next-lower integer gap]. Phase-2 joint feature rows use only the first two predictors.

Precision=TP/(TP+FP), recall=TP/(TP+FN), F1=2PR/(P+R), with zero assigned when the implementation has an empty denominator. R² uses the test-target mean in its variance denominator; it is not equivalent to beating the training-mean predictor on MAE. Empty calibration at 6 bits is recorded as failure, not perfect candidate reduction.

Stored seeds reproduce stochastic choices but do not make deterministic prime configurations independent statistical samples. Runtime ratios are descriptive measurements, and operation counts are not inferred from wall time.
