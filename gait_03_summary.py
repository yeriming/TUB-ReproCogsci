import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()

# Definitions - using relative paths
figure_folder = script_dir / "Figures"
results_folder = script_dir / "Results"

# Create directories if they don't exist
figure_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

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


        if participant_stride_times:
            # Stack stride times and compute mean across all reps
            all_strides = np.vstack(participant_stride_times)
            left_mean = np.nanmean(all_strides[:, 0])
            right_mean = np.nanmean(all_strides[:, 1])
            group_stride_averages[group].append([left_mean, right_mean])


# Convert lists to arrays
group_stride_averages["Co"] = np.array(group_stride_averages["Co"])
group_stride_averages["Pt"] = np.array(group_stride_averages["Pt"])


# Print summary
print("Control Group Stride Means (per participant):")
print(group_stride_averages["Co"])
print("\nPatient Group Stride Means (per participant):")
print(group_stride_averages["Pt"])

# Compute means
control_means = group_stride_averages["Co"]
patient_means = group_stride_averages["Pt"]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

x_control_left = np.ones(len(control_means)) * 0.8
x_control_right = np.ones(len(control_means)) * 1.2
x_patient_left = np.ones(len(patient_means)) * 1.8
x_patient_right = np.ones(len(patient_means)) * 2.2

jitter = 0.05
np.random.seed(42)

ax.scatter(x_control_left + np.random.uniform(-jitter, jitter, len(control_means)),
           control_means[:, 0], color='blue', alpha=0.6, label='Control Left')
ax.scatter(x_control_right + np.random.uniform(-jitter, jitter, len(control_means)),
           control_means[:, 1], color='blue', alpha=0.6, label='Control Right')

ax.scatter(x_patient_left + np.random.uniform(-jitter, jitter, len(patient_means)),
           patient_means[:, 0], color='red', alpha=0.6, label='Patient Left')
ax.scatter(x_patient_right + np.random.uniform(-jitter, jitter, len(patient_means)),
           patient_means[:, 1], color='red', alpha=0.6, label='Patient Right')

mean_vals = {
    'Control Left': np.mean(control_means[:, 0]),
    'Control Right': np.mean(control_means[:, 1]),
    'Patient Left': np.mean(patient_means[:, 0]),
    'Patient Right': np.mean(patient_means[:, 1]),
}

ax.scatter(0.8, mean_vals['Control Left'], color=(0.2, 0.2, 0.8), s=150, marker='D', label='Mean Control Left')
ax.scatter(1.2, mean_vals['Control Right'], color=(0.2, 0.2, 0.8), s=150, marker='D', label='Mean Control Right')
ax.scatter(1.8, mean_vals['Patient Left'], color=(0.8, 0.2, 0.2), s=150, marker='D', label='Mean Patient Left')
ax.scatter(2.2, mean_vals['Patient Right'], color=(0.8, 0.2, 0.2), s=150, marker='D', label='Mean Patient Right')

ax.set_xticks([1, 2])
ax.set_xticklabels(['Control', 'Patient'])
ax.set_xlim(0.5, 2.5)
ax.set_ylabel('Stride Time (s)')
ax.set_title('Stride Times per Participant - Left and Right Foot by Group')

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.3, 1))

plt.tight_layout()
plt.show()

