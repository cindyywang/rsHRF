import os
import numpy as np
from scipy.signal import fftconvolve

# --------------------------------------------------
# paths
# --------------------------------------------------

neural_path = "results"
hrf_path = "ds001226/derivatives/TVB"   # where subject HRFs are stored
output_path = "results"

os.makedirs(output_path, exist_ok=True)

# --------------------------------------------------
# canonical HRF (simple double-gamma approximation)
# --------------------------------------------------

def canonical_hrf(length=32, dt=0.5):
    t = np.arange(0, length, dt)

    peak1 = (t ** 8.6) * np.exp(-t / 0.547)
    peak2 = 0.35 * (t ** 9) * np.exp(-t / 0.6)

    hrf = peak1 - peak2
    hrf = hrf / np.max(hrf)

    return hrf

canonical = canonical_hrf()

# --------------------------------------------------
# loop over subjects
# --------------------------------------------------

for file in os.listdir(neural_path):

    if file.endswith("_neural_tvb.npy"):

        subject = file.replace("_neural_tvb.npy", "")
        print("Processing:", subject)

        neural = np.load(f"{neural_path}/{subject}_neural_tvb.npy")

        # shape = time x regions
        n_time, n_regions = neural.shape

        # ------------------------------------------
        # load subject-specific HRF
        # ------------------------------------------

        hrf_file = f"{hrf_path}/{subject}/ses-preop/HRF.csv"

        if not os.path.exists(hrf_file):
            print("Missing HRF for", subject)
            continue

        subject_hrf = np.loadtxt(hrf_file, delimiter=",")

        # ------------------------------------------
        # convolve neural signal
        # ------------------------------------------

        bold_diffHRF = np.zeros_like(neural)
        bold_sameHRF = np.zeros_like(neural)

        for region in range(n_regions):

            bold_diffHRF[:, region] = fftconvolve(neural[:, region], subject_hrf, mode="same")
            bold_sameHRF[:, region] = fftconvolve(neural[:, region], canonical, mode="same")

        # ------------------------------------------
        # save both versions
        # ------------------------------------------

        np.save(f"{output_path}/{subject}_bold_diffHRF.npy", bold_diffHRF)
        np.save(f"{output_path}/{subject}_bold_sameHRF.npy", bold_sameHRF)

print("Finished generating BOLD signals for all subjects.")
