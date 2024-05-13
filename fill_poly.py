import tkinter as tk
import time

def fill_poly(vertices, canvas):
    
    # Calcula o tempo de execução
    start_time = time.time()
    
    # Verifica se os 3 vértices estão na lista, se não, exibe uma mensagem de 
    # erro e interrompe o preenchimento.
    if len(vertices) != 3:
        tk.messagebox.showerror("Erro", "Deve-se colorir todos os vértices do triângulo para executar o preenchimento")
        return
    
    # Passa uma camada branca no trinângulo
    canvas.create_polygon(*vertices[0][0], *vertices[1][0], *vertices[2][0], fill='white', outline='white')
    
    # Cham ao método rasterize_triangle para preencher o triângulo
    rasterize_triangle(vertices[0][0], vertices[1][0], vertices[2][0], vertices[0][1], vertices[1][1], vertices[2][1], canvas)

    # Atualiza a tela
    canvas.update()
    
    # Calcula o tempo de execução
    print("Tempo de execução (FillPoly):", time.time() - start_time)


def rasterize_triangle(v1, v2, v3, c1, c2, c3, canvas):
    
    # Verifica se o triângulo é degenerado
    if v1[1] == v2[1] == v3[1] or v1[0] == v2[0] == v3[0]:
        print("Triângulo degenerado")
        return
    
    # Ordena os vértices por coordenada y, o menor y primeiro, o maior y por último
    # usando a função sorted com a chave lambda
    vertices = sorted([(v1, c1), (v2, c2), (v3, c3)], key=lambda v: v[0][1])
    
    # Separa os vértices e as cores respectivamente
    v1, c1 = vertices[0]
    v2, c2 = vertices[1]
    v3, c3 = vertices[2]
    
    # Calcula as taxas de variação das cores
    dc12 = [((1 / (v2[1] - v1[1])) * (c2[i] - c1[i])) for i in range(3)]
    dc13 = [((1 / (v3[1] - v1[1])) * (c3[i] - c1[i])) for i in range(3)]
    dc23 = [((1 / (v3[1] - v2[1])) * (c3[i] - c2[i])) for i in range(3)]
    
    # Inicializa as cores nos vértices
    c12_r, c12_g, c12_b = c1
    c13_r, c13_g, c13_b = c1
    c23_r, c23_g, c23_b = c2

    # Passa uma camada branca no trinângulo
    canvas.create_polygon(*vertices[0][0], *vertices[1][0], *vertices[2][0], fill='white', outline='white')
    
    # Rasteriza o triângulo linha por linha
    for y in range(v1[1], v3[1] + 1):

        # Rasteriza a parte superior do triângulo, até a sua metade, no caso
        # até o vertice 2
        if y < v2[1]:
    
            draw_scanline(v1, v2, [c12_r, c12_g, c12_b], v1, v3, [c13_r, c13_g, c13_b], y, canvas)
            c12_r += dc12[0]    # Incrementa a cor vermelha (1->2)
            c12_g += dc12[1]    # Incrementa a cor verde    (1->2)
            c12_b += dc12[2]    # Incrementa a cor azul     (1->2)
            
        # Rasteriza a parte inferior do triângulo, a partir da metade, no caso
        # abaixo do vertice 2
        else:

            draw_scanline(v2, v3, [c23_r, c23_g, c23_b], v1, v3, [c13_r, c13_g, c13_b], y, canvas)
            c23_r += dc23[0]    # Incrementa a cor vermelha (2->3)
            c23_g += dc23[1]    # Incrementa a cor verde    (2->3)
            c23_b += dc23[2]    # Incrementa a cor azul     (2->3)
            
        c13_r += dc13[0]        # Incrementa a cor vermelha (1->3)
        c13_g += dc13[1]        # Incrementa a cor verde    (1->3)
        c13_b += dc13[2]        # Incrementa a cor azul     (1->3)
        
    return

def draw_scanline(v1, v2, c1, v3, v4, c2, y, canvas):
    
    # Calcula as coordenadas x nas duas arestas do triângulo
    x1 = v1[0] + (v2[0] - v1[0]) * (y - v1[1]) / (v2[1] - v1[1]) if v2[1] != v1[1] else v1[0]
    x2 = v3[0] + (v4[0] - v3[0]) * (y - v3[1]) / (v4[1] - v3[1]) if v4[1] != v3[1] else v3[0]

    # Garante que x1 é a coordenada x mais à esquerda e x2 é a coordenada x mais à direita
    # sem isso, a linha não é desenhada corretamente ou até mesmo não é desenhada
    if x1 > x2:
        x1, x2 = x2, x1     # Troca os valores de x1 e x2
        c1, c2 = c2, c1     # Troca as cores de c1 e c2

    # Calcula a taxa de variação da cor
    dc_r = (c2[0] - c1[0]) / (x2 - x1) if x2 != x1 else 0   # Taxa de variação da cor vermelha
    dc_g = (c2[1] - c1[1]) / (x2 - x1) if x2 != x1 else 0   # Taxa de variação da cor verde
    dc_b = (c2[2] - c1[2]) / (x2 - x1) if x2 != x1 else 0   # Taxa de variação da cor azul
    
    # Inicializa a cor no pixel mais à esquerda
    c_r, c_g, c_b = c1

    # Desenha a linha de varredura pixel por pixel
    # percorrendo a linha de varredura de x1 até x2
    for x in range(int(x1), int(x2)):       
        set_pixel_color(x, y, [c_r, c_g, c_b], canvas)  # Define a cor do pixel
        c_r += dc_r    # Incrementa a cor vermelha
        c_g += dc_g    # Incrementa a cor verde
        c_b += dc_b    # Incrementa a cor azul

def set_pixel_color(x, y, color, canvas):
    # Converte a lista de cor para uma string no formato '#RRGGBB'
    color = '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))

    # Desenha um pixel na posição (x, y) com a cor especificada
    canvas.create_line(x, y, x+1, y, fill=color)