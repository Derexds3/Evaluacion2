import urllib.parse
import requests

# URL base de la API de Graphhopper
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

# Ingrese aquí su Token / API Key de Graphhopper
KEY = "59364a38-31c5-42f6-acd8-ca0ffa8c06fd"


def obtener_coordenadas(ubicacion, key):
    """Obtiene la latitud, longitud y nombre formateado de una ubicación."""
    while ubicacion.strip() == "":
        ubicacion = input("Por favor, ingrese una ubicación válida: ")

    url = GEOCODE_URL + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": key})
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        
        if respuesta.status_code == 200 and len(datos["hits"]) > 0:
            punto = datos["hits"][0]["point"]
            nombre = datos["hits"][0]["name"]
            pais = datos["hits"][0].get("country", "")
            
            nombre_completo = f"{nombre}, {pais}" if pais else nombre
            return respuesta.status_code, punto["lat"], punto["lng"], nombre_completo
        else:
            print(f"Error: No se pudo geolocalizar la ubicación '{ubicacion}'.")
            return respuesta.status_code, None, None, ubicacion
    except Exception as e:
        print(f"Error de conexión con la API: {e}")
        return 500, None, None, ubicacion


def main():
    while True:
        print("\n" + "=" * 60)
        print("      SISTEMA DE NAVEGACIÓN Y RUTA - BIBLIOTECA NACIONAL      ")
        print("=" * 60)
        
        # 1 y 3. Solicitud en español y opción de salida con 's' o 'salir'
        origen = input("Ingrese el punto de Origen (o 's' / 'salir' para finalizar): ").strip()
        if origen.lower() in ["s", "salir"]:
            print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
            break

        destino = input("Ingrese el punto de Destino (o 's' / 'salir' para finalizar): ").strip()
        if destino.lower() in ["s", "salir"]:
            print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
            break

        # Obtener coordenadas mediante Geocoding
        status_orig, lat_orig, lng_orig, nom_orig = obtener_coordenadas(origen, KEY)
        status_dest, lat_dest, lng_dest, nom_dest = obtener_coordenadas(destino, KEY)

        if status_orig == 200 and status_dest == 200 and lat_orig and lat_dest:
            # 4. Parámetro 'locale': 'es' para obtener la narrativa traducida desde la API
            parametros = [
                ("point", f"{lat_orig},{lng_orig}"),
                ("point", f"{lat_dest},{lng_dest}"),
                ("vehicle", "car"),
                ("locale", "es"),
                ("key", KEY)
            ]
            
            url_ruta = ROUTE_URL + urllib.parse.urlencode(parametros)
            respuesta_ruta = requests.get(url_ruta)
            datos_ruta = respuesta_ruta.json()

            if respuesta_ruta.status_code == 200:
                ruta = datos_ruta["paths"][0]
                
                # 2. Formateo de valores numéricos a máximo dos decimales
                distancia_km = ruta["distance"] / 1000.0
                distancia_millas = distancia_km * 0.621371
                tiempo_ms = ruta["time"]
                
                # Conversión de tiempo a formato legible
                segundos = int((tiempo_ms / 1000) % 60)
                minutos = int((tiempo_ms / (1000 * 60)) % 60)
                horas = int(tiempo_ms / (1000 * 60 * 60))

                print("\n" + "-" * 60)
                print(f"Origen  : {nom_orig}")
                print(f"Destino : {nom_dest}")
                print("-" * 60)
                print(f"Distancia total : {distancia_km:.2f} km ({distancia_millas:.2f} mi)")
                print(f"Tiempo estimado : {horas:02d}h {minutos:02d}m {segundos:02d}s")
                print("-" * 60)

                # 4. Impresión de la narrativa paso a paso en español
                print("\nINSTRUCCIONES DEL VIAJE (PASO A PASO):")
                print("-" * 60)
                
                for i, paso in enumerate(ruta["instructions"], start=1):
                    texto_paso = paso["text"]
                    dist_paso_km = paso["distance"] / 1000.0
                    print(f"{i:2d}. {texto_paso} ({dist_paso_km:.2f} km)")
                
                print("-" * 60)
            else:
                print("Error al calcular la ruta en la API de Graphhopper.")
        else:
            print("Verifique las direcciones ingresadas e intente de nuevo.")


if __name__ == "__main__":
    main()