import openrouteservice
import sys

# API Key real de OpenRouteService
client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA1YjFhY2I5ODM3ZDQxZmY5YWQ4NDMyMTk0MWI5NDZkIiwiaCI6Im11cm11cjY0In0=")

# Coordenadas básicas para algunas ciudades de Chile y Perú
ciudades = {
    "santiago": (-70.6483, -33.4569),
    "valparaíso": (-71.6127, -33.0472),
    "arica": (-70.3146, -18.4783),
    "iquique": (-70.1319, -20.2307),
    "lima": (-77.0428, -12.0464),
    "arequipa": (-71.5375, -16.4090),
    "cusco": (-71.9675, -13.5319)
}

# Formato de duración
def formato_duracion(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    return f"{horas}h {minutos}m"

# Opciones de transporte
medios_transporte = {
    "1": "driving-car",
    "2": "cycling-regular",
    "3": "foot-walking"
}

print("=== CALCULADORA DE RUTA ENTRE CIUDADES ===")

# Entrada de datos
origen = input("Ingrese ciudad de origen (ej: Santiago) o 's' para salir: ").strip().lower()
if origen == "s":
    sys.exit()

destino = input("Ingrese ciudad de destino (ej: Lima) o 's' para salir: ").strip().lower()
if destino == "s":
    sys.exit()

if origen not in ciudades or destino not in ciudades:
    print("Una o ambas ciudades no están disponibles.")
    sys.exit()

# Elegir medio de transporte
print("\nSeleccione medio de transporte:")
print("1 - Automóvil")
print("2 - Bicicleta")
print("3 - A pie")
opcion = input("Opción: ").strip()

if opcion not in medios_transporte:
    print("Opción inválida.")
    sys.exit()

# Coordenadas para el cálculo
coords = [ciudades[origen], ciudades[destino]]

# Llamada a la API
try:
    ruta = client.directions(
        coordinates=coords,
        profile=medios_transporte[opcion],
        format="json"
    )
except Exception as e:
    print(f"Error al obtener la ruta: {e}")
    sys.exit()

# Procesar respuesta
distancia_metros = ruta['routes'][0]['summary']['distance']
duracion_segundos = ruta['routes'][0]['summary']['duration']
narrativa = ruta['routes'][0]['segments'][0]['steps']

# Mostrar resultados
print("\n=== RESULTADOS ===")
print(f"De: {origen.title()} → {destino.title()}")
print(f"Distancia: {distancia_metros / 1000:.2f} km / {distancia_metros * 0.000621371:.2f} millas")
print(f"Duración estimada: {formato_duracion(int(duracion_segundos))}")

print("\nPasos del trayecto:")
for paso in narrativa:
    print(f"- {paso['instruction']}")

