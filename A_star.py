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


def astar(maze, start, end, DEBUG=False):
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
        nodes_created += 1

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

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + maze[child.position[0]][child.position[1]]
            child.h = manhattan_distance(current_node, end_node)
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

def main():

    # Test Case 1
    maze1 = [
        [2, 4, 2, 1, 4, 5, 2],
        [0, 1, 2, 3, 5, 3, 1],
        [2, 0, 4, 4, 1, 2, 4],
        [2, 5, 5, 3, 2, 0, 1],
        [4, 3, 3, 2, 1, 0, 1]
    ]
    start1 = (1, 2)
    end1 = (4, 3)

    # Test Case 2
    maze2 = [
        [1, 3, 2, 5, 1, 4, 3],
        [2, 1, 3, 1, 3, 2, 5],
        [3, 0, 5, 0, 1, 2, 2],
        [5, 3, 2, 1, 5, 0, 3],
        [2, 4, 1, 0, 0, 2, 0],
        [4, 0, 2, 1, 5, 3, 4],
        [1, 5, 1, 0, 2, 4, 1]
    ]
    start2 = (3, 6)
    end2 = (5, 1)

    # Test Case 3
    maze3 = [
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
    ]
    start3 = (8, 8)
    end3 = (1, 2)

    # Test Case 4
    maze4 = [
        [1, 3, 2, 1, 4],
        [2, 0, 3, 5, 1],
        [3, 2, 1, 0, 2],
        [4, 1, 2, 3, 4],
        [1, 5, 3, 2, 1]
    ]
    start4 = (0, 0)
    end4 = (4, 4)

    # Test Case 5
    maze5 = [
        [1, 0, 2, 1, 4],
        [0, 0, 3, 5, 1],
        [3, 2, 1, 0, 2],
        [4, 1, 2, 3, 4],
        [1, 5, 3, 2, 1]
    ]
    start5 = (0, 0)
    end5 = (4, 4)

    # Test Case 6
    maze6 = [
        [1, 1, 1, 0, 4],
        [0, 0, 1, 0, 1],
        [3, 2, 1, 0, 2],
        [4, 0, 0, 3, 4],
        [1, 5, 3, 2, 1]
    ]
    start6 = (0, 0)
    end6 = (4, 4)

    print("\nMaze 1")
    path = astar(maze1, start1, end1, DEBUG=False)
    print("\nMaze 2")
    path = astar(maze2, start2, end2, DEBUG=False)
    print("\nMaze 3")
    path = astar(maze3, start3, end3, DEBUG=False)
    print("\nMaze 4")
    path = astar(maze4, start4, end4, DEBUG=False)
    print("\nMaze 5")
    path = astar(maze5, start5, end5, DEBUG=False)
    print("\nMaze 6")
    path = astar(maze6, start6, end6, DEBUG=False)


if __name__ == '__main__':
    main()