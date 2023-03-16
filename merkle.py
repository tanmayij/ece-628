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
for i in file1:
    data = str(i)

leaves = [h(str(i + 900) + data + str(random_numbers[i])) for i in range(n)]
class MerkleTreeNode:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = hashlib.sha3_224(str(value).encode('utf-8')).hexdigest()

nodecount = 0
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
            #print ("node a[", i, "][",i+1,"]")#hash value: ", node1.hashValue)
            #f.write("Left child : "+ str(node1.value) + " | Hash : " + str(node1.hashValue) + " \n")
            #f.write("Right child : "+ str(node2.value) + " | Hash : " + str(node2.hashValue) +" \n")
            concatenatedHash = str(node1.hashValue) + str(node2.hashValue)
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write("Parent(concatenation of "+ str(node1.value) + " and " + str(node2.value) + ") : " +str(parent.value) + " | Hash : " + str(parent.hashValue) +" \n")
            temp.append(parent)
        nodes = temp 
    return nodes[0]


def retrieve_and_verify(data, root, leaves):
    # Retrieve the leaf node corresponding to the data
    leaf_index=
    leaf = leaves[leaf_index]

    # Traverse up the tree from the leaf node to the root node, computing the hash value of each parent node
    current_node = leaf
    while current_node != root:
        parent = current_node.left if current_node.right == None else MerkleTreeNode(str(current_node.left.hashValue) + str(current_node.right.hashValue))
        current_node = parent

    # Compare the final computed root hash value with the expected root hash value
    expected_root_hash = root.hashValue
    actual_root_hash = current_node.hashValue
    if expected_root_hash == actual_root_hash:
        print("Data is verified to be part of the Merkle tree.")
    else:
        print("Data is not part of the Merkle tree.")

#inputString = sys.argv[1]
#leaves = data
#leaves = leavesString.split(",")
f = open("merkle.tree", "w")
root = buildTree(leaves,f)
retrieve_and_verify(data, root, leaves)

f.close()