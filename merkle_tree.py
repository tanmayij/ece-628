import hashlib

class MerkleTree:
    def __init__(self, data):
        self.leaves = [self._hash(IDi + data + str(si)) for IDi, si in enumerate(data)]
        self.levels = [self.leaves]

        while len(self.levels[-1]) > 1:
            level = []
            for i in range(0, len(self.levels[-1]), 2):
                left = self.levels[-1][i]
                right = self.levels[-1][i+1] if i+1 < len(self.levels[-1]) else ''
                level.append(self._hash(left + right))
            self.levels.append(level)

        self.root = self.levels[-1][0]

    def _hash(self, data):
        return hashlib.sha3_224(data.encode()).hexdigest()

    def get_proof(self, index):
        proof = []
        level_index = 0
        while len(self.levels[level_index]) > 1:
            is_right_node = index % 2
            sibling_index = index - 1 if is_right_node else index + 1
            sibling = self.levels[level_index][sibling_index] if sibling_index < len(self.levels[level_index]) else ''
            proof.append(sibling)
            index = index // 2
            level_index += 1
        return proof

def verify_authenticity(data, proof, root):
    current_hash = hashlib.sha256(data.encode()).hexdigest()
    for sibling in proof:
        current_hash = hashlib.sha256((current_hash + sibling).encode()).hexdigest()
    return current_hash == root



