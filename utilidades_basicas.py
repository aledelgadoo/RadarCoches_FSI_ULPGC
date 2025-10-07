import cv2
import numpy as np
import matplotlib.pyplot as plt


def leer_video(video):
    cap = cv2.VideoCapture(video)

    # Mensaje por si no podemos acceder al archivo
    if not cap.isOpened():
        print("Error!")
        exit()

    # Visualizar el vídeo
    while(True):
        
        ret, frame = cap.read()
        
        # Comprobamos que se esté visualizando correctamente
        if not ret:
            print("Fin del vídeo")
            break

        # Ajustamos para que el vídeo ocupe menos
        frame = cv2.resize(frame, (1000, 700))

        cv2.imshow('Video original', frame)
        
        # Para cerrar el vídeo
        if cv2.waitKey(5) & 0xFF == 27:# Código ACII esc == 27:
            break

    cv2.destroyAllWindows()

    # Release el frame
    cap.release()
