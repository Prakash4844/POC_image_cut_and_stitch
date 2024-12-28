# Author: Prakash Sahu <github.com/prakash4844> <pk484442@gmail.com>

# This file contains code for serializing the image cut resolution data into desired data format.
class TreeNode:
    def __init__(self, position, resolution, status=None):
        self.position = position  # Block position, e.g., (1, 1)
        self.resolution = resolution  # Resolution, e.g., (1000, 1333)
        self.status = status  # Processing status, e.g., "within threshold"
        self.children = []  # Sub-blocks

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return (f"TreeNode(position={self.position}, resolution={self.resolution}, "
                f"status={self.status}, children={len(self.children)})")

def parse_and_build_tree(log_lines):
    """Parses the log lines and constructs the tree structure."""
    stack = []  # To maintain the hierarchy
    root = None

    for line in log_lines:
        line = line.strip()
        if line.startswith("Original resolution:"):
            resolution = tuple(map(int, line.split(":")[1].strip().strip("()").split(", ")))
            root = TreeNode("root", resolution)
            stack.append(root)
        elif line.startswith("Processing resolution:"):
            resolution = tuple(map(int, line.split(":")[1].strip().strip("()").split(", ")))
        elif line.startswith("Block"):
            block_info = line.split("with")[0].strip()
            position = tuple(map(int, block_info.split(" ")[1].strip("()").split(", ")))
            resolution = tuple(map(int, line.split("resolution")[1].strip().strip("()").split(", ")))
            node = TreeNode(position, resolution)
            if stack:
                stack[-1].add_child(node)
            stack.append(node)
        elif "Resolution" in line and "within the threshold" in line:
            status = "within threshold"
            stack[-1].status = status
            stack.pop()  # Current block processing is complete

    return root

def print_tree(node, depth=0):
    """Recursively prints the tree structure."""
    print("  " * depth + f"{node}")
    for child in node.children:
        print_tree(child, depth + 1)


def get_log_lines(file_path):
    """Get the log lines from the file."""
    with open(f"/tmp/{file_path}.tree") as file:
        log_data = file.readlines()
    return log_data

def serialize(filename):
    """Serialize the image cut resolution data."""
    log_lines = get_log_lines(filename)  # Get the log lines from the file
    tree = parse_and_build_tree(log_lines)
    print_tree(tree)

