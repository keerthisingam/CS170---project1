import heapq  # Used for the priority queue (min heap)
import copy

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

#function to print the puzzle in a readable format
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(map(str, row)))
    print()

#node class to represent a state in the search
class Node:
    def __init__(self, puzzle, parent=None, depth=0, h_cost=0):
        self.puzzle = puzzle  # Current puzzle state (2D list)
        self.parent = parent  # Reference to the parent node
        self.depth = depth  # Depth (g(n)): Cost to reach this node
        self.h_cost = h_cost  # Heuristic cost (h(n))
        self.child1 = None  # First child (e.g., move up)
        self.child2 = None  # Second child (e.g., move down)
        self.child3 = None  # Third child (e.g., move left)
        self.child4 = None  # Fourth child (e.g., move right)
    def __lt__(self, other):
        return (self.depth + self.h_cost) < (other.depth + other.h_cost)

# finds all possible moves of the blank tile and returns new puzzle states
def get_neighbors(state):
    neighbors = []
    blank_row, blank_col = None, None
    #fnds where the blank tile is
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                blank_row, blank_col = i, j
                break 
    # Move Up
    new_row, new_col = blank_row - 1, blank_col
    if 0 <= new_row < len(state): 
        new_state = copy.deepcopy(state)  
        new_state[blank_row][blank_col], new_state[new_row][new_col] = (
            new_state[new_row][new_col],
            new_state[blank_row][blank_col],
        ) 
        neighbors.append(new_state)  
    # Move Down
    new_row, new_col = blank_row + 1, blank_col
    if 0 <= new_row < len(state):  
        new_state = copy.deepcopy(state)  
        new_state[blank_row][blank_col], new_state[new_row][new_col] = (
            new_state[new_row][new_col],
            new_state[blank_row][blank_col],
        )
        neighbors.append(new_state)
    # Move Left
    new_row, new_col = blank_row, blank_col - 1
    if 0 <= new_col < len(state[0]):  
        new_state = copy.deepcopy(state)  
        new_state[blank_row][blank_col], new_state[new_row][new_col] = (
            new_state[new_row][new_col],
            new_state[blank_row][blank_col],
        )
        neighbors.append(new_state)
    # Move Right
    new_row, new_col = blank_row, blank_col + 1
    if 0 <= new_col < len(state[0]):  
        new_state = copy.deepcopy(state)  
        new_state[blank_row][blank_col], new_state[new_row][new_col] = (
            new_state[new_row][new_col],
            new_state[blank_row][blank_col],
        )
        neighbors.append(new_state)
    return neighbors

#generates and assigns children nodes
def generate_children(node, goal_state, heuristic=0):
    neighbors = get_neighbors(node.puzzle)  #gets all the valid neighbors
    if len(neighbors) > 0:
        node.child1 = Node(
            puzzle=neighbors[0], parent=node, depth=node.depth + 1,
            h_cost=(node.depth + 1 + (heuristic(neighbors[0], goal_state) if heuristic else 0))
        )
    if len(neighbors) > 1:
        node.child2 = Node(
            puzzle=neighbors[1], parent=node, depth=node.depth + 1,
            h_cost=(node.depth + 1 + (heuristic(neighbors[1], goal_state) if heuristic else 0))
        )
    if len(neighbors) > 2:
        node.child3 = Node(
            puzzle=neighbors[2], parent=node, depth=node.depth + 1,
            h_cost=(node.depth + 1 + (heuristic(neighbors[2], goal_state) if heuristic else 0))
        )
    if len(neighbors) > 3:
        node.child4 = Node(
            puzzle=neighbors[3], parent=node, depth=node.depth + 1,
            h_cost=(node.depth + 1 + (heuristic(neighbors[3], goal_state) if heuristic else 0))
        )

#backtracks the solution path to help you see all the steps you took
def trace_solution(node):
    path = []
    while node:
        path.append(node.puzzle)
        node = node.parent
    return list(reversed(path))

#function to check if a node's puzzle state has been seen before
def is_revisited(child):
    parent = child.parent
    while parent:
        if child.puzzle == parent.puzzle:
            return True
        parent = parent.parent 
    return False 

#solves function with Uniform Cost Search and A*
def solve_puzzle(initial_state, goal_state, heuristic=0):
    root = Node(puzzle=initial_state, h_cost=0)
    priority_queue = []  #priority queue to store nodes
    heapq.heappush(priority_queue, (root.h_cost, root)) 
    while priority_queue:
        cost, current_node = heapq.heappop(priority_queue)  #gets node with the lowest cost

        if current_node.puzzle == goal_state: 
            return trace_solution(current_node)

        #generates all possible moves/children
        generate_children(current_node, goal_state, heuristic)

        # adds only valid and unvisited children to the priority queue
        for child in [current_node.child1, current_node.child2, current_node.child3, current_node.child4]:
            if child and not is_revisited(child):  #ignores already explored states
                heapq.heappush(priority_queue, (child.h_cost, child))

    return None 

# Calcluates the Misplaced Tiles heuristic
def misplaced_tiles(state, goal_state):
    #changed from 3 to n so it works for any size puzzle
    n = len(goal_state)
    return sum(
        1 for i in range(n) 
            for j in range(n) 
                if state[i][j] != 0 and state[i][j] != goal_state[i][j]
    )
# Calcluates the Manhattan Distance heuristic
def manhattan_distance(state, goal_state):
    distance = 0
    #changed from 3 to n so it works for any size puzzle
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if state[i][j] != 0:
                value = state[i][j]
                goal_i, goal_j = divmod(value - 1, n)
                distance += abs(i - goal_i) + abs(j - goal_j) #formula for manhattan distance
    return distance

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

    goal_state = eight_goal_state  # Goal state is predefined

    if algorithm == "1":
        print("You selected Uniform Cost Search.")
        solution = solve_puzzle(puzzle, goal_state, heuristic=0)
    elif algorithm == "2":
        print("You selected A* with the Misplaced Tile Heuristic.")
        solution = solve_puzzle(puzzle, goal_state, heuristic=misplaced_tiles)
    elif algorithm == "3":
        print("You selected A* with the Manhattan Distance Heuristic.")
        solution = solve_puzzle(puzzle, goal_state, heuristic=manhattan_distance)
    else:
        print("Invalid algorithm choice. Exiting program.")
        return

    # Output the solution
    if solution:
        print("\n YAYYY!! Solution found! Here are the steps to solve:")
        for step in solution:
            print_puzzle(step)
    else:
        print(" OH NO! No solution found :(")

if __name__ == "__main__":
    main()
