import os
import numpy as np
import pandas as pd

# --------------------------------------------------
# path
# --------------------------------------------------

results_path = "results"

# --------------------------------------------------
# helper: compute FC matrix
# --------------------------------------------------

def compute_fc(bold):
    return np.corrcoef(bold)

# --------------------------------------------------
# find subjects automatically
# --------------------------------------------------

subjects = []

for file in os.listdir(results_path):
    if file.endswith("_bold_sameHRF.npy"):
        subject = file.replace("_bold_sameHRF.npy", "")
        subjects.append(subject)

print("Subjects found:", subjects)

# --------------------------------------------------
# compute FC correlations
# --------------------------------------------------

rows = []

for subject in subjects:

    empirical_file = f"{results_path}/{subject}_bold.npy"
    same_file      = f"{results_path}/{subject}_bold_sameHRF.npy"
    diff_file      = f"{results_path}/{subject}_bold_diffHRF.npy"

    if not os.path.exists(empirical_file):
        print("Missing empirical BOLD for", subject)
        continue

    empirical = np.load(empirical_file)
    sameHRF   = np.load(same_file)
    diffHRF   = np.load(diff_file)

    fc_empirical = compute_fc(empirical)
    fc_sameHRF   = compute_fc(sameHRF)
    fc_diffHRF   = compute_fc(diffHRF)

    corr_same = np.corrcoef(fc_empirical.flatten(), fc_sameHRF.flatten())[0,1]
    corr_diff = np.corrcoef(fc_empirical.flatten(), fc_diffHRF.flatten())[0,1]

    rows.append([subject, corr_same, corr_diff, corr_diff - corr_same])

# --------------------------------------------------
# save table
# --------------------------------------------------

df = pd.DataFrame(rows, columns=[
    "Subject",
    "FC_sameHRF",
    "FC_diffHRF",
    "Improvement"
])

df.to_csv(f"{results_path}/FC_HRF_comparison_recomputed.csv", index=False)

print("Saved:", f"{results_path}/FC_HRF_comparison_recomputed.csv")
