# -*- coding: utf-8 -*-

import math
import pickle

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
    """
    def __init__(self, jugador, camino, camino_id):
        self.pos_sig = 1  # el usuario ya esta en posicion 0
        self.camino = camino
        self.jugador = jugador
        self.moves = []
        self.camino_id = camino_id

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

    def guardar_juego(self, path):
        """
        Guarda los datos de la partida en un archivo

        Args:
          path (str): direccion del archivo
        """

        archivo = open(path, "wb")
        pickle.dump(self.jugador, archivo)
        pickle.dump(self.camino_id, archivo)
        pickle.dump(self.moves, archivo)
        archivo.close()
