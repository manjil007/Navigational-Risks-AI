import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the data
data = pd.read_csv('data/entity_within_one_radius.csv')

# Calculate the vector A (from player to entity)
data['vector_a_x'] = data['entity_x_position'] - data['player_x_position']
data['vector_a_y'] = data['entity_y_position'] - data['player_y_position']

# Calculate the magnitude of vector A
data['magnitude_a'] = np.sqrt(data['vector_a_x']**2 + data['vector_a_y']**2)

# Normalize vector A to a unit vector
data['unit_vector_a_x'] = data['vector_a_x'] / data['magnitude_a']
data['unit_vector_a_y'] = data['vector_a_y'] / data['magnitude_a']

# Calculate the magnitude of vector B (player's facing direction)
data['magnitude_b'] = np.sqrt(data['controlX_player']**2 + data['controlY_player']**2)

# Normalize vector B to a unit vector
data['unit_vector_b_x'] = data['controlX_player'] / data['magnitude_b']
data['unit_vector_b_y'] = data['controlY_player'] / data['magnitude_b']

# Calculate the dot product of A_bar and B_bar
data['dot_product'] = (data['unit_vector_a_x'] * data['unit_vector_b_x'] +
                       data['unit_vector_a_y'] * data['unit_vector_b_y'])

# Select only the columns you want to save
columns_to_save = ['player_x_position', 'player_y_position', 'controlX_player', 'controlY_player',
                   'entity_x_position', 'entity_y_position', 'dot_product']

# Save the selected columns to a new CSV file
data[columns_to_save].to_csv('entity_within_one_with_dot_product.csv', index=False)

print("Dot product calculated and saved to 'entity_within_three_with_dot_product.csv'")


# Load the data from CSV
data = pd.read_csv('data/entity_within_one_with_dot_product.csv')  # Update the path to your CSV file


# Translate the entities' positions to be relative to the player's position
data['relative_entity_x'] = data['entity_x_position'] - data['player_x_position']
data['relative_entity_y'] = data['entity_y_position'] - data['player_y_position']

# Plot the relative positions of the entities
plt.figure(figsize=(12, 12))  # Increase figure size
plt.scatter(data['relative_entity_x'], data['relative_entity_y'], c='blue', label='Entities', s=50)  # Increase marker size with s parameter
plt.scatter(0, 0, c='red', label='Player', s=100)  # Player at the origin with a larger marker

# Add labels and legend
plt.xlabel('X Position (relative to player)')
plt.ylabel('Y Position (relative to player)')
plt.title('Entities Around the Player When Killed')
plt.legend()
plt.grid(True)

# Set axis limits if necessary
# Here we're taking the maximum absolute value for x and y to set symmetrical limits
max_x = max(abs(data['relative_entity_x'].min()), data['relative_entity_x'].max(), key=abs)
max_y = max(abs(data['relative_entity_y'].min()), data['relative_entity_y'].max(), key=abs)
plt.xlim(-max_x-1, max_x+1)
plt.ylim(-max_y-1, max_y+1)

# Ensure equal aspect ratio
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()