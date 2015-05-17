# -*- coding: utf-8 -*-

import pilasengine


ANCHO = 2751
ALTO = 1306


def fil_a_y(fila):
    return (ALTO - fila) - ALTO // 2


def col_a_x(columna):
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

        self.boton_jugar = self.pilas.interfaz.Boton("Jugar")
        self.boton_jugar.y -= 200
        self.boton_jugar.escala = 2
        self.boton_jugar.conectar(self.ir_al_juego)

    # cambia la escena si el usuario ingreso un nombre valido
    def ir_al_juego(self):
        # TO-DO: mejorar la validacion del nombre
        if (self.input_nombre.texto != ""):
            self.pilas.escenas.PantallaJuego()
        else:
            self.boton_jugar.decir("El nombre es invalido")


class PantallaJuego(pilasengine.escenas.Escena):
    """
    Interfaz grafica principal del juego
    """

    def iniciar(self):
        self.fondo = self.pilas.fondos.Fondo()
        self.fondo.imagen = (
            self.pilas.imagenes.cargar('assets/fondo_juego.png')
        )

        self.protagonista = self.pilas.actores.Actor(
            imagen='assets/personaje.png'
        )
        self.protagonista.escala = 0.5
        self.protagonista.x = col_a_x(2567)
        self.protagonista.y = fil_a_y(392)

        self.label_fila = self.pilas.actores.Texto("Fila :")
        self.label_fila.centro = ("izquierda", "centro")
        self.label_fila.x = col_a_x(60)
        self.label_fila.y = fil_a_y(1150)
        self.label_fila.color = pilasengine.colores.negro

        self.input_fila = self.pilas.interfaz.IngresoDeTexto("")
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
        self.input_columna.centro = ("izquierda", "centro")
        self.input_columna.x = col_a_x(120)
        self.input_columna.y = fil_a_y(1250)
        self.input_columna.escala = 2
