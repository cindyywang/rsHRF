import os
import numpy as np
import scipy.io as sio
import pandas as pd

# --------------------------------
# Paths
# --------------------------------
base_dir = "./ds001226/derivatives/TVB"
results_dir = "./results"

# --------------------------------
# Helper: FC correlation
# --------------------------------
def fc_corr(sim_bold, emp_fc):
    sim_fc = np.corrcoef(sim_bold)
    sim_vec = sim_fc[np.triu_indices_from(sim_fc, k=1)]
    emp_vec = emp_fc[np.triu_indices_from(emp_fc, k=1)]
    return np.corrcoef(sim_vec, emp_vec)[0,1]

# --------------------------------
# Get subject list
# --------------------------------
subjects = sorted(set(f.split("_")[0] for f in os.listdir(results_dir) if f.endswith(".npy")))

rows = []

# --------------------------------
# Main loop
# --------------------------------
for subj in subjects:

    bold_same_file = os.path.join(results_dir, f"{subj}_bold_sameHRF.npy")
    bold_diff_file = os.path.join(results_dir, f"{subj}_bold_diffHRF.npy")
    fc_file = os.path.join(base_dir, subj, "ses-preop", "FC.mat")

    if not (os.path.exists(bold_same_file) and os.path.exists(bold_diff_file) and os.path.exists(fc_file)):
        continue

    bold_same = np.load(bold_same_file)
    bold_diff = np.load(bold_diff_file)
    emp_fc = sio.loadmat(fc_file)["FC_cc_DK68"]

    corr_same = fc_corr(bold_same, emp_fc)
    corr_diff = fc_corr(bold_diff, emp_fc)

    rows.append({
        "Subject": subj,
        "Group": "Control" if "CON" in subj else "Patient",
        "FC_sameHRF": corr_same,
        "FC_diffHRF": corr_diff,
        "Improvement": corr_diff - corr_same
    })

# --------------------------------
# Create dataframe
# --------------------------------
df = pd.DataFrame(rows)
df.to_csv("FC_HRF_comparison.csv", index=False)

# --------------------------------
# Group statistics
# --------------------------------
mean_all = df["Improvement"].mean()
mean_control = df[df["Group"]=="Control"]["Improvement"].mean()
mean_patient = df[df["Group"]=="Patient"]["Improvement"].mean()

n_improved = (df["Improvement"] > 0).sum()
n_total = len(df)

# --------------------------------
# Final output
# --------------------------------
print("\n========== FINAL RESULTS ==========\n")

print(f"Subjects analysed: {n_total}")
print(f"Subjects improved with subject-specific HRF: {n_improved}/{n_total}\n")

print(f"Mean improvement (ALL subjects): {mean_all:.4f}")
print(f"Mean improvement (Controls):     {mean_control:.4f}")
print(f"Mean improvement (Patients):     {mean_patient:.4f}")

print("\nResults saved as: FC_HRF_comparison.csv\n")
