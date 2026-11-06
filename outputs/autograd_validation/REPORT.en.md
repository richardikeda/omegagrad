# Phase 1 — scalar autograd navigation check

English companion to the [original Portuguese execution report](REPORT.md). The [reference data](results.json) contain the full diagnostics.

## Configuration and method

UTC run time: 2026-11-06T05:11:47.323060+00:00. Seeds: [0]. Backend: autograd.

The operational horizon is the largest prime at most 2**S_bits. The logarithmic potential sums log((z-p/P_omega)^2+epsilon), and the wave sums sin²(pi*x/p). Fixed epsilon is 1e-6. The scaled control is 1e-6*(61/P_omega)^2, preserving a smoothing width of 0.061 in integer units.

Root screening uses sign changes, Brent refinement and safeguarded Newton polishing. The grid doubles from 8 and 16 samples per smoothing width up to a maximum of 128. Agreement under refinement checks numerical stability. Degenerate roots may escape detection. Maxima bound the basins of the deterministic flow on [0,1].

OmegaSieve starts at z=1 with gradient, momentum, relative noise and backtracking. After convergence, external leftward transport crosses the barrier. Labels require rounding within 0.25 integer units and membership in the reference set. Coverage measures recovery of primes already encoded in the potential.

## Coverage and stationary points

| epsilon | Bits | Horizon | Primes | Minima | Barriers | Mean coverage |
| --- | --- | --- | --- | --- | --- | --- |
| fixed | 6 | 61 | 18 | 18 | 17 | 100.00% |

## Numerical diagnostics

- fixed S=6: maximum AD vs analytical gradient error=5.68e-14; maximum root residual=1.04e-10; estimate |L'/L''|=5.3e-17; grid stable=True; run status=lower_boundary.

## Barrier asymmetry and next lower gap

The regression uses log(lambda), where lambda is the ratio of distances from the barrier to its two bounding primes. Training uses the upper 70%, followed by a one-interval embargo and lower-region testing. Only gaps with one barrier qualify. The complete field still contains the targets, so scores describe a retrospective association.

| epsilon | Bits | Train/test | Spearman rho | Training-mean MAE | Fitted-gap MAE | log(lambda) MAE | log(lambda) R² |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fixed | 6 | 11/4 | 0.399 | 1.932 | 2.307 | 2.343 | -4.715 |

## Scale comparison

This run uses a single scale and smoothing policy, so it provides no cross-scale comparison.

## Interpretation and artifacts

Other terms can shift a minimum away from its prime. Fixed smoothing grows in integer units as the horizon increases and can merge wells. Maxima are one-dimensional barriers. The zeros of W are common multiples of the base, including zero. Each full-field evaluation is linear in the number of known primes. These observations support finite comparisons. A test of blind prediction needs observables built without the hidden targets.

See [summary.csv](summary.csv) and the per-universe directories for stationary roots, basins, gaps, predictions and trajectories. The [reproduction guide](../../docs/en/REPRODUCIBILITY.md) lists commands and checkpoints.
