import glob
import os
import pandas as pd
import io

# Environment variables for paths
# for data inside game_data folder
root_path = os.getenv('ROOT_PATH')
# for verified.csv
verified_root_path = os.getenv('DATASET')
base_path = "/nfs/ltgroup/TORIN/for_manjil/game_data/"
column_names = ['timestamp', 'posX', 'posY', 'angle', 'accelX', 'accelY', 'velocityX', 'velocityY', 'controlX',
                'controlY', 'disable', 'userControl', 'userInputX', 'userInputY', 'isTouching', 'motionX', 'motionY',
                'motionZ', 'nanoTime']  # Column names for the CSV files


def get_folder_names(csv_file_path):
    """
        Read a CSV file and return a list of folder names.
        Assumes that the second column of the CSV contains the folder names.
    """
    # Read the CSV file
    df = pd.read_csv(os.path.join(verified_root_path, "verified.csv"))

    # Assuming the second column contains folder names
    return df.iloc[:, 1].tolist()


def find_last_row_of_csv(file_path):
    """
        Find the last row of a CSV file by reading from the end.
        Returns the last row as a pandas DataFrame or None if an error occurs.
    """
    try:
        with open(file_path, 'rb') as f:
            f.seek(-2, os.SEEK_END)  # Jump to the second last byte
            while f.read(1) != b'\n':  # Until EOL is found...
                f.seek(-2, os.SEEK_CUR)  # ...jump back, over the read byte plus one more
            last_line = f.readline().decode()  # Read last line

        return pd.read_csv(io.StringIO(last_line), names=column_names, header=None)
    except Exception as e:
        print(f"Error reading last row of file {file_path}: {e}")
        return None


def find_unsuccessful_player_data_files(root_dir, folder_names):
    """
        Find player data files where the player was unsuccessful.
        Checks both the .info.csv and player.data.csv files for specific conditions.
        Returns a list of file paths that match the criteria.
    """
    game_data_files = []
    base_dir = "/nfs/ltgroup"

    for folder_name in folder_names:
        folder_path = os.path.join(root_dir, folder_name, "auto-26b8dc5ecbd2e79e")

        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        pattern = os.path.join(folder_path, "**", "player.*.data.csv")
        matched_files = glob.glob(pattern, recursive=True)
        if not matched_files:
            print(f"No matching files in: {pattern}")

        for file in matched_files:
            try:
                # Check .info.csv file
                info_file = file.replace('.data.csv', '.info.csv')
                if os.path.exists(info_file):
                    info_df = pd.read_csv(info_file)
                    if not info_df.iloc[0, 0]:  # Check second row, first column
                        # Check last row of player.data.csv file for 'userControl'
                        player_df = find_last_row_of_csv(file)
                        if player_df is not None and not player_df.iloc[0]['userControl']:
                            # Trimming the file path
                            absolute_file_path = os.path.join(base_dir, file.split("/", 3)[-1])
                            game_data_files.append(absolute_file_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    return game_data_files


csv_file_path = os.path.join(verified_root_path, "verified.csv")

# Get the folder names from the CSV file
folder_names = get_folder_names(csv_file_path)

# Find all game data files
player_data_files = find_unsuccessful_player_data_files(root_path, folder_names)
print(len(player_data_files))


def find_matching_entity_files(root_dir, player_file_pattern):
    """
        Find entity files that match the level and attempt of player data files.
        Returns a dictionary mapping player files to their corresponding entity files.
    """
    # Dictionary to store player files as keys and a list of corresponding entity files as values
    player_entity_pairs = {}
    base_dir = "/nfs/ltgroup"

    for player_file in player_data_files:
        absolute_player_file = os.path.join(base_dir, player_file)
        # Extract the directory, level (L), and attempt (A) from the player file name
        directory, filename = os.path.split(absolute_player_file)
        level, attempt = filename.split('.')[1:3]

        # Find all entity files in the same directory with matching L and A
        entity_pattern = os.path.join(directory, f"entity.{level}.{attempt}.*.data.csv")
        entity_files = glob.glob(entity_pattern)

        # Add the pair to the dictionary
        player_entity_pairs[player_file] = entity_files

    return player_entity_pairs


# Set the root directory and player file pattern
root_dir = "/nfs/ltgroup/TORIN/for_manjil/game_data"
player_file_pattern = os.path.join(root_dir, "**", "player.*.data.csv")

# Find all matching entity files for each player data file
player_entity_pairs = find_matching_entity_files(root_dir, player_file_pattern)


def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def find_closest_entity(player_file, entity_files):
    """
        Find the closest entity to the player in the last frame of the player's data file.
        Returns the closest entity file name, distance, entity position, and angle.
        Also counts the number of entities within a radius of 3.
    """
    # Read the last row of the player's data file
    last_frame_player = find_last_row_of_csv(player_file)
    player_pos = (last_frame_player['posX'][0], last_frame_player['posY'][0])
    player_angle = last_frame_player['angle'][0]
    closest_entity = None
    min_distance = float('inf')
    closest_entity_pos = None
    facing_same_direction = False
    nearest_entity_angle = float('inf')
    player_controlXY = (last_frame_player['controlX'], last_frame_player['controlY'])
    count = 0

    # Iterate over all player files and find the closest entity
    for entity_file in entity_files:
        last_frame_entity = find_last_row_of_csv(entity_file)
        entity_pos = (last_frame_entity['posX'][0], last_frame_entity['posY'][0])
        entity_angle = last_frame_entity['angle'][0]
        distance = calculate_distance(player_pos[0], player_pos[1], entity_pos[0], entity_pos[1])
        entity_pos = (last_frame_entity['posX'][0], last_frame_entity['posY'][0])

        if distance <= 3:
            count += 1

        # Update closest entity if this one is closer
        if distance < min_distance:
            min_distance = distance
            closest_entity = os.path.basename(entity_file)
            closest_entity_pos = entity_pos
            nearest_entity_angle = entity_angle

    return closest_entity, min_distance, closest_entity_pos, player_angle, nearest_entity_angle, count


# Create a list to hold all the results
results = []

# Iterate over all player files
for player_file, entity_files in player_entity_pairs.items():
    closest_entity, distance, entity_position, player_angle, entity_angle, nearestEntityCount = find_closest_entity(player_file,
                                                                                                entity_files)
    # find_all_entity_within_three_radius(player_file, entity_files, i)

    player_df = pd.read_csv(player_file)
    last_frame_player = player_df.iloc[-1]
    player_pos = (last_frame_player['posX'], last_frame_player['posY'])
    player_control = (last_frame_player['controlX'], last_frame_player['controlY'])

    # Append the result for this player to the results list
    results.append({
        'player_file': player_file,
        'closest_entity_file': closest_entity,
        'player_x_position': player_pos[0],
        'player_y_position': player_pos[1],
        'controlX_player': player_control[0],
        'controlY_player': player_control[1],
        'player_angle': player_angle,
        'entity_x_position': entity_position[0],
        'entity_y_position': entity_position[1],
        'entity_angle': entity_angle,
        'distance': distance,
        'Nearest Entity Count': nearestEntityCount
        # 'facing_same_direction': facing_same_direction
    })

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
results_df.to_csv('closest_entity_results.csv', index=False)

