import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Existing code to obtain 'indv', 'tasks', 'robots', 'task_pos', 'robot_pos'
NUM_ROBOTS = 4

ROBOT_POS = [[1,0], [4,0], [7,0], [10, 0]]

task_dict = {
    0: [[1, 1], 5],
    1: [[1, 2], 5],
    2: [[0, 1], 5],
    3: [[3, 2], 5],
    4: [[3, 4], 5],
    5: [[3, 3], 5],
    6: [[7, 6], 5],
    7: [[8, 6], 5],
    8: [[7, 8], 5],
    9: [[8, 8], 5],
    10: [[0, 3], 5],
    11: [[0, 4], 5],
    12: [[1, 6], 5],
    13: [[2, 6], 5],
    14: [[4, 6], 5],
    15: [[5, 3], 5],
    16: [[7, 4], 5],
    17: [[5, 7], 5],
    18: [[8, 2], 5],
    19: [[10, 4], 5],
    20: [[11, 6], 5],
}

robot_dict = {
    1: [1, 0],
    2: [3, 0],
    3: [5, 0],
    4: [7, 0]
}

coordinates_list = [info[0] for info in task_dict.values()]
TASK_POS = coordinates_list
NUM_TASKS = len(TASK_POS)

############################## MAIN VIZ CODE ###########################
indv = [3, 7, 19, 9, 2, 8, 20, 10, 17, 11, 5, 15, 6, 4, 16, 14, 1, 13, 12, 0, 18, 2, 4, 3, 4, 1, 4, 3, 1, 3, 1, 2, 3, 4, 2, 4, 2, 1, 2, 2, 1, 4]
tasks = (indv[:NUM_TASKS])
robots = (indv[NUM_TASKS:])

def sub1(n):
    return n - 1  # Adjust robot indices to start from 0
robots = list(map(sub1, robots))

task_pos = TASK_POS  # List of task positions
robot_pos = ROBOT_POS  # List of robot positions

pairs = list(zip(tasks, robots))

# Create a dictionary mapping robots to their task sequences
robot_task_sequences = {}
for robot_index in set(robots):
    robot_tasks = [pair[0] for pair in pairs if pair[1] == robot_index]
    robot_task_sequences[robot_index] = robot_tasks

# Settings
grid_size = (12, 14)
robot_colors = ['red', 'blue', 'green', 'orange']
task_marker = 's'  # Square for tasks
robot_marker = 'o'  # Circle for robots
path_alpha = 0.7  # Transparency for paths
speed = 1.0  # Units per time unit
time_step = 0.1  # Time units per frame

# Compute interpolated paths
robot_paths = {}
max_steps = 0

for robot_index in robot_task_sequences:
    # Initial position of the robot
    start_pos = robot_pos[robot_index]
    start_pos = (start_pos[0], start_pos[1], 0)  # Ensure it's a 3D point
    # Sequence of tasks assigned to the robot
    task_sequence = robot_task_sequences[robot_index]
    # List to store positions and times
    positions = [start_pos]
    times = [0.0]
    current_pos = start_pos
    current_time = 0.0

    # Iterate through assigned tasks
    for task_num in task_sequence:
        # Get task position
        task_p = task_pos[task_num]
        task_p = (task_p[0], task_p[1], 0)  # Ensure it's a 3D point
        # Calculate distance and travel time
        dist = np.hypot(task_p[0] - current_pos[0], task_p[1] - current_pos[1])
        travel_time = dist / speed
        num_steps = max(int(travel_time / time_step), 1)
        # Interpolate positions
        x_vals = np.linspace(current_pos[0], task_p[0], num_steps)
        y_vals = np.linspace(current_pos[1], task_p[1], num_steps)
        z_vals = np.zeros(num_steps)
        segment_positions = list(zip(x_vals, y_vals, z_vals))
        # Append positions and times
        positions.extend(segment_positions[1:])
        times.extend([current_time + time_step * i for i in range(1, num_steps)])
        current_time += travel_time
        current_pos = task_p  # current_pos is already 3D

    # Return to initial position
    dist = np.hypot(start_pos[0] - current_pos[0], start_pos[1] - current_pos[1])
    travel_time = dist / speed
    num_steps = max(int(travel_time / time_step), 1)
    x_vals = np.linspace(current_pos[0], start_pos[0], num_steps)
    y_vals = np.linspace(current_pos[1], start_pos[1], num_steps)
    z_vals = np.zeros(num_steps)
    segment_positions = list(zip(x_vals, y_vals, z_vals))
    positions.extend(segment_positions[1:])
    times.extend([current_time + time_step * i for i in range(1, num_steps)])
    current_time += travel_time

    # Store positions and times
    robot_paths[robot_index] = {'positions': positions, 'times': times}
    max_steps = max(max_steps, len(positions))

# Pad paths to ensure all have the same length
for robot_index in robot_paths:
    positions = robot_paths[robot_index]['positions']
    times = robot_paths[robot_index]['times']
    if len(positions) < max_steps:
        last_pos = positions[-1]
        positions.extend([last_pos] * (max_steps - len(positions)))
        last_time = times[-1]
        times.extend([last_time] * (max_steps - len(times)))
        robot_paths[robot_index]['positions'] = positions
        robot_paths[robot_index]['times'] = times

# Set up the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Set axes labels and limits
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_xlim(0, grid_size[0])
ax.set_ylim(0, grid_size[1])
ax.set_zlim(0, 1)  # Since z=0 for all points

# Plot tasks with labels
for i, pos in enumerate(task_pos):
    ax.scatter(pos[0], pos[1], 0, c='grey', s=50, marker=task_marker, label='Task' if i == 0 else "", zorder=2)
    ax.text(pos[0], pos[1], 0, f'T{i+1}', fontsize=8, ha='center', va='center_baseline', zorder=3)

# Plot the paths for each robot
for idx, robot_data in robot_paths.items():
    positions = robot_data['positions']
    xs, ys, zs = zip(*positions)
    ax.plot(xs, ys, zs, color=robot_colors[idx], linewidth=2, linestyle='--', label=f'Robot {idx+1} Path')

# Initialize scatter plots for robots
robot_scatters = []
for idx, color in enumerate(robot_colors):
    x, y, z = robot_paths[idx]['positions'][0]
    scatter = ax.scatter(x, y, z, c=color, s=100, marker=robot_marker)
    robot_scatters.append(scatter)

# Create a legend
ax.legend()

# Define the update function
def update(frame):
    for idx, scatter in enumerate(robot_scatters):
        x, y, z = robot_paths[idx]['positions'][frame]
        # Update the positions
        scatter._offsets3d = (np.array([x]), np.array([y]), np.array([z]))
    return robot_scatters

# Verify data
for idx, robot_data in robot_paths.items():
    print(f"Robot {idx} path length: {len(robot_data['positions'])}")
    print(f"First position: {robot_data['positions'][0]}")
    print(f"Last position: {robot_data['positions'][-1]}")

# Create the animation
anim = FuncAnimation(fig, update, frames=max_steps, interval=100, blit=False)

# Display the animation
plt.show()
