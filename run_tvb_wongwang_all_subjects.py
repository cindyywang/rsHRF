import os
import numpy as np
import scipy.io

from tvb.simulator.lab import *

# --------------------------------------------------
# dataset root
# --------------------------------------------------

tvb_root = "ds001226/derivatives/TVB"
output_path = "results"

os.makedirs(output_path, exist_ok=True)

# --------------------------------------------------
# find all subjects automatically
# --------------------------------------------------

subjects = []

for folder in os.listdir(tvb_root):
    if folder.startswith("sub-"):
        subjects.append(folder)

print("Subjects:", subjects)

# --------------------------------------------------
# loop over subjects
# --------------------------------------------------

for subject in subjects:

    print("Running TVB for:", subject)

    sc_file = f"{tvb_root}/{subject}/ses-preop/SCthrAn.mat"

    if not os.path.exists(sc_file):
        print("SC file missing for", subject)
        continue

    # ---------- load SC from MATLAB file ----------
    mat = scipy.io.loadmat(sc_file)

    # check keys once using: print(mat.keys())
    weights = mat["SC"]          # usually stored as SC
    lengths = mat["dist"]        # usually stored as distances

    # ---------- create connectivity ----------
    connectivity = connectivity.Connectivity()
    connectivity.weights = weights
    connectivity.tract_lengths = lengths
    connectivity.configure()

    # ---------- Wong-Wang model ----------
    model = models.ReducedWongWang()

    coupling = coupling.Linear(a=0.2)
    integrator = integrators.HeunDeterministic(dt=0.5)
    monitor = monitors.Raw(period=2.0)

    sim = simulator.Simulator(
        model=model,
        connectivity=connectivity,
        coupling=coupling,
        integrator=integrator,
        monitors=[monitor]
    )

    sim.configure()

    time, data = sim.run(simulation_length=2000.0)[0]

    neural = data[:, 0, :, 0]

    np.save(f"{output_path}/{subject}_neural_tvb.npy", neural)

print("Finished.")
