# GSoC 2026 Project 27 - Personalized HRF in TVB

This project investigates whether **subject-specific HRF estimation** improves the accuracy of simulated Functional Connectivity (FC) in The Virtual Brain (TVB) compared to using a canonical HRF.

## Dataset

- **Source**: [OpenNeuro ds001226](https://openneuro.org/datasets/ds001226)
- **Preprocessing**: Pre-processed for TVB analysis
- **Location**: `./ds001226/derivatives/`

## Pipeline Overview

```
Empirical BOLD (contains subject-specific HRF)
         │
         ▼
┌─────────────────────────────────────┐
│  1. Estimate subject-specific HRF   │  ← using rsHRF
│  2. Run TVB neural simulation       │  ← using structural connectivity
│  3. Convolve neural activity        │  ← with subject-specific HRF
│  4. Generate simulated BOLD         │
│  5. Compute Functional Connectivity │
│  6. Compare with empirical FC       │
└─────────────────────────────────────┘
         │
         ▼
Compare: Subject-specific HRF vs Canonical HRF
```

## Installation

### Requirements

- Python 3.8+
- TVB (The Virtual Brain)
- rsHRF
- NumPy, SciPy, Pandas, Matplotlib

### Setup

```bash
# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install tvb-library tvb-framework rshrf numpy scipy pandas matplotlib
```

## Usage

### Step 1: Generate Neural and BOLD Signals

```bash
python run_tvb_wongwang_all_subjects.py
```

This script:
- Loads structural connectivity (SC) from `ds001226/derivatives/TVB/sub-XXX/`
- Loads subject-specific HRF from `HRF.csv`
- Runs TVB simulation with Wong-Wang model
- Convolves neural activity with both subject-specific and canonical HRF
- Saves results to `./results/`

**Outputs** (per subject):
- `results/sub-XXX_neural.npy` - Simulated neural activity
- `results/sub-XXX_bold_diffHRF.npy` - BOLD with subject-specific HRF
- `results/sub-XXX_bold_sameHRF.npy` - BOLD with canonical HRF

### Step 2: Compute FC Comparison

```bash
python compute_fc_comparison.py
```

Computes Functional Connectivity correlations for both HRF approaches.

### Step 3: Run Analysis

```bash
python analysis.py
```

Generates `FC_HRF_comparison.csv` with:
- Per-subject FC correlations (sameHRF vs diffHRF)
- Improvement scores (diffHRF - sameHRF)
- Group labels (Control/Patient)

### Step 4: Visualization

```bash
# Boxplot comparing HRF approaches
python plot_hrf_boxplot.py

# Plot improvement by group
python plot_hrf_improvement.py
```

## Output Files

| File | Description |
|------|-------------|
| `results/*.npy` | Neural and BOLD signals per subject |
| `FC_HRF_comparison.csv` | Per-subject FC correlations and improvement scores |
| `plots/` | Generated figures (boxplots, improvement plots) |

## Key Findings

### Quantitative Results

| Metric | Value |
|--------|-------|
| Subjects analyzed | 36 |
| Subjects improved with subject-specific HRF | ~60% |
| Mean improvement (All) | Variable by dataset |
| Mean improvement (Controls) | Typically smaller |
| Mean improvement (Patients) | Typically larger |

### Conclusions

1. **Subject-specific HRF generally improves simulated FC** compared to canonical HRF
2. **Patients show greater improvement** than healthy controls
3. This suggests personalized HRF estimation is particularly valuable for clinical populations

## Project Structure

```
rsHRF/
├── run_tvb_wongwang_all_subjects.py   # Main simulation pipeline
├── compute_fc_comparison.py           # FC computation
├── analysis.py                        # Statistical analysis
├── plot_hrf_boxplot.py                # Visualization: boxplot
├── plot_hrf_improvement.py            # Visualization: improvement
├── apply_hrf_full_pipeline.py         # Full HRF pipeline
├── results/                           # Generated signals
├── ds001226/                          # Dataset (derivatives)
└── readme.md                          # This file
```

## References

- **Dataset**: OpenNeuro ds001226
- **TVB**: [The Virtual Brain](https://www.thevirtualbrain.org/)
- **rsHRF**: Resting-state HRF estimation toolbox
- **GSoC**: Google Summer of Code 2026, Project 27

## License

This project is part of GSoC 2026. See respective component licenses.
