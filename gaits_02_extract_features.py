import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Contents of this script is based on Hausdorff, Ladin, and Wei (1995)
# Created for course Digital Tools for Reproducible Research @ TU Berlin
# author Sein Jeung, github @sjeung

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()

# Definitions - using relative paths
data_folder = script_dir / "Data"
figure_folder = script_dir / "Figures"
results_folder = script_dir / "Results"

# Create directories if they don't exist
data_folder.mkdir(exist_ok=True)
figure_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

# Analysis parameters
rise_fall_edge = 500
local_minima_window = 33  # samples
offset_contact = 10  # in Newton

def find_slope_min(signal, start_idx, direction=1, window=5, slope_thresh=0.01):
    """
    Walk along `signal` from `start_idx` in `direction` (+1=forward, -1=backward)
    Fit a line to the last `window` points at each step
    Stop when slope ~ 0 (abs(slope) < slope_thresh)
    Return final index.
    """
    idx = start_idx
    N = len(signal)

    while True:
        # Ensure we have enough points to fit
        if direction == 1:
            if idx + 1 >= N:
                break
            fit_idx = np.arange(max(0, idx - window + 1), idx + 1)
        else:
            if idx - 1 < 0:
                break
            fit_idx = np.arange(idx, min(N, idx + window))

        y = signal[fit_idx]
        x = fit_idx

        # Fit line: polyfit degree 1
        p = np.polyfit(x, y, 1)
        slope = p[0]

        # Check slope magnitude
        if abs(slope) < slope_thresh:
            break

        # Step in direction
        idx += direction

        # Stop if out of bounds
        if idx <= 0 or idx >= N - 1:
            break

    return idx

def detect_edges(force, threshold):
    above_threshold = force > threshold
    crossings = np.diff(above_threshold.astype(int))
    return np.where(crossings != 0)[0] + 1

def find_slope_minima(force, edges, direction=1, window=5, slope_thresh=0.01):
    slope_minima = []
    for idx in edges:
        min_idx = find_slope_min(force, idx, direction, window, slope_thresh)
        slope_minima.append(min_idx)
    return np.array(slope_minima)

def find_final_contacts(force, time, minima_indices, offset):
    FC_times = []
    FC_indices = []

    for min_idx in minima_indices:
        if min_idx is None or not isinstance(min_idx, (int, np.integer)):
            continue  # Skip if index is invalid

        threshold = force[min_idx] - offset

        # Search forward for FC
        FC_idx = min_idx
        while FC_idx < len(force) - 1 and force[FC_idx] < threshold:
            FC_idx += 1

        FC_times.append(time[FC_idx])
        FC_indices.append(FC_idx)

    return FC_times, FC_indices

def compute_stride_times(FC_times):
    return [FC_times[i+1] - FC_times[i] for i in range(1, len(FC_times)-1)]



for group in participant_groups:
    for pi in range(1, max_n_participant + 1):  # goes up to 33, the max nr of participants in a group
        for rep in ('01', '02', '10'):
            # participant string
            participant_ID = subset_name + group + f"{pi:02}"

            # construct file path
            file_path = os.path.join(
                data_folder, '01_raw-data', f'sub-{participant_ID}', 'beh',
                f'sub-{participant_ID}_run-{rep}_task-gait_beh.tsv'
            )

            try:
                # Try to load the file
                data = np.loadtxt(file_path, delimiter='\t')
            except FileNotFoundError:
                print(f"File not found: {file_path}. Breaking loop.")
                break  # Exit the for loop if file not found

            # parse data into variables
            time = data[:, 0]
            left_force = data[:, 1]
            right_force = data[:, 2]

            # step 1. determine rising & falling edges
            # ------------------------------------------------------------------------------------------------------
            edgesLeft = detect_edges(left_force, rise_fall_edge)
            edgesRight = detect_edges(right_force, rise_fall_edge)

            # step 2. find local minima near each edge
            # ------------------------------------------------------------------------------------------------------
            slope_minima_left = find_slope_minima(left_force, edgesLeft)
            slope_minima_right = find_slope_minima(right_force, edgesRight)

            # step 3. For each minimum, find FC
            # -------------------------------------------------------------------------------------------------------
            FC_times_left, FC_indices_left = find_final_contacts(left_force, time, slope_minima_left,
                                                                 offset_contact)
            FC_times_right, FC_indices_right = find_final_contacts(right_force, time, slope_minima_right,
                                                                   offset_contact)

            # step 4. compute stride times
            # ------------------------------------------------------------------------------------------------------
            stride_times_left = compute_stride_times(FC_times_left)
            stride_times_right = compute_stride_times(FC_times_right)

            max_len = max(len(stride_times_left), len(stride_times_right))

            def pad(array, length):
                return array + [np.nan] * (length - len(array))

            stride_left_padded = pad(stride_times_left, max_len)
            stride_right_padded = pad(stride_times_right, max_len)

            out_data = np.column_stack((stride_left_padded, stride_right_padded))

            # resave the resulting file in "raw-data folder" following BIDS conventions
            out_dir = results_folder + '/'
            os.makedirs(out_dir, exist_ok=True)  # when saving anything, the target folder needs to exist first
            out_file = 'sub-' + participant_ID + '_strides.tsv'
            np.savetxt(out_dir + out_file, out_data, delimiter='\t', fmt='%.6f')

            # VISUALIZATION ----------------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------------------------------
            # visualize step 1. rising and falling edges------------------------------------------------------------
            plt.plot(time[1:2000], left_force[1:2000], label='Left Foot Total Force')
            plt.plot(time[1:2000], right_force[1:2000], label='Right Foot Total Force')
            for idx in edgesLeft[edgesLeft < 2000]:
                plt.axvline(x=time[idx], color='g', linestyle='--', label='Edge Left')
            for idx in edgesRight[edgesRight < 2000]:
                plt.axvline(x=time[idx], color='r', linestyle='--', label='Edge Left')

            figure_filename = figure_folder + '/02_edge_detection/' + 'edges_' + participant_ID + '_' + rep + '.png'
            os.makedirs(figure_folder + '/02_edge_detection/', exist_ok=True)
            plt.savefig(figure_filename)
            plt.close()

            # visualizing final contact points  --------------------------------------------------------------------
            # Plot only the first 2000 data points
            plt.plot(time[:2000], left_force[:2000], label='Force signal')

            # show thresholds only for minima in first 2000 points
            for min_idx in slope_minima_left:
                if min_idx < 2000:
                    threshold = left_force[min_idx] - offset_contact
                    plt.axhline(threshold, color='grey', linestyle='--', alpha=0.5)

            # Mark FC points only if they are within first 2000
            FC_in_range = [i for i in FC_indices_left if i < 2000]
            plt.plot([time[i] for i in FC_in_range], [left_force[i] for i in FC_in_range],
                    'ro', label='Final Contacts')

            # Labels and legend
            plt.xlabel('Time (s)')
            plt.ylabel('Force (N)')
            plt.title('Force Signal (first 2000 samples) with Final Contacts')
            plt.legend()

            figure_filename = figure_folder + '/03_final_contacts/' + 'fc_' + participant_ID + '_' + rep + '.png'
            os.makedirs(figure_folder + '/03_final_contacts/', exist_ok=True)
            plt.savefig(figure_filename)
            plt.close()



