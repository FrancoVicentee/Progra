from functools import reduce
from paquete_2 import val_datos

def menu_matrices(clientes_lista, habitaciones_lista, reservas_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE MATRICES")
        print("---------------------------")
        print("[1] Ordenar clientes por apellido")
        print("[2] Ordenar habitaciones por número")
        print("[3] Ordenar reservas por fecha de ingreso")
        print("[4] Ver habitaciones disponibles")
        print("[5] Ver capacidad total del hotel")
        print("[6] Ver números de habitación registrados")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 6)

        if opcion == 1:
            print("\n--- Clientes ordenados por apellido ---")
        elif opcion == 2:
            print("\n--- Habitaciones ordenadas por número ---")
        elif opcion == 3:
            print("\n--- Reservas ordenadas por fecha de ingreso ---")
        elif opcion == 4:
            print("\n--- Habitaciones disponibles ---")
        elif opcion == 5:
           print("\n--- Capacidad total del hotel ---")
        elif opcion == 6:
            print("\n--- Números de habitación registrados ---")

