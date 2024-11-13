class Node:
    def __init__(self, value='', code=-1):
        self.value = value
        self.code = code
        self.children = []
        self.isLeaf = True

    def set_code(self, code):
        self.code = code

    def set_isLeaf(self, bool_value):
        self.isLeaf = bool_value

    def print_trie(self):
        if self.isLeaf:
            if self.value == '':
                print("e")
                return
            print(self.value)
            return

        for child in self.children:
            child.print_trie()
        print(self.value)
        return

    def insert(self, text):
        # Caso base: se o texto for vazio, o nó atual é uma chave válida
        if text == '':
            self.isLeaf = True
            return

        # Se não houver filhos, insere diretamente como novo nó
        if not self.children:
            new_node = Node(text)
            self.children.append(new_node)
            self.set_isLeaf(False)
            return

        # Ordena os filhos pelo valor para garantir uma ordem de inserção consistente
        self.children.sort(key=lambda node: node.value)

        for child in self.children:
            # Calcula o comprimento do prefixo comum entre o filho e o texto a ser inserido
            common_prefix_length = self.common_prefix_length(child.value, text)

            if common_prefix_length > 0:
                # Se há um prefixo comum entre o nó filho e o texto a ser inserido
                if common_prefix_length < len(child.value):
                    # Divide o nó filho existente
                    remaining_suffix = child.value[common_prefix_length:]
                    split_node = Node(remaining_suffix, code=child.code)
                    split_node.children = child.children
                    split_node.isLeaf = child.isLeaf

                    child.value = child.value[:common_prefix_length]
                    child.children = [split_node]
                    child.set_isLeaf(False)

                # Insere o restante do texto como novo nó filho
                remaining_text = text[common_prefix_length:]
                if remaining_text:
                    new_text_node = Node(remaining_text)
                    child.children.append(new_text_node)
                    child.set_isLeaf(False)
                else:
                    # Se não restar mais texto, insere um nó vazio como indicador de chave válida
                    empty_node = Node('')
                    child.children.append(empty_node)
                    child.set_isLeaf(True)
                return

        # Caso nenhum prefixo comum seja encontrado, adiciona o texto como um novo nó filho
        new_node = Node(text)
        self.children.append(new_node)

    def common_prefix_length(self, s1, s2):
        # Calcula o comprimento do prefixo comum entre duas strings
        length = min(len(s1), len(s2))
        for i in range(length):
            if s1[i] != s2[i]:
                return i
        return length

    def search(self, text):
        # Função de busca para verificar se a chave "text" está presente na Trie
        if text == '':
            return self.isLeaf

        for child in self.children:
            if text.startswith(child.value):
                return child.search(text[len(child.value):])

        return False


class Trie:
    def __init__(self):
        self.root = Node()

    def insert_node(self, value):
        self.root.insert(value)

    def search_node(self, key):
        return self.root.search(key)


# Teste do Trie
trie = Trie()
trie.insert_node('C')
trie.insert_node('CAB')
trie.insert_node('CB')
trie.insert_node('CD')
trie.insert_node('DA')

trie.root.print_trie()

print(trie.search_node('C'))    # True
print(trie.search_node('DA'))   # True
print(trie.search_node('CAB'))  # True
print(trie.search_node('CB'))   # True
print(trie.search_node('CD'))   # True
print(trie.search_node('CE'))   # False
