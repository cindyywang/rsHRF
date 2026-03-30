import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --------------------------------------------------
# load data
# --------------------------------------------------

df = pd.read_csv("results/FC_HRF_comparison_recomputed.csv")

# extract group from subject IDs
df["Group"] = df["Subject"].apply(lambda x: "Control" if "CON" in x else "Patient")
df_melt = df.melt(id_vars=["Subject","Group"], value_vars=["FC_sameHRF","FC_diffHRF"],
                  var_name="HRF_type", value_name="FC_correlation")

# --------------------------------------------------
# set labels
# --------------------------------------------------

df_melt["HRF_type"] = df_melt["HRF_type"].map({
    "FC_sameHRF": "Canonical HRF",
    "FC_diffHRF": "Subject-specific HRF"
})

# --------------------------------------------------
# plotting
# --------------------------------------------------

plt.figure(figsize=(8,6))
sns.boxplot(x="Group", y="FC_correlation", hue="HRF_type", data=df_melt, palette="Set2")
sns.stripplot(x="Group", y="FC_correlation", hue="HRF_type", data=df_melt,
              dodge=True, color="k", alpha=0.5, size=4)

plt.title("Effect of Subject-Specific HRF on Simulated FC")
plt.ylabel("FC correlation with empirical BOLD")
plt.xlabel("")
plt.legend(title="HRF type")
plt.tight_layout()

plt.savefig("results/HRF_boxplot_figure.png", dpi=300)
plt.show()
