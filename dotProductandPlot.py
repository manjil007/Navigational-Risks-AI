import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('data/closest_entity_results.csv')

print(data.columns)

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

# Check the conditions for the number of entities within radius 3 and the dot product range
# For simplicity, I'm assuming 'Nearest Entity Count' is the count of entities within radius 3
data['one_entity_within_radius_3_and_dot_0_9'] = ((data['Nearest Entity Count'] == 1) &
                                                   (data['dot_product'] >= -1.0) &
                                                   (data['dot_product'] <= 0.9)).astype(int)

data['one_entity_within_radius_3_and_dot_0_8'] = ((data['Nearest Entity Count'] == 1) &
                                                   (data['dot_product'] >= -1.0) &
                                                   (data['dot_product'] <= 0.8)).astype(int)

# Select only the columns you want to save
columns_to_save = ['player_file', 'closest_entity_file', 'player_x_position', 'player_y_position', 'controlX_player', 'controlY_player',
                   'entity_x_position', 'entity_y_position', 'dot_product', 'distance', 'Nearest Entity Count',
                   'one_entity_within_radius_3_and_dot_0_9',
                   'one_entity_within_radius_3_and_dot_0_8']

# Save the selected columns to a new CSV file
data[columns_to_save].to_csv('data/closest_entity_results_with_dot_product.csv', index=False)

print("Dot product and conditions calculated and saved to 'closest_entity_results_with_dot_product_and_conditions.csv'")


# Code for plot starts here
# Create the histogram with bins of size 0.1
bins = [-1 + i * 0.1 for i in range(21)]  # Generates bins from -1 to 1 in steps of 0.1
plt.figure(figsize=(10, 6))
plt.hist(data['dot_product'], bins=bins, edgecolor='black')

# Add labels and title
plt.xlabel('Dot Product')
plt.ylabel('Frequency')
plt.title('Histogram of Dot Product Values')
plt.xticks(bins, rotation=90)  # Set x-ticks to align with bin edges, rotated for readability

plt.savefig('plot/dot_product_histogram_0.1_intervals.png')

# Show the plot
plt.show()



