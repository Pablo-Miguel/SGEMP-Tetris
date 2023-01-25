import pygame
import random

VENTANA_WIDTH, VENTANA_HEIGHT = 500, 601
TABLA_WIDTH, TABLA_HEIGHT = 300, 600
SPACE = 30

COLORES_FIGURAS = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

FIGURAS = [
    [[1, 2, 5, 6]],  # Cuadrado
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I-Vertical, I-Horizontal
    # [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T-Arr, T-Izq, T-Aba, T-Der
    # [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L'-Izq, L'-Aba, L'-Der, L'-Arr
    # [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # L-Der, L-Arr, L-Izq, L-Aba
    # [[4, 5, 9, 10], [2, 6, 5, 9]], # Z, Z-Vertical
    # [[6, 7, 9, 10], [1, 5, 6, 10]], # Z', Z'-Vertical
]


class Figura:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo_figura = random.randint(0, len(FIGURAS) - 1)
        self.color = random.randint(1, len(COLORES_FIGURAS) - 1)
        self.rotacion = 0

    # Obtener el contorno de la figura
    def contorno(self):
        return FIGURAS[self.tipo_figura][self.rotacion]

    # cont % num_tot_rotaciones -> [Módulo]
    # Ej: Si la rotación de la figura tiene dos posiciones, el resto irá alternando entre 0 y 1,
    # y si tiene más posiciones se irán repitiendo en orden con su módulo -> 0, 1 ,2, 3 en bucle
    def rotar(self):
        self.rotacion = (self.rotacion + 1) % len(FIGURAS[self.tipo_figura])


class Tetris:
    nivel = 2
    puntos = 0
    estado = "start"
    tablero = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figura = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tablero = []
        self.puntos = 0
        self.estado = "empezar"
        self.dibuja_tablero()

    def dibuja_tablero(self):
        for i in range(self.height):
            linea = []
            for j in range(self.width):
                linea.append(0)
            self.tablero.append(linea)

    def nueva_figura(self):
        self.figura = Figura(3, 0)

    def intersecta_bordes(self):
        FIGURA_WIDTH = len(FIGURAS[0])
        intersecta = False
        for i in range(FIGURA_WIDTH):
            for j in range(FIGURA_WIDTH):
                if i * FIGURA_WIDTH + j in self.figura.contorno():
                    if (
                        i + self.figura.y > self.height - 1
                        or j + self.figura.x > self.width - 1
                        or j + self.figura.x < 0
                        or self.tablero[i + self.figura.y][j + self.figura.x] > 0
                    ):
                        intersecta = True
        return intersecta

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines**2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.quit()
