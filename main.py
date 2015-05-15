# -*- coding: utf-8 -*-

import pilasengine
from pantallas import PantallaInicial, PantallaJuego

# crea una instancia del motor de pilas
pilas = pilasengine.iniciar(ancho=2700, alto=1500)

# añade las escenas al gestor de escenas
pilas.escenas.vincular(PantallaInicial)
pilas.escenas.vincular(PantallaJuego)

# seleccionar la escena inicial
pilas.escenas.PantallaInicial()

# correr motor ya configurado
pilas.ejecutar()
