import tkinter as tk
import canvas_controller as cc
import os

if __name__ == "__main__":
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Determina a criação de um novo poligono, e suas manipulações
    novo_poligono = True
    
    # Cria a janela principal do programa (Canvas)
    root = tk.Tk()
    root.title("Trabalho 01 - Computação Gráfica - Algoritmo de Fillpoly")

    # Determina o tamanho da janela em HD
    canvas = tk.Canvas(root, width=1600, height=720)
    canvas.pack()
    while True:
        
        # * Cria uma lista de vertices, usada praticamente em todo o programa 
        vertices = []
        
        # Cria um menu de opções
        cc.menu_opcoes(root, canvas, vertices)
        
        # Usa uma função lambda para atrasar a chamada da função clicar
        if novo_poligono == True:
            canvas.bind("<Button-1>", lambda event: cc.clicar(event, vertices, canvas))
            
        root.update()
        root.mainloop()
