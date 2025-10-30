# 🚗 Radar de Coches FSI - ULPGC  
**Autores:** Alejandro Delgado y Tomás Santana  
**Asignatura:** Fundamentos de Sistemas Inteligentes  
**Universidad de Las Palmas de Gran Canaria**  
**Versión:** v0.1  

---

## 🧠 Descripción general

Este proyecto desarrolla un **sistema de conteo y seguimiento de vehículos** en un entorno de tráfico real a partir de un vídeo base (`trafico01.mp4`), utilizando **visión por computador con OpenCV**.  
El objetivo principal es detectar, identificar y contabilizar los vehículos que circulan por una vía, diferenciando los que **entran y salen del encuadre**, con el fin de establecer una base sólida sobre la cual añadir funcionalidades más avanzadas como la clasificación por tipo o el cálculo de velocidad.

---

## 🎯 Objetivos iniciales de la práctica

A partir del vídeo oficial de tráfico proporcionado, se busca cumplir los siguientes puntos:

1. Desarrollar un **contador de vehículos** funcional que monitorice una vía.
2. Ampliar el sistema para **varios carriles y diferentes sentidos** de circulación.  
3. Adaptar la técnica a otros vídeos similares o con condiciones distintas.  
4. Manejar vías de doble sentido con coches entrando y saliendo.  
5. Ser robusto frente a **diferentes velocidades** y **tipos de vehículo**.  
6. (Opcional) Implementar **contadores por tipo de vehículo** y estimación de velocidad.

La práctica debe realizarse **exclusivamente con OpenCV** como librería de visión por computador.

---

## ⚙️ Estructura y arquitectura del proyecto

El proyecto está dividido en varios módulos para mantener la organización y escalabilidad del código:

- **`main.py`** → Punto de entrada del programa. Gestiona la lectura del vídeo, la inicialización de los módulos y el bucle principal de procesamiento.  
- **`gestor_vehiculos.py`** → Controla el flujo de información entre detecciones y el seguimiento de vehículos. Administra las listas de coches activos y actualiza sus estados entre frames.  
- **`coche.py`** → Define la clase `Coche`, que representa cada vehículo individual, con su centroide, bounding box y recorte del frame.  
- **`funcionesV1.py` y `funcionesV2.py`** → Versiones progresivas del conjunto de funciones de procesamiento, encargadas de tareas como la detección de movimiento, filtrado de ruido, extracción de contornos y gestión de líneas de conteo.

Cada versión (`V1`, `V2`, etc.) introduce mejoras sobre la anterior, incluyendo optimización en el filtrado de detecciones, estabilidad en el seguimiento y pruebas con distintos métodos de segmentación.

---

## 🧩 Desarrollo e implementación

El sistema actual se basa en la **detección de movimiento mediante diferencias de frames y técnicas de segmentación de fondo**, aplicando transformaciones morfológicas para eliminar ruido y mejorar la precisión en la detección de contornos.

Una vez detectados los objetos en movimiento:

1. Se obtiene la **bounding box** y el **centroide** de cada vehículo.  
2. Cada detección se gestiona como una **instancia de la clase `Coche`**, la cual almacena información relevante del objeto (posición, frame, estado…).  
3. El módulo `gestor_vehiculos` se encarga de actualizar las instancias activas, comprobar colisiones entre detecciones y mantener la coherencia entre frames consecutivos.  

En la versión actual (v0.1), el sistema ya **detecta y representa correctamente los vehículos** en movimiento, manteniendo un seguimiento visual estable en los casos básicos de tráfico fluido.

---

## 🧪 Resultados actuales

- El sistema consigue **identificar y seguir vehículos** que aparecen en el vídeo de tráfico principal (`trafico01.mp4`).  
- Se ha conseguido una **estructura modular** clara que permite escalar el proyecto fácilmente (añadir clasificación, conteo por carril o velocidad).  
- Se han realizado **pruebas preliminares** con diferentes parámetros de segmentación y morfología para ajustar la robustez del detector.  
- Se ha implementado el **seguimiento mediante instancias de clase** que mantienen la identidad de cada coche a lo largo del vídeo.

---

## 🔍 Conclusiones parciales

El sistema ya cumple la base del punto **1 de la práctica (contador funcional básico)** y sienta la estructura necesaria para abordar el resto de requisitos.  
A partir de esta versión, se trabajará en:

- Refinar el conteo por carriles y sentidos.  
- Diferenciar tipos de vehículos.  
- Añadir estimación de velocidad.  
- Mejorar la robustez ante distintos escenarios.

---

## 🧩 Tecnologías y dependencias

- **Lenguaje:** Python 3.12  
- **Librerías principales:**  
  - `opencv-python`  
  - `numpy`  
- **Recursos:** vídeo de tráfico proporcionado (`trafico01.mp4`)

---

> **Nota:** Este documento sirve como memoria técnica intermedia (v0.1).  
> La memoria final incluirá los apartados restantes una vez completadas las fases de clasificación, conteo por sentido y cálculo de velocidad.

