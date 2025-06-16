import os
import numpy as np
import matplotlib.pyplot as plt

# Contents of this script is based on Hausdorff, Ladin, and Wei (1995)
# author Sein Jeung, github @sjeung


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

# Definitions
data_folder = "P:/Sein_Jeung/Teaching/ReproResearch/Data"
#figure_folder = "P:/Sein_Jeung/Teaching/ReproResearch/Figures"
results_folder = "P:/Sein_Jeung/Teaching/ReproResearch/Results"
subset_name = "Ga"  # enter one of the following : Ju, Si, Ga
participant_groups = "Co", "Pt"  # Co for controls, Pt for patients
max_n_participant = 2  # maximal number of participants per group

# Analysis parameters
rise_fall_edge = 500
local_minima_window = 5  # samples
offset_contact = 10  # in Newton

for group in participant_groups:
    for pi in range(1, max_n_participant + 1):  # goes up to 33, the max nr of participants in a group
        for rep in ('01', '02', '10'):
            try:
                # participant string
                participant_ID = subset_name + group + f"{pi:02}"

                # Load the data
                data = np.loadtxt(data_folder + '/01_raw-data/sub-' + participant_ID + '/beh/sub-' + participant_ID +
                                  '_run-' + rep + '_task-gait_beh.tsv', delimiter='\t')

                # parse data into variables
                time = data[:, 0]
                left_force = data[:, 1]
                right_force = data[:, 2]

                # step 1. determine rising & falling edges
                # ------------------------------------------------------------------------------------------------------
                # Left foot
                above_threshold = left_force > rise_fall_edge
                crossings = np.diff(above_threshold.astype(int))
                # Indices of all crossings (either +1 or -1)
                edgesLeft = np.where(crossings != 0)[0] + 1  # +1 because np.diff shifts index by 1;

                # Right foot
                above_threshold = right_force > rise_fall_edge
                crossings = np.diff(above_threshold.astype(int))
                edgesRight = np.where(crossings != 0)[0] + 1

                # step 2. find local minima near each edge
                # ------------------------------------------------------------------------------------------------------
                slope_minima = []
                for idx in edgesLeft:
                    # Example: assume you want to search FORWARD in time only
                    min_idx = find_slope_min(left_force, idx, direction=1, window=5, slope_thresh=0.01)
                    slope_minima.append(min_idx)

                slope_minima = np.array(slope_minima)

                left_force_deriv = np.diff(left_force)
                time_deriv = time[:-1]  # diff shortens length by 1

                # step 3. For each minimum, find FC
                #-------------------------------------------------------------------------------------------------------
                FC_times = []
                FC_indices = []

                for min_idx in slope_minima:
                    threshold = left_force[min_idx] - offset_contact

                    # Search forward for FC
                    FC_idx = min_idx
                    while FC_idx < len(left_force) - 1 and left_force[FC_idx] < threshold:
                        FC_idx += 1

                    FC_times.append(time[FC_idx])
                    FC_indices.append(FC_idx)

                # step 4. compute stride times
                stride_times = []
                for step_idx in range(1, len(FC_indices)-1):
                    stride_time = FC_times[step_idx + 1] - FC_times[step_idx]
                    stride_times.append(stride_time)

                out_data = np.column_stack((stride_time, stride_time))

                # resave the resulting file in "raw-data folder" following BIDS conventions
                out_dir = results_folder + '/'
                os.makedirs(out_dir, exist_ok=True)  # when saving anything, the target folder needs to exist first
                out_file = 'sub-' + participant_ID + '_strides.tsv'
                np.savetxt(out_dir + out_file, stride_times, delimiter='\t', fmt='%.6f')

                # visualize step 1. rising and falling edges------------------------------------------------------------
                plt.plot(time[1:2000], left_force[1:2000], label='Left Foot Total Force')
                plt.plot(time[1:2000], right_force[1:2000], label='Right Foot Total Force')
                for idx in edgesLeft[edgesLeft < 2000]:
                    plt.axvline(x=time[idx], color='g', linestyle='--', label='Edge Left')
                for idx in edgesRight[edgesRight < 2000]:
                    plt.axvline(x=time[idx], color='r', linestyle='--', label='Edge Left')
                plt.show()
                # ------------------------------------------------------------------------------------------------------


                # # visualize step 2. derivative and vertical lines
                # plt.plot(time_deriv[1:2000], left_force_deriv[1:2000], label='Left Force Derivative')
                # for i, idx in enumerate(edgesLeft[edgesLeft < 2000]):
                #     # Adjust index for derivative (because np.diff shifts by -1)
                #     plt.axvline(time_deriv[idx], color='m', ls='--', label='Edge' if i == 0 else None)
                #
                # # slope_minima
                # valid_minima = slope_minima[slope_minima < len(time_deriv)]
                # plt.plot(time_deriv[valid_minima[valid_minima < 2000]],
                #          left_force_deriv[valid_minima[valid_minima < 2000]],
                #          'ko', label='Slope-based Min')
                #
                # plt.xlabel('Time [s]')
                # plt.ylabel('Derivative of Force [N/s]')
                # plt.legend()
                # plt.show()
                # # ------------------------------------------------------------------------------------------------------


                # Plot only the first 2000 data points
                plt.plot(time[:2000], left_force[:2000], label='Force signal')

                # show thresholds only for minima in first 2000 points
                for min_idx in slope_minima:
                    if min_idx < 2000:
                        threshold = left_force[min_idx] - offset_contact
                        plt.axhline(threshold, color='grey', linestyle='--', alpha=0.5)

                # Mark FC points only if they are within first 2000
                FC_in_range = [i for i in FC_indices if i < 2000]
                plt.plot([time[i] for i in FC_in_range], [left_force[i] for i in FC_in_range],
                        'ro', label='Final Contacts')

                # Labels and legend
                plt.xlabel('Time (s)')
                plt.ylabel('Force (N)')
                plt.title('Force Signal (first 2000 samples) with Final Contacts')
                plt.legend()
                plt.show()

            except:
                print('error')


