import os
import numpy as np
import pandas as pd
import subprocess
from scipy.signal import convolve
from tvb.simulator.lab import *

# -----------------------------
# Common HRF (same for everyone)
# -----------------------------
def create_common_hrf(length=30):
    t = np.linspace(0, 30, length)
    hrf = t ** 8 * np.exp(-t / 1.5)
    hrf = hrf / np.max(hrf)
    return hrf

common_hrf = create_common_hrf()

# -----------------------------
# Config
# -----------------------------
base_dir = "./ds001226/derivatives/TVB"
subjects = [d for d in os.listdir(base_dir) if d.startswith("sub-CON") or d.startswith("sub-PAT")]

output_dir = "./results"
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Helper functions
# -----------------------------
def ensure_sc_unzipped(subdir):
    sc_zip = os.path.join(subdir, "SC.zip")
    sc_folder = os.path.join(subdir, "SC")
    if not os.path.exists(sc_folder):
        if os.path.exists(sc_zip):
            print(f"Unzipping SC.zip for {subdir}")
            subprocess.run(f'unzip "{sc_zip}" -d "{sc_folder}"', shell=True)
        else:
            print(f"No SC.zip found for {subdir}, skipping...")
            return None
    return sc_folder

def load_sc(sc_folder):
    weights_file = os.path.join(sc_folder, "weights.txt")
    lengths_file = os.path.join(sc_folder, "tract_lengths.txt")
    if not os.path.exists(weights_file) or not os.path.exists(lengths_file):
        print(f"Missing weights or lengths in {sc_folder}, skipping...")
        return None, None
    return np.loadtxt(weights_file), np.loadtxt(lengths_file)

def load_hrf(subdir):
    hrf_file = os.path.join(subdir, "HRF.csv")
    if not os.path.exists(hrf_file):
        print(f"No HRF.csv for {subdir}, skipping HRF convolution")
        return None
    return pd.read_csv(hrf_file, header=None).values.flatten()

def simulate_tvb(SC_weights, SC_lengths, sim_length=1000):
    """Minimal TVB simulation placeholder. Returns neural activity array [n_nodes, n_timepoints]."""
    n_nodes = SC_weights.shape[0]
    neural_activity = np.random.randn(n_nodes, sim_length) * 0.1  # placeholder random activity
    return neural_activity

def convolve_hrf(neural_activity, hrf):
    """Convolve each node's neural activity with HRF."""
    if hrf is None:
        return neural_activity
    n_nodes = neural_activity.shape[0]
    bold = np.zeros_like(neural_activity)
    for i in range(n_nodes):
        bold[i, :] = convolve(neural_activity[i, :], hrf, mode='same')
    return bold

# -----------------------------
# Main loop
# -----------------------------
for subject in subjects:
    print(f"\n=== Processing {subject} ===")
    subdir = os.path.join(base_dir, subject, "ses-preop")

    # 1. Ensure SC is unzipped
    sc_folder = ensure_sc_unzipped(subdir)
    if sc_folder is None:
        continue

    # 2. Load SC
    SC_weights, SC_lengths = load_sc(sc_folder)
    if SC_weights is None:
        continue

    # 3. Load HRF
    hrf = load_hrf(subdir)

    # 4. Run neural simulation
    neural_data = simulate_tvb(SC_weights, SC_lengths, sim_length=1000)

    # 5A. BOLD with subject-specific HRF
    bold_diffHRF = convolve_hrf(neural_data, hrf)

    # 5B. BOLD with SAME HRF for everyone
    bold_sameHRF = convolve_hrf(neural_data, common_hrf)

    # 6. Save results
    np.save(os.path.join(output_dir, f"{subject}_neural.npy"), neural_data)
    np.save(os.path.join(output_dir, f"{subject}_bold_diffHRF.npy"), bold_diffHRF)
    np.save(os.path.join(output_dir, f"{subject}_bold_sameHRF.npy"), bold_sameHRF)

    print(f"{subject} done. Neural & BOLD saved.")
