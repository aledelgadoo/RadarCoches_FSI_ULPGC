import numpy as np
import cv2
from funcionesV1 import *
from gestor_vehiculos import *
from vehiculos import *

def detectar_cochesV2(ruta_video, ruta_fondo, 
                       escala=0.5, 
                       roi_base=None,
                       umbral_sensibilidad=30, 
                       min_area_base=250, 
                       kernel_size_base=7, 
                       umbral_dist_base=50, 
                       max_frames_perdido=20,
                       frames_para_confirmar=8,
                       
                       filtro_sentido=None):
    
    # --- Inicialización ---
    cap = leer_video(ruta_video)
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Ancho original
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Alto original

    # Redimensionamos según la escala
    new_size = (int(original_width * escala), int(original_height * escala))
    fondo_redimensionado = cv2.resize(cv2.imread(ruta_fondo), new_size).astype(np.uint8)

    # --- Definir la ROI ---
    if roi_base:
        # Si ROI pasada como parámetro
        roi_escalada = [int(roi_base[0] * escala), int(roi_base[1] * escala), 
                        int(roi_base[2] * escala), int(roi_base[3] * escala)]
        mask_roi = np.zeros((new_size[1], new_size[0]), dtype=np.uint8)
        mask_roi[roi_escalada[0]:roi_escalada[1], roi_escalada[2]:roi_escalada[3]] = 255
    else:
        # Si no tenemos ROI como parámetro
        mask_roi = np.ones((new_size[1], new_size[0]), dtype=np.uint8) * 255 # Todo bits blancos para que el bitwise_and no haga nada
        roi_escalada = None # Para que no intente dibujarla posteriormente


    # --- Cálculo de parámetros escalados ---
    min_area_escalada = min_area_base * (escala**2) # Ajusta el área (2D) de forma cuadrática a la escala
    kernel_size_val = int(np.ceil(kernel_size_base * escala)) // 2 * 2 + 1 # Ajusta el kernel (1D) a la escala y fuerza que sea impar
    kernel_escalado = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size_val, kernel_size_val)) # Crea la matriz del kernel con el tamaño escalado
    umbral_dist_escalado = umbral_dist_base * escala # Ajusta la distancia (1D) de seguimiento a la escala

    # --- Gestor con Filtro de Kalman ---
    gestor = GestorVehiculos(
        umbral_distancia=umbral_dist_escalado, 
        max_frames_perdido=max_frames_perdido
    )

    frame_num = 0 # Inicializa el contador de frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_num += 1 # Incrementa el contador de fotogramas
        frame = cv2.resize(frame, new_size)

        # --- Detección ---
        diff = cv2.absdiff(frame, fondo_redimensionado) # Resta el fondo estático al frame actual
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # Convierte la imagen de diferencia a escala de grises
        _, fgmask = cv2.threshold(diff, umbral_sensibilidad, 255, cv2.THRESH_BINARY) # Binariza la imagen
        fgmask = cv2.bitwise_and(fgmask, mask_roi) # Aplica la máscara ROI (pone a negro todo lo que esté fuera de la región)
        
        # Operaciones morfológicas para limpiar la máscara
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel_escalado) # Rellena agujeros blancos dentro de los blobs
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel_escalado) # Elimina pequeños puntos blancos (ruido)

        contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Encuentra todos los contornos (blobs blancos) en la máscara
        detecciones = [] # Inicializa una lista vacía para guardar las detecciones de este frame
        
        for c in contornos: # Recorre cada contorno (blob) encontrado
            if cv2.contourArea(c) < min_area_escalada:
                continue
            x, y, w, h = cv2.boundingRect(c) # Calcula la caja delimitadora (bounding box) del contorno
            detecciones.append((x, y, w, h)) # Añade las coordenadas de la caja a la lista de detecciones
        
        # --- Actualizar el gestor ---
        gestor.actualizar(detecciones, frame, frame_num)
        
        # --- Contadores en tiempo real ---
        contador_actual = 0
        contador_suben_rt = 0
        contador_bajan_rt = 0

        # Iteramos sobre los vehículos activos
        for v in gestor.vehiculos_activos():
            
            # Solo dibujamos y contamos los coches "confirmados"
            if v.frames_activo > frames_para_confirmar:
            
                x, y, w, h = map(int, v.bbox) # Obtiene la caja (bbox) del vehículo y convierte sus coordenadas a enteros
                cx, cy = v.centroide # Obtiene el centroide (x, y) suavizado por el Filtro de Kalman
                vx, vy = v.velocidad # Obtiene la velocidad (vx, vy) estimada por el Filtro de Kalman
                
                # 1. Calcular la magnitud de la velocidad (velocidad en p/f)
                velocidad_mag = np.linalg.norm(v.velocidad) # Calcula la magnitud del vector velocidad (Pitágoras) para tener un solo número (píxeles/frame)
                
                # 2. Si el sentido del coche aún no está definido
                if not v.sentido:
                    # Comprobamos si la velocidad en Y es lo bastante fuerte para "fijarlo"
                    # Umbral +-0.5
                    if vy < -0.5: 
                        v.sentido = 'SUBE' # Fijado
                    elif vy > 0.5:
                        v.sentido = 'BAJA' # Fijado
                
                # 3. Filtro de Sentido
                if filtro_sentido is not None and v.sentido != filtro_sentido:
                    continue
                
                # --- Si pasa todos los filtros, lo contamos y dibujamos ---
                contador_actual += 1
                
                color_sentido = (255, 0, 0) # Azul (por defecto, si aún es None)
                texto_sentido = '(...)'     # Texto por defecto
                
                if v.sentido == 'SUBE':
                    contador_suben_rt += 1
                    color_sentido = (0, 255, 0) # Verde
                    texto_sentido = 'SUBE'
                elif v.sentido == 'BAJA':
                    contador_bajan_rt += 1
                    color_sentido = (0, 0, 255) # Rojo
                    texto_sentido = 'BAJA'

                # --- Dibujar en pantalla ---
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # ID del vehículo
                cv2.putText(frame, f"ID {v.id}", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
                
                # Velocidad (magnitud)
                cv2.putText(frame, f"{velocidad_mag:.1f} p/f", (x, y + h + 15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                
                # Sentido (ahora usa las variables 'texto_sentido' y 'color_sentido')
                cv2.putText(frame, texto_sentido, (x, y + h + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, color_sentido, 1)
        
        # Dibujar contadores en pantalla
        # Obtenemos el contador histórico (total de IDs únicos creados)
        contador_historico = Vehiculo._next_id
        # (Ajusta las coordenadas (20, 50) y (20, 90) si lo necesitas)
        cv2.putText(frame, f"Vehiculos Activos: {contador_actual}", (65, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, f"Total Historico: {contador_historico}", (65, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        # --- Dibujar nuevos contadores de sentido (en tiempo real) ---
        cv2.putText(frame, f"Subiendo: {contador_suben_rt}", (410, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Bajando: {contador_bajan_rt}", (410, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Dibujamos la ROI en el frame original para debug
        if roi_escalada:
            cv2.rectangle(frame, (roi_escalada[2], roi_escalada[0]), (roi_escalada[3], roi_escalada[1]), (255, 0, 0), 2)

        cv2.imshow("Máscara", fgmask)
        cv2.imshow("Video Original", frame)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()