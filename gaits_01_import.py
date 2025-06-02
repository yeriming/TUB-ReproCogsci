import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = np.loadtxt('C:/Users/seinj/OneDrive/Desktop/ReproCogsciSoSe25/Data/00_source-data/GaCo01_01.txt')  # Or use pandas if working with CSV

# parse data into variables
time = data[:, 0]
left_sensors = data[:, 1:8]
right_sensors = data[:, 9:16]
left_force = data[:, 17]
right_force = data[:, 18]

# Visualise total force data
plt.plot(time[1:2000], left_force[1:2000], label='Left Foot Total Force')
#plt.plot(time, right_force, label='Right Foot Total Force')
#plt.ylabel('Force (N)')
#plt.legend()
#plt.title('Total Vertical Ground Reaction Force')
plt.show()

