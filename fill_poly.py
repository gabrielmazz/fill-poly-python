import tkinter as tk

def fill_poly(vertices, canvas):
    
    def interpolate_color(color1, color2, color3, t1, t2, t3):
        # Interpola as componentes RGB
        r = int(t1 * color1[0] + t2 * color2[0] + t3 * color3[0])
        g = int(t1 * color1[1] + t2 * color2[1] + t3 * color3[1])
        b = int(t1 * color1[2] + t2 * color2[2] + t3 * color3[2])

        # Garante que os valores RGB estejam no intervalo correto (0-255)
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))

        # Retorna a cor como uma tupla (r, g, b)
        return r, g, b


    def rgb_to_hex(rgb):
        # Converte a cor RGB para o formato #RRGGBB
        return f'#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'
    
    # Esta função preenche um polígono triangular com uma cor no canvas fornecido.
    # Ela recebe uma lista de vértices do polígono e o canvas onde o polígono será desenhado.

    # Verifica se os 3 vértices estão na lista, se não, exibe uma mensagem de erro e interrompe o preenchimento.
    if len(vertices) != 3:
        tk.messagebox.showerror("Erro", "Deve-se colorir todos os vértices do triângulo para executar o preenchimento")
        return

    # Encontra a coordenada y mínima e máxima dos vértices do triângulo.
    min_y = min(vertices, key=lambda p: p[0][1])[0][1]
    max_y = max(vertices, key=lambda p: p[0][1])[0][1]

    # ! Neste trecho de código, esta sendo percorrido cada linha vertical de um triângulo 
    # ! e verificando as interseções entre essa linha e as arestas do triângulo.
    for y in range(min_y, max_y + 1):
        
        # Lista de interseções entre a linha vertical e as arestas do triângulo.
        intersections = []

        # ? Percorre cada uma das três arestas do triângulo. Dentro desse loop, obtemos as 
        # ? coordenadas x e y dos pontos inicial e final da aresta.
        for i in range(3):
            x1, y1 = vertices[i][0]
            x2, y2 = vertices[(i + 1) % 3][0]

            # ! Verifica-se se a linha vertical cruza a aresta do triângulo. Para fazer isso, compara-se
            # ! as coordenadas y dos pontos inicial e final da aresta com a coordenada y da linha vertical
            # * Adiciona-se uma pequena tolerância de 1e-6 para lidar com possíveis erros de arredondamento
            # * evitando erros de ser igual a 0 e não ser considerado como interseção.
            if y1 <= y + 1e-6 <= y2 or y2 <= y + 1e-6 <= y1:
                if y2 - y1 != 0:
                    
                    # Calcula a coordenada x da interseção usando interpolação linear.
                    x = int(x1 + (y + 1e-6 - y1) * (x2 - x1) / (y2 - y1))
                    intersections.append(x)

        # Ordena as interseções em ordem crescente.
        intersections.sort()
        
        # ? O resultado final será uma lista de coordenadas x das interseções entre a linha vertical e as 
        # ? arestas do triângulo, ordenadas em ordem crescente.

        # ! Preenche a linha horizontal entre cada par de interseções
        # ! A cada iteração, pega-se dois valores de interseção consecutivos, x1 e x2. 
        # ! Se não houver um próximo valor de interseção, pega-se o primeiro valor novamente.
        for i in range(0, len(intersections), 2):
            
            x1 = intersections[i]
            x2 = intersections[i + 1] if i + 1 < len(intersections) else intersections[0]

            # ! Itera sobre os valores de x na faixa de x1 a x2. Isso significa que estamos percorrendo 
            # ! cada pixel na linha horizontal entre as interseções.
            for x in range(x1, x2 + 1):
                
                # ! Calcula os pesos de interpolação para cada vértice do triângulo.
                
                # * A variável d é inicializada como uma lista vazia. Ela será usada para armazenar 
                # * as distâncias entre cada vértice do triângulo e um ponto de referência (x, y).
                
                # * É feito um loop através dos vértices do triângulo. Cada vértice é uma tupla ((vx, vy), _), 
                # * onde (vx, vy) representa as coordenadas do vértice e _ é um valor não utilizado.
                
                # ? É calculada a distância entre o vértice atual e o ponto de referência (x, y) usando a fórmula da distância euclidiana: 
                # ? ((vx - x) ** 2 + (vy - y) ** 2) ** 0.5. Essa fórmula calcula a distância entre dois pontos em um plano cartesiano.
                d = [((vx - x) ** 2 + (vy - y) ** 2) ** 0.5 for ((vx, vy), _) in vertices]
                
                # ? Total é inicializada como a soma dos inversos dos quadrados de cada distância em d. 
                # * O valor 1e-6 é adicionado ao denominador para evitar divisão por zero
                total = sum(1 / ((di + 1e-6) ** 2) for di in d)
                
                # ? É feito outro loop através das distâncias em d. Para cada distância di, é calculado o peso de interpolação correspondente 
                # ? usando a fórmula 1 / ((di + 1e-6) ** 2). O valor 1e-6 é adicionado ao denominador novamente para evitar divisão por zero.
                # * Aqui é garantido que as cores dos vértices sejam interpoladas de acordo com a distância entre o vértice e o ponto de referência (x, y)
                # * fazendo o efeito de gradiente necessário para o preenchimento, isso garante tambem que o inicio perto dos vertices seja mais forte por causa
                # * do peso de interpolação ser maior e conforme vai se afastando o peso vai diminuindo e a cor vai ficando mais fraca
                t = [(1 / ((di + 1e-6) ** 2)) / total for di in d]

                # ! Essa função recebe três cores (representadas como tuplas RGB), juntamente com três pesos de interpolação (t1, t2, t3).
                # ! Ela realiza a interpolação das componentes RGB das cores de acordo com os pesos fornecidos
                
                # ? Para cada componente (vermelho, verde e azul), a função calcula o valor interpolado multiplicando cada componente da cor pelo peso correspondente 
                # ? e somando os resultados. (r = int(t1 * color1[0] + t2 * color2[0] + t3 * color3[0]))
                color = interpolate_color(vertices[0][1], vertices[1][1], vertices[2][1], t[0], t[1], t[2])

                # Converte a cor RGB para o formato hexadecimal apenas para exibição no canvas
                color_hex = rgb_to_hex(color)

                # Desenha o pixel na tela usando a cor calculada.
                canvas.create_line(x, y, x + 1, y, fill=color_hex)