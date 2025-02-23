import random
import time
 
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, heuristic, DEBUG=False):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    nodes_created = 0

    # Add the start node
    open_list.append(start_node)

    print("Starting A* with start:", start, "and end:", end)

    # Start measuring runtime
    start_time = time.time()

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Print the current node and its f, g, h
        if DEBUG:
            print(f"\nExpanding Node: {current_node.position}, f={current_node.f}, g={current_node.g}, h={current_node.h}")
        #nodes_created += 1

        # Found the goal
        if current_node == end_node:
            path = []
            cost = current_node.g
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            
            end_time = time.time()
            runtime = (end_time - start_time) * 1000  
            print("Total cost:", cost)
            print("Path:", path[::-1])
            print("Nodes created:", nodes_created)
            print(f"Runtime: {runtime:.2f} ms")
            return path[::-1]

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            nodes_created += 1

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + maze[child.position[0]][child.position[1]]

            if heuristic ==  modified_manhattan_distance2:
                child.h = heuristic(child, end_node, maze)
            else:
                child.h = heuristic(child, end_node)
            child.f = child.g + child.h

            if DEBUG:
                print(f"Child Node: {child.position}, g={child.g}, h={child.h}, f={child.f}")

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node:
                    if child.g < open_node.g:
                        open_node.g = child.g
                        open_node.f = child.g + open_node.h
                        open_node.parent = current_node
                    break
            else:
                # Add the child to the open list
                open_list.append(child)


    end_time = time.time()
    runtime = (end_time - start_time) * 1000 
    print("No path found.")
    print(f"Nodes created: {nodes_created}")
    print(f"Runtime: {runtime:.2f} ms")
    print("Total cost: -1")
    print("Path: NULL")
    return []

def manhattan_distance(node, goal):
    return abs(goal.position[0] - node.position[0]) + abs(goal.position[1] - node.position[1])

def all_zeros(node, goal):
    return 0

def manhattan_distance_error(node, goal):
    distance = manhattan_distance(node, goal)
    #add errors from -3 to +3, excluding 0
    error = random.choice([-3, -2, -1, 1, 2, 3])
    final_distance = distance + error
    #we start from 0, because we cant have negative cost
    return max(0,final_distance)

def modified_manhattan_distance(node, goal):
    power=1.2
    return abs(node.position[0] - goal.position[0]) ** power + abs(node.position[1] - goal.position[1]) ** power


def modified_manhattan_distance2(node, goal, maze):
    # Created a heirustic to consider the number of obstacles between points
    distance = manhattan_distance(node,goal)

    min_row = min(node.position[0], goal.position[0])
    max_row = max(node.position[0], goal.position[0])
    min_col = min(node.position[1], goal.position[1])
    max_col = max(node.position[1], goal.position[1])

    obstacles = 0
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if maze[i][j] == 0:
                obstacles += 1
    obstacle_penalty = 1.5
    distance_with_obstacles = distance + (obstacles * obstacle_penalty)
    return distance_with_obstacles


def main(test_case_number, heuristic_fucntion):

    test_cases = {
    1: [[
            [2, 4, 2, 1, 4, 5, 2],
            [0, 1, 2, 3, 5, 3, 1],
            [2, 0, 4, 4, 1, 2, 4],
            [2, 5, 5, 3, 2, 0, 1],
            [4, 3, 3, 2, 1, 0, 1]
        ], (1,2), (4,3)],
    2: [[
            [1, 3, 2, 5, 1, 4, 3],
            [2, 1, 3, 1, 3, 2, 5],
            [3, 0, 5, 0, 1, 2, 2],
            [5, 3, 2, 1, 5, 0, 3],
            [2, 4, 1, 0, 0, 2, 0],
            [4, 0, 2, 1, 5, 3, 4],
            [1, 5, 1, 0, 2, 4, 1]
        ], (3,6), (5,1)],
    3: [[
            [2, 0, 2, 0, 2, 0, 0, 2, 2, 0],
            [1, 2, 3, 5, 2, 1, 2, 5, 1, 2],
            [2, 0, 2, 2, 1, 2, 1, 2, 4, 2],
            [2, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 0, 5, 0, 3, 2, 2, 2],
            [2, 2, 2, 2, 1, 0, 1, 2, 1, 0],
            [1, 0, 2, 1, 3, 1, 4, 3, 0, 1],
            [2, 0, 5, 1, 5, 2, 1, 2, 4, 1],
            [1, 2, 2, 2, 0, 2, 0, 1, 1, 0],
            [5, 1, 2, 1, 1, 1, 2, 0, 1, 2]
        ], (1,2), (8,8)],
    4: [[
            [1, 3, 2, 1, 4],
            [2, 0, 3, 5, 1],
            [3, 2, 1, 0, 2],
            [4, 1, 2, 3, 4],
            [1, 5, 3, 2, 1]
        ], (0,0), (4,4)],
    5: [[
            [1, 0, 2, 1, 4],
            [0, 0, 3, 5, 1],
            [3, 2, 1, 0, 2],
            [4, 1, 2, 3, 4],
            [1, 5, 3, 2, 1]
        ], (0,0), (4,4)],
    6: [[
            [1, 1, 1, 0, 4],
            [0, 0, 1, 0, 1],
            [3, 2, 1, 0, 2],
            [4, 0, 0, 3, 4],
            [1, 5, 3, 2, 1]
        ], (0,0), (4,4)]
    }   

    heuristic_fucntions = {
        1: manhattan_distance,
        2: all_zeros,
        3: manhattan_distance_error,
        4: modified_manhattan_distance,
        5: modified_manhattan_distance2

    }

    astar(test_cases[test_case_number][0], test_cases[test_case_number][1], test_cases[test_case_number][2], heuristic_fucntions[heuristic_fucntion], DEBUG=False)

if __name__ == '__main__':
    while True:
        try:
            choice = int(input("Select a test case (1 - 6) or 7 to print all test cases with both heuristics: "))
            
            if 1 <= choice <= 7:
                break
            else:
                print("Not a valid value. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if choice == 7:
        for test_case in range(1, 7):  
            for heuristic in [1,2,3,4,5]:   
                main(test_case, heuristic)
                print(heuristic)
                print("\n")

    else:
        while True:
            try:
                heuristic_function = input("Enter heuristic function (1 for manhattan_distance, 2 for all_zeros, 3 for manhattan_distance_error): ")

                if 1 <= heuristic_function <= 3:
                    main(choice, heuristic_function)
                    break
                else:
                    print("Not a valid heuristic function. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")