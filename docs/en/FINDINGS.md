# Consolidated findings

**Richard Ikeda — Author & Lead Investigator**

## H1: smoothing and topology

With fixed epsilon, minima counts were 18,53,110,74 against prime counts 18,54,172,564. With scaled epsilon, all prime-associated wells were retained in the tested 6–12-bit configurations and all reference primes were recovered by controlled navigation. The inverse-square relationship preserves smoothing width in integer coordinates by definition; preservation of all wells beyond these tests is not established.

## H2: residual geometry

The phase-2 joint two-feature regression improved MAE against the training-mean baseline but retained negative test R². In phase 3, adding barrier displacement produced R² of 0.0398,0.1216,0.1841 at 12,14,16 bits. At 16 bits MAE was 4.6450 against 5.4999. These are retrospective associations, because the complete potential contains the target primes.

Residual-basin KS distances were 0.0375 (12/14 bits) and 0.0285 (14/16). This finite sequence supports descriptive similarity, not proven convergence or universality.

## H3: blind candidates and verification

In 12 bits the phase-2 wave produced 536 true positives, 2211 false positives and 10 false negatives. Phase-3 phase restriction plus filtering produced 326 true positives, 57 false positives and 220 false negatives. False-positive counts fell by 97.42%, while recall fell from 98.17% to 59.71%. Since the phase restriction and base changed, this reduction cannot be attributed solely to energy/curvature thresholds. The phase-locked pre/post-threshold comparison is the relevant within-pipeline ablation.

At 16 bits the hybrid achieved 99.86% precision and 67.49% recall; at 18 bits, 99.89% and 69.03%. Strong pseudoprimes survived the one-base verifier. The hybrid cost about 66.8 times direct MR at 16 bits and 58.8 times at 18; smaller nonempty configurations ranged up to 114.4 times. Reduced modular-call counts therefore did not translate to an observed speed benefit.

## Removal test and derivative validation

The simple retained-gap midpoint heuristic recovered no removed prime exactly in the four phase-2 scales. This limits that rule, not all possible inverse models.

The largest measured scalar-AD gradient difference was 7.28e-11. The 2048-coordinate tensor check had gradient difference 2.05e-12 and second-derivative difference 1.40e-9. The statement “all errors below 1e-10” would be inaccurate.

The [paper](PAPER.md) includes full tables, provenance and limitations. Future work should use target-independent observables, nonprime controls, transferable calibration and repeated timings.
