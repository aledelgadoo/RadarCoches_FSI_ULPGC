import numpy as np
import cv2
from funcionesV1 import *
from gestor_vehiculos import *


def detectar_cochesV2(ruta_video, background_img, width, height):
    """
    Procesa un vídeo detectando y siguiendo vehículos mediante el GestorVehiculos.
    Usa una imagen del fondo proporcionada y redimensiona los frames a (width, height).
    """

    # --- Inicialización ---
    cap = leer_video(ruta_video)
    fondo = cv2.resize(cv2.imread(background_img), (width, height)).astype(np.uint8)

    # Creamos el objeto gestor
    gestor = GestorVehiculos(umbral_distancia=50, max_frames_perdido=10)

    # Redimensionamos la imagen de fondo al tamaño deseado
    background_img = fondo
    background_gray = cv2.cvtColor(background_img, cv2.COLOR_BGR2GRAY)

    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1

        # --- Redimensionar y preprocesar el frame ---
        frame = cv2.resize(frame, (width, height))
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

        # --- Sustracción de fondo usando la imagen proporcionada ---
        diff = cv2.absdiff(background_gray, frame_blur)
        _, fgmask = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))

        # --- Detección de contornos ---
        contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detecciones = []
        for c in contornos:
            if cv2.contourArea(c) < 500:  # filtro de ruido
                continue
            x, y, w, h = cv2.boundingRect(c)
            detecciones.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

        # --- Actualizar el gestor ---
        gestor.actualizar(detecciones, frame, frame_num)

        # --- Dibujar resultados ---
        for v in gestor.vehiculos_activos():
            x, y, w, h = map(int, v.bbox)
            cx, cy = map(int, v.centroide)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {v.id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
            # Trazo del historial
            for i in range(1, len(v.historial)):
                cv2.line(frame,
                         (int(v.historial[i-1][0]), int(v.historial[i-1][1])),
                         (int(v.historial[i][0]), int(v.historial[i][1])),
                         (0, 255, 255), 1)

        # --- Mostrar ---
        cv2.imshow("Detección y seguimiento", frame)
        cv2.imshow("Máscara", fgmask)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
