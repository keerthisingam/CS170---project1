import heapq  # Used for the priority queue

# Predefined puzzles for testing
trivial = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
very_easy = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
easy = [[1, 2, 0], [4, 5, 3], [7, 8, 6]]
doable = [[0, 1, 2], [4, 5, 3], [7, 8, 6]]
oh_boy = [[8, 7, 1], [6, 0, 2], [5, 4, 3]]
eight_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Function to initialize the default puzzle
def init_default_puzzle_mode():
    selected_difficulty = input(
        "You wish to use a default puzzle. Please enter a difficulty on a scale from 0 to 4.\n"
    )
    if selected_difficulty == "0":
        print("Difficulty 'Trivial' selected.")
        return trivial
    elif selected_difficulty == "1":
        print("Difficulty 'Very Easy' selected.")
        return very_easy
    elif selected_difficulty == "2":
        print("Difficulty 'Easy' selected.")
        return easy
    elif selected_difficulty == "3":
        print("Difficulty 'Doable' selected.")
        return doable
    elif selected_difficulty == "4":
        print("Difficulty 'Oh Boy' selected.")
        return oh_boy
    else:
        print("Invalid difficulty selected. Defaulting to 'Trivial'.")
        return trivial

# Function to print the puzzle in a readable format
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(map(str, row)))
    print()

# Function to handle the main program flow
def main():
    print("Welcome to the 8-Puzzle Solver!")
    puzzle_mode = input(
        "Type '1' to use a default puzzle, or '2' to create your own.\n"
    )

    # Handle default or custom puzzle input
    if puzzle_mode == "1":
        puzzle = init_default_puzzle_mode()
    elif puzzle_mode == "2":
        print(
            "Enter your puzzle, using 0 to represent the blank space. "
            "Enter each row as space-separated numbers."
        )
        puzzle = []
        for i in range(3):
            row = list(map(int, input(f"Enter row {i + 1}: ").split()))
            puzzle.append(row)
    else:
        print("Invalid option. Exiting program.")
        return

    # Print the selected puzzle
    print("\nYour puzzle is:")
    print_puzzle(puzzle)

    # Select the algorithm to solve the puzzle
    algorithm = input(
        "Select the algorithm to solve the puzzle:\n"
        "(1) Uniform Cost Search\n"
        "(2) A* with the Misplaced Tile Heuristic\n"
        "(3) A* with the Manhattan Distance Heuristic\n"
    )

    if algorithm == "1":
        print("You selected Uniform Cost Search.")
        # Call the Uniform Cost Search algorithm here
        uniform_cost_search(puzzle)
    elif algorithm == "2":
        print("You selected A* with the Misplaced Tile Heuristic.")
        # Call the A* algorithm with the misplaced tile heuristic here
        misplaced_tile(puzzle)  # Placeholder
    elif algorithm == "3":
        print("You selected A* with the Manhattan Distance Heuristic.")
        # Call the A* algorithm with the Manhattan Distance heuristic here
        manhattan_distance(puzzle)  # Placeholder
    else:
        print("Invalid algorithm choice. Exiting program.")
        return

# Placeholder function for Uniform Cost Search (to be implemented)
def uniform_cost_search(puzzle):
    print("Uniform Cost Search not implemented yet.")
    # This is where the solving logic will go

# Placeholder function for Uniform Cost Search (to be implemented)
def misplaced_tile(puzzle):
    print("A* not implemented yet.")
    # This is where the solving logic will go

    # Placeholder function for Uniform Cost Search (to be implemented)
def manhattan_distance(puzzle):
    print("A* not implemented yet.")
    # This is where the solving logic will go

# Run the main program
if __name__ == "__main__":
    main()
