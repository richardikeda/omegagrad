# Phase 3 — spectral radar and extended geometry

English companion to the [original Portuguese execution report](REPORT.md). The [reference data](results.json) contain the full diagnostics.

## Protocol

The radar excludes 2 and 3 from the wave sum and scans width-0.98 cells centered on 6k±1. Energy is centered on the calibration-minimum mean. Energy and curvature ceilings use four quantiles, and fractional-distance cutoffs are 0.1, 0.25 and 0.49. Thresholds maximize F1 on small-base labels. Small-base primes cancel their own sine terms, creating a calibration distribution shift whose causal effect is unisolated. The 6-bit calibration gives an empty candidate set.

Survivors receive strong Miller–Rabin with base 2. One base can accept pseudoprimes. Field evaluation uses NumPy, while cell enumeration and root refinement retain scalar work. TensorValue was checked against analytical gradients and local second derivatives over 2048 independent coordinates.

## Filter and hybrid results

| Bits | Filter P | Filter R | Filter F1 | Hybrid P | Hybrid R | Hybrid F1 | FP before/after thresholds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/0 |
| 8 | 0.8667 | 0.5417 | 0.6667 | 1.0000 | 0.5417 | 0.7027 | 9/4 |
| 10 | 0.8197 | 0.6211 | 0.7067 | 1.0000 | 0.6211 | 0.7663 | 76/22 |
| 12 | 0.8512 | 0.5971 | 0.7018 | 1.0000 | 0.5971 | 0.7477 | 426/57 |
| 14 | 0.3786 | 0.6517 | 0.4790 | 0.9967 | 0.6517 | 0.7881 | 2071/1999 |
| 16 | 0.3183 | 0.6749 | 0.4326 | 0.9986 | 0.6749 | 0.8055 | 9379/9377 |
| 18 | 0.2810 | 0.6903 | 0.3994 | 0.9989 | 0.6903 | 0.8164 | 40820/40454 |

## Modular calls and recorded wall time

| Bits | Calls | Reduction vs all | Reduction vs 6k±1 | Radar s | Verifier s | Direct MR s |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 0 | 100.00% | 100.00% | 0.002626 | 0.000001 | 0.000044 |
| 8 | 30 | 87.29% | 62.03% | 0.011098 | 0.000024 | 0.000097 |
| 10 | 122 | 87.68% | 63.03% | 0.035063 | 0.000100 | 0.000484 |
| 12 | 383 | 90.50% | 71.50% | 0.157473 | 0.000356 | 0.002234 |
| 14 | 3217 | 80.21% | 40.62% | 0.732292 | 0.003169 | 0.010257 |
| 16 | 13756 | 78.92% | 36.77% | 3.044246 | 0.015230 | 0.045797 |
| 18 | 56263 | 78.50% | 35.48% | 14.187090 | 0.085695 | 0.242789 |

At 12 bits, the difference between 2211 phase-2 false positives and 57 phase-3 false positives combines a base change, phase restriction and filtering. The within-phase comparison is 426 to 57. The hybrid saves calls but takes longer than direct base-2 verification in the measured runs. Its recall inherits the primes lost by the filter.

## Extended geometry

Batched bisection checks central gap brackets and negative barrier curvature. Widths are normalized by mean adjacent prime gap. The model uses residual asymmetry, log absolute curvature and barrier displacement. Training uses the upper 70%, one embargo row and lower-region testing. The refined background uses 4097 global knots plus edge refinement and split integration. Initial results at 2049 knots are retained in the JSON.

| Bits | Test R² | MAE | Baseline MAE | Barriers | Missing brackets |
| --- | --- | --- | --- | --- | --- |
| 12 | 0.039780 | 2.872059 | 3.457788 | 563 | 0 |
| 14 | 0.121601 | 3.905009 | 4.587535 | 1899 | 0 |
| 16 | 0.184125 | 4.644964 | 5.499923 | 6541 | 0 |

| Bits A | Bits B | Descriptive KS |
| --- | --- | --- |
| 12 | 14 | 0.037545 |
| 14 | 16 | 0.028529 |

Positive test R² describes retrospective association. The full potential still contains the target primes. The recorded comparisons support finite-scale similarity and leave asymptotic invariance open.

See [benchmark CSV](summary.csv) and the [reproduction guide](../../docs/en/REPRODUCIBILITY.md).
