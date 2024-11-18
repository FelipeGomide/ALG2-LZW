class Node:
    def __init__(self, value="", code=-1):
        self.value = value
        self.code = code
        self.children = []
        self.isLeaf = True

    def __repr__(self) -> str:
        if self.value == "":
            return f'\"ε->{self.code}\"'
        return f'\"{self.value}->{self.code}\"'
    
    def __str__(self) -> str:
        if self.value == "":
            return f'\"ε->{self.code}\"'
        return f'\"{self.value}->{self.code}\"'

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

    def print_trie(self, spacing = 0):
        for i in range(spacing):
            print("|  ", end="")

        if self.isLeaf:
            if self.value == '':
                print("ε", self.code)
                return
            print(self.value, self.code)
            return

        if self.value == '': print("Root")
        else: print(self.value)

        for child in self.children:
            child.print_trie(spacing+1)
        return

    def insert(self, text, code):
        i = self.common_prefix_length(text, self.value)
        # print(f'I = {i}, text = {text}, nó = {self.value}')

        if i == len(self.value) and i == len(text):
            # Texto e nó são iguais, adicionar epsilon
            epsilon = Node('', code = code)

            self.children.append(epsilon)
            self.set_isLeaf(False)

            return

        if i == len(self.value) and i < len(text): 
            # Nó possui um prefixo do texto inserido
            # Já que a inserção parte de uma busca, garanto que não existe filho do qual poderia ser realizada a inserção
            if self.isLeaf: #Se o nó era folha acrescento um nó Epsilon
                epsilon = Node(value= '', code= self.code)
                self.set_isLeaf(False)
                self.children.append(epsilon)
            
            new_text = text[i:]
            new_node = Node(value=new_text, code = code)
            self.children.append(new_node)

            # print('Caso 1')
            return

        if i < len(self.value) and i == len(text):  #O texto é um prefixo do nó
            suffix = self.value[i:]
            suffix_node = Node(value=suffix, code= self.code)
            suffix_node.children = self.children.copy()
            suffix_node.set_isLeaf(self.isLeaf)

            self.children.clear()
            self.children.append(suffix_node)
            self.value = self.value[:i]
            self.set_isLeaf(False)

            epsilon = Node(value='', code=code)
            self.children.append(epsilon)

            # print('Caso 2')
            return

        if i < len(self.value) and i < len(text): #Nó e texto possuem um prefixo em comum
            suffix = self.value[i:]
            # print("Suffix = ", suffix)
            suffix_node = Node(value=suffix, code= self.code)
            suffix_node.children = self.children.copy()
            # print("Filhos do suffix:", suffix_node.children)

            if len(suffix_node.children) > 0:
                suffix_node.set_isLeaf(False)

            self.children.clear()
            self.children.append(suffix_node)
            self.value = self.value[:i]
            self.set_isLeaf(False)

            new_node = Node(value= text[i:], code= code)
            self.children.append(new_node)

            # print(self.children)

            # print('Caso 3')
            return

        print("Inserção não bateu com nenhum dos casos")
        return
    
    def insert_search(self, text, code):
        #Função auxiliar da inserção, faz uma busca de casamento parcial
        i = self.common_prefix_length(text, self.value)
        text_suffix = text[i:]

        if i == len(self.value):
            for child in self.children:
                if child.value != '' and text_suffix != '':
                    if child.value[0] == text_suffix[0]:
                        child.insert_search(text_suffix, code)
                        return
        
        self.insert(text, code)
        return

    def search(self, text):
        # Função de busca para verificar se a chave "text" está presente na Trie
        if text == '' and self.isLeaf: return self.code

        for child in self.children:
            if text.startswith(child.value):
                return child.search(text[len(child.value):])

        return False


class Trie:
    def __init__(self):
        self.root = Node()

    def find(self, text):
        return self.root.search(text)
    
    def print(self):
        return self.root.print_trie()
    
    def insert(self, text, code):
        self.root.insert_search(text, code)

# Teste do Trie
# trie = Trie()
# trie.insert_node('C')
# trie.insert_node('CAB')
# trie.insert_node('CB')
# trie.insert_node('CD')
# trie.insert_node('DA')

# trie.insert_node('CBD')
# trie.insert_node('CAA')

# trie.insert_node('DAA')
# trie.insert_node('DAD')
# trie.insert_node('DD')

# trie.print()

# print(trie.search_node('C'))    # True
# print(trie.search_node('DA'))   # True
# print(trie.search_node('CAB'))  # True
# print(trie.search_node('CB'))   # True
# print(trie.search_node('CD'))   # True
# print(trie.search_node('CE'))   # False

if __name__ == '__main__':
    trie = Trie()
    trie.root.set_isLeaf(False)
    trie.insert('CABA', 1)
    trie.insert('CADD', 2)
    trie.insert('CAB', 3)
    trie.insert('CB', 4)
    trie.insert('CD', 5)
    trie.insert('DA', 6)

    trie.print()
    print("-------------------------")

    outra = Trie()
    outra.root.set_isLeaf(False)

    outra.insert("MELÃO", 1)
    outra.insert("MELANCIA", 2)
    outra.insert('MAMÃO', 3)
    outra.insert('MORANGO', 4)
    outra.insert('MEL', 5)
    outra.insert('MAÇÃ', 6)
    outra.insert('BANANA', 7)
    outra.insert('MARACUJÁ', 8)
    outra.insert('MARMELO', 9)
    outra.insert('MACADÂMIA', 10)
    outra.insert('MEXERICA', 11)
    outra.insert('MIRTILO', 12)
    outra.insert('MANGA', 13)

    outra.insert('LIMÃO', 14)
    outra.insert('LARANJA', 15)
    outra.insert('LICHIA', 16)

    outra.insert('ABACAXI', 17)
    outra.insert('ACEROLA', 18)
    outra.insert('AMEIXA', 19)
    outra.insert('ameixa', 20)
    outra.insert('AMORA', 21)
    outra.insert('AÇAÍ', 22)
    outra.insert('AVELÃ', 23)

    outra.insert('MELADO', 24)

    outra.print()

    print(outra.find('MORANGO'))
    print(outra.find('MEL'))
    print(outra.find('ABACAXI'))
    print(outra.find('MAMÃO'))
    print(outra.find('MELADO'))
    print(outra.find('COCO'))
    print(outra.find(''))

    mydict = Trie()
    mydict.insert('010', 3)
    mydict.insert('0101', 1)
    mydict.insert('0111', 2)
    mydict.insert('0', 4)
    mydict.print()