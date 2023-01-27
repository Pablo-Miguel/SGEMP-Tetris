from model.global_variables import *
from model.figura import *
from model.tetris import *
import pygame

# Inicilización de Pygame
pygame.init()

# Fuentes que tendrá mi programa
FONT = pygame.font.Font(None, 25)

# Se le da nombre a la ventana
pygame.display.set_caption("Teris")

# Aquí se define el bucle principal que correrá el juego y se escucharán los eventos efectuados
# por el usuario, respondiendo con el modelo creado anteriormente y determinando el refresco del
# juego.
# Variables iniciales antes de empezar el juego
contador = 0
max_puntuacion = 0

# Se define el tablero en el modelo
tetris = Tetris(FILAS, COLUMNAS)

# Empieza el juego en este bucle
run = True
while run:
    # Pinta la venta de negro para poder simular los FPS.
    VENTANA.fill(NEGRO)

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
                VENTANA.blit(SQ_FIGURA[tetris.tablero[x][y]], (y * TAM_CELDA, x * TAM_CELDA))
                # Dibujamos un cuadrado detrás de la imagen para que se vea con un borde la imagen y se vea la figura mucho más definida.
                pygame.draw.rect(VENTANA, GRIS, (y * TAM_CELDA, x * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)

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
                    VENTANA.blit(SQ_FIGURA[tetris.figura.color], (x, y))
                    # Dibujamos un cuadrado detrás de la imagen para que se vea con un borde la imagen y se vea la figura mucho más definida.
                    pygame.draw.rect(VENTANA, GRIS, (x, y, TAM_CELDA, TAM_CELDA), 1)

    # Si ha perdido porque la figura activa ha colisionado con la parte superior del tablero se ejecutará esta parte de código porque
    # habrá perdido.
    if tetris.perdido:
        menu_bkg = pygame.Rect((0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(VENTANA, NEGRO, menu_bkg)

        titulo = FONT.render('Has perdido :C', True, BLANCO)
        mensaje1 = FONT.render('Pulsa `R` repetir', True, ROJO)
        mensaje2 = FONT.render('Pulsa `Q` quitar', True, ROJO)

        VENTANA.blit(titulo, (menu_bkg.centerx - titulo.get_width() / 2, menu_bkg.y + 20))
        VENTANA.blit(mensaje1, (menu_bkg.centerx - mensaje1.get_width() / 2, menu_bkg.y + 80))
        VENTANA.blit(mensaje2, (menu_bkg.centerx - mensaje2.get_width() / 2, menu_bkg.y + 110))

    # En este `if` comprobamos que el máximo no sea menor a la puntuación actual, en el caso de que se cumpla se actualizaría la puntuación máxima.
    if max_puntuacion < tetris.puntos:
        max_puntuacion = tetris.puntos

    # Dibujamos las puntuaciones por pantalla.
    puntos = FONT.render(f'Puntos: {tetris.puntos}', True, BLANCO)
    VENTANA.blit(puntos, (WIDTH / 2 - puntos.get_width() / 2, HEIGHT + 30))

    puntos_max = FONT.render(f'Max puntos: {max_puntuacion}', True, BLANCO)
    VENTANA.blit(puntos_max, (WIDTH / 2 - puntos_max.get_width() / 2, HEIGHT + 50))

    # Controlamos la frecuencia de refresco (FPS).
    pygame.time.Clock().tick(FPS)
    # Actualizamos la ventana.
    pygame.display.update()

# Cierra el Tetris.
pygame.quit()
