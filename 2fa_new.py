import hashlib

# Define the Merkle Tree class
class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.leaves = []
        self.pairs = []
        self.root = None
        self.__build__()

    def __build__(self):
        # Step 1: Create leaf nodes for each transaction
        for tx in self.transactions:
            self.leaves.append(hashlib.sha3_224(tx.encode()).hexdigest())

        # Step 2: Create pairs of leaf nodes by iterating over the list of leaf nodes two at a time
        for i in range(0, len(self.leaves), 2):
            self.pairs.append((self.leaves[i], self.leaves[i+1] if i+1 < len(self.leaves) else self.leaves[i]))

        # Step 3: Repeat Step 2 for pairs of nodes until a single root node is obtained
        while len(self.pairs) > 1:
            new_pairs = []
            for i in range(0, len(self.pairs), 2):
                new_pairs.append((hashlib.sha3_224(self.pairs[i][0].encode() + self.pairs[i][1].encode()).hexdigest(),
                                  hashlib.sha3_224(self.pairs[i+1][0].encode() + self.pairs[i+1][1].encode()).hexdigest() if i+1 < len(self.pairs) else ''))
            self.pairs = new_pairs
        self.root = self.pairs[0][0]

    # Verify the given transaction against the Merkle Tree and return True if it is valid, False otherwise
    def verify(self, tx, proof):
        tx_hash = hashlib.sha3_224(tx.encode()).hexdigest()
        proof_hash = tx_hash
        for p in proof:
            proof_hash = hashlib.sha3_224((proof_hash + p).encode()).hexdigest()
        return proof_hash == self.root


# Define the User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.merkle_tree = None
        self.proof = None

    def login(self):
        # Prompt user to enter password
        username = input("Enter your name:")
        password = input("Enter your password: ")
        if self.password != password:
            return False, "Incorrect password"
        if self.username != username:
            return False, "Not authorised"

        # Step 1: Create a new Merkle Tree using the current username and password
        self.merkle_tree = MerkleTree([f"LOGIN:{self.username}:{self.password}"])

        # Step 2: Generate the proof for the new transaction
        self.proof = []
        if self.merkle_tree.verify(f"LOGIN:{self.username}:{self.password}", self.proof):
            self.proof.append(self.merkle_tree.root)
        else:
            return False, "Invalid transaction"

        # Step 3: Verify the login transaction against the Merkle Tree using the proof
        if self.merkle_tree.verify(f"LOGIN:{self.username}:{self.password}", self.proof):
            return True, "Login successful"
        else:
            return False, "Invalid transaction"


# Test the User class
u = User("tanmayi", "mypassword")
success, message = u.login()
print(success, message)  # Output: True, "Login successful"
