# 🚗 Radar de Coches FSI - ULPGC  
**Autores:** Alejandro Delgado y Tomás Santana  
**Asignatura:** Fundamentos de Sistemas Inteligentes  
**Universidad de Las Palmas de Gran Canaria**  
**Versión:** v0.1  

---

## 1. Introducción y Objetivos
El presente proyecto tiene como objetivo el desarrollo de un sistema de visión artificial capaz de detectar, contar, clasificar y estimar la velocidad de vehículos en vías de tráfico. La implementación se ha realizado en Python utilizando la librería **OpenCV** para el procesamiento de imagen y **Tkinter** para la interfaz de usuario, siguiendo una metodología de desarrollo incremental que culminó en una refactorización modular.

## 2. Metodología y Evolución del Desarrollo

El desarrollo del sistema ha seguido un enfoque iterativo dividido en cuatro fases claramente diferenciadas, que permitieron evolucionar desde pruebas de concepto básicas hasta una aplicación robusta y estructurada.

### Fase 1: Prototipado Inicial (`funcionesV1.py`)
En la etapa inicial, se desarrollaron scripts procedimentales para validar las técnicas básicas de visión por computador:
* **Extracción de Fondo:** Implementación del algoritmo de promedio temporal (`obtener_fondo`) para generar un modelo estático del fondo vacío, eliminando los vehículos en movimiento de la escena base.
* **Detección Básica:** Uso de la diferencia absoluta (`cv2.absdiff`) y umbralización binaria para detectar movimiento y validar la obtención de Regiones de Interés (ROIs).
* *Limitación:* Estas funciones sirvieron como prueba de concepto pero carecían de persistencia temporal (*tracking*), lo que provocaba conteos erróneos ante parpadeos o detenciones.

### Fase 2: Arquitectura Orientada a Objetos
Para resolver los problemas de pérdida de identidad y dotar al sistema de "memoria", se migró el núcleo lógico hacia un paradigma de Orientación a Objetos:
* **Modelo `Vehiculo` (`vehiculos.py`):** Se encapsuló el estado de cada coche en un objeto. La mejora crítica fue la integración del **Filtro de Kalman** (`cv2.KalmanFilter`). Este filtro permite predecir la posición futura del vehículo y suavizar su trayectoria, siendo esencial para obtener una estimación estable de la velocidad y evitar saltos en la detección.
* **Controlador `GestorVehiculos` (`gestor_vehiculos.py`):** Se desarrolló un gestor de identidades capaz de asociar las detecciones de cada *frame* con los vehículos existentes, minimizando la distancia euclidiana. Además, maneja oclusiones temporales mediante un sistema de "paciencia" (`max_frames_perdido`), permitiendo recuperar la identidad de un coche tras pasar tras un obstáculo.

### Fase 3: Lógica Avanzada (`funcionesV2.py`)
Sobre la base de objetos, se desarrollaron algoritmos complejos para cumplir los requisitos funcionales de la práctica:
* **Corrección de Fragmentación:** Se detectó que vehículos grandes (camiones) se dividían en múltiples detecciones. Se implementó el algoritmo `fusionar_detecciones_cercanas` para agrupar detecciones próximas en una sola entidad.
* **Clasificación y Física:** Implementación de lógica para diferenciar entre **Motos, Coches y Camiones** analizando el área del contorno y su relación de aspecto (*aspect ratio*). Cálculo de la velocidad vectorial y determinación del sentido de la marcha (Subiendo/Bajando, Izquierda/Derecha).
* **Gestión de Atascos:** Integración del sustractor de fondo dinámico **MOG2**, permitiendo al sistema adaptarse a cambios de luz y gestionar vehículos que se detienen (incorporándolos al fondo temporalmente).

### Fase 4: Refactorización e Integración Final (`functions.py`)
En la etapa final del desarrollo, se realizó una limpieza y unificación del código (**Refactoring**) para mejorar la calidad del software.
* **Unificación de Módulos:** Se fusionaron las primitivas robustas de la Fase 1 (lectura y preprocesamiento) con la lógica avanzada de la Fase 3 en un único módulo consolidado llamado **`functions.py`**.
* **Beneficio:** Esta reestructuración eliminó redundancias, centralizó toda la lógica de visión computacional en un solo fichero y simplificó las dependencias del proyecto.

## 3. Aporte Personal: Interfaz Gráfica de Usuario (GUI)

Como valor añadido significativo al proyecto, se ha desarrollado una aplicación de escritorio completa utilizando la librería **Tkinter**. El objetivo de este aporte es transformar el script de detección en una herramienta de software usable por un usuario final sin conocimientos de programación.

Las características principales de la interfaz (`main.py`) incluyen:

* **Carga de Vídeos Intuitiva:** Permite al usuario seleccionar archivos de vídeo locales mediante un explorador de archivos nativo.
* **Panel de Configuración Dinámica:** Se ha diseñado un panel de control lateral que permite ajustar en tiempo real los parámetros críticos del algoritmo sin reiniciar la aplicación:
    * Ajuste de sensibilidad de detección y áreas mínimas/máximas para filtrar ruido.
    * Selección del método de fondo (Estático vs Dinámico MOG2).
    * Configuración de la orientación de la vía (Vertical/Horizontal).
* **Visualización Parametrizable:** Controles (*Checkboxes*) para activar o desactivar capas de información sobre el vídeo (mostrar/ocultar IDs, vectores de velocidad, contadores globales, cajas delimitadoras, etc.).

Esta interfaz actúa como orquestador, conectando la entrada del usuario con la lógica del módulo `functions.py` y el `GestorVehiculos`, haciendo del sistema una solución flexible y adaptable a diferentes escenarios de tráfico.

## 4. Conclusiones
El sistema final combina la robustez matemática de la estimación de estados (Kalman) con la usabilidad de una aplicación gráfica moderna. La evolución desde scripts básicos hasta una aplicación con GUI y código refactorizado demuestra no solo la resolución de los problemas de visión por computador planteados, sino también la aplicación de buenas prácticas de ingeniería de software.

