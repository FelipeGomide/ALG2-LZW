class Node:
    def __init__(self, value='', code=-1):
        self.value = value
        self.code = code
        self.children = []
        self.isLeaf = True
        self.isKey = False

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

        self.children.sort(key=lambda node: node.value)
        for child in self.children:
            child.print_trie()
        print(self.value)
        return

    def search(self, key):
        # Verifica se é uma folha e se a chave completa é uma chave válida
        # print("--> key = " + key)
        # print("--> self.value = " + self.value)
        if self.isLeaf:
            return self.isKey and self.value == key

        # Ordena os filhos para busca binária
        self.children.sort(key=lambda node: node.value)
        binary_search = list(self.children.copy())

        while len(binary_search) > 0:
            pivot = len(binary_search) // 2
            if pivot >= len(binary_search):
                break

            if key[0] < binary_search[pivot].value[0]:
                binary_search = binary_search[:pivot]
            elif key[0] > binary_search[pivot].value[0]:
                binary_search = binary_search[pivot + 1:]
            elif key[0] == binary_search[pivot].value[0]:
                length_node = len(binary_search[pivot].value)
                if len(key) < length_node:
                    return False
                length = min(length_node, len(key))

                # print("entrou!!")
                # Verifica se o restante da chave coincide com o valor do nó atual
                for i in range(1, length):
                    if i >= len(key) or i >= len(binary_search[pivot].value) or key[i] != binary_search[pivot].value[i]:
                        return False

                # Se a chave é completamente igual até seu comprimento, verifica se é uma chave completa
                if length == len(key):
                    return binary_search[pivot].isKey  # Confirma se o nó atual é uma chave completa
                return binary_search[pivot].search(key[length:])
        return False

    def insert(self, text):
        if len(self.children) == 0:
            new_node = Node(text)
            new_node.isKey = True  # Marca o nó completo como chave
            self.children.append(new_node)
            if self.isLeaf and self.isKey:
                self.children.append(Node(''))  # epsilon
            self.set_isLeaf(False)
            return

        self.children.sort(key=lambda node: node.value)
        binary_search = list(self.children.copy())

        while len(binary_search) > 0:
            pivot = len(binary_search) // 2
            if pivot >= len(binary_search):
                break

            if len(binary_search[pivot].value) == 0:
                binary_search.remove(binary_search[pivot])
                if len(binary_search) == 0:
                    break
                pivot = len(binary_search) // 2

            if text[0] < binary_search[pivot].value[0]:
                binary_search = binary_search[:pivot]
            elif text[0] > binary_search[pivot].value[0]:
                binary_search = binary_search[pivot + 1:]
            elif text[0] == binary_search[pivot].value[0]:
                length_node = len(binary_search[pivot].value)
                length = min(length_node, len(text))

                # Encontra o comprimento do prefixo comum
                i = 1
                while i < length and text[i] == binary_search[pivot].value[i]:
                    i += 1

                if i == length:
                    # Se há uma correspondência completa, continua inserindo a parte restante
                    binary_search[pivot].insert(text[i:])
                    return
                else:
                    # Divide o nó existente e cria um novo nó filho
                    aux = Node(binary_search[pivot].value[i:])
                    aux.children = binary_search[pivot].children
                    aux.isLeaf = binary_search[pivot].isLeaf
                    aux.isKey = binary_search[pivot].isKey  # Preserve isKey status for existing prefix

                    binary_search[pivot].value = binary_search[pivot].value[:i]
                    binary_search[pivot].children = [aux]
                    binary_search[pivot].isLeaf = False
                    binary_search[pivot].isKey = False  # Intermediate node, no longer a full key

                    # Adiciona a parte restante do texto como um novo filho
                    aux2 = Node(text[i:])
                    aux2.isKey = True
                    binary_search[pivot].children.append(aux2)
                    return

        # Se nenhuma correspondência foi encontrada, adiciona um novo nó
        new_node = Node(text)
        new_node.isKey = True
        self.children.append(new_node)
        return


class Trie:
    def __init__(self):
        self.root = Node()

    def insert_node(self, value):
        self.root.insert(value)

    def search_node(self, value):
        return self.root.search(value)


# Exemplo de uso da Trie
trie = Trie()

trie.insert_node('C')
trie.insert_node('CAB')
trie.insert_node('CB')
trie.insert_node('CD')
trie.insert_node('DA')
trie.insert_node('B')
trie.insert_node('DBBA')
trie.insert_node('DBDD')
trie.insert_node('BAAA')

# Imprime a estrutura da trie
trie.root.print_trie()

# Realiza buscas na trie
print(trie.search_node("CB"))     # True
print(trie.search_node("CAB"))    # True
print(trie.search_node("DA"))     # True
print(trie.search_node("CB"))     # True
print(trie.search_node("C"))      # True
print(trie.search_node("B"))      # True
print(trie.search_node("BA"))     # False
print(trie.search_node("DBBA"))   # True
print(trie.search_node("DBDD"))   # True
print(trie.search_node("D"))      # False
print(trie.search_node("DB"))     # False
