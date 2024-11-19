# ALG2-LZW
Trabalho de algoritmos 2, que busca a implementação do algoritmo de compressão LZW utilizando a estrutura de dados Trie Compacta

# 1. INTRODUÇÃO

No Trabalho Prático 1 proposto, foi solicitado a implementação do método Lempel-Ziv-Welch (LZW), cujo principal objetivo é realizar a compressão e a descompressão de arquivos. Esse método consiste em armazenar as sub-cadeias lidas em um dicionário e, a cada sub-cadeia, atribui-se um código correspondente que será usado para representar a sub-cadeia de maneira mais comprimida. Mas, ao ler uma sub-cadeia, sempre checa primeiro se essa sequência já foi lida previamente e, caso tenha sido, escreve o código associado à sequência. Caso contrário, insere a nova sub-cadeia no dicionário e atribui um novo código a ela.

O diferencial da implementação proposta nesse trabalho é que o dicionário que armazena as sub-cadeias deve ser representado como uma Trie de Prefixos Compacta Binária, conteúdo que foi estudado em sala de aula. A seguir, será explicado como foi feita a implementação do trabalho e as estruturas de dados que o compõem.

# 2. DETALHES DA IMPLEMENTAÇÃO

## 2.1. Implementação da Trie

Essa estrutura foi implementada a partir da criação das classes `Node` e `Trie`. A classe `Node` é responsável por armazenar os dados correspondentes a cada nó que compõe a trie. Os dados armazenados são:
- A substring armazenada no nó em questão (string binária).
- Um dado do tipo `bool` que indica se aquele nó é folha ou não.
- Um dado do tipo inteiro que armazena o código (se o nó for folha).
- Três ponteiros para filhos: o filho à esquerda, o à direita e o filho que armazena ε (indica que o nó corrente armazena uma cadeia inserida na trie). O filho à esquerda armazena apenas as sub-cadeias que começam com zero e o à direita, as que começam com um.

### 2.1.1. Inserção na Trie

A estrutura de dados responsável por armazenar o nó da árvore é representada pela classe `Trie`, cujo construtor cria o nó da raiz, que armazena uma string vazia. As cadeias inseridas no dicionário são adicionadas como filhas desse nó raiz. A inserção é feita através da função `insert` da classe `Trie`, que chama a função `insert_search` de `Node`, passando a string a ser inserida na árvore como parâmetro.

A inserção segue os passos:
1. Verificar o maior prefixo comum entre a string que deseja adicionar e a chave armazenada no nó `n`.
2. Dependendo da relação entre o prefixo e o sufixo, há quatro possibilidades de inserção:
   - **Caso 1:** A chave do nó pai é igual ao texto inserido. Cria-se um ramo `epsilon_child` apontando para um novo nó vazio.
   - **Caso 2:** A cadeia a ser inserida é maior que a armazenada no nó pai. Insere-se o sufixo como filho à esquerda ou à direita.
   - **Caso 3:** A chave da cadeia a ser inserida é prefixo do valor armazenado no nó pai. Divide-se o nó pai em subárvores.
   - **Caso 4:** Os sufixos das cadeias não casam. Adicionam-se dois novos nós, dividindo o nó pai.

Cada cadeia inserida recebe um código associado, armazenado no nó folha que representa o final da cadeia.

### 2.1.2. Busca na Trie

A busca é implementada pela função `search`, que recebe a cadeia desejada como parâmetro. Partindo da raiz, verifica se o texto armazenado no nó corresponde à string buscada. Caso positivo, retorna `True` e o código associado. Caso contrário, verifica qual dos filhos possui um valor prefixo da cadeia e chama recursivamente a função passando o sufixo restante. Se nenhum filho satisfizer a condição, retorna `False`.

### 2.1.3. Remoção na Trie

A função `remove` realiza a remoção de uma cadeia, verificando inicialmente sua existência com o método `search`. Se o nó atual for folha e corresponder à cadeia, permite a remoção. Para nós internos, calcula-se o prefixo comum entre a string e o valor do nó. O sufixo restante determina o próximo passo:
- Se vazio, remove o filho ε e ajusta os valores dos filhos restantes.
- Caso contrário, delega a remoção ao filho correspondente.

Após a remoção, a trie é ajustada para eliminar redundâncias, mantendo a compactação e a eficiência.

## 2.2. Compressão no método LZW

Inicialmente, o dicionário é preenchido com os 256 unicodes e seus respectivos códigos ASCII, armazenados como folhas da Trie. O texto a ser comprimido é lido de um arquivo e representado em binário. O processo lê blocos de 8 bits, verifica se a cadeia concatenada à última lida já existe na Trie (usando `search`), e:
- Caso exista, adiciona o código associado à cadeia comprimida.
- Caso contrário, insere a nova cadeia na Trie e associa a ela o próximo código disponível.

O resultado final é uma string de códigos comprimidos.

## 2.3. Descompressão no método LZW

Na descompressão, cria-se um dicionário inicial similar ao da compressão. Cada código lido no arquivo comprimido é buscado na Trie, e a cadeia correspondente é reconstruída. O processo concatena as cadeias conforme necessário, atualizando o dicionário de forma incremental.

# 3. ABORDAGENS DA REPRESENTAÇÃO DAS CADEIAS NO MÉTODO LZW

Existem duas formas de representar os códigos:
- **Tamanho fixo:** Usa um número pré-definido de bits, limitado pelo tamanho máximo do dicionário.
- **Tamanho dinâmico:** Começa com 8 bits (necessários para unicodes) e aumenta conforme necessário, até um limite máximo.

A abordagem dinâmica é mais eficiente em memória, mas ambas garantem a compressão com base nas chaves já inseridas.

# 4. ORGANIZAÇÃO
