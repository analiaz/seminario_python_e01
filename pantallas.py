# -*- coding: utf-8 -*-

import pilasengine
import juego


ANCHO = 2751
ALTO = 1306

# Caminos (tuplas de fila y columna) posibles a seleccionar por el jugador
BLACK_PATH = [(392, 2567), (444, 1992), (892, 1576), (688, 1332), (1008, 1040),
              (656, 640), (436, 836), (272, 664), (168, 656)]
RED_PATH = [(392, 2567), (40, 2188), (262, 1984), (128, 1836), (456, 1544),
            (232, 1292), (340, 1176), (132, 956), (238, 852), (158, 760),
            (168, 656)]
PATHS = {"rojo": RED_PATH, "negro": BLACK_PATH}

# Cantidad de segundo que toma un movimiento del personaje
VELOCIDAD_MOVE = 2


def fil_a_y(fila):
    """
    Convierte una fila desde coordenadas matriciales a su
    coordenada cartesiana "y" equivalente.
    Se aplica inversion de eje y luego desplazamiento.
    """
    return (ALTO - fila) - ALTO // 2


def col_a_x(columna):
    """
    Convierte una columna desde coordenadas matriciales a su
    coordenada cartesiana "x" equivalente
    Se aplica solo desplazamiento.
    """
    return columna - ANCHO // 2


class PantallaInicial(pilasengine.escenas.Escena):
    """
    Pantalla de bienvenida, pide al jugador su nombre
    """

    def iniciar(self):
        self.label_nombre = self.pilas.actores.Texto("Ingrese nombre:")
        self.label_nombre.y += 100
        self.input_nombre = self.pilas.interfaz.IngresoDeTexto("")
        self.input_nombre.escala = 2

        self.boton_negro = self.pilas.interfaz.Boton("Camino Negro")
        self.boton_negro.x -= 100
        self.boton_negro.y -= 200
        self.boton_negro.escala = 2
        self.boton_negro.conectar(
            lambda: self.ir_al_juego("negro")
        )

        self.boton_rojo = self.pilas.interfaz.Boton("Camino Rojo")
        self.boton_rojo.x += 100
        self.boton_rojo.y -= 200
        self.boton_rojo.escala = 2
        self.boton_rojo.conectar(
            lambda: self.ir_al_juego("rojo")
        )

    # cambia la escena si el usuario ingreso un nombre valido
    def ir_al_juego(self, camino_id):
        # TO-DO: mejorar la validacion del nombre
        if (self.input_nombre.texto != ""):
            self.pilas.escenas.PantallaJuego(self.input_nombre.texto,
                                             camino_id)
        else:
            self.input_nombre.decir("El nombre es invalido")


class PantallaJuego(pilasengine.escenas.Escena):
    """
    Interfaz grafica principal del juego
    Arguments
      camino_id (str): eleccion de camino "rojo o negro"

    """

    def iniciar(self, nombre, camino_id):
        self._crear_interfaz()
        self.etiquetas = []

        camino = [juego.Punto(c, f) for f, c in PATHS[camino_id]]
        self.partida = juego.Juego(nombre, camino, camino_id)

        # Mostramos posiciones guardadas, ya descubiertas
        for move in self.partida.moves:
            self.agregar_etiqueta(move.y, move.x)

        self.protagonista = self.pilas.actores.Actor(
            imagen='assets/personaje.png'
        )
        self.protagonista.escala = 0.5
        self._posicionar_inicio()

    def _posicionar_inicio(self):
        self.protagonista.x = col_a_x(self.partida.camino[0].x)
        self.protagonista.y = fil_a_y(self.partida.camino[0].y)

    def _crear_interfaz(self):
        self.fondo = self.pilas.fondos.Fondo()
        self.fondo.imagen = (
            self.pilas.imagenes.cargar('assets/fondo_juego.png')
        )

        self.label_fila = self.pilas.actores.Texto("Fila :")
        self.label_fila.centro = ("izquierda", "centro")
        self.label_fila.x = col_a_x(60)
        self.label_fila.y = fil_a_y(1150)
        self.label_fila.color = pilasengine.colores.negro

        self.input_fila = self.pilas.interfaz.IngresoDeTexto("")
        self.input_fila.solo_numeros()
        self.input_fila.centro = ("izquierda", "centro")
        self.input_fila.x = col_a_x(120)
        self.input_fila.y = fil_a_y(1150)
        self.input_fila.escala = 2

        self.label_columna = self.pilas.actores.Texto("Columna :")
        self.label_columna.centro = ("izquierda", "centro")
        self.label_columna.x = col_a_x(60)
        self.label_columna.y = fil_a_y(1250)
        self.label_columna.color = pilasengine.colores.negro

        self.input_columna = self.pilas.interfaz.IngresoDeTexto("")
        self.input_columna.solo_numeros()
        self.input_columna.centro = ("izquierda", "centro")
        self.input_columna.x = col_a_x(120)
        self.input_columna.y = fil_a_y(1250)
        self.input_columna.escala = 2

        self.boton_probar = self.pilas.interfaz.Boton("Probar")
        self.boton_probar.x = col_a_x(800)
        self.boton_probar.y = fil_a_y(1150)
        self.boton_probar.escala = 2
        self.boton_probar.conectar(self.probar_punto)

        self.boton_recorrido = self.pilas.interfaz.Boton("Recorrido")
        self.boton_recorrido.x = col_a_x(800)
        self.boton_recorrido.y = fil_a_y(1250)
        self.boton_recorrido.escala = 2
        self.boton_recorrido.conectar(self.mover_personaje)

        self.boton_guardar = self.pilas.interfaz.Boton("Guardar Partida")
        self.boton_guardar.x = col_a_x(1300)
        self.boton_guardar.y = fil_a_y(1150)
        self.boton_guardar.escala = 2
        self.boton_guardar.conectar(
            lambda: self.partida.guardar_juego()
        )

    def agregar_etiqueta(self, fila, columna):
        etiqueta = self.pilas.actores.Texto("({},{})"
                                            .format(columna, fila))
        etiqueta.x = col_a_x(columna)
        etiqueta.y = fil_a_y(fila)
        etiqueta.color = pilasengine.colores.magenta
        etiqueta.escala = 2
        self.etiquetas.append(etiqueta)

    def probar_punto(self):
        if ((self.input_fila.texto != "" and
             self.input_columna.texto != "")):
            fila = int(self.input_fila.texto)
            columna = int(self.input_columna.texto)
            if (self.partida.probar_movimiento(juego.Punto(columna, fila))):
                self.boton_probar.decir("Correcto")

                # Mostramos la posicion descuebierta en el mapa
                self.agregar_etiqueta(fila, columna)

                # Se vacian las cajas de entrada
                self.input_columna.texto = ""
                self.input_fila.texto = ""

                if (self.partida.cumple_fin_juego()):
                    self.boton_probar.desactivar()
                    self.mover_personaje()
                    self.mostrar_distancia()
            else:
                self.boton_probar.decir("Incorrecto")
        else:
            self.boton_probar.decir("invalido")

    def mostrar_distancia(self):
        distancia = juego.distancia_total(self.partida.camino)
        self.protagonista.decir("He recorrido {} de distancia"
                                .format(distancia))

    def mover_personaje(self):
        """
        Realiza animacion del recorrido, utilizando interpolacion de la forma:
          coordenada = [lista de valores], velocidad
        """
        self._posicionar_inicio()

        # Se hace uso de Generator en vez de List Comprehension para mejorar
        # performance, ya que evalua bajo demanda
        xs = (col_a_x(move.x) for move in self.partida.moves)
        ys = (fil_a_y(move.y) for move in self.partida.moves)

        self.protagonista.x = xs, VELOCIDAD_MOVE
        self.protagonista.y = ys, VELOCIDAD_MOVE
