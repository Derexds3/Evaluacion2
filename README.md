# Evaluación 2: Sistema de Geolocalización y Gestión de Biblioteca

Proyecto desarrollado para la consultora **API Ltda.** en colaboración con la **Biblioteca Nacional**, enfocado en la integración de APIs REST, automatización con Python y servicios de geolocalización utilizando el entorno **DEVASC VM**.

## Descripción del Proyecto

Este repositorio contiene las soluciones desarrolladas para la modernización de los sistemas de la Biblioteca Nacional:

1. **Software de Geolocalización:** Script interactivo (`geolocalizacion.py`) que consume la API de **GraphHopper** para calcular rutas hacia la biblioteca, ofreciendo:
   - Interfaz y narrativa del viaje paso a paso completamente en español.
   - Formato numérico de distancia y tiempo redondeado a un máximo de dos decimales.
   - Opción de salida limpia mediante las palabras clave `"s"` o `"salir"`.

---

## Requisitos Previos

- **Python 3.x**
- Biblioteca `requests` instalada.
- Conexión a internet (para la API de GraphHopper) y acceso al servicio local de la API de la biblioteca.

Para instalar la dependencia necesaria, ejecute:

```bash
pip install requests

