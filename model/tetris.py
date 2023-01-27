from model.global_variables import *
from model.figura import *
import pygame

# Esta otra clase contendrá los métodos y poriedades necesarios para poder
# dibujar en la pantalla el tablero y que las piezas colisionen, bajen, giren, etc.
class Tetris:

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = self.tablero_modelo()
        self.figura = Figura(3, 0)
        self.puntos = 0
        self.perdido = False

    # Genera el tablero interno del tetris, por lo que se generará una matriz, siendo las
    # filas una array y las columnas rellenas con el número `0`, el cual indica que no hay
    # ninguna pieza que compone la figura de teris en esa posición
    def tablero_modelo(self):
        tablero = []
        for i in range(self.filas):
            tablero.append([])
            for j in range(self.columnas):
                tablero[i].append(0)
        return tablero

    # Dibuja líneas verticales y horizontales para dibujar el tablero del tetris en la ventana,
    # calculado para que ocupe exactamente el tamaño de la ventana y concuerde con el número de
    # filas y columnas
    def dibujar_celdas(self):
        for i in range(self.filas + 1):
            pygame.draw.line(VENTANA, GRIS, (0, TAM_CELDA * i), (WIDTH, TAM_CELDA * i))
        for j in range(self.columnas + 1):
            pygame.draw.line(VENTANA, GRIS, (TAM_CELDA * j, 0), (TAM_CELDA * j, HEIGHT))

    # Método que cambia la figura activa del tablero por una nueva figura, creando un nuevo objeto
    # figura, el cual internamente devuelve una forma de figura aleatoria nada más instanciarse
    def nueva_figura(self):
        self.figura = Figura(3, 0)

    # Método en el que se comprueba si la figura activa se ha chocado con los límites de la pantalla
    # o con otra figura.
    def se_choca(self):
        es_chocado = False
        for i in range(4):
            for j in range(4):
                # En el primer `if` se comprueba si en la matriz 4x4 en la que se construía la figura
                # existe los números en los que se constituye la figura dentro de esa matriz.
                if i * 4 + j in self.figura.get_forma():
                    # 1º Comprobación: Si la figura activa choca con el final del tablero.
                    # 2º Comprobación: Si la figura activa se sale del lateral derecho del tablero.
                    # 3º Comprobación: Si la figura activa se sale del lateral izquierdo del tablero.
                    # 4º Comprobación: Si la figura activa choca con alguna figura del tablero.
                    # Si alguna de estas comprobaciones se cumple quiere decir que la figura activa
                    # se ha chocado con algo, ya sea los límites del tablero u otra figura.
                    if i + self.figura.y > self.filas - 1 or j + self.figura.x > self.columnas - 1 or j + self.figura.x < 0 or self.tablero[i + self.figura.y][j + self.figura.x] > 0:
                        es_chocado = True
        return es_chocado

    # Método que comprueba si se ha completado una fila de figuras, para eliminar la fila y volver a
    # a insertarla al principio del tablero del modelo, es decir, al principio de la matriz.
    def eliminar_linea(self):
        recursivo = False
        # Recorro el tablero del modelo desde abajo, es decir, empezando desde el final de la matriz.
        for y in range(self.filas - 1, 0, -1):
            fila_completa = True
            # Recorro todas las columnas de la fila actual y compruebo si hay alún elemento de esa columna
            # que sea `0`, ya que `0` representa que no hay figura, por lo que no se eliminaría la fila.
            for x in range(0, self.columnas):
                if self.tablero[y][x] == 0:
                    fila_completa = False
            # Si la fila comprobada con el bucle anterior, diese el caso de que si que está sin ningún `0`,
            # es decir, que no hay ningún hueco libre en esa fila, se procede a borrar la referencia completa
            # de memoria de la variable que contiene la array que conforma esa fila, el borrado en memoria de
            # la variable se puede realizar con el selector `del` delante de la variable a eliminar.
            # Posteriormente se añadiría una fila vacía, es decir una array rellena de `0s`, en la primera fila
            # que conforma la matriz del tablero.
            if fila_completa:
                del self.tablero[y]
                self.tablero.insert(0, [0 for i in range(self.columnas)])
                # Además al haberse borrado una fila completa se suma `10` a los puntos
                self.puntos += 10
                recursivo = True
        # Si la variable `recursivo` está a `True`, quiere decir que una fila se ha eliminado, por lo que se volverá
        # a llamar a si mismo para volver a hacer el mismo recorrido explicado anteriormente y eliminar más filas
        # que puedan estar sin ningún `0`, es decir, que no haya ningún hueco libre sin figura en cada línea.
        if recursivo:
            self.eliminar_linea()

    # Este método se ejecutará al final de cada movimiento, para poder así representar la figura activa en el modelo
    # de la matriz que compone el tablero, de esta forma donde se encuentre la figura activa en la pantalla, en la matriz
    # que funciona como tablero se cambiarán los `0s` (Que indican una celda vacía) por el valor del color que compone
    # la figura activa. De esta manera posteriormente se podrá representar facilmente la figura en la ventana.
    def inmovilizar(self):
        for i in range(4):
            for j in range(4):
                # En este `if` se comprueba si en la matriz 4x4 en la que se construía la figura
                # existe los números en los que se constituye la figura dentro de esa matriz.
                if i * 4 + j in self.figura.get_forma():
                    # En el momento que exista, en el tablero se cambia el `0`, que indica que esa celda está vacía,
                    # por el número del color que conforma la figura.
                    # Por lo que en esa celda ya no habría un `0` y para nuestro código contaría como celda ocupada
                    # por una figura.
                    self.tablero[i + self.figura.y][j + self.figura.x] = self.figura.color
        # Como ha habido un cambio en el tablero se procede a llamar a los métodos creados anterior mente para comprobar
        # que no hay ninguna fila completa, y si es el caso eliminarla, y generar una nueva figura.
        self.eliminar_linea()
        self.nueva_figura()
        # En este `if` se compruena si la figura se choca con algún límite de la pantalla o con otra figura.
        if self.se_choca():
            self.perdido = True

    # Método en el que la figura se colocará automáticamente en la parte inferior de la pantalla
    # o encima de la figura con la que colisiona, para no tener que esperar a que la figura baje al completo.
    def ir_rapido_abajo(self):
        # Para que la figura vaya rápdio hacia abajo se mete la figura activa en un bucle que no termine hasta que colisione o con
        # el inferior de la pantalla o con alguna pieza, esta comprobación puede realizarse gracias al método realizado
        # anteriormente que comprueba las colisiones.
        while self.se_choca() is False:
            self.figura.y += 1
        # Una vez la figura llega abajo se resta una a su posición `y`, ya que como en python no existe la posibilidad de
        # implementar un `do while()` conocido en otros lenguajes de programación, nuestro bucle da por tanto una vuelta de más,
        # por lo que le restamos `1` a su posición para dejar la figura en la posición correcta.
        self.figura.y -= 1
        # Finalmente inmovilizamos la figura activa una vez haya colisionado ya sea con la parte inferior de la pantalla u otra figura,
        # para que esta pueda ser representada en la ventana de forma gráfica posteriormente.
        self.inmovilizar()

    # Método que cada vez que sea llamado bajará la figura activa una posición, es decir, restará uno a la variable `y` que indica la
    # posición en el eje horizontal del tablero.
    def ir_abajo(self):
        # La figura activa se incrementará en `1` el valor en su eje horizontal, es decir, se incrementará su `y` a no ser de que se choque,
        # ya que en ese momento se le restará `1` a la posición horizontal de la figura, ya que antes del `if` se había desplazado una posición
        # y al colisionar hay que volver a la posición anterior para que no se solape con otra pieza o se salga de la pantalla.
        self.figura.y += 1
        if self.se_choca():
            self.figura.y -= 1
            # Al chocar, inmovilizamos la figura activa para que esta pueda ser representada en la ventana de forma gráfica posteriormente.
            self.inmovilizar()

    # Método que cada vez que sea llamado desplazará la figura a la izquierda si le pasamos por el parámetro `dx` el número `-1` o por el
    # contrario para moverse a la derecha se pasaría por el parámetro `dx` el valor `1`.
    # Pasamos simepre el valor de 1 en 1 ya que sino se movería la figura de `n` casillas en `n` casillas siendo `n` cualquier número.
    def ir_a_un_lado(self, dx):
        # La figura activa se incrementará o decrementará en `1` el valor en su eje vertical, es decir, se incrementará o decrementará
        # su `x` a no ser de que se choque, ya que en ese momento se le restará o sumará `1` a la posición vertical de la figura, ya que antes
        # del `if` se había desplazado una posición y al colisionar hay que volver a la posición anterior para que no se solape con otra pieza
        # o se salga de la pantalla.
        self.figura.x += dx
        if self.se_choca():
            self.figura.x -= dx

    # Método que girará la pieza cada vez que sea llamado, ya que la figura activa contiene un método en el que cada vez que se llama girará la
    # la figura activa, este efecto se consige cambiando el array por otro array que contiene la misma figura pero girada.
    def girar(self):
        # Primero se guarda la posición de giro de la figura activa para posteriormente girarla.
        # Una vez girada, en el `if` se comprueba si la figura girada ha colisionado con los límites de la pantalla o con otra figura, para que
        # en el caso de que esta condición sea cierta poder volver a la posición de giro anterior, gracias a haber guardado la posición inicial
        # de giro al inicio del método en la variable `giro` para poder volver al estado anterior y por lo tanto no girar la figura.
        giro = self.figura.giro
        self.figura.girar()
        if self.se_choca():
            self.figura.giro = giro