from model.global_variables import *
import random

# Objetos que definen el juego del tetris:
# Esta clase va a determinar las formas de las figuras, sus rotaciones.
class Figura:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.choice(TIPO)
        self.forma = FIGURAS[self.tipo[0]]
        self.color = self.tipo[1]
        self.giro = 0

    # Obtener la forma de la figura
    def get_forma(self):
        return self.forma[self.giro]

    # cont % num_tot_rotaciones -> [Módulo]
    # Ej: Si la rotación de la figura tiene dos posiciones, el resto irá alternando entre 0 y 1,
    # y si tiene más posiciones se irán repitiendo en orden con su módulo -> 0, 1 ,2, 3 en bucle
    def girar(self):
        self.giro = (self.giro + 1) % len(self.forma)