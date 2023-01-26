import pygame
from random import *
from os import *
import sys

def showBoard():
    for fila in BOARD:
        for valor in fila:
            print(valor, end=" ")

#Inicia el juego
pygame.init()

#Variables constantes globales
#Paleta de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HC74225 = (199, 66, 37)
H61CD35 = (97, 205, 53)

#Matriz que define mi tablero
BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

#Definición de tamaños
MARGIN = 20
SQ_WIDTH = 30
SPACING = 3
WN_WIDTH = (MARGIN * 2) + ((SQ_WIDTH + SPACING) * len(BOARD[0])) - 5
WN_HEIGHT = (MARGIN * 2) + ((SQ_WIDTH + SPACING) * len(BOARD)) - 5

#Tamaño y color de fondo de la ventana
WN = pygame.display.set_mode((WN_WIDTH, WN_HEIGHT))
WN.fill(BLACK);

#Titulo de la ventana
pygame.display.set_caption("Teris")

#Definir rectangulos en la ventana
def draw_board():
    CONT_X = MARGIN
    CONT_Y = MARGIN
    for i in BOARD:
        for j in i:
            if j == 0:
                pygame.draw.rect(WN, RED, (CONT_X, CONT_Y, SQ_WIDTH, SQ_WIDTH))
            else:
                pygame.draw.rect(WN, GREEN, (CONT_X, CONT_Y, SQ_WIDTH, SQ_WIDTH))
            CONT_X += SQ_WIDTH + SPACING
        CONT_X = MARGIN
        CONT_Y += SQ_WIDTH + SPACING

#Defino figura y su spawn
SPAWN = [4, 5]
FIGURE = [
    [0, 1],
    [1, 1],
    [1, 0]
]

def draw_spawn_figure(figure, spawn):
    for f in range(len(figure)):
        for c in range(len(figure[f])):
            if figure[f][c] == 1:
                BOARD[f][spawn[c]] = 1


#Bucle principal del juego
draw_board()
draw_spawn_figure(FIGURE, SPAWN)
contRow = 1
run = True
gravity = True
collide = False
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_board()

    if gravity:
        for f in range(len(FIGURE)):
            for c in range(len(FIGURE[f])):
                if FIGURE[f][c] == 1:
                    if (f + contRow) < len(BOARD):
                        BOARD[f + contRow][SPAWN[c]] = 1
                        BOARD[f + contRow - (len(FIGURE) - 1)][SPAWN[c]] = 0
                        if (f + contRow) == len(BOARD) - 1 or BOARD[f + contRow + 1][SPAWN[c]] == 1:
                            collide = True
                            gravity = False
                            contRow = 1
        contRow += 1
        
    else:
        draw_spawn_figure(FIGURE, SPAWN)
        gravity = True
        collide = False

    pygame.display.flip()
    pygame.time.Clock().tick(5)

pygame.quit()