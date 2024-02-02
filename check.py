import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data/closest_entity_results.csv')

# Normalize the entity positions relative to the player
data['relative_entity_x'] = data['entity_x_position'] - data['player_x_position']
data['relative_entity_y'] = data['entity_y_position'] - data['player_y_position']

# Plotting
plt.figure(figsize=(8, 8))
plt.scatter(data['relative_entity_x'], data['relative_entity_y'], label='Entities')
plt.scatter([0], [0], color='red', label='Player')  # Player at origin

# Add labels and title
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Entity Positions Relative to Player')
plt.axhline(0, color='grey', lw=1)
plt.axvline(0, color='grey', lw=1)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
