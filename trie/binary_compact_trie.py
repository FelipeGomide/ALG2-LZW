class Node:
    def __init__(self, key="", code=-1):
        self.key = key
        self.code = code

        self.isLeaf = True

        self.left_child = None
        self.right_child = None
        self.epsilon_child = None

    def __repr__(self) -> str:
        if self.key == "":
            return f'\"ε->{self.code}\"'
        return f'\"{self.key}->{self.code}\"'
    
    def __str__(self) -> str:
        if self.key == "":
            return f'\"ε->{self.code}\"'
        return f'\"{self.key}->{self.code}\"'
    
    def set_code(self, code):
        self.code = code

    def set_isLeaf(self, bool_value):
        self.isLeaf = bool_value

    def common_prefix_length(self, s1, s2):
    # Calcula o comprimento do prefixo comum entre duas strings
        length = min(len(s1), len(s2))
        for i in range(length):
            if s1[i] != s2[i]:
                return i
        return length    
    

class Trie:
    def __init__(self):
        self.root = Node()
        self.root.set_isLeaf(False)

    def find(self, text):
        return self.root.search(text)
    
    def print(self):
        return self.root.print_trie()
    
    def insert(self, text, code):
        self.root.insert_search(text, code)
