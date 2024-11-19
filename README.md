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

A estrutura de dados responsável por armazenar o nó da árvore é representado pela classe "Trie", cujo construtor cria o nó da raiz, que armazena uma string vazia e as cadeias inseridas no dicionário são inseridas como filhas desse nó raiz. Após criar a raiz, a inserção é feita através da função "insert" da classe "Trie" que chama a função "insert_search" de "Node", na qual passa-se a string como parâmetro (que é a que será inserida na árvore ). 
		A primeira tarefa realizada é verificar qual o maior prefixo comum entre a string que deseja adicionar na trie e a chave armazenada no nó 'n' que chama essa função. Se o prefixo for igual à string armazenada em 'n', deve-se adicionar o sufixo restante da chave que deseja adicionar como filho à esquerda do nó n (se o sufixo começa com zero) ou como filho à direita de n (se o sufixo começa com um). Caso contrário, deverá modificar o valor armazenado no nó 'n', para adicionar a nova chave na trie.
		Há quatro possibilidades de inserção da nova chave:
  
   - **Caso 1:** Chave do nó pai é igual ao texto inserido. Define que o ramo "epsilon_child" apontará para um novo nó que será criado e que armazenará uma cadeia vazia. Além disso, define que o nó pai (que recebeu a inserção) não é mais folha).
   - **Caso 2:** Cadeia que será inserida no nó é maior do que a cadeia armazenada no nó pai. O nó que armazena o sufixo da cadeia a ser inserida deverá será definido como filho à esquerda, se o primeiro elemento dessa sub-cadeia for zero, ou como filho à direita, caso contrário.
   - **Caso 3:** A chave da cadeia a ser inserido é prefixo do valor armazenado no nó pai dessa inserção. Deve-se adicionar o nó que armazena o epsilon (para indicar que inseriu a última cadeia) e deve adicionar o sufixo da cadeia do nó que se tornou o nó pai da subárvore originária dessa nova inserção como um novo filho dele. Mantém-se a lógica que será filho à esquerda se o primeiro elemento do sufixo for zero, mas será filho à direita, caso contrário.
   - **Caso 4:** Tanto a cadeia que está sendo inserida, quanto o valor armazenado no nó da sub-árvore em questão têm sufixos que não casam entre si. Assim, adiciona-se dois nós: entre os dois sufixos que não casaram, aquele que começa com zero é o filho da esquerda no nó pai da sub-árvore e o outro, que começa com um, é o filho à direita.

Além disso, é importante mencionar que cada cadeia inserida na trie é associada a um código que é armazenado no nó folha que indica o final da cadeia. Assim, ao inserir uma string no dicionário, deve-se passar não apenas a cadeia a ser inserida, como também o código.

### 2.1.2. Busca na Trie

Essa operação, implementada pela função `search` recebe como parâmetro a cadeia que se deseja buscar e, a partir do nó raiz da árvore completa, verifica se o texto armazenado no nó onde está é igual ao texto que está buscando. Se for, retorna `True` e o código associado ao nó onde está. Caso contrário, verifica qual dos filhos desse nó tem um valor que é prefixo da cadeia que se deseja inserir e se encontrar um filho que satisfaça isso deve mover para esse nó filho e chamar a função `search` recursivamente, mas, dessa vez, passando como parâmetro apenas o sufixo da cadeia que não casou com o valor armazenado no nó onde estava. Caso não encontre nenhum filho do nó onde está cujo valor armazenado seja prefixo do texto (que quer inserir passado como parâmetro à função, retorna-se `False`.

### 2.1.3. Remoção na Trie

A função `remove` realiza a remoção de uma cadeia passada como parâmetro a ela e o 0 primeiro passo é verificar se cadeia que deseja-se remover existe na árvore (usa-se o método "search" para verificar isso) e, se existir, prosseguimos com o processo de remoção.
	
Se o nó atual for uma folha, verifica se seu valor corresponde à string a ser removida; se sim, permite a remoção retornando True. Para nós internos, calcula-se o prefixo comum entre a string e o valor do nó. O sufixo restante determina o próximo passo: se vazio, o nó remove seu filho épsilon (caso exista) e verifica se deve combinar valores de filhos restantes ou transformar-se em folha. Caso o sufixo não seja vazio, delega a remoção ao filho correspondente (0 ou 1).

Após cada remoção, a função ajusta a trie para eliminar redundâncias. Se um nó tem apenas um filho restante, combina os valores para manter a compactação. A estrutura resultante permanece eficiente, com o menor número possível de nós, garantindo a integridade da trie após a remoção da string.

## 2.2. Compressão no método LZW

O primeiro passo, após, obviamente, criar o dicionário que armazenará as cadeias lidas, é inserir todos os 256 unicodes e o respectivo código ASCII que será armazenado na folha Trie (que indica o fim da cadeia). 

Na nossa implementação, definimos que o texto que será comprimido será lido de um arquivo. Assim, após ler o arquivo a ser comprimido, obtém-se a sua representação correspondente em binário e, em seguida, lê-se o conteúdo de 8 em 8 bits,que serão inseridos no dicionário. 

Após ler cada byte, primeiro verifica se a última cadeia inserida na Trie, concatenada a essa nova cadeia lida, já foi inserida no dicionário (usa a operação "search" descrita anteriormente para verificar isso) e, se já tiver sido, adiciona o código associado a essa cadeia à string que armazena os códigos comprimidos. Caso contrário, insere a concatenação da última cadeia lida com a nova lida no dicionário e define que o código dessa cadeia é igual ao tamanho do dicionário (em seguida, soma 1 unidade à variável que armazena o tamanho dessa estrutura). Por fim, nesse último caso, deve-se atualizar qual foi a última cadeia lida. Após concluir a leitura do documento em binário, será retornada a string composta pela representação em código.

## 2.3. Descompressão no método LZW

Assim como na compressão, o primeiro passo é criar um dicionário que armazena os unicodes e os seus respectivos códigos ASCII. O dicionário construído na descompressão mapeia o código à string correspondente e, a cada código lido, concatena a string lida às lidas anteriormente. 

Após criar o dicionário, deve-se ler qual o primeiro conjunto de bits do arquivo que contém a compressão. Como essa primeira leitura corresponde a um único caracter (sempre será assim), lê qual o código no arquivo comprimido e busca-o na Trie e insere a cadeia associada a ele. Se não estiver na Trie, COMPLETAR

# 3. ABORDAGENS DA REPRESENTAÇÃO DAS CADEIAS NO MÉTODO LZW

Foram implementadas duas formas como representar o código que é usado para realizar a compressão: o número de bits usado para representar o código por ser fixo ou pode ser dinâmico. No fixo, os códigos são sempre escritos usando uma quantidade pré-definidas de bits, que é depende do tamanho máximo do dicionário. Caso tente inserir uma nova cadeia na árvore, mas todos os códigos no intervalo [0; tamanho dicionário] já foram atribuídos a outras cadeias, a inserção não poderá ser feita e a compressão só poderá ser realizada usando as chaves já inseridas no dicionário.

Já na abordagem dinâmica, o tamanhos em bits para ser usado na representação dos códigos começa com um tamanho pré-definido de 8 bits (é o número de bits necessário para representar os códigos dos unicodes), mas, de acordo com a necessidade, pode-se usar mais bits para representar os códigos. Essa abordagem é mais vantajosa no que tange ao uso da memória, pois, como o aumento é feito de acordo com a necessidade, não há uso desnecessário de bits, logo, a compressão feita se torna mais eficiente. Mas assim como na abordagem anterior, na dinâmica também há um número máximo de bits que pode ser usado para representar os códigos e, caso atinja esse máximo, não podem ser feitas novas inserções e, dessa forma, as compressões das novas cadeias lidas devem ser feitas usando as chaves já inseridas na Trie.

Essa ideia do número de bits usado ser fixa ou variável é aplicável tanto na construção do dicionário durante a compressão, quanto durante as descompressão, mas sempre respeitando o número de bits que pode ser usado para representar os códigos.

# 4. ORGANIZAÇÃO
