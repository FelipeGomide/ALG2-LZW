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
            return f'ε->{self.code}'
        return f'{self.key}->{self.code}'
    
    def __str__(self) -> str:
        if self.key == "":
            return f'ε->{self.code}'
        return f'{self.key}->{self.code}'
    
    def copy_children(self, other):
        self.left_child = other.left_child
        self.right_child = other.right_child
        self.epsilon_child = other.epsilon_child

    def clear_children(self):
        self.left_child = None
        self.right_child = None
        self.epsilon_child = None

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
    
    def print_trie(self, spacing=0):
        for i in range(spacing):
            print("| ", end="")

        if self.isLeaf:
            print(self)
            return
        
        if self.key == '': print('Root')
        else: print(self.key)

        if self.left_child != None:
            self.left_child.print_trie(spacing+1)

        if self.right_child != None:
            self.right_child.print_trie(spacing+1)
        
        if self.epsilon_child != None:
            self.epsilon_child.print_trie(spacing+1)

        return

    def insert(self, text, code):
        i = self.common_prefix_length(text, self.key)

        if i == len(self.key) and i == len(text):
        #Texto e nó são iguais, adiciono nó epsilon como filho
            epsilon = Node('', code = code)

            self.epsilon_child = epsilon
            self.set_isLeaf(False)

            print('Caso 1')
            return
        
        if i == len(self.key) and i < len(text):
            # Nó é prefixo do texto a ser inserido

            if self.isLeaf:
            #Se o nó era folha acrescento nó Epsilon
                #epsilon = Node('', code = code)
                epsilon = Node('', code=self.code) # mudei aqui!!
                self.set_isLeaf(False)
                self.epsilon_child = epsilon

            new_text = text[i:]
            new_node = Node(key=new_text, code=code)
            
            new_node = Node(new_text, code = code)
            if new_text[0] == '0':
                self.left_child = new_node
            else:
                self.right_child = new_node
            
            print('Caso 2')
            return

        if i < len(self.key) and i == len(text):
        # O texto é um prefixo do nó
            suffix = self.key[i:]
            suffix_node = Node(suffix, code = self.code)
            suffix_node.copy_children(self)
            suffix_node.set_isLeaf(self.isLeaf)

            self.clear_children()
            self.key = self.key[:i]
            self.set_isLeaf(False)

            if suffix[0] == '0':
                self.left_child = suffix_node
            else:
                self.right_child = suffix_node

            epsilon = Node('', code = code)
            self.epsilon_child = epsilon

            print('Caso 3')
            return
            
        if i < len(self.key) and i < len(text):
        # Nó e texto possuem um prefixo em comum
            suffix = self.key[i:]
            suffix_node = Node(suffix, code= self.code)
            suffix_node.copy_children(self)
            suffix_node.set_isLeaf(self.isLeaf)

            self.clear_children()
            self.key = self.key[:i]
            self.set_isLeaf(False)
            
            new_node = Node(text[i:], code= code)

            if suffix[0] == '0':
                self.left_child = suffix_node
                self.right_child = new_node
            else:
                self.right_child = suffix_node
                self.left_child = new_node

            print('Caso 4')
            return

        print('Falta esse caso ainda')
        print(f'I = {i}, text = {text}, nó = {self.key}')
        return

    def insert_search(self, text, code):
        i = self.common_prefix_length(text, self.key)
        text_suffix = text[i:]

        if i == len(self.key):
            # if len(text_suffix) == 0 and self.epsilon_child != None:
            #     self.epsilon_child.insert_search(text_suffix, code)
            #     return

            if text_suffix != '':
                first = text_suffix[0]
                if first =='0':
                    if self.left_child != None:
                        self.left_child.insert_search(text_suffix, code)
                        return

                if self.right_child != None:
                    self.right_child.insert_search(text_suffix, code)
                    return

        self.insert(text, code)
        return
        
    def search(self, text):
      # Verifica se há uma correspondência exata com o nó atual
      if text == self.key:
          return True, self.code

      # Se o nó atual é um prefixo, continua a busca nos seus filhos
      if text.startswith(self.key):
          text_suffix = text[len(self.key):]  # Texto restante para a busca

          # Verifica se há um filho epsilon (indica o final de uma sequência)
          if text_suffix == '' and self.epsilon_child:
              return True, self.epsilon_child.code

          # Busca no filho à esquerda
          if self.left_child and text_suffix.startswith(self.left_child.key):
              return self.left_child.search(text_suffix)

          # Busca no filho à direita
          if self.right_child and text_suffix.startswith(self.right_child.key):
              return self.right_child.search(text_suffix)

      # Nenhuma correspondência encontrada
      return False, -1


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
