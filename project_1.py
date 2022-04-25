import numpy as np

# setting up lists used across the program
# input_arr should be starting point matrix, goal_arr is the goal
# visited nodes stores all the visited nodes in the search
input_arr = np.array([[1, 4, 7], [5, 0, 8], [2, 3, 6]])
goal_arr = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 0]])
visited_nodes = []


# setting up Node class, each Node holds the matrix with the variable state, the parent idx and the node idx
class Node:
    # initialized with the matrix and parent index, node idx is set when the node is added to the visited list
    def __init__(self, matrix, parent_idx=None):
        self.val = matrix
        self.parent_idx = parent_idx
        self.idx = None

    # returns string with line of numbers with a space in between to make file from at the end
    def __str__(self):
        one_line = ""
        for i in range(0, 3):
            for j in range(0, 3):
                one_line += str(self.val[i, j]) + " "
        return one_line

    # returns index of blank tile from numpy function
    def blank_tile(self):
        raw_index = np.where(self.val == 0)
        return raw_index[0][0], raw_index[1][0]

    # if the blank tile isn't in the top row, makes new node with blank tile moved up and parent idx set to current idx
    # if in the top row, returns None
    def move_up(self):
        row, col = self.blank_tile()
        if row > 0:
            new_matrix = self.val.copy()
            new_matrix[row, col] = new_matrix[row - 1, col]
            new_matrix[row - 1, col] = 0
            return Node(new_matrix, self.idx)
        else:
            return None

    # following three do the same as above but for down, left, and right
    def move_down(self):
        row, col = self.blank_tile()
        if row < 2:
            new_matrix = self.val.copy()
            new_matrix[row, col] = new_matrix[row + 1, col]
            new_matrix[row + 1, col] = 0
            return Node(new_matrix, self.idx)
        else:
            return None

    def move_left(self):
        row, col = self.blank_tile()
        if col > 0:
            new_matrix = self.val.copy()
            new_matrix[row, col] = new_matrix[row, col - 1]
            new_matrix[row, col - 1] = 0
            return Node(new_matrix, self.idx)
        else:
            return None

    def move_right(self):
        row, col = self.blank_tile()
        if col < 2:
            new_matrix = self.val.copy()
            new_matrix[row, col] = new_matrix[row, col + 1]
            new_matrix[row, col + 1] = 0
            return Node(new_matrix, self.idx)
        else:
            return None

# define Queue class that holds a list and has check to peek at the first value, enqueue to add a value,
# and pop to return the first value
# probably could be more efficient if made like a linked list and not use a python list
class Queue:
    # initialize queue with the start node
    def __init__(self, first_node):
        self.queue = [first_node]

    def check(self):
        return self.queue[0]

    # the enqueue function checks if the input is not None first, as an invalid move returns None
    def enqueue(self, node):
        if node:
            self.queue.append(node)

    def pop(self):
        return self.queue.pop(0)

# loops through parent indexes and makes appends to list of nodes in a single path
# returns reversed list which should start at start node and go to goal node
def generate_path(node):
    curr_node = node
    path_list = []
    while curr_node.parent_idx is not None:
        path_list.append(curr_node)
        curr_node = visited_nodes[curr_node.parent_idx]
    path_list.append(curr_node)
    return path_list[::-1]

# function that computes breadth first search based on start node
# returns goal node and path from start to goal node
def bfs(init_node):
    # reset visited nodes in case the function is repeatedly used for multiple start nodes
    visited_nodes.clear()

    # make an instance of queue for the search starting with first node
    # loop through the queue as long as there is a node in it and pop the initial value
    # if the initial value is not in the visited list, check if goal, if goal return node and path
    # if not goal, attempt every move and add them to the end of the queue
    bfs_queue = Queue(init_node)
    while bfs_queue.check():
        curr_node = bfs_queue.queue.pop(0)
        if not any((curr_node.val == i.val).all() for i in visited_nodes):
            curr_node.idx = len(visited_nodes)
            visited_nodes.append(curr_node)
            if (curr_node.val == goal_arr).all():
                return curr_node, generate_path(curr_node)
            bfs_queue.enqueue(curr_node.move_up())
            bfs_queue.enqueue(curr_node.move_down())
            bfs_queue.enqueue(curr_node.move_left())
            bfs_queue.enqueue(curr_node.move_right())

# runs bfs based on input_arr at top of file
start_node = Node(input_arr)
result_node, result_path = bfs(start_node)

# writes each output file as instructed in the requirements for the project
nodes = open("Nodes.txt", mode='w')
for visited_node in visited_nodes:
    nodes.write(str(visited_node) + "\n")
nodes.close()

node_path = open("nodePath.txt", mode='w')
for path_node in result_path:
    node_path.write(str(path_node) + "\n")
node_path.close()

nodes_info = open("NodesInfo.txt", mode='w')
nodes_info.write("Node_index   Parent_Node_index\n")
for visited_node in visited_nodes:
    nodes_info.write(f"{visited_node.idx} {visited_node.parent_idx}\n")
nodes_info.close()
