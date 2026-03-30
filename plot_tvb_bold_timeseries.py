#!/usr/bin/env python
"""
Plot TVB canonical BOLD timeseries for a subject.
Shows comparison between empirical BOLD, simulated BOLD with canonical HRF,
and simulated BOLD with subject-specific HRF.
"""

import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

# -----------------------------
# Config
# -----------------------------
results_dir = "./results"
tvb_dir = "./ds001226/derivatives/TVB"

# Select a subject to visualize (change as needed)
SUBJECT = "sub-CON01"  # Options: sub-CON01 to sub-CON11, sub-PAT01 to sub-PAT31

# -----------------------------
# Load data
# -----------------------------
print(f"Loading data for {SUBJECT}...")

# Load simulated BOLD signals
bold_same = np.load(os.path.join(results_dir, f"{SUBJECT}_bold_sameHRF.npy"))
bold_diff = np.load(os.path.join(results_dir, f"{SUBJECT}_bold_diffHRF.npy"))
neural = np.load(os.path.join(results_dir, f"{SUBJECT}_neural.npy"))

# Load empirical BOLD from TVB
empirical_bold_path = os.path.join(tvb_dir, SUBJECT, "ses-preop", "ROIts.dat")
empirical_bold = np.loadtxt(empirical_bold_path)

print(f"  Neural shape: {neural.shape}")
print(f"  BOLD sameHRF shape: {bold_same.shape}")
print(f"  BOLD diffHRF shape: {bold_diff.shape}")
print(f"  Empirical BOLD shape: {empirical_bold.shape}")

# -----------------------------
# Plotting
# -----------------------------
fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

# Time axis (assuming TR ~ 2s, adjust if needed)
n_timepoints = neural.shape[1]
time = np.arange(n_timepoints) * 2  # seconds

# Select a few representative nodes to plot
n_nodes_to_show = min(4, neural.shape[0])
node_indices = [0, 10, 20, 30] if neural.shape[0] >= 31 else list(range(n_nodes_to_show))

# Plot 1: Neural activity
ax = axes[0]
for i, node_idx in enumerate(node_indices):
    ax.plot(time, neural[node_idx, :] + i * 0.5, label=f'Node {node_idx}', linewidth=0.8)
ax.set_ylabel('Amplitude (a.u.)')
ax.set_title(f'{SUBJECT} - Neural Activity (Wong-Wang Model)', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 2: Simulated BOLD with Canonical HRF
ax = axes[1]
for i, node_idx in enumerate(node_indices):
    ax.plot(time, bold_same[node_idx, :] + i * 0.5, linewidth=0.8)
ax.set_ylabel('Amplitude (a.u.)')
ax.set_title('Simulated BOLD - Canonical HRF (Same for All Subjects)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)

# Plot 3: Simulated BOLD with Subject-Specific HRF
ax = axes[2]
for i, node_idx in enumerate(node_indices):
    ax.plot(time, bold_diff[node_idx, :] + i * 0.5, linewidth=0.8)
ax.set_ylabel('Amplitude (a.u.)')
ax.set_title('Simulated BOLD - Subject-Specific HRF (from rsHRF)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)

# Plot 4: Empirical BOLD (from TVB ROIts)
ax = axes[3]
for i, node_idx in enumerate(node_indices):
    ax.plot(time[:empirical_bold.shape[1]], empirical_bold[node_idx, :time.shape[0] if time.shape[0] < empirical_bold.shape[1] else empirical_bold.shape[1]] + i * 0.5, linewidth=0.8, alpha=0.7)
ax.set_ylabel('Amplitude (a.u.)')
ax.set_xlabel('Time (seconds)')
ax.set_title('Empirical BOLD (Resting-State fMRI)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()

# Save figure
output_path = f"fig_{SUBJECT}_bold_timeseries.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\nSaved: {output_path}")

plt.show()
