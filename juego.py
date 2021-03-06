# -*- coding: utf-8 -*-

import math
import pickle

# Ubicacion por default del archivo
_FILE_PATH = "./partidas.bin"

# distancia requerida para que un movimiento sea valido
_MIN_DISTANCIA = 20


def distancia_total(posiciones):
    """
    Calcula la suma de las distancias entre varias posiciones

    Args:
      posiciones (list of Punto)

    Returns:
      int
    """

    suma = 0
    # tomo elementos de a pares
    for a, b in zip(posiciones, posiciones[1:]):
        suma += a.distancia(b)
    return suma


class Punto:
    """
    Attributes:
      x (int)
      y (int)
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, otro_punto):
        """
        Calcula la distancia aplicando el Teorema de Pitagoras

        Args:
          otro_punto (Punto)
        Returns:
          (float) Distancia entre ambos puntos
        """

        dx = otro_punto.x - self.x
        dy = otro_punto.y - self.y

        return math.sqrt(dx * dx + dy * dy)


class Juego:
    """
    Args:
      jugador (str): Nombre del jugador
      camino (list of Punto): Puntos que el jugador debe encontrar
      camino_id (str): Identificador del camino seleccionado

    Attributes:
      pos_sig (int): Ubicacion del punto a comparar con los movimientos.
        Se incrementa cuando el jugador descubre el punto
      camino (list of Punto): Puntos que el jugador debe encontrar
      jugador (str): Nombre del jugador
      moves (list of Punto): Puntos ya descubiertos por el jugador
      camino_id (str): Identificador del camino seleccionado
      hist (dict of (str, str) : (list of Punto)):
        guarda partidas como pares (jugador, camino_id): moves
    """
    def __init__(self, jugador, camino, camino_id):
        self.camino = camino
        self.jugador = jugador
        self.camino_id = camino_id

        # Recuperamos, si existen, los movimientos guardados
        try:
            self.cargar_juego()

            # Obtener el 1er resultado, sino vacio para un jugador nuevo
            busqueda = (self.hist[k] for k in self.hist.keys()
                        if k == (self.jugador, self.camino_id))
            self.moves = next(busqueda, [])
        except:
            # Movimientos no encontrados -> creamos unos vacios
            self.moves = []
            self.hist = {}

        # Guardamos ya sea porque no existia el archivo o solo el jugador
        if (len(self.moves) == 0):
            self.guardar_juego()

        self.pos_sig = len(self.moves) + 1  # el usuario ya esta en posicion 0

    def probar_movimiento(self, mov):
        """
        Verifica si el movimiento adivinado por el jugador es correcto
        En ese caso, se incrementa pos_sig

        Args:
          mov (Punto): movimiento del jugador
        Returns:
          True si el movimiento se encuentra dentro del rango
          False en caso contrario o fuera del limite
        """

        if (self.pos_sig == len(self.camino)):
            return False

        if (self.camino[self.pos_sig].distancia(mov) <= _MIN_DISTANCIA):
            self.moves.append(mov)
            self.pos_sig += 1
            return True

        return False

    def cumple_fin_juego(self):
        if (self.pos_sig == len(self.camino)):
            return True

        return False

    def guardar_juego(self):
        """
        Guarda el historial de partidas en el archivo
        """
        self.hist[(self.jugador, self.camino_id)] = self.moves
        archivo = open(_FILE_PATH, "wb")
        pickle.dump(self.hist, archivo)
        archivo.close()

    def cargar_juego(self):
        """
        Carga el historial de partidas desde el archivo
        """
        archivo = open(_FILE_PATH, "rb")
        self.hist = pickle.load(archivo)
        archivo.close()
