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
def buildTree(leaves):
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
            #f.write("Parent(concatenation of "+ str(node1.value) + " and " + str(node2.value) + ") : " +str(parent.value) + " | Hash : " + str(parent.hashValue) +" \n")
            temp.append(parent)
        nodes = temp 
    return nodes[0]

def get_proof(self, index):
        """
        Generates the proof trail in a bottom-up fashion
        """
        if self.levels is None:
            return None

        # if merkle tree not complete or incorrect index
        elif not self.complete or index > len(self.leaves)-1 or index < 0:
            return None
        else:
            proof_result = []
            no_of_levels = len(self.levels)
            for x in range(no_of_levels - 1, 0, -1):
                level_nodes = len(self.levels[x])

                # skip if this is an odd end node
                if (index == level_nodes - 1) and (level_nodes % 2 == 1):
                    index = int(index / 2.)

                # if mod 2 = 0 , an even index , hashed with right sibling else with left
                # checks if the merkle_node is the left sibling or the right sibling
                Right_node = index % 2
                if Right_node:
                    sibIndex = index - 1
                    sibPos = "left"
                else:
                    sibIndex = index + 1
                    sibPos = "right"

                sibVal = self.convert_to_hex(
                    self.levels[x][sibIndex])
                proof_result.append({sibPos: sibVal})
                # current node gets adjusted as we go up the merkle tree
                index = int(index / 2.)
            return proof_result

f = open("merkle.tree", "w")
root = buildTree(leaves)

get_proof(data,7)

f.close()