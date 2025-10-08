import cv2
import numpy as np
import matplotlib.pyplot as plt
from utilidades_basicas import *

def main():
    video = 'images/trafico.mp4'
    fondo = 'images/fondo_sin_coches.jpg'
    ancho, alto = (800, 450) # Parámetros para la redimensión
    # visualizar_video(video)
    # fondo = obtener_fondo(video)
    quitar_fondo(video, fondo, ancho, alto)


if __name__ == "__main__":
    main()

