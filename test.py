# import rsHRF
# from rsHRF.spm_dep.spm import spm_hrf
# import numpy as np
# import matplotlib.pyplot as plt

# bold = np.random.rand(200)
# hrf = spm_hrf(RT=2.0)  # Generate canonical HRF with TR=2.0s
# print(hrf[:10])

# plt.plot(hrf)
# plt.title("Canonical HRF (TR=2.0s)")
# plt.xlabel("Time points")
# plt.ylabel("Amplitude")

# # Save the plot to a file
# plt.savefig("canonical_hrf.png", dpi=300)
# plt.close()  # Close the figure to free memory

import rsHRF
from rsHRF.spm_dep.spm import spm_hrf
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simulate BOLD signal and HRF
# -----------------------------
TR = 2.0
n_timepoints = 200
bold = np.random.rand(n_timepoints)

# Generate canonical HRF
hrf = spm_hrf(RT=TR)
print("First 10 HRF values:", hrf[:10])

# -----------------------------
# Plot canonical HRF
# -----------------------------
plt.figure()
plt.plot(hrf)
plt.title("Canonical HRF (TR=2.0s)")
plt.xlabel("Time points")
plt.ylabel("Amplitude")
plt.savefig("canonical_hrf.png", dpi=300)
plt.close()

# -----------------------------
# Convolve HRF with BOLD (simulated) to see predicted BOLD
# -----------------------------
bold_pred = np.convolve(bold, hrf)[:n_timepoints]

plt.figure()
plt.plot(bold, label="Original BOLD")
plt.plot(bold_pred, label="Convolved with HRF")
plt.title("BOLD Signal vs Convolved Signal")
plt.xlabel("Time points")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig("bold_convolved.png", dpi=300)
plt.close()
