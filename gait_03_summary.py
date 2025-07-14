import os
import numpy as np
import matplotlib.pyplot as plt

# Definitions
figure_folder = "P:/Sein_Jeung/Teaching/ReproResearch/Figures"
results_folder = "P:/Sein_Jeung/Teaching/ReproResearch/Results"
subset_name = "Ga"  # enter one of the following : Ju, Si, Ga
participant_groups = "Co", "Pt"  # Co for controls, Pt for patients
max_n_participant = 33  # maximal number of participants per group

# Initialize output containers
group_stride_averages = {
    "Co": [],
    "Pt": []
}

for group in participant_groups:
    for pi in range(1, max_n_participant + 1):  # goes up to 33, the max nr of participants in a group

        # Initialize participant stride list
        participant_stride_times = []

        # participant string
        participant_ID = subset_name + group + f"{pi:02}"

        # construct file path
        file_path = os.path.join(
            results_folder, f'sub-{participant_ID}_strides.tsv'
        )

        try:
            # Try to load the file
            data = np.loadtxt(file_path, delimiter='\t')
        except FileNotFoundError:
            print(f"File not found: {file_path}. Breaking loop.")
            continue  # skip if file not found

        participant_stride_times.append(data)

        # Stack stride times and compute mean across all reps
        all_strides = np.vstack(participant_stride_times)
        all_strides[all_strides == 0] = np.nan # because there are some zero values mixed in
        left_mean = np.nanmean(all_strides[:, 0])
        right_mean = np.nanmean(all_strides[:, 1])
        group_stride_averages[group].append([left_mean, right_mean])

# Convert lists to arrays
group_stride_averages["Co"] = np.array(group_stride_averages["Co"])
group_stride_averages["Pt"] = np.array(group_stride_averages["Pt"])

# Optionally print summary
print("Control Group Stride Means (per participant):")
print(group_stride_averages["Co"])
print("\nPatient Group Stride Means (per participant):")
print(group_stride_averages["Pt"])