import pygame
import math

# Inicialización de la superficie de dibujo
WIDTH = 300
HEIGHT = 600
VENTANA = pygame.display.set_mode((WIDTH, HEIGHT + 100))

TAM_CELDA = 30
FILAS = math.floor(HEIGHT / TAM_CELDA)
COLUMNAS = math.floor(WIDTH / TAM_CELDA)

# Defino los fotogramas por segundo de mi tetris
FPS = 24

# Defino los colores que tendrá mi programa
NEGRO = (0, 0, 0)
GRIS = (58, 58, 58)
ROJO = (252, 91, 122)
BLANCO = (255, 255, 255)

# Defino las imágenes que va a tener mi tetris
sq_1 = pygame.image.load('./assets/imgs/sq_1.jpg')
sq_1 = pygame.transform.scale(sq_1, (TAM_CELDA, TAM_CELDA))

sq_2 = pygame.image.load('./assets/imgs/sq_2.jpg')
sq_2 = pygame.transform.scale(sq_2, (TAM_CELDA, TAM_CELDA))

sq_3 = pygame.image.load('./assets/imgs/sq_3.jpg')
sq_3 = pygame.transform.scale(sq_3, (TAM_CELDA, TAM_CELDA))

sq_4 = pygame.image.load('./assets/imgs/sq_4.jpg')
sq_4 = pygame.transform.scale(sq_4, (TAM_CELDA, TAM_CELDA))

sq_5 = pygame.image.load('./assets/imgs/sq_5.jpg')
sq_5 = pygame.transform.scale(sq_5, (TAM_CELDA, TAM_CELDA))

sq_6 = pygame.image.load('./assets/imgs/sq_6.jpg')
sq_6 = pygame.transform.scale(sq_6, (TAM_CELDA, TAM_CELDA))

sq_7 = pygame.image.load('./assets/imgs/sq_7.jpg')
sq_7 = pygame.transform.scale(sq_7, (TAM_CELDA, TAM_CELDA))

# Imágenes definidas en un array relacional, por lo que sus
# índices se conoceran por el valor puesto delate de los `:`
SQ_FIGURA = {
    1: sq_1,
    2: sq_2,
    3: sq_3,
    4: sq_4,
    5: sq_5,
    6: sq_6,
    7: sq_7
}

# Definimos la forma que puede tener cada figura con un array relacional para
# poder dar un nombre a cada elemento de la array y no utilizar ínidices
FIGURAS = {
    'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
    'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
    'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
    'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    'O': [[1, 2, 5, 6]]
}

# Definimos los tipos de figuras en una array para poder acceder a la forma
# de la figura en el array relacional
TIPO = [['I', 1], ['Z', 2], ['S', 3], ['L', 4], ['J', 5], ['T', 6], ['O', 7]]