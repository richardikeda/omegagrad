# Reproducibility and archival provenance

**Richard Ikeda — Author & Lead Investigator**

## Environment

Install Python 3.10+ and `python -m pip install -e ".[test,report]"`. Reference runs used Python 3.12; exact numerical-library versions are stored in campaign JSON metadata and requirements-lock.txt. Floating-point results and wall times can vary across platforms. The lock reflects a particular environment, not a universal dependency solution for every supported interpreter.

Run `python -m pytest -q`, then the four examples documented in [REUSE_GUIDE.md](REUSE_GUIDE.md). CI runs these checks on Python 3.10 and 3.12.

## Campaign commands

```bash
python -m omegagrad.experiments --output outputs/reproduction_phase1
python -m omegagrad.experiments --bits 6 --modes fixed --seeds 0 --backend autograd --output outputs/reproduction_autograd
python -m omegagrad.phase2
python -m omegagrad.phase3
python -m omegagrad.phase3_refine
python build_results_pdf.py --phase2
python build_results_pdf.py --phase3
python build_technical_papers.py
```

The last command renders the archived paper sources rather than rerunning experiments. The phase-2 and phase-3 campaign runners overwrite fixed directories, so reproduce them in a separate clone. The default phase-1 runner also writes a reference path unless `--output` is supplied. Full extended geometry can be much more expensive than unit tests.

## Artifact lineage

| Campaign | Published code checkpoint | Data |
|---|---|---|
| Phase 1 | 2c828e8 | outputs/first_run; outputs/autograd_validation |
| Phase 2 | dc54a92 | outputs/phase2 |
| Phase 3 | 8579a08 | outputs/phase3 |

These are repository commits, not claims that every stored execution hash equals every source in the archival release. JSON hashes preserve the files present during execution. Phase-1 metadata separately records raw working-file and Git-LF hashes. Line-ending normalization and later numerical refinements can change bytes. Reproduce historical results from their checkpoint; use the 1.0.0 sources for the final consolidated implementation.

Phase 3 retains initial_geometry and refined geometry. The split quadrature used in the refined run raised no IntegrationWarning with warnings treated as errors. The refinement sensitivity supports the reported signs of R²; it does not certify all extrema or validate an asymptotic law.

## Architecture and cost

Scalar Value: first-order reverse AD with iterative graph traversal. TensorValue: broadcasting, reverse gradients and forward directional second derivatives. Background: model-specific quadrature plus spline. Residual: generic subtraction of field-compatible objects. Root scanning: vectorized field evaluation followed by scalar Brent refinement; the phase-3 central-gap solver uses batched bisection. These are distinct algorithms.

The full prime potential costs O(number of primes) per coordinate. Batching increases throughput but does not remove that cost. Radar uses only the small base, yet cell enumeration and root refinement remain Python loops. Reference crivo construction is not a new primality-discovery result.

## Preservation

The [Portuguese archive](../pt-BR/ARCHIVE.md) links all original reports and PDFs without moving or rewriting campaign data. Legacy docs paths redirect to the reviewed English versions. No chat transcripts or source conversations are part of the public study. “Final archival release” does not set GitHub's read-only archived flag.
