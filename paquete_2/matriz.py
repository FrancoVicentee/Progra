from functools import reduce
from paquete_2 import val_datos

#ordena la lista de clientes por apellido, utilizando el tercer elemento de cada cliente como clave de ordenamiento

def ordenar_por_apellido(lista_de_clientes):
    lista_de_clientes.sort(key=lambda cliente: cliente[2])
    print("Clientes ordenados por apellido:")
    for cliente in lista_de_clientes:
        print(cliente)
    return lista_de_clientes

#ordena la lista de habitaciones por número, utilizando el segundo elemento de cada habitación como clave de ordenamiento

def ordenar_por_numero(lista_de_habitaciones):
    lista_de_habitaciones.sort(key=lambda habitacion: habitacion[1])
    print("Habitaciones ordenadas por número:")
    for habitacion in lista_de_habitaciones:
        print(habitacion)
    return lista_de_habitaciones

#ordena la lista de reservas por fecha de ingreso, utilizando el cuarto elemento de cada reserva como clave de ordenamiento

def ordenar_por_fecha_ingreso(lista_de_reservas):
    lista_de_reservas.sort(key=lambda reserva: reserva[3])
    print("Reservas ordenadas por fecha de ingreso:")
    for reserva in lista_de_reservas:
        print(reserva)
    return lista_de_reservas

#verifica qué habitaciones están disponibles en la lista de habitaciones

def ver_habitaciones_disponibles(lista_de_habitaciones):
    habitaciones_disponibles = [habitacion for habitacion in lista_de_habitaciones if habitacion[4] == 'Disponible']
    print("Habitaciones disponibles:")
    for habitacion in habitaciones_disponibles:
        print(habitacion)
    return habitaciones_disponibles

#calcula la capacidad total del hotel sumando la capacidad de cada habitación en la lista de habitaciones

def calcular_capacidad_total(lista_de_habitaciones):
    capacidad_total = reduce(lambda total, habitacion: total + habitacion[3], lista_de_habitaciones, 0)
    return capacidad_total

#imprime los numeros de las habitaciones registradas en la lista de habitaciones

def obtener_numeros_de_habitacion(lista_de_habitaciones):
    numeros_de_habitacion = [habitacion[1] for habitacion in lista_de_habitaciones]
    return numeros_de_habitacion


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
            ordenar_por_apellido(clientes_lista)
        elif opcion == 2:
            print("\n--- Habitaciones ordenadas por número ---")
            ordenar_por_numero(habitaciones_lista)
        elif opcion == 3:
            print("\n--- Reservas ordenadas por fecha de ingreso ---")
            ordenar_por_fecha_ingreso(reservas_lista)
        elif opcion == 4:
            print("\n--- Habitaciones disponibles ---")
            ver_habitaciones_disponibles(habitaciones_lista)
        elif opcion == 5:
            print("\n--- Capacidad total del hotel ---")
            print(calcular_capacidad_total(habitaciones_lista))
        elif opcion == 6:
            print("\n--- Números de habitación registrados ---")
            print(obtener_numeros_de_habitacion(habitaciones_lista))
        else:
            print("Saliendo del menú de matrices...")
