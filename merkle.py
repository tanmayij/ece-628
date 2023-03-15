from pymerkle import MerkleTree
tree = MerkleTree(algorithm='sha3-224', encoding='utf-8', security=False)
#print (tree.length)


#code to write d
for d in range(665):
    f = open("textbytes.txt", "w")
    f.write(bytes(d))
    f.close()



    