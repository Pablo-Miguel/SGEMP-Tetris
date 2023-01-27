import pygame
import random
import math

# Inicilización de Pygame
pygame.init()

# Inicialización de la superficie de dibujo
WIDTH = 300
HEIGHT = 600
ventana = pygame.display.set_mode((WIDTH, HEIGHT))

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
sq_1 = pygame.image.load('./assets/imgs/sq_1.png')
sq_1 = pygame.transform.scale(sq_1, (TAM_CELDA, TAM_CELDA))

sq_2 = pygame.image.load('./assets/imgs/sq_2.png')
sq_2 = pygame.transform.scale(sq_2, (TAM_CELDA, TAM_CELDA))

sq_3 = pygame.image.load('./assets/imgs/sq_3.png')
sq_3 = pygame.transform.scale(sq_3, (TAM_CELDA, TAM_CELDA))

sq_4 = pygame.image.load('./assets/imgs/sq_4.png')
sq_4 = pygame.transform.scale(sq_4, (TAM_CELDA, TAM_CELDA))

# Imágenes definidas en un array relacional, por lo que sus 
# índices se conoceran por el valor puesto delate de los `:`
SQ_FIGURA = {
    1 : sq_1,
    2 : sq_2,
    3 : sq_3,
    4 : sq_4
}

#Fuentes que tendrá mi programa
FONT = pygame.font.Font(None, 25)

# Definimos la forma que puede tener cada figura con un array relacional para
# poder dar un nombre a cada elemento de la array y no utilizar ínidices
FIGURAS = {    
    'C' : [[1, 2, 5, 6]],
    'I' : [[1, 5, 9, 13], [4, 5, 6, 7]],
    'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
}

# Definimos los tipos de figuras en una array para poder acceder a la forma 
# de la figura en el array relacional
TIPO = ['C', 'I', 'T']

# Objetos que definen el juego del tetris:
# Esta clase va a determinar las formas de las figuras, sus rotaciones.
class Figura:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.choice(TIPO)
        self.forma = FIGURAS[self.tipo]
        self.color = random.randint(1, 4)
        self.giro = 0

    # Obtener la forma de la figura
    def get_forma(self):
        return self.forma[self.giro]

    # cont % num_tot_rotaciones -> [Módulo]
    # Ej: Si la rotación de la figura tiene dos posiciones, el resto irá alternando entre 0 y 1,
    # y si tiene más posiciones se irán repitiendo en orden con su módulo -> 0, 1 ,2, 3 en bucle
    def girar(self):
        self.giro = (self.giro + 1) % len(self.forma)

# Esta otra clase contendrá los métodos y poriedades necesarios para poder
# dibujar en la pantalla el tablero y que las piezas colisionen, bajen, giren, etc.
class Tetris:

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tablero = self.tablero_modelo()
        self.figura = Figura(3, 0)
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
            pygame.draw.line(ventana, GRIS, (0, TAM_CELDA * i), (WIDTH, TAM_CELDA * i))
        for j in range(self.columnas + 1):
            pygame.draw.line(ventana, GRIS, (TAM_CELDA * j, 0), (TAM_CELDA * j, HEIGHT))

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

# Aquí se define el bucle principal que correrá el juego y se escucharán los eventos efectuados
# por el usuario, respondiendo con el modelo creado anteriormente y determinando el refresco del
# juego.
# Variables iniciales antes de empezar el juego
contador = 0

# Se define el tablero en el modelo
tetris = Tetris(FILAS, COLUMNAS)

# Empieza el juego en este bucle
run = True
while run:
    # Pinta la venta de negro para poder simular los FPS.
    ventana.fill(NEGRO)

    # Por cada 10 ciclos de while el contador se pondrá a `0`, de esta forma podremos luego controlar de manera más efectiva los FPS
    # y la animación de bajar la figura sea mucho más fluida.
    contador += 1
    if contador >= 10:
        contador = 0

    # Cuadno el módulo del contador entre los FPS de `0` entonces bajará la pieza.
    if contador % FPS == 0:
        if tetris.perdido is False:
            tetris.ir_abajo()

    # Comprobamos si se ha efectuado alguno de los eventos.
    for event in pygame.event.get():
        # Evento que escucha a si el usuario cierra la ventana.
        if event.type == pygame.QUIT:
            run = False
        # Evento que escucha la tecla que pulsa el usuairo.
        if event.type == pygame.KEYDOWN:
            # Si no se ha perdido se podrá mover la figura activa.
            if tetris.perdido is False:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # Mover la figura activa hacia la izquierda.
                    tetris.ir_a_un_lado(-1)

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Mover la figura activa hacia la derecha.
                    tetris.ir_a_un_lado(1)

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Girar la figura activa.
                    tetris.girar()

                if event.key == pygame.K_SPACE:
                    # Mover la figura activa instantáneamente a su posición inferior.
                    tetris.ir_rapido_abajo()
            
            if event.key == pygame.K_r:
                # Este evento reiniciará el juego y el tetris empezará de nuevo.
                tetris.__init__(FILAS, COLUMNAS)

            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                # Este evento escucha si el usuairo ha pulsado la tecla `esc` para salir del juego.
                run = False

    # Método que dibuja la cuadrícula del tablero en la vista de forma gráfica.
    tetris.dibujar_celdas()

    # En estos bucles que están anidados se recorrerá la matriz que conforma el tablero en el modelo, para ir leyendo cada celda, si el valor de la celda
    # es diferente de `0`, quiere decir que la celda no está vacía, por lo que se rellenará en la ventana gráfica esa posición con un cuadrado con la imagen 
    # del color asociado anteriormete en el objeto figura.
    for x in range(FILAS):
        for y in range(COLUMNAS):
            # Comprobamos que el valor de la celda no sea `0`, es decir que no esté vacía.
            if tetris.tablero[x][y] > 0:
                # Si no está vacía, cogemos el valor de la celda y sacamos la imagen asociada a ese color gracias al array relacional definida al inicio del programa.
                ventana.blit(SQ_FIGURA[tetris.tablero[x][y]], (y * TAM_CELDA, x * TAM_CELDA))
                # Dibujamos un cuadrado detrás de la imagen para que se vea con un borde la imagen y se vea la figura mucho más definida.
                pygame.draw.rect(ventana, NEGRO, (y * TAM_CELDA, x * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)
    
    # Esta parte de código se ejecutará mientras la figura está moviendose, es decir mientras no colisione ni con el final del tablero ni con otra figura,
    # sin embargo el anterior, redibuja todo el tiempo las figuras colocadas anteriormente, pero esta parte solo dibuja la figura activa.
    if tetris.figura is not None:
        for i in range(4):
            for j in range(4):
                # En el primer `if` se comprueba si en la matriz 4x4 en la que se construía la figura
                # existe los números en los que se constituye la figura dentro de esa matriz.
                if i * 4 + j in tetris.figura.get_forma():
                    # Obtenemos la posición `x` e `y` de la figura actriva para poder dibujar cada celda en la ventana de forma visual.
                    x = TAM_CELDA * (tetris.figura.x + j)
                    y = TAM_CELDA * (tetris.figura.y + i)
                    # Cogemos el valor de la celda y sacamos la imagen asociada a ese color gracias al array relacional definida al inicio del programa.
                    ventana.blit(SQ_FIGURA[tetris.figura.color], (x, y))
                    # Dibujamos un cuadrado detrás de la imagen para que se vea con un borde la imagen y se vea la figura mucho más definida.
                    pygame.draw.rect(ventana, NEGRO, (x, y, TAM_CELDA, TAM_CELDA), 1)

    # Si ha perdido porque la figura activa ha colisionado con la parte superior del tablero se ejecutará esta parte de código porque 
    # habrá perdido.
    if tetris.perdido:
        menu_bkg = pygame.Rect((0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(ventana, NEGRO, menu_bkg)

        titulo = FONT.render('Has perdido :C', True, BLANCO)
        mensaje1 = FONT.render('Pulsa `R` repetir', True, ROJO)
        mensaje2 = FONT.render('Press `Q` cerrar', True, ROJO)

        ventana.blit(titulo, (menu_bkg.centerx - titulo.get_width() / 2, menu_bkg.y + 20))
        ventana.blit(mensaje1, (menu_bkg.centerx - mensaje1.get_width() / 2, menu_bkg.y + 80))
        ventana.blit(mensaje2, (menu_bkg.centerx - mensaje2.get_width() / 2, menu_bkg.y + 110))
    
    # Controlamos la frecuencia de refresco (FPS).
    pygame.time.Clock().tick(FPS)
    # Actualizamos la ventana.
    pygame.display.update()

# Cierra el Tetris.
pygame.quit()