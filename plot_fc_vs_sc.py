#!/usr/bin/env python
"""
Plot FC vs SC comparison for TVB subjects.
Shows the relationship between Structural Connectivity (SC) and 
Functional Connectivity (FC) - both empirical and simulated.
"""

import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# -----------------------------
# Config
# -----------------------------
tvb_dir = "./ds001226/derivatives/TVB"
results_dir = "./results"

# Select subjects to visualize
SUBJECTS = ["sub-CON01", "sub-CON04", "sub-PAT03", "sub-PAT17"]  # Mix of controls and patients

# -----------------------------
# Helper functions
# -----------------------------
def load_sc(sc_folder):
    """Load structural connectivity matrix."""
    weights_file = os.path.join(sc_folder, "weights.txt")
    if os.path.exists(weights_file):
        return np.loadtxt(weights_file)
    return None

def load_fc(fc_file):
    """Load functional connectivity matrix from .mat file."""
    if os.path.exists(fc_file):
        data = sio.loadmat(fc_file)
        return data.get("FC_cc_DK68", None)
    return None

def load_simulated_bold(subject, hrf_type="sameHRF"):
    """Load simulated BOLD signal."""
    bold_file = os.path.join(results_dir, f"{subject}_bold_{hrf_type}.npy")
    if os.path.exists(bold_file):
        return np.load(bold_file)
    return None

def compute_fc(bold_signal):
    """Compute functional connectivity (correlation matrix) from BOLD signal."""
    return np.corrcoef(bold_signal)

def plot_fc_sc_comparison(ax, sc, fc_emp, fc_sim, subject, group):
    """Plot FC vs SC scatter comparison."""
    # Extract upper triangle (excluding diagonal)
    triu_idx = np.triu_indices_from(sc, k=1)
    
    sc_vec = sc[triu_idx]
    fc_emp_vec = fc_emp[triu_idx]
    fc_sim_vec = fc_sim[triu_idx]
    
    # Remove NaN values
    valid = ~(np.isnan(sc_vec) | np.isnan(fc_emp_vec) | np.isnan(fc_sim_vec))
    sc_vec = sc_vec[valid]
    fc_emp_vec = fc_emp_vec[valid]
    fc_sim_vec = fc_sim_vec[valid]
    
    # Compute correlations
    corr_emp = np.corrcoef(sc_vec, fc_emp_vec)[0, 1]
    corr_sim = np.corrcoef(sc_vec, fc_sim_vec)[0, 1]
    
    # Scatter plot
    ax.scatter(sc_vec, fc_emp_vec, alpha=0.3, s=10, c='blue', label=f'Empirical FC (r={corr_emp:.3f})')
    ax.scatter(sc_vec, fc_sim_vec, alpha=0.3, s=10, c='red', label=f'Simulated FC (r={corr_sim:.3f})', marker='x')
    
    ax.set_xlabel('Structural Connectivity (SC) Weight', fontsize=10)
    ax.set_ylabel('Functional Connectivity (FC)', fontsize=10)
    ax.set_title(f'{subject} ({group})\nSC-FC Correlation', fontsize=11, fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    return corr_emp, corr_sim

def plot_fc_matrices(ax, fc_matrix, title, cmap='RdBu_r'):
    """Plot FC matrix as heatmap."""
    im = ax.imshow(fc_matrix, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlabel('Brain Regions (DK68)', fontsize=9)
    ax.set_ylabel('Brain Regions (DK68)', fontsize=9)
    plt.colorbar(im, ax=ax, label='Correlation', shrink=0.8)

# -----------------------------
# Main plotting
# -----------------------------
fig = plt.figure(figsize=(16, 12))

for idx, subject in enumerate(SUBJECTS):
    group = "Control" if "CON" in subject else "Patient"
    print(f"\nProcessing {subject} ({group})...")
    
    # Paths
    subj_dir = os.path.join(tvb_dir, subject, "ses-preop")
    sc_folder = os.path.join(subj_dir, "SC")
    fc_file = os.path.join(subj_dir, "FC.mat")
    
    # Load SC
    sc = load_sc(sc_folder)
    if sc is None:
        print(f"  Skipping {subject}: No SC data")
        continue
    
    # Load empirical FC
    fc_emp = load_fc(fc_file)
    if fc_emp is None:
        print(f"  Skipping {subject}: No FC data")
        continue
    
    # Load simulated BOLD and compute simulated FC
    bold_sim = load_simulated_bold(subject, hrf_type="diffHRF")
    if bold_sim is None:
        print(f"  Skipping {subject}: No simulated BOLD data")
        continue
    
    fc_sim = compute_fc(bold_sim)
    
    # Create subplot grid for each subject (2x2)
    ax1 = plt.subplot(2, 2, idx + 1)
    corr_emp, corr_sim = plot_fc_sc_comparison(ax1, sc, fc_emp, fc_sim, subject, group)
    
    print(f"  SC-FC Empirical correlation: {corr_emp:.4f}")
    print(f"  SC-FC Simulated correlation: {corr_sim:.4f}")

plt.tight_layout()
output_path = "fig_FC_vs_SC_scatter.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\nSaved: {output_path}")
plt.show()

# -----------------------------
# Additional: FC Matrix Comparison
# -----------------------------
print("\n--- FC Matrix Comparison ---")

# Select one representative subject
rep_subject = "sub-CON01"
subj_dir = os.path.join(tvb_dir, rep_subject, "ses-preop")
fc_file = os.path.join(subj_dir, "FC.mat")

fc_emp = load_fc(fc_file)
bold_sim = load_simulated_bold(rep_subject, hrf_type="diffHRF")
fc_sim = compute_fc(bold_sim)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Empirical FC
plot_fc_matrices(axes[0], fc_emp, f'Empirical FC\n({rep_subject})')

# Simulated FC
plot_fc_matrices(axes[1], fc_sim, f'Simulated FC (Subject-Specific HRF)\n{rep_subject}')

# Difference
diff = fc_sim - fc_emp
im = axes[2].imshow(diff, cmap='RdBu_r', vmin=-0.5, vmax=0.5, aspect='auto')
axes[2].set_title(f'Difference (Simulated - Empirical)\n{rep_subject}', fontsize=11, fontweight='bold')
axes[2].set_xlabel('Brain Regions (DK68)', fontsize=10)
axes[2].set_ylabel('Brain Regions (DK68)', fontsize=10)
plt.colorbar(im, ax=axes[2], label='Correlation Difference', shrink=0.8)

plt.tight_layout()
output_path = "fig_FC_matrix_comparison.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Saved: {output_path}")
plt.show()

# -----------------------------
# Summary Statistics
# -----------------------------
print("\n========== SUMMARY ==========")
print(f"FC Matrix Comparison for {rep_subject}:")
print(f"  Mean absolute difference: {np.mean(np.abs(diff)):.4f}")
print(f"  Max difference: {np.max(np.abs(diff)):.4f}")
print(f"  FC correlation (empirical vs simulated): {np.corrcoef(fc_emp[np.triu_indices_from(fc_emp, k=1)], fc_sim[np.triu_indices_from(fc_sim, k=1)])[0, 1]:.4f}")
