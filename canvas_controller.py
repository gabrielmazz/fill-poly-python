import tkinter as tk
import fill_poly as fp
import math
import os

from tkinter import colorchooser
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
from rich.console import Console
from rich.table import Table

# Define a variável global que determina a iteração
iteracao = 0
vertices_globais = []
vertices_globais_save = []

# Determina a cor globalmente
cor = (0, 0, 0) 

# Determina vertice selecionado, usado para modificar os vertices de um polygono
selected_vertex = None
closest_vertex = None

# Lista de poligonos que forma preenchidos com fill poly
lista_poligonos_preenchidos = []

# Lista das arestas que foram pintadas, está lista contem tuplas com os indices dos vertices e a cor 
lista_arestas_pintadas = []

# Lista dos vertices que forma pintadas
lista_vertices_pintados = []

# Lista de poligonos que foram apenas pintados
lista_poligonos_apenas_pintados = []

# ? Estrutura de cada lista (INFO)
# ? vertices_globais = [(x1, y1), (x2, y2), (x3, y3)]
# ? lista_poligonos_preenchidos = [Px, [[(V1, V2), (R, G, B)], [(V2, V3), (R, G, B)], [(V3, V1), (R, G, B)]]]
# ? lista_arestas_pintadas = [[(x1, y1), (x2, y2)], (R, G, B), (a1, a2), Px]
# ? lista_vertices_pintados = [(x1, y1), (R, G, B), Px, Vx]
# ? lista_poligonos_apenas_pintados = [Px, (R, G, B)]
   
# Reinicia os botões do mouse para que outra função nao tenha influencia (não pegar lixo de memoória)
def desvincular_eventos_drag(canvas):
    # Desvincula os eventos de clique e arrastar no canvas
    canvas.unbind("<Button-3>")
    canvas.unbind("<B3-Motion>") 

# ! Função que define aonde será colocado os vertices do poligono, quando o usuário clicar no canvas, ele cria um novo vértice,
# ! sendo representado por uma bolinha preta. Quando o usuário clicar 3 vezes, ele desenha o triângulo automaticamente, completando-o
# ! e bloqueando até ser clicado para criar um novo poligono
# * Todos os vertices são armazenados na lista de vertices globais, podendo manipular cada um separadamente
def clicar(event, vertices, canvas):

    # Define a função que cria um novo vértice e adiciona na lista de vértices temporáriamente
    def define_vertices(canvas, vertices, x, y):
        
        # Define as variáveis globais
        global iteracao
        
        # Marca o ponto clicado
        canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")  
        
        # Adiciona o vértice clicado na lista de vértices
        vertices.append((x, y))
        
        # Incrementa a iteração
        iteracao = iteracao + 1
         
    # * A função que controla se o usuário pode criar um novo triangulo, é feita através da iteração, quando o usuário clicar 3 vezes,
    # * portanto teste_desenha_triangulo() e libera_novo_poligono() andam de mãos dadas
    def teste_desenha_triangulo(canvas, vertices):

        # Desenha o triângulo se houver 3 vértices na lista registrados
        if iteracao == 3:
            
            # Adiciona os vertices na lista de vertices globais
            adiciona_vertices_globais(vertices)
            
            # Chama a função que desenha o triângulo
            desenhar_triangulo(canvas, vertices, cor=(170, 0, 255))  # Cor inicial: roxo claro 
       
    # Define a função que desenha o triângulo quando tiver os 3 vertices, chamada pela função teste_desenha_triangulo()
    def desenhar_triangulo(canvas, vertices, cor):
    
        # Cria o poligono no canvas
        canvas.create_polygon(vertices, fill="", outline="black")  # Desenha o triângulo
        
    # Define a função que adiciona os vertices na lista de vertices globais
    def adiciona_vertices_globais(vertices):
        
        vertices_aux = []
        vertices_aux = vertices.copy()
        
        # Adiciona os vertices na lista de vertices globais
        vertices_globais.append(vertices_aux)

    # Define as variáveis de evento
    x, y = event.x, event.y

    # ! Define a condição que o usuário só pode clicar 3 vezes, pois o algoritmo só desenha triângulos, está é a primeira condição
    # ! que o usuário deve seguir para desenhar um triângulo, isso é feito automaticamente
    if (iteracao <= 2):

        # Cria um novo vertice
        define_vertices(canvas, vertices, x, y)
        
        # Testa se pode desenhar o triangulo
        teste_desenha_triangulo(canvas, vertices)
    
# ! Define a função que determina as coordenadas do clique do mouse, apenas sendo chamada em funções especificas que precisam 
# ! saber aonde o usuário clicou para saber aonde está o poligono mais próximo
def determina_clique(event):
    clique_x = event.x
    clique_y = event.y
    
    return clique_x, clique_y

# ! A função tem como objetivo determinar o polígono mais próximo do ponto de clique, iterando sobre a lista de vértices de polígonos, 
# ! calculando a distância entre o ponto de clique e cada vértice do polígono (Distância euclidiana).
def determina_poligono_mais_perto(clique_x, clique_y, vertices_globais):
    
    # ? A função que calcula a distância euclidiana entre esses dois pontos usando a fórmula matemática sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def calcula_distancia_entre_dois_pontos(ponto1, ponto2):
        x1, y1 = ponto1
        x2, y2 = ponto2
    
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    menor_distancia = float("inf") # Define a menor distancia como infinito para garantir que a primeira distancia será menor

    # Compara a posição do clique com a posição dos poligonos com todos os poligonos da lista de
    # vertices globais
    for i, vertices_poligono in enumerate(vertices_globais):
        
        # Calcula a distancia entre o clique do mouse e o poligono
        distancias = [calcula_distancia_entre_dois_pontos((clique_x, clique_y), ponto) for ponto in vertices_poligono]

        # Encontra a menor distancia entre o clique do mouse e o poligono
        menor_distancia_poligono = min(distancias)
        
        if menor_distancia_poligono < menor_distancia:
            menor_distancia = menor_distancia_poligono
            poligono_mais_proximo = i   
            
    return poligono_mais_proximo

# ! Função que determina quais vertices fazem parte do poligono mais próximo, usando a lista de vertices pintados, isso será utilizado
# ! para pintar o poligono com fill poly, tendo como sua base o vertice e cor nele presente
def determina_vertices_com_cores(lista_vertices_pintados, poligono_mais_perto):
     
    # Lista auxiliar que determina os vertices com cores
    lista_aux = []
    lista_final = []
    
    # Determina os vertices com cores
    for i in range(len(lista_vertices_pintados)):
        if lista_vertices_pintados[i][2] == poligono_mais_perto:
            
            # Determina a posição do vertice pego da lista de vertices pintados
            lista_aux.append(lista_vertices_pintados[i][0])
            
            # Determina a cor do vertice pego da lista de vertices pintados
            lista_aux.append(lista_vertices_pintados[i][1])
            
            # Copia a lista auxiliar para a lista final
            lista_final.append(lista_aux)
            
            lista_aux = []
            
    return lista_final
       
# ! Define a função que determina a cor, usando o próprio colorchooser do tkinter, a função retorna uma tupla com os valores RGB.
def determina_cor():
    global cor
    cor = colorchooser.askcolor(title="Escolha uma cor")
    
    # Extrai os componentes RGB da cor inicial
    cor = cor[0]

# ? Função que recria o canvas inteiro, usada para atualizar o canvas quando o usuário clicar em algum botão
def refresh_all(canvas):
    refaz_todo_o_canvas(canvas)
    refaz_arestas_coloridas(canvas)
    refaz_vertices_coloridos(canvas)
    refresh_poligonos_pintados(canvas)
    
# ? Toda vez que o usuário modificar um poligono que já está preenchido, ele pode atualizar o fill poly, usando esta função
# TODO: A função não é atualizada a todo momento pois ela faz tantas chamadas que o programa para de responder
def refresh_fill_poly(canvas):
    
    lista_aux = []
    
    def refaz_arestas(canvas):
        
        # Refaz as arestas do poligono pretas
        for poligono in vertices_globais:
            canvas.create_polygon(poligono, fill="", outline="black")
            
        # Refaz as arestas coloridas
        refaz_arestas_coloridas(canvas) 
    
    # Função que atualiza o fill poly, pegando os vertices globais e a cor do poligono da lista de vertices pintados
    for i in range(len(lista_poligonos_preenchidos)):
        
        # Determina os vertices com cores
        lista_aux = determina_vertices_com_cores(lista_vertices_pintados, lista_poligonos_preenchidos[i][0])

        # Chama a função que faz o fill poly
        fp.fill_poly(lista_aux, canvas)
        
    refaz_arestas(canvas)

# ? Toda vez que o usuário modificar um poligono que já está pintado, ele pode atualizar os poligonos pintados, usando esta função
def refresh_poligonos_pintados(canvas):
    
    # Refaz os poligonos pintados indicado na posicao 1 da lista e na posicao 2 possui o RGB
    for i in range(len(lista_poligonos_apenas_pintados)):
        canvas.create_polygon(vertices_globais[lista_poligonos_apenas_pintados[i][0]],
                              fill=f'#{int(lista_poligonos_apenas_pintados[i][1][0]):02X}{int(lista_poligonos_apenas_pintados[i][1][1]):02X}{int(lista_poligonos_apenas_pintados[i][1][2]):02X}',
                              outline="black")
    
    refaz_arestas_coloridas(canvas)
    
    # Refaz os vertices coloridos
    refaz_vertices_coloridos(canvas)

# ? Toda vez que o usuário der um refresh no canvas, as arestas que foram pintadas serão atualizadas, pois elas 
# ? são armazenadas em uma lista, e quando o usuário arrasta um vértice, a aresta é atualizada com a sua devida cor
# TODO: Da mesma forma que a função refresh_fill_poly(), esta função não é atualizada a todo momento pois ela faz tantas 
# TODO chamadas que o programa para de responder, são muito funções para serem calculadas
def refaz_arestas_coloridas(canvas):
    
    # ! Função que atualiza as arestas, função estrutura de forma bem mais complexa que a maioria das funções
    # ! sua construção depende de vários cálculos e uma estrutura de dados muito ligada uma na outra
    def atualiza_arestas(canvas, i):
    
        # Diferença de valores de distancia entre os vertices, pegando o valor do vertice global
        diferenca_x_arestas_A = int(vertices_globais[lista_arestas_pintadas[i][3]][lista_arestas_pintadas[i][2][0]][0])
        diferenca_y_arestas_A = int(vertices_globais[lista_arestas_pintadas[i][3]][lista_arestas_pintadas[i][2][0]][1])

        diferenca_x_arestas_B = int(vertices_globais[lista_arestas_pintadas[i][3]][lista_arestas_pintadas[i][2][1]][0])
        diferenca_y_arestas_B = int(vertices_globais[lista_arestas_pintadas[i][3]][lista_arestas_pintadas[i][2][1]][1])
        
        # Diferença de valores de distancia entre os vertices, pegando o valor do vertice pintado
        diferenca_x_arestas_A_pintada = lista_arestas_pintadas[i][0][0][0]
        diferenca_y_arestas_A_pintada = lista_arestas_pintadas[i][0][0][1]

        diferenca_x_arestas_B_pintada = lista_arestas_pintadas[i][0][1][0]
        diferenca_y_arestas_B_pintada = lista_arestas_pintadas[i][0][1][1]

        # Calcula a diferença entre os valores de distancia entre os vertices, do global e do pintado
        diferenca_x_vertice_A_final = diferenca_x_arestas_A - diferenca_x_arestas_A_pintada
        diferenca_y_vertice_A_final = diferenca_y_arestas_A - diferenca_y_arestas_A_pintada

        diferenca_x_vertice_B_final = diferenca_x_arestas_B - diferenca_x_arestas_B_pintada
        diferenca_y_vertice_B_final = diferenca_y_arestas_B - diferenca_y_arestas_B_pintada

        # Atualiza a posição na lista_arestas_pintadas com a nova diferença somando com a posição antiga
        lista_arestas_pintadas[i][0][0] = (lista_arestas_pintadas[i][0][0][0] + diferenca_x_vertice_A_final, lista_arestas_pintadas[i][0][0][1] + diferenca_y_vertice_A_final)
        lista_arestas_pintadas[i][0][1] = (lista_arestas_pintadas[i][0][1][0] + diferenca_x_vertice_B_final, lista_arestas_pintadas[i][0][1][1] + diferenca_y_vertice_B_final)

        # Separa os valores de x e y para serem usados na função create_line()
        x0 = lista_arestas_pintadas[i][0][0][0]
        y0 = lista_arestas_pintadas[i][0][0][1]
        x1 = lista_arestas_pintadas[i][0][1][0]
        y1 = lista_arestas_pintadas[i][0][1][1]
        
        # Recria a aresta com a nova posição e a sua cor correspondente
        canvas.create_line(x0, y0, x1, y1, fill=f'#{int(lista_arestas_pintadas[i][1][0]):02X}{int(lista_arestas_pintadas[i][1][1]):02X}{int(lista_arestas_pintadas[i][1][2]):02X}')


    # Atualiza todas as arestas pintadas
    for i in range(len(lista_arestas_pintadas)):
        atualiza_arestas(canvas, i)
 
# ? Toda vez que o usuário modificar um poligono que já está preenchido, ele pode atualizar os vertices coloridos, usando esta função
# ? usando como base os vertices globais e a cor do poligono da lista de vertices pintados
def refaz_vertices_coloridos(canvas): 
    
    # Atualiza todos os vertices pintados pintando-os novamente
    for i in range(len(lista_vertices_pintados)):
        
        canvas.create_oval(vertices_globais[lista_vertices_pintados[i][2]][lista_vertices_pintados[i][3]][0]-2, 
                           vertices_globais[lista_vertices_pintados[i][2]][lista_vertices_pintados[i][3]][1]-2, 
                           vertices_globais[lista_vertices_pintados[i][2]][lista_vertices_pintados[i][3]][0]+2, 
                           vertices_globais[lista_vertices_pintados[i][2]][lista_vertices_pintados[i][3]][1]+2, 
                           fill=f'#{int(lista_vertices_pintados[i][1][0]):02X}{int(lista_vertices_pintados[i][1][1]):02X}{int(lista_vertices_pintados[i][1][2]):02X}')
        
    # Atualiza todos os vertices pintados na lista de vertices pintados
    for i in range(len(lista_vertices_pintados)):
        
        lista_vertices_pintados[i][0] = vertices_globais[lista_vertices_pintados[i][2]][lista_vertices_pintados[i][3]]
  
# ? Toda vez que o usuário modificar qualquer coisa, o canvas será limpo e todos os poligonos serão desenhados 
# ? novamente, dando um update completo na tela
def refaz_todo_o_canvas(canvas):
    
    # Limpa o canvas
    canvas.delete("all")
    
    for poligono in vertices_globais:
        canvas.create_polygon(poligono, fill="", outline="black")
        
    # Refaz a marca dos vertices no canvas
    for poligono in vertices_globais:
        for vertice in poligono:
            canvas.create_oval(vertice[0]-2, vertice[1]-2, vertice[0]+2, vertice[1]+2, fill="black")
    
# ! Função principal que determina o poligono mais próximo do clique do mouse e chama a função fill_poly() para pintar o poligono
# * A função fill_poly() é baseada em um algoritmo de preenchimento de polígonos aonde ele pinta pixel a pixel iterando de cima para baixo
def vertices_para_fill_poly(canvas, vertices):

    def refaz_arestas(canvas):
        
        # Refaz as arestas do poligono pretas
        for poligono in vertices_globais:
            canvas.create_polygon(poligono, fill="", outline="black")
            
        # Refaz as arestas coloridas
        refaz_arestas_coloridas(canvas)
    
    def usa_fill_poly(event):
        
        # Define uma lista que determina as coordenadas do clique do mouse, será usada no fill_poly()
        lista_aux_fill_poly = []
        
        # Lista da cor dos vertices pintados do poligono indicado
        lista_aux_cor_vertices = []
        
        # Variavel de controle que determina se o poligono já foi pintado
        poligono_pintado = False
        
        # Chama a função que determina as coordenadas do clique do mouse
        clique_x, clique_y = determina_clique(event)
    
        # Chama a função que determina o poligono mais perto
        poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
        # Determina os vertices com cores
        lista_aux = determina_vertices_com_cores(lista_vertices_pintados, poligono_mais_perto)
             
        # Chama a função que faz o fill poly
        fp.fill_poly(lista_aux, canvas)
        
        # Refaz as arestas
        refaz_arestas(canvas)
        
        # Verifica se o poligono já foi pintado anteriormente, se sim substitui a cor antiga pela nova
        for i in range(len(lista_poligonos_preenchidos)):
            if lista_poligonos_preenchidos[i][0] == poligono_mais_perto:
                lista_poligonos_preenchidos[i][1] = lista_aux
                poligono_pintado = True
                break
            
        # Verifica se o poligono foi apenas pintado anteriormente, se sim apaga ele da lista de poligonos apenas pintados
        for i in range(len(lista_poligonos_apenas_pintados)):
            if lista_poligonos_apenas_pintados[i][0] == poligono_mais_perto:
                lista_poligonos_apenas_pintados.pop(i)
                break
       
        # Se o poligono não foi pintado, adiciona ele na lista de poligonos preenchidos
        if poligono_pintado == False:
            
            # Adiciona o poligono preenchido na lista de poligonos preenchidos
            lista_aux_fill_poly.append(poligono_mais_perto)
            lista_aux_fill_poly.append(lista_aux)
        
            lista_poligonos_preenchidos.append(lista_aux_fill_poly)
      
    # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
    desvincular_eventos_drag(canvas)    
    
    # Chama a função que seleciona o poligono que o usuário deseja pintar
    canvas.bind("<Button-3>", lambda event: usa_fill_poly(event))       
  
# * Define a função que cria o menu de opções, na parte de cima do canvas, estará todas as opções e modificações que podem ser feitas
# * no programa, como por exemplo, criar um novo poligono, escolher a cor, limpar o canvas, etc.
def menu_opcoes(root, canvas, vertices):
    
    # Define a função que mostra uma caixa de diálogo com a descrição do programa
    def sobre_descricao():
        tk.messagebox.showinfo("Sobre", "Algoritmo de Fillpoly\n\n"
                                        "Desenvolvido por:\n"
                                        "    - Gabriel Mazzuco\n"
                                        "Disciplina: Computação Gráfica\n"
                                        "Professor: Adair Santa Catarina\n"
                                        "Instituição: Universidade Estadual do Oeste do Paraná\n"
                                        "Curso: Ciência da Computação\n")
    
    # Define uma função que apenas mostra um guia de comandos do teclado para o programa  
    def guia_comandos():
        tk.messagebox.showinfo("Guia de comandos",
                               "N - Novo polígono\n"
                               "C - Escolhe a cor\n"
                               "E - Editar polígono\n"
                               "F - Fill Poly\n"
                               "DEL - Excluir polígono\n\n"
                               "Para executar o comando em tela, clique botão direito do mouse\n")
  
    # ! Função de controle que libera um novo poligono para ser desenhado, quando o usuário clicar no botão "Novo poligono"
    # ! sendo usado para controlar a iteração, quando o usuário clicar 3 vezes, ele desenha o triângulo automaticamente, completando-o
    def libera_novo_poligono(vertices):
        global iteracao
        iteracao = 0
        
        # Limpa a lista de vertices
        vertices.clear()

    # ! Função que exclui um poligono em especifico, quando o usuário clicar no botão "Excluir poligono", ele poderá excluir
    # ! qualquer poligono que ele desejar
    def exclui_poligono():
        
        def refresh_all_local(canvas):
            refaz_todo_o_canvas(canvas)
            
            # Repinta no mesmo lugar as arestas coloridas
            for i in range(len(lista_arestas_pintadas)):
                canvas.create_line(lista_arestas_pintadas[i][0][0][0], lista_arestas_pintadas[i][0][0][1], lista_arestas_pintadas[i][0][1][0], lista_arestas_pintadas[i][0][1][1], fill=f'#{int(lista_arestas_pintadas[i][1][0]):02X}{int(lista_arestas_pintadas[i][1][1]):02X}{int(lista_arestas_pintadas[i][1][2]):02X}')
            
            # Repinta no mesmo lugar os vertices coloridos
            for i in range(len(lista_vertices_pintados)):
                
                x = lista_vertices_pintados[i][0][0]
                y = lista_vertices_pintados[i][0][1]
                
                canvas.create_oval(x-2, y-2, x+2, y+2, fill=f'#{int(lista_vertices_pintados[i][1][0]):02X}{int(lista_vertices_pintados[i][1][1]):02X}{int(lista_vertices_pintados[i][1][2]):02X}')

            refresh_fill_poly(canvas)
        
        # Determina o poligono no qual está sendo alterado
        def determina_poligono(event):
            
            # Chama a função que determina as coordenadas do clique do mouse
            clique_x, clique_y = determina_clique(event)
        
            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
            # Copia os vertices do poligono mais perto para a lista auxiliar
            lista_aux = vertices_globais[poligono_mais_perto].copy()
            
            return lista_aux, poligono_mais_perto
        
        # ! Função que exclui o poligono, quando o usuário clicar no botão "Excluir poligono", ele poderá 
        # ! excluir qualquer poligono que ele desejar
        def exclui(event, canvas):
            list_poligono, poligono_mais_perto = determina_poligono(event)
            
            # Exclui o poligono
            canvas.delete(list_poligono)
            
            refresh_all(canvas)
            
            # Exclui o poligono da lista de vertices globais
            vertices_globais.pop(poligono_mais_perto)
                        
            # Exclui o poligono da lista de arestas pintadas
            indices_to_remove = []
            for i in range(len(lista_arestas_pintadas)-1, -1, -1):
                if lista_arestas_pintadas[i][3] == poligono_mais_perto:
                    indices_to_remove.append(i)
            
            for index in indices_to_remove:
                lista_arestas_pintadas.pop(index)
            
            # Exclui o poligono da lista de vertices pintados
            indices_to_remove = []
            for i in range(len(lista_vertices_pintados)-1, -1, -1):
                if lista_vertices_pintados[i][2] == poligono_mais_perto:
                    indices_to_remove.append(i)
                    
            for index in indices_to_remove:
                lista_vertices_pintados.pop(index)
                
            # Exclude o poligono da lista de poligonos apenas pintados
            indices_to_remove = []
            for i in range(len(lista_poligonos_apenas_pintados)-1, -1, -1):
                if lista_poligonos_apenas_pintados[i][0] == poligono_mais_perto:
                    indices_to_remove.append(i)    
                    
            for index in indices_to_remove:
                lista_poligonos_apenas_pintados.pop(index)
            
            # Exclui o poligono da lista de poligonos preenchidos
            indices_to_remove = []
            for i in range(len(lista_poligonos_preenchidos)-1, -1, -1):
                if lista_poligonos_preenchidos[i][0] == poligono_mais_perto:
                    indices_to_remove.append(i)
                    
            for index in indices_to_remove:
                lista_poligonos_preenchidos.pop(index)
                
            # Refaz o canvas inteiro
            refresh_all_local(canvas)

        # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
        desvincular_eventos_drag(canvas)

        canvas.bind("<Button-3>", lambda event: exclui(event, canvas))  # TODO: Registro do clique do mouse
    
    # ! Função que determina a edição de um poligono, quando o usuário clicar no botão "Editar poligono", 
    # ! ele poderá editar todos os vertices de qualquer poligono, usando o algoritmo de edição de poligono
    def edita_poligono():
    
        # * Define a função que determina o poligono mais próximo do clique do mouse. Funcionando
        # * da mesma forma que qualquer função deste programa que determina o poligono mais próximo
        def determina_poligono(event):
            
            # Chama a função que determina as coordenadas do clique do mouse
            clique_x, clique_y = determina_clique(event)
        
            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
            # Copia os vertices do poligono mais perto para a lista auxiliar
            lista_aux = vertices_globais[poligono_mais_perto].copy()
            
            return lista_aux
        
        # ! Função essencial para o funcionamento da edição de uma aresta do poligono, ela determina o 
        # ! vértice mais próximo do clique, ainda usando a distância euclidiana mas agora com os vértices
        def click_canvas(event, canvas):
            
            global selected_vertex
            
            # Encontra o vértice mais próximo do clique do usuário
            x, y = determina_clique(event)
            
            # Determina a distancias minima
            min_distance = float('inf')

            # Vertices do poligono
            vertices = determina_poligono(event)

            for i, (vx, vy) in enumerate(vertices):
                distance = ((x - vx)**2 + (y - vy)**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    selected_vertex = i
            
        # ! Função muito essencial, aqui será pego a coordenada do novo vértice, e será atualizado na lista 
        # ! de vertices globais
        # TODO A função funciona segurando o mouse com o botão direito, e arrastando o vértice para a posição desejada
        def canvas_drag(event, canvas):
            x, y = determina_clique(event)
            
            # Determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(x, y, vertices_globais)
            
            polygon = determina_poligono(event)
                        
            # Atualiza a posição do vértice selecionado enquanto o usuário arrasta o mouse, atualiza tambem a posição das arestas
            # com base na lista de arestas pintadas e nos novos vertices
            if selected_vertex is not None:
                vertices_globais[poligono_mais_perto][selected_vertex] = (event.x, event.y)
                coords = sum(vertices_globais[poligono_mais_perto], ())  # Concatena as coordenadas x e y
                canvas.coords(polygon, *coords)  # Passa as coordenadas separadamente para a função canvas.coords()
            
            refresh_all(canvas)

        # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
        desvincular_eventos_drag(canvas)
        
        global vertices_globais_save
        
        # Copia os vertices globais para o save
        vertices_globais_save = vertices_globais.copy()
        
        # Chama a função que seleciona o poligono que será editado
        canvas.bind("<Button-3>", lambda event: click_canvas(event, canvas))  # TODO: Registro do clique do mouse
        canvas.bind("<B3-Motion>", lambda event: canvas_drag(event, canvas))  # TODO: Registro do arraste do mouse
    
    # Define a função que limpa o canvas completamente
    def limpar(canvas):
        global cor
        
        canvas.delete("all")
        vertices_globais.clear()
        lista_poligonos_preenchidos.clear()
        lista_arestas_pintadas.clear()
        lista_vertices_pintados.clear()
        lista_poligonos_apenas_pintados.clear()
        cor = (0, 0, 0)
          
    # ! Função que pinta as arestas, quando o usuário clicar no botão "Pintar arestas", ele poderá colorir qualquer aresta
    # ! de qualquer um dos poligonos
    # * Para pintar uma aresta nesse algoritmo, existe uma lógica bem mais desenvolvida, no caso quando o usuário clicar em uma aresta
    # * é salvo vários parametros em uma lista, como por exemplo, a cor, os vertices, o poligono, etc
    def pinta_arestas(canvas):
        
        # Define a função em que vai pintar a aresta
        def paint_aresta(event, edge_to_paint):

            lista_arestas_pintadas_aux = []
            aresta_pintada = False

            # Chama a função que determina as coordenadas do clique do mouse
            x, y = determina_clique(event)

            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(x, y, vertices_globais)

            # Obtém as coordenadas dos vértices
            x0, y0 = vertices_globais[poligono_mais_perto][edge_to_paint[0]]
            x1, y1 = vertices_globais[poligono_mais_perto][edge_to_paint[1]]

            # Pinta a aresta alterando a cor
            canvas.create_line(x0, y0, x1, y1, fill=f'#{int(cor[0]):02X}{int(cor[1]):02X}{int(cor[2]):02X}')
            
            # Determina o poligono que foi pintado sua aresta
            poligono = determina_poligono_mais_perto(x, y, vertices_globais)
            
            # Verifica se a aresta já foi pintada anteriormente, se sim substitui a cor antiga pela nova
            for i in range(len(lista_arestas_pintadas)):
                if lista_arestas_pintadas[i][2] == edge_to_paint and lista_arestas_pintadas[i][3] == poligono:
                    lista_arestas_pintadas[i][1] = cor
                    aresta_pintada = True
                    return
            
            
            if aresta_pintada == False:
            
                # Adiciona a aresta na lista de arestas pintadas e qual aresta foi pintada
                lista_coordena_aresta = [(x0, y0), (x1, y1)]
                
                lista_arestas_pintadas_aux.append(lista_coordena_aresta)
                lista_arestas_pintadas_aux.append(cor)
                lista_arestas_pintadas_aux.append(edge_to_paint)
                lista_arestas_pintadas_aux.append(poligono)          
                
                lista_arestas_pintadas.append(lista_arestas_pintadas_aux)       
           
        # ? A fórmula utilizada para calcular a distância entre um ponto e uma linha é conhecida como a fórmula da distância ponto-linha. 
        # ? Ela é baseada na geometria analítica e envolve a aplicação de conceitos como a fórmula da distância entre dois pontos e a equação geral de uma linha.
        def distancia_do_ponto_a_linha(x, y, x1, y1, x2, y2):
            
            # Calcula a distância do ponto à aresta usando a fórmula da distância ponto-linha
            numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
            denominator = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
            
            return numerator / denominator if denominator != 0 else 0
        
        # Define a função que determina o poligono mais próximo do clique do mouse
        def determina_poligono(event):
            
            # Chama a função que determina as coordenadas do clique do mouse
            clique_x, clique_y = determina_clique(event)
        
            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
            # Copia os vertices do poligono mais perto para a lista auxiliar
            lista_aux = vertices_globais[poligono_mais_perto].copy()
            
            return lista_aux
        
        # Função que determina a aresta que será pintada, quando o usuário clicar no botão "Pintar arestas",
        # será possivel saber qual aresta será pintada pela sua distancia
        def define_aresta(event):
            
            # Resgate das coordenadas do clique do mouse
            x, y = determina_clique(event)
            
            # Verifica a distância entre o ponto clicado e cada aresta do triângulo
            min_distance = float('inf')
            selected_edge = None
            
            # Determina o poligono mais perto
            vertices = determina_poligono(event)
            
            for i in range(len(vertices)):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % len(vertices)]  # Próximo vértice para fechar o polígono

                # Calcula a distância do ponto à aresta usando a fórmula da distância ponto-linha
                distance = distancia_do_ponto_a_linha(x, y, x1, y1, x2, y2)

                # Atualiza a aresta mais próxima se a distância for menor
                if distance < min_distance:
                    min_distance = distance
                    selected_edge = (i, (i + 1) % len(vertices))
                
            return selected_edge
      
        # Função apenas de controle, que chama as funções que determinam a aresta que será pintada e a função que pinta a aresta
        def controle(event):
            
            # Chama a função que determina a aresta que será pintada
            edge_to_paint = define_aresta(event)
            
            # Chama a função que pinta a aresta
            paint_aresta(event, edge_to_paint)
            
        # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
        desvincular_eventos_drag(canvas)

        canvas.bind("<Button-3>", lambda event: controle(event))  # TODO: Registro do clique do mouse
        
    # ! Função que pinta os vertices, quando o usuário clicar no botão "Pintar vertices", ele poderá colorir qualquer vertice
    def pinta_vertices(canvas):
        
        # Determina o poligono no qual está sendo alterado
        def determina_poligono(event):
            
            # Chama a função que determina as coordenadas do clique do mouse
            clique_x, clique_y = determina_clique(event)
        
            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
            return poligono_mais_perto
        
        def pinta_vertice(x, y, canvas):
            
            # Variavel de controle que determina se o vertice já foi pintado
            vertice_pintado = False
            
            lista_vertices_pintados_aux = []
            
            # Determina o poligono que foi pintado sua aresta
            poligono = determina_poligono_mais_perto(x, y, vertices_globais)
        
            # Desenha o vertice colorido
            canvas.create_oval(x-2, y-2, x+2, y+2, fill=f'#{int(cor[0]):02X}{int(cor[1]):02X}{int(cor[2]):02X}')
        
            # Verifica se o vertice já foi pintado anteriormente, se sim substitui a cor antiga pela nova
            for i in range(len(lista_vertices_pintados)):
                if lista_vertices_pintados[i][0] == (x, y):
                    lista_vertices_pintados[i][1] = cor
                    vertice_pintado = True
                    break
                    
            # Se o vertice não foi pintado, adiciona ele na lista de vertices pintados
            if vertice_pintado == False:
                
                # Adiciona o vertice na lista de vertices pintados
                lista_vertices_pintados_aux.append((x, y))
                lista_vertices_pintados_aux.append(cor)
                lista_vertices_pintados_aux.append(poligono)
                lista_vertices_pintados_aux.append(closest_vertex)
                
                # Adiciona o vertice na lista de vertices reais pintados
                lista_vertices_pintados.append(lista_vertices_pintados_aux)
       
        def define_vertice_proximo(event):
            
            global closest_vertex
            
            # Chama a função que determina as coordenadas do clique do mouse
            x, y = determina_clique(event)
            
            # Inicializa as váriveis para armazenar o vértice mais próximo e a distância mínima
            min_distance = float('inf')
            
            # Determina o poligono mais perto
            poligono_mais_perto = determina_poligono(event)
            
            # Calcula a distância entre o ponto clicado e cada vértice
            for i, (vx, vy) in enumerate(vertices_globais[poligono_mais_perto]):
                distance = ((x - vx)**2 + (y - vy)**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_vertex = i
            
            return poligono_mais_perto

        def controle_vertices(event):
            
            # Chama a função que determina o vertice mais próximo
            poligono_mais_perto = define_vertice_proximo(event)
            
            # Pinta o vertice
            pinta_vertice(vertices_globais[poligono_mais_perto][closest_vertex][0], vertices_globais[poligono_mais_perto][closest_vertex][1], canvas)
        
        # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
        desvincular_eventos_drag(canvas)
        
        canvas.bind("<Button-3>", lambda event: controle_vertices(event))  # TODO: Registro do clique do mouse  
    
    # ? Função que permite o usuário escolher a cor que ele deseja pintar os poligonos com apenas uma cor
    def pinta_poligono(canvas):
            
        # Determina o poligono no qual está sendo alterado
        def determina_poligono(event):
            
            # Chama a função que determina as coordenadas do clique do mouse
            clique_x, clique_y = determina_clique(event)
        
            # Chama a função que determina o poligono mais perto
            poligono_mais_perto = determina_poligono_mais_perto(clique_x, clique_y, vertices_globais)
        
            return poligono_mais_perto
        
        def pinta_poligono(event):
            
            # Determina o poligono que foi pintado sua aresta
            poligono = determina_poligono(event)
            
            # Desenha o poligono colorido
            canvas.create_polygon(vertices_globais[poligono], fill=f'#{int(cor[0]):02X}{int(cor[1]):02X}{int(cor[2]):02X}', outline="black")
            
            # Verifica se o poligono já foi pintado anteriormente, se sim substitui a cor antiga pela nova
            for i in range(len(lista_poligonos_apenas_pintados)):
                if lista_poligonos_apenas_pintados[i][0] == poligono:
                    lista_poligonos_apenas_pintados[i][1] = cor
                    return
                
            # Verifica se o poligono foi preenchido com o fillpoly, se sim, apaga-lo da lista de poligonos preenchidos
            for i in range(len(lista_poligonos_preenchidos)):
                if lista_poligonos_preenchidos[i][0] == poligono:
                    lista_poligonos_preenchidos.pop(i)
                    break
            
            # Se o poligono não foi pintado, adiciona ele na lista de poligonos pintados
            if poligono not in lista_poligonos_apenas_pintados:
                
                # Adiciona o poligono na lista de poligonos pintados
                lista_poligonos_apenas_pintados.append((poligono, cor))
                
        def controle_poligono(event):
            
            # Chama a função que determina o poligono mais próximo
            pinta_poligono(event)
        
        # Reinicia o botão do mouse para que outra função nao tenha influencia aqui
        desvincular_eventos_drag(canvas)
        
        canvas.bind("<Button-3>", lambda event: controle_poligono(event))
     
    # * Função que permite o usuário salvar um arquivo de dados, com todas as informações do programa, para posteriormente poder
    # * carregar o arquivo e continuar de onde parou
    def salva_arquivo_dados():
        
        # Abre uma caixa de diálogo para escolher o nome do arquivo
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".tk", filetypes=[("Arquivos de Texto", "*.tk")])

        # Se o usuário pressionar "Cancelar" na caixa de diálogo, nome_arquivo será uma string vazia
        if nome_arquivo:
            # Salva o arquivo de dados com o nome escolhido pelo usuário
            with open(nome_arquivo, "w") as arquivo:
                arquivo.write(f"{vertices_globais}\n")
                arquivo.write(f"{lista_poligonos_preenchidos}\n")
                arquivo.write(f"{lista_arestas_pintadas}\n")
                arquivo.write(f"{lista_vertices_pintados}\n")
                arquivo.write(f"{lista_poligonos_apenas_pintados}\n")
                arquivo.write(f"{cor}")
                
    # * Função que permite o usuário carregar um arquivo de dados, com todas as informações do programa, para continuar de onde parou
    def leitura_arquivos_dados():
        
        global vertices_globais, lista_poligonos_preenchidos, lista_arestas_pintadas, lista_vertices_pintados, lista_poligonos_apenas_pintados, cor
        
        # Leitura do arquivo de dados
        arquivo_selecionado = filedialog.askopenfilename(defaultextension=".tk", filetypes=[("Arquivos de Texto", "*.tk")], title="Selecione o arquivo de dados")
        
        # Tenta abrir o arquivo
        try:
            with open(arquivo_selecionado, "r") as arquivo:
                vertices_globais = eval(arquivo.readline())
                lista_poligonos_preenchidos = eval(arquivo.readline())
                lista_arestas_pintadas = eval(arquivo.readline())
                lista_vertices_pintados = eval(arquivo.readline())
                lista_poligonos_apenas_pintados = eval(arquivo.readline())
                cor = eval(arquivo.readline())
                
        except Exception as e:
            print("Erro ao ler o arquivo de dados")
                    
        # Refaz o canvas inteiro
        refaz_todo_o_canvas(canvas)
        
        # Repinta no mesmo lugar as arestas coloridas
        for i in range(len(lista_arestas_pintadas)):
            canvas.create_line(lista_arestas_pintadas[i][0][0][0], lista_arestas_pintadas[i][0][0][1], lista_arestas_pintadas[i][0][1][0], lista_arestas_pintadas[i][0][1][1], fill=f'#{int(lista_arestas_pintadas[i][1][0]):02X}{int(lista_arestas_pintadas[i][1][1]):02X}{int(lista_arestas_pintadas[i][1][2]):02X}')
        
        # Repinta no mesmo lugar os vertices coloridos
        for i in range(len(lista_vertices_pintados)):
            
            x = lista_vertices_pintados[i][0][0]
            y = lista_vertices_pintados[i][0][1]
            
            canvas.create_oval(x-2, y-2, x+2, y+2, fill=f'#{int(lista_vertices_pintados[i][1][0]):02X}{int(lista_vertices_pintados[i][1][1]):02X}{int(lista_vertices_pintados[i][1][2]):02X}')
              
        # Atualiza poligonos apenas pintados
        refresh_poligonos_pintados(canvas)
        
        # Atualiza o fill poly
        refresh_fill_poly(canvas)
    
    # * Função que permite o usuário salvar a imagem do canvas em png
    def salva_canvas_imagem(canvas):
            
        # Abre uma caixa de diálogo para escolher o nome do arquivo
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos de Imagem", "*.png")])
        
        # Se o usuário pressionar "Cancelar" na caixa de diálogo, nome_arquivo será uma string vazia
        if nome_arquivo:
            
            # Salva a imagem do canvas
            canvas.postscript(file=f"{nome_arquivo}.eps", colormode='color')
            img = Image.open(f"{nome_arquivo}.eps")
            
            img.save(f"{nome_arquivo}")
            
        # Apaga o arquivo .eps
        os.remove(f"{nome_arquivo}.eps")
     
     # ? Estrutura de cada lista (INFO)
       
    # Função para debugar o código
    def debuga_vertices_globais():
        
        def printa_info_vertices_globais():
            
            console = Console()

            vertices_globais = [
                f'(x1, y1)',
                f'(x2, y2)',
                f'(x3, y3)'
            ]

            console.print(f"Vertices Globais: {vertices_globais}", style="bold yellow")
            console.print(f"Aonde x1, y1, x2, y2, x3, y3 são as coordenadas dos vertices do poligono", style="yellow")
            
        console = Console()
        
        printa_info_vertices_globais()
        
        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Vertices Globais", title_style="bold magenta")
        table.add_column("Poligono indicado", justify="center")
        table.add_column("Coordenadas do Vertices", justify="center")

        # Adicionar dados à tabela
        for i in range(len(vertices_globais)):
            vertices = vertices_globais[i]
            vertices_str = "\n".join([f"({v[0]}, {v[1]})" for v in vertices])
            table.add_row(str(i), vertices_str)    

        console.print(table)
        
    def debuga_lista_poligonos_preenchidos():
        
        def printa_info_lista_poligonos_preenchidos():
            
            console = Console()

            lista_poligonos_preenchidos = [
                f'Px',
                f'[(V1, V2), (R, G, B)], [(V2, V3), (R, G, B)], [(V3, V1), (R, G, B)]'
            ]

            console.print(f"Lista de Poligonos Preenchidos: {lista_poligonos_preenchidos}", style="bold yellow")
            console.print(f"Aonde Px é o numero do poligono, V1, V2, V3 são os vertices do poligono e R, G, B são as cores", style="yellow")
        
        console = Console()
        
        printa_info_lista_poligonos_preenchidos()

        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Poligonos Preenchidos", title_style="bold magenta")
        table.add_column("Poligono indicado", justify="center")
        table.add_column("Coordenadas dos Vertices", justify="center")
        table.add_column("Cores", justify="center")

        # Adicionar dados à tabela
        for poligono in lista_poligonos_preenchidos:
            if len(poligono) >= 2:
                num_vertices, vertices_cor = poligono
                if len(vertices_cor) >= 2:
                    vertices, cores = zip(*vertices_cor)
                    
                    # Formatar os dados para impressão
                    vertices_str = "\n".join([f"({v[0]}, {v[1]})" for v in vertices])
                    cores_str = "\n".join([f"({c[0]}, {c[1]}, {c[2]})" for c in cores])

                    # Adicionar uma linha à tabela
                    table.add_row(str(num_vertices), vertices_str, cores_str)    

        console.print(table)
           
    def debuga_lista_arestas_pintadas():
        
        def printa_info_lista_arestas_pintadas():
            
            console = Console()

            lista_arestas_pintadas = [
                f'[(x1, y1), (x2, y2)]',
                f'(R, G, B)',
                f'(a1, a2)',
                f'Px'
            ]

            console.print(f"Lista de Arestas Pintadas: {lista_arestas_pintadas}", style="bold yellow")
            console.print(f"Aonde x1, y1, x2, y2 são as coordenadas das vertices, R, G, B são as cores, a1, a2 é a numeração da arestas e Px é o numero do poligono", style="yellow")
           
        console = Console()
        
        printa_info_lista_arestas_pintadas()

        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Arestas Pintadas", title_style="bold magenta")
        table.add_column("Aresta indicada", justify="center")
        table.add_column("Coordenada dos Vertices", justify="center")
        table.add_column("Cores", justify="center")
        table.add_column("Poligono indicado", justify="center")

        # Adicionar dados à tabela
        for aresta in lista_arestas_pintadas:
            vertices, cor, aresta_num, poligono = aresta
            vertices_str = "\n".join([f"({v[0]}, {v[1]})" for v in vertices])
            table.add_row(str(aresta_num), vertices_str, str(cor), str(poligono))    

        console.print(table)
        
    def debuga_lista_vertices_pintados():
        
        def printa_info_lista_vertices_pintados():
            
            console = Console()

            lista_vertices_pintados = [
                f'(x1, y1)',
                f'(R, G, B)',
                f'Px',
                f'Vx'
            ]

            console.print(f"Lista de Vertices Pintados: {lista_vertices_pintados}", style="bold yellow")
            console.print(f"Aonde x1, y1 são as coordenadas das vertices, R, G, B são as cores, Px é o numero do poligono e Vx é o numero do vertice", style="yellow")
        
        console = Console()
        
        printa_info_lista_vertices_pintados()

        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Vertices Pintados", title_style="bold magenta")
        table.add_column("Vertice indicado", justify="center")
        table.add_column("Coordenada dos Vertices", justify="center")
        table.add_column("Cores", justify="center")
        table.add_column("Poligono indicado", justify="center")
        
        # Adicionar dados à tabela
        for vertice in lista_vertices_pintados:
            vertices, cor, poligono, vertice_num = vertice
            table.add_row(str(vertice_num), str(vertices), str(cor), str(poligono))


        console.print(table)
        
    def debuga_lista_poligonos_apenas_pintados():
        
        def printa_info_lista_poligonos_apenas_pintados():
            
            console = Console()

            lista_poligonos_apenas_pintados = [
                f'Px',
                f'(R, G, B)'
            ]

            console.print(f"Lista de Poligonos Apenas Pintados: {lista_poligonos_apenas_pintados}", style="bold yellow")
            console.print(f"Aonde Px é o numero do poligono e R, G, B são as cores", style="yellow")
         
        console = Console()
        
        printa_info_lista_poligonos_apenas_pintados()

        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Poligonos Apenas Pintados", title_style="bold magenta")
        table.add_column("Poligono indicado", justify="center")
        table.add_column("Cores", justify="center")

        # Adicionar dados à tabela
        for poligono in lista_poligonos_apenas_pintados:
            poligono_num, cor = poligono
            table.add_row(str(poligono_num), str(cor))    

        console.print(table)    
     
    def debuga_cor():
          
        def printa_info_cor():
            
            console = Console()

            cor = [
                f'R',
                f'G',
                f'B'
            ]

            console.print(f"Cor: {cor}", style="bold yellow")
            console.print(f"Aonde R, G, B são as cores indicadas na entrada do tkinter", style="yellow")  
         
        console = Console()
        
        printa_info_cor()

        print("\n")
        table = Table(show_header=True, header_style="bold magenta", show_lines=True, title="Cor", title_style="bold magenta")
        table.add_column("R", justify="center")
        table.add_column("G", justify="center")
        table.add_column("B", justify="center")

        # Adicionar dados à tabela
        table.add_row(str(cor[0]), str(cor[1]), str(cor[2]))    

        console.print(table)    
       
    def debuga_todas_lista():
        
        limpa_console()
        
        debuga_vertices_globais()
        print("\n\n")
        
        debuga_lista_poligonos_preenchidos()
        print("\n\n")
        
        debuga_lista_arestas_pintadas()
        print("\n\n")
        
        debuga_lista_vertices_pintados()
        print("\n\n")
        
        debuga_lista_poligonos_apenas_pintados()
        print("\n\n")
        
        debuga_cor()
     
    def limpa_console():
        os.system('cls' if os.name == 'nt' else 'clear')
     
    # Cria um menu de opções (Parte de cima)
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    # Cria um menu "Arquivo"
    arquivo_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Arquivo", menu=arquivo_menu)
    
    # Cria um menu "Editar"
    menu_bar_editar = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Editar", menu=menu_bar_editar)
    
    # Cria um menu "Pintar"
    menu_bar_pintar = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Pintar", menu=menu_bar_pintar)
    
    # Cria um menu "Refrash"
    menu_bar_refrash = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Refrash", menu=menu_bar_refrash)
    
    # Cria um menu "Sobre"
    menu_bar_sobre = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Sobre", menu=menu_bar_sobre)
    
    # Cria um menu "Debug"
    menu_bar_debug = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Debug", menu=menu_bar_debug)
      
    # Cria um menu "Sair"
    menu_bar_sair = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Sair", menu=menu_bar_sair)
    
    #-----------------------------------------------------------------------------------------------------------------#
    
    # Adiciona o botão "Salvar dados" no menu "Arquivo"
    arquivo_menu.add_command(label="Salvar dados", command=lambda: salva_arquivo_dados())
    
    # Adiciona o botão "Carregar dados" no menu "Arquivo"
    arquivo_menu.add_command(label="Carregar dados", command=lambda: leitura_arquivos_dados())
    
    # Adiciona o botão "Salvar imagem" no menu "Arquivo"
    arquivo_menu.add_command(label="Salvar imagem", command=lambda: salva_canvas_imagem(canvas))
       
    #-----------------------------------------------------------------------------------------------------------------#
        
    # Adiciona um botão "Novo poligono" no menu "Editar"
    menu_bar_editar.add_command(label="Novo poligono", command=lambda: libera_novo_poligono(vertices))
    
    # Adiciona o botão N para criar um novo poligono
    root.bind("<n>", lambda event: libera_novo_poligono(vertices))
        
    # Adiciona um botão "Editar vértices" no menu "Editar"
    menu_bar_editar.add_command(label="Editar vértices", command=edita_poligono)
    
    # Adiciona o botão E para editar um poligono
    root.bind("<e>", lambda event: edita_poligono())
    
    # Adiciona um botão "Excluir poligono" no menu "Editar"
    menu_bar_editar.add_command(label="Excluir poligono", command=exclui_poligono)
    
    # Adiciona o botão DEL para excluir um poligono
    root.bind("<Delete>", lambda event: exclui_poligono())
    
    # Adiciona um botão "Limpar" no menu "Editar"
    menu_bar_editar.add_command(label="Limpar canvas", command=lambda: limpar(canvas))
    
    #-----------------------------------------------------------------------------------------------------------------#
        
    # Adiciona um botão "Pintar arestas" no menu "Pintar"
    menu_bar_pintar.add_command(label="Pintar arestas", command=lambda: (pinta_arestas(canvas)))
    
    # Adiciona um botão "Pintar vertices" no menu "Pintar"
    menu_bar_pintar.add_command(label="Pintar vertices", command=lambda: (pinta_vertices(canvas)))
    
    # Adiciona um botão "Pintar poligono" no menu "Pintar"
    menu_bar_pintar.add_command(label="Pintar poligono", command=lambda: (pinta_poligono(canvas)))
    
    # Adiciona um botão "Escolher cor" no menu "Pintar"
    menu_bar_pintar.add_command(label="Escolher cor", command=lambda: determina_cor())
    
    # Adciona o botão C para escolher a cor
    root.bind("<c>", lambda event: determina_cor())
    
    # Adiciona um botão "Fill Poly" no menu "Arquivo"
    menu_bar_pintar.add_command(label="Fill Poly", command=lambda: (vertices_para_fill_poly(canvas, vertices)))
    
    # Adiciona o botão F para o fill poly
    root.bind("<f>", lambda event: (vertices_para_fill_poly(canvas, vertices)))
    
    #-----------------------------------------------------------------------------------------------------------------#
        
    # Adiciona um botão "Refrash Fill Poly" no menu "Refrash"
    menu_bar_refrash.add_command(label="Refrash Fill Poly", command=lambda: refresh_fill_poly(canvas))
    
    #-----------------------------------------------------------------------------------------------------------------#
        
    # Adiciona um botão "Sobre" no menu "Sobre"
    menu_bar_sobre.add_command(label="Descrição", command=sobre_descricao)
    
    menu_bar_sobre.add_command(label="Guia de comandos", command=guia_comandos)  
    
    #-----------------------------------------------------------------------------------------------------------------#
    
    # Adiciona um botão "Debuga vertices globais" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga vertices globais", command=debuga_vertices_globais)
    
    # Adiciona um botão "Debuga lista poligonos preenchidos" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga lista poligonos preenchidos", command=debuga_lista_poligonos_preenchidos)
    
    # Adiciona um botão "Debuga lista poligonos apenas pintados" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga lista poligonos apenas pintados", command=debuga_lista_poligonos_apenas_pintados)
    
    # Adiciona um botão "Debuga lista arestas pintadas" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga lista arestas pintadas", command=debuga_lista_arestas_pintadas)
    
    # Adiciona um botão "Debuga lista vertices pintados" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga lista vertices pintados", command=debuga_lista_vertices_pintados)
    
    # Adiciona um botão "Debuga cor" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga cor", command=debuga_cor)
    
    # Adiciona um botão "Debuga todas as listas" no menu "Debug"
    menu_bar_debug.add_command(label="Debuga todas as listas", command=debuga_todas_lista)
    
    #-----------------------------------------------------------------------------------------------------------------#
    
    # O botão sair no menu "Sair" fecha a janela
    menu_bar_sair.add_command(label="Sair", command=root.destroy)
    
    #-----------------------------------------------------------------------------------------------------------------#