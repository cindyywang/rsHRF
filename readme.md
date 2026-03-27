# GSoC 2026 Project 27 - Personalized HRF in TVB

## Dataset
- OpenNeuro ds001226, pre-processed for TVB

## Pipeline
1. Run `test.py` to generate neural and BOLD signals.
2. `analysis.py` computes correlations with empirical FC and improvements.

## Outputs
- `results/` contains:
  - `*_neural.npy`
  - `*_bold_diffHRF.npy`
  - `*_bold_sameHRF.npy`
- `FC_HRF_comparison.csv` contains per-subject correlations and group-level summary.

## Findings
- Subject-specific HRF generally improves simulated FC.
- Preliminary analysis shows stronger improvement in patients than controls.
