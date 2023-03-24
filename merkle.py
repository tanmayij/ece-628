#!/usr/bin/python3
import hashlib,sys
    
#Gen 
#hash function
def h(x):
    return int(hashlib.sha3_224(x.encode('utf-8')).hexdigest(), 16)
#prng function
def prng(seed):
    return int(hashlib.sha3_224(b'\xff\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01' + seed).hexdigest(), 16)
#random numbers
n = 32
random_numbers = [prng(bytes(str(i + 900), 'utf-8')) for i in range(n)]
#print (random_numbers)
#self.leaves = [self._hash((i+900) + data + str(si)) for i in range(n)]
file1 = open("data.txt", "r")
for t in file1:
    data = str(t)
#print (data)
leaves = [h(str(i + 900) + data + str(random_numbers[i])) for i in range(n)]
#print (leaves[int(i)] % n)
class MerkleTreeNode:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = hashlib.sha3_224(str(value).encode('utf-8')).hexdigest()

def buildTree(leaves,f):
    nodes = []
    for i in leaves:
        nodes.append(MerkleTreeNode(i))

    while len(nodes)!=1:
        temp = []
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                temp.append(nodes[i])
                break
            concatenatedHash = node1.hashValue + node2.hashValue
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write("Parent(concatenation of "+ str(node1.value) + " and " + str(node2.value) + ") : " +str(parent.value) + " | Hash : " + str(parent.hashValue) +" \n")
            temp.append(parent)
        nodes = temp 
    return nodes[0]

#retrieve the 7th node
node_index = 6  # zero-based index
node = None

# Traverse the Merkle tree to find the 7th node
def traverse(node, index):
    if node is None:
        return None
    if index == 0:
        return node
    left_size = get_tree_size(node.left)
    if index <= left_size:
        return traverse(node.left, index - 1)
    else:
        return traverse(node.right, index - left_size - 1)

# Get the size of the subtree rooted at node
def get_tree_size(node):
    if node is None:
        return 0
    return 1 + get_tree_size(node.left) + get_tree_size(node.right)
f = open("merkle.tree", "w")
root = buildTree(leaves,f)
#retrieve_and_verify(data, root, leaves)
f.close()

# Find the 7th node and retrieve its hash value and data
node = traverse(root, node_index)
if node is not None:
    print("Hash value of 7th node:", node.hashValue)
    print("Data of 7th node:", node.value)
else:
    print("Node not found")


#Authenticate 7th node
def authenticate_node(root_node, node_index, node_data, node_hash):
    # Traverse the Merkle tree to find the 7th node
    node = traverse(root_node, node_index)
    if node is None:
        return False

    # Verify that the retrieved node has the expected data and hash value
    if node.value != node_data or node.hashValue != node_hash:
        return False

    # Verify the path from the retrieved node to the root
    path = []
    current_node = node
    while current_node is not None:
        if current_node.left is not None and current_node.right is not None:
            if current_node.left.value == node_data:
                path.append(current_node.right.hashValue)
            else:
                path.append(current_node.left.hashValue)
        current_node = current_node.parent
    path.reverse()

    current_hash = node.hashValue
    for sibling_hash in path:
        concatenated_hash = current_hash + sibling_hash
        current_hash = hashlib.sha3_224(bytes.fromhex(concatenated_hash)).hexdigest()

    # Verify that the computed root hash matches the actual root hash
    if current_hash == root_node.hashValue:
        print ("Data is verified")