import heapq  # Used for the priority queue (min heap)
import copy
import time

# Predefined puzzles for testing
trivial = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
very_easy = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
easy = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
doable = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
oh_boy = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
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
#used this article: https://dev.to/catundanatalia/map-and-join-and-strings-2p8 
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(map(str, row)))
    print()

#node class to represent a state in the search
#used these articles: https://www.geeksforgeeks.org/8-puzzle-problem-in-ai/ and https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm
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
#used this article and ta help: https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm
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
#got ta help
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
# used this article: https://www.geeksforgeeks.org/8-puzzle-problem-in-ai/
def trace_solution(node):
    path = []
    while node:
        path.append(node)
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
#used article, ta help and lecture slides: https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm
def solve_puzzle(initial_state, goal_state, heuristic=0):
    root = Node(puzzle=initial_state, h_cost=0)
    priority_queue = []  #priority queue to store nodes
    heapq.heappush(priority_queue, (root.h_cost, root)) 

    max_queue_length = 0  #tracks the max length of the priority queue
    nodesExpanded = 0  #counts the number of nodes expanded

    while priority_queue:
        if len(priority_queue) > max_queue_length:  #updates the max queue length
            max_queue_length = len(priority_queue)

        cost, current_node = heapq.heappop(priority_queue)  #gets node with the lowest cost

        if current_node.puzzle == goal_state: 
            depth = current_node.depth  # Solution depth
            return trace_solution(current_node), depth, max_queue_length, nodesExpanded  # Return values
        
        nodesExpanded += 1  #increments the number of nodes expanded
        #generates all possible moves/children
        generate_children(current_node, goal_state, heuristic)

        # adds only valid and unvisited children to the priority queue
        for child in [current_node.child1, current_node.child2, current_node.child3, current_node.child4]:
            if child and not is_revisited(child):  #ignores already explored states
                heapq.heappush(priority_queue, (child.h_cost, child))

    return None,None,None,max_queue_length,nodesExpanded 

#calcluates the Misplaced Tiles heuristic
#used lecture slides
def misplaced_tiles(state, goal_state):
    #changed from 3 to n so it works for any size puzzle
    n = len(goal_state)
    return sum(
        1 for i in range(n) 
            for j in range(n) 
                if state[i][j] != 0 and state[i][j] != goal_state[i][j]
    )

#calcluates the Manhattan Distance heuristic
#used lecture slides and this article: https://www.educative.io/answers/how-to-solve-the-8-puzzle-problem-using-the-a-star-algorithm
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
    startTime=time.perf_counter() #starting the timer
    if algorithm == "1":
        print("You selected Uniform Cost Search.")
        solution, depth, max_queue_length, nodes_expanded = solve_puzzle(puzzle, goal_state, heuristic=0)
    elif algorithm == "2":
        print("You selected A* with the Misplaced Tile Heuristic.")
        solution, depth, max_queue_length, nodes_expanded = solve_puzzle(puzzle, goal_state, heuristic=misplaced_tiles)
    elif algorithm == "3":
        print("You selected A* with the Manhattan Distance Heuristic.")
        solution, depth, max_queue_length, nodes_expanded = solve_puzzle(puzzle, goal_state, heuristic=manhattan_distance)
    else:
        print("Invalid algorithm choice. Exiting program.")
        return

    # outputs the solution, depth, and time
    if solution:
        endTime = time.perf_counter()
        print("\nYAYYY!! Solution found!")
        print("Depth:", depth)
        print("Time taken:", round(endTime - startTime, 4), "seconds")
        print("\nHere are the steps to solve:")
        for step in solution:
            print(f"The best state to expand with g(n): {step.depth} and h(n): {step.h_cost} is...")
            print_puzzle(step.puzzle)
    else:
        print(" OH NO! No solution found :(")
    #Print max queue length and number of nodes expanded
    print(f"Max queue length: {max_queue_length}")
    print(f"Nodes expanded: {nodes_expanded}")

if __name__ == "__main__":
    main()