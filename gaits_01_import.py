import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()

# Definitions - using relative paths
data_folder = script_dir / "Data"
figure_folder = script_dir / "Figures"

# Create directories if they don't exist
data_folder.mkdir(exist_ok=True)
figure_folder.mkdir(exist_ok=True)

subset_name = "Ga"  # enter one of the following : Ju, Si, Ga
participant_groups = "Co", "Pt"  # Co for controls, Pt for patients
max_n_participant = 33  # maximal number of participants per group

for group in participant_groups:
    for pi in range(1, max_n_participant + 1):  # goes up to 33, the max nr of participants in a group
        for rep in ('01', '02', '10'):
            try:
                # participant string
                participant_ID = subset_name + group + f"{pi:02}"

                # Load the data
                data = np.loadtxt(data_folder + '/00_source-data/' + participant_ID + '_' + rep + '.txt')

                # parse data into variables
                time = data[:, 0]
                left_force = data[:, 17]
                right_force = data[:, 18]

                # select only the relevant data (for simplicity)
                out_data = np.column_stack((time, left_force, right_force))

                # resave the resulting file in "raw-data folder" following BIDS conventions
                out_dir = data_folder + '/01_raw-data/sub-' + participant_ID + '/beh/'
                os.makedirs(out_dir, exist_ok=True)  # when saving anything, the target folder needs to exist first
                out_file = 'sub-' + participant_ID + '_run-' + rep + '_task-gait_beh.tsv'
                np.savetxt(out_dir + out_file, out_data, delimiter='\t', fmt='%.6f')

                # Visualise total force data
                plt.plot(time[1:2000], left_force[1:2000], label='Left Foot Total Force')
                plt.plot(time[1:2000], right_force[1:2000], label='Right Foot Total Force')
                plt.ylabel('Force (N)')
                plt.legend()
                plt.title('Total Vertical Ground Reaction Force')


                # save the figure
                figure_filename = figure_folder + '/01_raw-data/' + 'raw_' + participant_ID + '_' + rep + '.png'
                os.makedirs(figure_folder + '/01_raw-data/', exist_ok=True)  # when saving anything, the target folder needs to exist first

                # plt.show()

      
                plt.savefig(figure_filename)
                plt.close()

            except:  #these lines are executed when some files do not exist
                print('error')  # print('Could not import ' + participant_ID + '_' + rep + '.txt')
            else:
                print('Imported ' + participant_ID + '_' + rep + '.txt')

