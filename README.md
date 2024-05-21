# <p align="center">Algoritmo do Caixeiro Viajante com Busca Tabu</p>
#### <p align="center">Trabalho de Otimização Combinatória, faculdade de Ciência da Computação, UNIOESTE (Universidade Estadual do Oeste do Paraná)</p>
##### <p align="center">Desenvolvido por: [Gabriel Mazzuco](https://github.com/gabrielmazz)

---

# <p align="center">Introdução</p>

O Problema do Caixeiro Viajante (PCV) é um problema clássico de otimização combinatória que consiste em encontrar o menor caminho que passa por todos os vértices de um grafo, visitando cada vértice uma única vez e retornando ao vértice de origem. O PCV é um problema NP-difícil, o que significa que não se conhece um algoritmo polinomial que resolva o problema de forma exata em tempo polinomial. Por isso, a maioria dos algoritmos para resolver o PCV são heurísticas, que buscam encontrar uma solução aproximada em tempo polinomial.

Uma das heurísticas mais conhecidas para resolver o PCV é a Busca Tabu. A Busca Tabu é uma técnica de busca local que utiliza uma lista tabu para evitar que o algoritmo fique preso em ótimos locais locais. A Busca Tabu é uma técnica muito eficiente para resolver problemas de otimização combinatória, como o PCV.


# <p align="center">Formato de entrada</p>

O formato de cada arquivo de entrada é baseado na Figura 1, na ilustração, cada linha representa o cuso de cada aresta a partir do vértice de origem até o destino. Por exemplo, na primeira linha temos o valor 6. Ele indica que o custo para ir do vértice 1 até o quinto vértice é igual a seis. Alem de que na primeira linha do arquivo, representa o número de vértices do grafo. A representação de como o grafo fica com a entrada da Figura 1, está sendo representada na Figura 2

<br>

<p align="center">
    <img src="img/img1.png" width="40%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

<br>

<p align="center">
    <img src="img/img2.png" width="70%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>


# <p align="center">Implementação do Algoritmo</p>

A implementação do algoritmo foi feita em Python, e o código fonte está disponível no repositório do GitHub. O algoritmo foi implementado utilizando a biblioteca *networkX* para representar o grafo, a biblioteca *heapq* para implementar facilitar a implementação da fila de prioridade, além que para input e prints, a biblioteca *rich* é utilizada

A implementação do Caixeiro viajante é um algoritmo bem caro de ser executado, portanto fica inviável a sua utilização em grandes grafos, tanto que passando de 150 vertices, o algoritmo demora muito para encontrar uma solução e ainda existe a chance dos recursos computacionais acabarem e o Python "matar" o processo por falta de memória e além de ter muitas chamadas.


## <p align="center">Definição da parâmetros</p>


O usuário pode definir, qual arquivo será lido e utilizado no algoritmo, com base nas entradas que estão disponiveis na pasta, terá um menu para que ela possa selecionar

Para a utilização do algoritmo da busca tabu, o usuário define os parâmetros do tamanho da lista tabu que será utilizada e também quantas iterações serão feitas. Estas duas entradas devem ser feitas pelo usuário, e a partir delas o algoritmo irá rodar e retornar o menor caminho encontrado.

## <p align="center">Leitura do Arquivo</p>

Os arquivos de entrada já estão predefindos dentro da pasta **Entradas**, tendo grafos de tamanho de 10 até 1500 vertices, todos com seus respectivos pesos. A leitura do arquivo lê todas as linhas, recebendo o número de vertices, assim sendo possivel criar e adicionar os nodes ao grafo, utilizando a biblioteca *networkx*

<p align="center">
    <img src="img/img3.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

<p align="center">
    <img src="img/img4.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>


# <p align="center">Implementação da Busca Tabu</p>


## <p align="center">Solução inicial do Caixeiro Viajante</p>


Para a solução inicial do caixeiro viajante, foi utilizado o algoritmo de Hamilton, onde ele percorre todos os vertices do grafo, e retorna um caminho possível, dentro do escopo do problema. O código do caminho hamiltoniano foi feito com base no vertice 1 como ponto de partida e caminhando por todo o grafo, voltando nele, mas nessa implementação, ele só consegue retornar o caminho, quando encontra o vertice inicial, sendo uma função recursiva, continuando a sua busca.

<br>

<p align="center">
    <img src="img/img5.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

## <p align="center">Percurso da Busca Tabu</p>

O algoritmo da busca tabu funciona com base nas suas iterações, assim gerando uma lista de vizinhos possiveis com base na solução inicial, no caso sendo destinado para o TSP, trocando 1 cidade com a outra, criando uma lista de vizinhos possiveis e impossiveis, sendo sorteado um vertice que será trocado, a implementação pode ser vista na Figura 06

<p align="center">
    <img src="img/img7.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

Na geração de vizinhos, é verificado se as gerações são possiveis, seria a verificação se o caminho é possivel até o final, percorrendo toda a lista e criando uma nova apenas dos que conseguem chegar no final. A implementação pode ser vista na Figura 07

<p align="center">
    <img src="img/img8.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

Com todos os vizinhos gerado e válidados, a hora agora é realizar a busca tabu, no caso ele passa por todos os vizinhos válidos selecionando-os, calculando o seu custo e verificando se ele está na lista tabu e também verificando se o custo do vizinho é melhor que o melhor custo encontrado até o momento. Inclusive, dentro deste laço é realizado o append na lista tabu, além da sua manipulação, no caso retirando o primeiro elemento da lista sendo o item mais velho já registrado. A implementação pode ser vista na Figura 08.

<p align="center">
    <img src="img/img6.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>


# <p align="center">Como o algoritmo mostra seus resultados</p>

O algoritmo mostra os resultados de forma bem simples, contendo as informaçõs de qual arquivo foi escolhido, o tamano da lista tabu e quantas iterações foram executadas. Conta o tempo de execução do código e si e também quanto tempo que demorou para achar uma solução inicial viavel. Mostra o caminho inicial, o último caminho encontrado, o melhor caminho e também o pior caminho encontrado, todos com os seus respectivos custos.

<p align="center">
    <img src="img/img9.png" width="80%" height="" 
    style="box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
</p>

# <p align="center">Requisitos mínimos de hardware</p>


- Processador: Intel Core i3 ou superior
- Memória RAM: 8GB sendo recomendado 16GB mas para uma execução razoável 32GB é o ideal
- Espaço em disco: 1GB
- Sistema Operacional: Windows 10 | 11 ou Linux

# <p align="center">Requisitos mínimos de software</p>

- Python 3.8 ou superior
- Bibliotecas: networkx, heapq, rich, para instalar as bibliotecas, basta executar o comando abaixo:
    - `pip install networkx`
    - `pip install heapq`
    - `pip install rich`

# <p align="center">Como usar</p>

Para executar o algoritmo, basta executar o arquivo `main.py` e seguir as instruções que aparecerão no terminal. O algoritmo irá pedir o arquivo de entrada, o tamanho da lista tabu e o número de iterações. Após isso, o algoritmo irá rodar e mostrar os resultados.

# <p align="center">Referências</p>

- [Documentação do NetworkX](https://networkx.org/)
- [Documentação do Heapq](https://docs.python.org/3/library/heapq.html)
- [Documentação do Rich](https://rich.readthedocs.io/en/latest/)
- [Busca Tabu](https://pt.wikipedia.org/wiki/Busca_tabu)
- [Problema do Caixeiro Viajante](https://pt.wikipedia.org/wiki/Problema_do_caixeiro-viajante)

