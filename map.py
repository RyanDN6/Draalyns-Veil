import random

def generateRandomMap(matrix_width, matrix_height, symbol, num_groups, group_size_range):
    """
    Generate a simple map with random groups of symbols.

    Parameters:
    - matrix_width (int): The width of the map.
    - matrix_height (int): The height of the map.
    - symbol (str): The symbol to place on the map (e.g., '^' for mountains).
    - num_groups (int): Number of groups of symbols to create.
    - group_size_range (tuple): The range of group sizes (min, max) to randomly generate.

    Returns:
    - matrix (list of list): A map (matrix) with random groups of the symbol.
    """
    
    # Create a matrix filled with '.'
    matrix = [["." for _ in range(matrix_width)] for _ in range(matrix_height)]

    for _ in range(num_groups):
        # Pick a random starting point for the group
        start_x = random.randint(0, matrix_width - 1)
        start_y = random.randint(0, matrix_height - 1)
        
        # Randomly determine the size of the group (how many symbols to place)
        group_size = random.randint(*group_size_range)

        # Place the symbols for this group
        for _ in range(group_size):
            # Offset the placement within a small random range around the start
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            # Calculate new positions, ensuring we're within the matrix boundaries
            new_x = max(0, min(matrix_width - 1, start_x + offset_x))
            new_y = max(0, min(matrix_height - 1, start_y + offset_y))
            
            # Place the symbol on the map
            matrix[new_y][new_x] = symbol

    return matrix

def generateRiver(matrix, flow_direction="random", symbol="~", num_bridges=3, bridge_symbol="#", min_bridge_distance=6):
    """
    Generate a river on the existing matrix with specified flow direction and optional bridges.
    
    Parameters:
    - matrix (list of list): The matrix representing the map.
    - flow_direction (str): Direction of river flow. Options:
        "random": randomly choose between left-to-right or top-to-bottom
        "left-right": flows from left edge to right
        "top-down": flows from top edge to bottom
    - symbol (str): The symbol to represent the river (default is '~').
    - num_bridges (int): Number of bridge symbols to add across the river (default is 0).
    - bridge_symbol (str): The symbol to represent bridges (default is '#').
    - min_bridge_distance (int): Minimum distance between bridges (default is 5).
    
    Returns:
    - matrix (list of list): The modified map with a river and bridges.
    """
    
    height = len(matrix)
    width = len(matrix[0])
    river_path = []  # To keep track of river coordinates
    
    # Set starting position and direction based on flow_direction
    if flow_direction == "random":
        flow_direction = random.choice(["left-right", "top-down"])
    
    if flow_direction == "left-right":
        start_x = 0
        start_y = random.randint(5, height - 6)
        direction = "right"
    elif flow_direction == "top-down":
        start_x = random.randint(10, width - 11)
        start_y = 0
        direction = "down"
    else:
        raise ValueError("Invalid flow direction. Please choose from: 'random', 'left-right', 'top-down'")
    
    current_x, current_y = start_x, start_y
    
    # Create the river path
    while True:
        # Place the river symbol in the current position and add to river_path
        matrix[current_y][current_x] = symbol
        river_path.append((current_y, current_x))
        
        # Move in the chosen direction with slight random deviations
        if direction == "right":
            current_x += 1
            current_y += random.choice([-1, 0, 0, 0, 1])  # Bias towards straight movement
        elif direction == "down":
            current_y += 1
            current_x += random.choice([-1, 0, 0, 0, 1])
        
        # Check if we've reached the boundary
        if current_x < 0 or current_x >= width or current_y < 0 or current_y >= height:
            break
        
        # Prevent the river from moving out of bounds
        current_x = max(0, min(current_x, width - 1))
        current_y = max(0, min(current_y, height - 1))
    
    # Add bridges if requested
    if num_bridges > 0 and len(river_path) > num_bridges * min_bridge_distance:
        # Filter river path to ensure minimum distance between bridges
        potential_bridge_positions = []
        last_bridge_position = -min_bridge_distance  # Initialize far enough to allow first bridge
        
        for i, position in enumerate(river_path):
            if i - last_bridge_position >= min_bridge_distance:
                potential_bridge_positions.append(position)
                last_bridge_position = i  # Update position of the last placed bridge candidate
        
        # Randomly select bridge positions from the filtered list
        bridge_positions = random.sample(potential_bridge_positions, num_bridges)
        for y, x in bridge_positions:
            matrix[y][x] = bridge_symbol  # Replace river tile with bridge

    return matrix


def generateClusters(matrix, symbol, clusters_count, cluster_size_range):
    """
    Generate multiple connected clusters of symbols on a map.

    Parameters:
    - matrix (list of list): The existing matrix to add clusters to.
    - symbol (str): The symbol to place on the map (e.g., '^' for mountains).
    - clusters_count (int): Number of clusters to generate.
    - cluster_size_range (tuple): The range of cluster sizes (min, max) to randomly generate.

    Returns:
    - matrix (list of list): A map (matrix) with the specified number of connected clusters.
    """
    
    matrix_width = len(matrix[0])
    matrix_height = len(matrix)
    
    for _ in range(clusters_count):
        # Randomly determine size for this cluster
        cluster_size = random.randint(*cluster_size_range)
        
        # Pick a random starting point for the cluster
        start_x = random.randint(0, matrix_width - 1)
        start_y = random.randint(0, matrix_height - 1)
        
        # List of points to expand from, starting with the initial point
        points_to_expand = [(start_x, start_y)]
        
        # Place the first symbol
        matrix[start_y][start_x] = symbol
        placed_symbols = 1
        
        # Directions for expansion (up, down, left, right, and diagonals)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Expand this cluster until the desired cluster size is reached
        while placed_symbols < cluster_size and points_to_expand:
            # Choose a random point to expand from
            current_x, current_y = random.choice(points_to_expand)
            
            # Try expanding in random directions
            random.shuffle(directions)  # Shuffle directions to add randomness
            for direction in directions:
                new_x = current_x + direction[0]
                new_y = current_y + direction[1]
                
                # Ensure the new point is within the matrix boundaries and not yet filled
                if (0 <= new_x < matrix_width and 
                    0 <= new_y < matrix_height and 
                    matrix[new_y][new_x] == "."):
                    # Place the symbol and add the new point to the list for future expansion
                    matrix[new_y][new_x] = symbol
                    points_to_expand.append((new_x, new_y))
                    placed_symbols += 1
                    
                    # Stop if we have placed enough symbols for this cluster
                    if placed_symbols >= cluster_size:
                        break
            
            # If no valid expansion happened from this point, remove it
            points_to_expand.remove((current_x, current_y))
    
    return matrix

def addVillage(matrix, position=None):
    """
    Add a village ASCII art to the matrix at specified position or random valid position.
    The village looks like:
           +
          A_
         /\\.\\
    jgs  *||"|*
       ~^~^~^~^

    Parameters:
    - matrix (list of list): The existing matrix to add the village to.
    - position (tuple): Optional (x, y) position for the bottom-left of the village.
                       If None, a random valid position will be chosen.

    Returns:
    - matrix (list of list): The modified matrix with the village added.
    - position (tuple): The (x, y) position where the village was placed, or None if placement failed.
    """
    
    # Village dimensions
    village_width = 8
    village_height = 10
    
    # Get matrix dimensions
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    
    # Define the village layout (each line of the ASCII art)
    village = [
        "   +   ",
        "   A_  ",
        "  /\\-\\ ",
        "  ||\\-| ",
        "  ¬¬¬¬¬"
    ]
    
    # If no position provided, find a random valid position
    if position is None:
        # Try up to 100 times to find a valid position
        for _ in range(500):
            # Generate random position (accounting for village size)
            x = random.randint(0, matrix_width - village_width)
            y = random.randint(0, matrix_height - village_height)
            
            # Check if position is valid (no other features in the way)
            valid = True
            for dy in range(village_height):
                for dx in range(village_width):
                    if matrix[y + dy][x + dx] != ".":
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                position = (x, y)
                break
        else:
            # If we couldn't find a valid position after 100 tries
            return matrix, None
    
    # Validate the provided/found position
    x, y = position
    if (x < 0 or x + village_width > matrix_width or 
        y < 0 or y + village_height > matrix_height):
        return matrix, None
    
    # Add the village to the matrix
    for dy, line in enumerate(village):
        for dx, char in enumerate(line):
            if char != " ":  # Only place non-space characters
                matrix[y + dy][x + dx] = char
    
    return matrix

def displayMap(matrix):

    width = len(matrix[0]) * 2 + 1

    print("-" * width)
    for i in range(len(matrix)):
        print("|" + " ".join(matrix[i]) + "|")
    
    print("-" * width)

def spawn(matrix, village=True, random=False, safe="."):

    while True:
        if random:
            x = random.randint(0, len(matrix[0]) - 1)
            y = random.randint(0, len(matrix) - 1)

            if matrix[y][x] == safe:
                return (x, y)
        
        else:
            x = 0
            y = 0
            for y in range(len(matrix)):
                for x in range(len(matrix[0]) - 1):
                    if matrix[y][x] == "|" == matrix[y][x + 1]:
                        return (x, y)

