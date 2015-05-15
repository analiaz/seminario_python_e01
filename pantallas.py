# -*- coding: utf-8 -*-

import pilasengine


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
