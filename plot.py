import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('data/closest_entity_results_with_dot_product.csv')

total_count = len(data)

# Define the bins and colors for the histogram
bins = [-1 + i * 0.1 for i in range(21)]  # Generates bins from -1 to 1 in steps of 0.1
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']  # Define more colors as needed

# Create an empty list to store the bar information
bars_info = []

# Calculate the frequency for each bin based on the number of nearest entities
for i in range(len(bins) - 1):
    for entity_count in range(1, len(colors) + 1):  # Adjust range based on maximum count of nearest entities
        # Get the dot product values that fall into the current bin and have the correct entity count
        mask = (data['dot_product'] >= bins[i]) & (data['dot_product'] < bins[i+1]) & (data['Nearest Entity Count'] == entity_count)
        # Append the bar information with the count, left edge of the bin, and color
        bars_info.append((mask.sum(), bins[i], colors[entity_count-1]))

# Sort bars_info by the left edge of the bins
bars_info.sort(key=lambda x: x[1])

# Now create the bar plot
plt.figure(figsize=(10, 6))


# Plot each bar and add labels
for bar_count, left_edge, color in bars_info:
    bar = plt.bar(left_edge, bar_count, width=0.1, color=color, edgecolor='black', align='edge')
    # Calculate the percentage
    percentage = (bar_count / total_count) * 100
    # Add text label above each bar if percentage is greater than 2%
    if percentage > 2:
        plt.text(left_edge + 0.1 / 2, bar_count, f'{percentage:.1f}%', ha='center', va='bottom')

# Add labels and title
plt.xlabel('Dot Product')
plt.ylabel('Frequency')
plt.title('Histogram of Dot Product Values by Nearest Entity Count')
plt.xticks(bins, rotation=90)  # Set x-ticks to align with bin edges, rotated for readability

# Add custom legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[i], edgecolor='black', label=f'{i+1} Nearest Entities') for i in range(len(colors))]
plt.legend(handles=legend_elements, title='Nearest Entities Count')

plt.savefig('dot_product_histogram_colored_by_entity_count.png')

# Show the plot
plt.show()
