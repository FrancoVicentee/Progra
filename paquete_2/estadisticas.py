import re 
from paquete_2 import val_datos
from functools import reduce

def calcular_capacidad_total(lista_de_habitaciones):
    capacidad_total = reduce(lambda total, habitacion: total + habitacion[3], lista_de_habitaciones, 0)
    print(f"Capacidad total del hotel: {capacidad_total} personas")
    val_datos.pausar_menu()
    return capacidad_total

def promedio_capacidad_habitaciones(habitaciones_lista):
    print("\n--- Promedio general de capacidad ---")
    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return 0

    capacidades = [habitacion[3] for habitacion in habitaciones_lista]
    promedio = sum(capacidades) / len(capacidades)
    print(f"Capacidad promedio de las habitaciones: {promedio:.2f}")
    val_datos.pausar_menu()
    return promedio


def conteo_habitaciones_por_estado(habitaciones_lista):
    print("\n--- Conteo de habitaciones por estado ---")
    estados = {habitacion[4] for habitacion in habitaciones_lista}

    conteo = {}
    for estado in estados:
        conteo[estado] = len([h for h in habitaciones_lista if h[4] == estado])

    print(f"Total de habitaciones: {len(habitaciones_lista)}")
    for estado, cantidad in conteo.items():
        print(f"{estado}: {cantidad}")

    val_datos.pausar_menu()
    return conteo


def porcentaje_ocupacion(habitaciones_lista):
    print("\n--- Porcentaje de ocupación ---")
    total = len(habitaciones_lista)
    if total == 0:
        print("No hay habitaciones cargadas.")
        return 0

    ocupadas = len([h for h in habitaciones_lista if h[4] == "Ocupada"])
    porcentaje = (ocupadas / total) * 100
    print(f"Habitaciones ocupadas: {ocupadas} de {total} ({porcentaje:.1f}%)")
    val_datos.pausar_menu()
    return porcentaje


def habitacion_capacidad_max_min(habitaciones_lista):
    print("\n--- Habitación con mayor y menor capacidad ---")
    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return

    mayor = max(habitaciones_lista, key=lambda habitacion: habitacion[3])
    menor = min(habitaciones_lista, key=lambda habitacion: habitacion[3])
    print(f"Mayor capacidad: {mayor}")
    print(f"Menor capacidad: {menor}")
    val_datos.pausar_menu()


def resumen_estadistico(clientes_lista, habitaciones_lista, reservas_lista):
    print("\n--- Resumen estadístico general ---")
    print(f"Total de clientes: {len(clientes_lista)}")
    print(f"Total de habitaciones: {len(habitaciones_lista)}")
    print(f"Total de reservas: {len(reservas_lista)}")

    if len(habitaciones_lista) > 0:
        capacidades = [habitacion[3] for habitacion in habitaciones_lista]
        print(f"Capacidad promedio: {sum(capacidades) / len(capacidades):.2f}")
        ocupadas = len([h for h in habitaciones_lista if h[4] == "Ocupada"])
        print(f"Porcentaje de ocupación: {(ocupadas / len(habitaciones_lista)) * 100:.1f}%")

    val_datos.pausar_menu()

def menu_estadisticas(clientes_lista, habitaciones_lista, reservas_lista):
    opcion = -1

    while opcion != 0:
        titulo = " Menú Principal > Menú de Estadísticas "
        print(f"\n{titulo:-^50}")
        print("[1] Ver capacidad total del hotel")
        print("[2] Promedio general de capacidad")
        print("[3] Conteo de habitaciones por estado")
        print("[4] Porcentaje de ocupación")
        print("[5] Habitación con mayor y menor capacidad")
        print("[6] Resumen estadístico general")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 6)

        match opcion:
            case 1:
                subtitulo = " Capacidad total del hotel "
                print(f"\n{subtitulo:-^50}")
                calcular_capacidad_total(habitaciones_lista)
            case 2:
                subtitulo = " Promedio general de capacidad "
                print(f"\n{subtitulo:-^50}")
                promedio_capacidad_habitaciones(habitaciones_lista)
            case 3:
                subtitulo = " Conteo de habitaciones por estado "
                print(f"\n{subtitulo:-^50}")
                conteo_habitaciones_por_estado(habitaciones_lista)
            case 4:
                subtitulo = " Porcentaje de ocupación "
                print(f"\n{subtitulo:-^50}")
                porcentaje_ocupacion(habitaciones_lista)
            case 5:
                subtitulo = " Habitación con mayor y menor capacidad "
                print(f"\n{subtitulo:-^50}")
                habitacion_capacidad_max_min(habitaciones_lista)
            case 6:
                resumen_estadistico(clientes_lista, habitaciones_lista, reservas_lista)
            case 0:
             print("Saliendo del menú de estadísticas...")