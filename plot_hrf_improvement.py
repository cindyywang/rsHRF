import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# load results
# --------------------------------------------------

df = pd.read_csv("results/FC_HRF_comparison_recomputed.csv")

# --------------------------------------------------
# sort by improvement (so the plot looks clean)
# --------------------------------------------------

df = df.sort_values("Improvement")

# --------------------------------------------------
# plot
# --------------------------------------------------

plt.figure(figsize=(10,6))

plt.bar(df["Subject"], df["FC_sameHRF"], label="Canonical HRF")
plt.bar(df["Subject"], df["FC_diffHRF"], bottom=0, alpha=0.6, label="Subject-specific HRF")

plt.xticks(rotation=90)
plt.ylabel("FC correlation with empirical data")
plt.title("Effect of Subject-Specific HRF on Simulated Functional Connectivity")

plt.legend()
plt.tight_layout()

plt.savefig("results/HRF_improvement_figure.png", dpi=300)
plt.show()
