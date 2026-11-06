# Phase 1 — reference campaign

English companion to the [original Portuguese execution report](REPORT.md). The [reference data](results.json) contain the full diagnostics.

## Configuration and method

UTC run time: 2026-11-06T05:12:36.606801+00:00. Seeds: [0, 1, 2]. Backend: analytic.

The operational horizon is the largest prime at most 2**S_bits. The logarithmic potential sums log((z-p/P_omega)^2+epsilon), and the wave sums sin²(pi*x/p). Fixed epsilon is 1e-6. The scaled control is 1e-6*(61/P_omega)^2, preserving a smoothing width of 0.061 in integer units.

Root screening uses sign changes, Brent refinement and safeguarded Newton polishing. The grid doubles from 8 and 16 samples per smoothing width up to a maximum of 128. Agreement under refinement checks numerical stability. Degenerate roots may escape detection. Maxima bound the basins of the deterministic flow on [0,1].

OmegaSieve starts at z=1 with gradient, momentum, relative noise and backtracking. After convergence, external leftward transport crosses the barrier. Labels require rounding within 0.25 integer units and membership in the reference set. Coverage measures recovery of primes already encoded in the potential.

## Coverage and stationary points

| epsilon | Bits | Horizon | Primes | Minima | Barriers | Mean coverage |
| --- | --- | --- | --- | --- | --- | --- |
| fixed | 6 | 61 | 18 | 18 | 17 | 100.00% |
| scaled | 6 | 61 | 18 | 18 | 17 | 100.00% |
| fixed | 8 | 251 | 54 | 53 | 52 | 98.15% |
| scaled | 8 | 251 | 54 | 54 | 53 | 100.00% |
| fixed | 10 | 1021 | 172 | 110 | 109 | 43.02% |
| scaled | 10 | 1021 | 172 | 172 | 171 | 100.00% |
| fixed | 12 | 4093 | 564 | 74 | 73 | 2.84% |
| scaled | 12 | 4093 | 564 | 564 | 563 | 100.00% |

## Numerical diagnostics

- fixed S=6: maximum AD vs analytical gradient error=5.68e-14; maximum root residual=1.04e-10; estimate |L'/L''|=5.3e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- scaled S=6: maximum AD vs analytical gradient error=5.68e-14; maximum root residual=1.04e-10; estimate |L'/L''|=5.3e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- fixed S=8: maximum AD vs analytical gradient error=2.27e-13; maximum root residual=1.05e-10; estimate |L'/L''|=5.57e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- scaled S=8: maximum AD vs analytical gradient error=2.27e-13; maximum root residual=1.5e-09; estimate |L'/L''|=5.45e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- fixed S=10: maximum AD vs analytical gradient error=1.82e-12; maximum root residual=9.45e-11; estimate |L'/L''|=5.55e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- scaled S=10: maximum AD vs analytical gradient error=3.64e-12; maximum root residual=2.95e-08; estimate |L'/L''|=5.54e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- fixed S=12: maximum AD vs analytical gradient error=7.28e-12; maximum root residual=1.29e-10; estimate |L'/L''|=5.79e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.
- scaled S=12: maximum AD vs analytical gradient error=7.28e-11; maximum root residual=4.97e-07; estimate |L'/L''|=5.57e-17; grid stable=True; run status=lower_boundary;lower_boundary;lower_boundary.

## Barrier asymmetry and next lower gap

The regression uses log(lambda), where lambda is the ratio of distances from the barrier to its two bounding primes. Training uses the upper 70%, followed by a one-interval embargo and lower-region testing. Only gaps with one barrier qualify. The complete field still contains the targets, so scores describe a retrospective association.

| epsilon | Bits | Train/test | Spearman rho | Training-mean MAE | Fitted-gap MAE | log(lambda) MAE | log(lambda) R² |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fixed | 6 | 11/4 | 0.399 | 1.932 | 2.307 | 2.343 | -4.715 |
| scaled | 6 | 11/4 | 0.399 | 1.932 | 2.307 | 2.343 | -4.715 |
| fixed | 8 | 36/15 | -0.076 | 2.033 | 2.225 | 3.565 | -4.965 |
| scaled | 8 | 36/15 | -0.081 | 2.033 | 2.225 | 3.499 | -4.758 |
| fixed | 10 | 76/32 | -0.050 | 3.056 | 3.317 | 4.673 | -3.056 |
| scaled | 10 | 118/51 | -0.053 | 2.983 | 3.207 | 4.331 | -1.680 |
| fixed | 12 | 51/21 | 0.112 | 4.534 | 4.485 | 5.388 | -4.527 |
| scaled | 12 | 393/168 | -0.190 | 3.458 | 3.518 | 5.324 | -1.811 |

## Scale comparison

Widths are divided by the mean of adjacent gaps, excluding edge primes. KS is descriptive. The arithmetic mean of raw widths is the inverse of the number of basins when they partition [0,1].

| epsilon | Bits A/B | Median A | Median B | KS distance |
| --- | --- | --- | --- | --- |
| fixed | 6/8 | 1.011 | 1.022 | 0.226 |
| fixed | 8/10 | 1.022 | 1.019 | 0.317 |
| fixed | 10/12 | 1.019 | 6.965 | 0.576 |
| scaled | 6/8 | 1.011 | 1.012 | 0.188 |
| scaled | 8/10 | 1.012 | 1.020 | 0.060 |
| scaled | 10/12 | 1.020 | 1.022 | 0.070 |

## Interpretation and artifacts

Other terms can shift a minimum away from its prime. Fixed smoothing grows in integer units as the horizon increases and can merge wells. Maxima are one-dimensional barriers. The zeros of W are common multiples of the base, including zero. Each full-field evaluation is linear in the number of known primes. These observations support finite comparisons. A test of blind prediction needs observables built without the hidden targets.

See [summary.csv](summary.csv), [scale comparisons](scale_comparisons.csv) and the per-universe directories for stationary roots, basins, gaps, predictions and trajectories. The [reproduction guide](../../docs/en/REPRODUCIBILITY.md) lists commands and checkpoints.
