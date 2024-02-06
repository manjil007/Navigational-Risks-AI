import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data/closest_entity_results_with_dot_product.csv')

# Plotting the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(data['dot_product'], data['Nearest Entity Count'], alpha=0.5)  # alpha for transparency

# Add labels and title
plt.xlabel('Dot Product (Obstacle Heading)')
plt.ylabel('Number of Nearest Entities')
plt.title('Scatter Plot of Collisions by Obstacle Heading and Nearest Entity Count')
plt.grid(True)

plt.savefig('plot/dot_product_scatterplot_colored_by_entity_count.png')
# Show the plot
plt.show()
