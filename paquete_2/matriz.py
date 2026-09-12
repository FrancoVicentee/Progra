import re 
from functools import reduce
from paquete_2 import val_datos
 
#ordena la lista de clientes por apellido, utilizando el tercer elemento de cada cliente como clave de ordenamiento
 
def ordenar_por_apellido(lista_de_clientes):
    lista_de_clientes.sort(key=lambda cliente: cliente[2])
    print("Clientes ordenados por apellido:")
    for cliente in lista_de_clientes:
        print(cliente)
    val_datos.pausar_menu()
    return lista_de_clientes
 
#ordena la lista de habitaciones por número, utilizando el segundo elemento de cada habitación como clave de ordenamiento
 
def ordenar_por_numero(lista_de_habitaciones):
    lista_de_habitaciones.sort(key=lambda habitacion: habitacion[1])
    print("Habitaciones ordenadas por número:")
    for habitacion in lista_de_habitaciones:
        print(habitacion)
    val_datos.pausar_menu()
    return lista_de_habitaciones
 
#ordena la lista de reservas por fecha de ingreso, utilizando el cuarto elemento de cada reserva como clave de ordenamiento
 
def ordenar_por_fecha_ingreso(lista_de_reservas):
    lista_de_reservas.sort(key=lambda reserva: reserva[3])
    print("Reservas ordenadas por fecha de ingreso:")
    for reserva in lista_de_reservas:
        print(reserva)
    val_datos.pausar_menu()
    return lista_de_reservas
 
#verifica qué habitaciones están disponibles en la lista de habitaciones
 
def ver_habitaciones_disponibles(lista_de_habitaciones):
    habitaciones_disponibles = [habitacion for habitacion in lista_de_habitaciones if habitacion[4] == 'Disponible']
    print("Habitaciones disponibles:")
    for habitacion in habitaciones_disponibles:
        print(habitacion)
    val_datos.pausar_menu()
    return habitaciones_disponibles
 
#calcula la capacidad total del hotel sumando la capacidad de cada habitación en la lista de habitaciones
 
def calcular_capacidad_total(lista_de_habitaciones):
    capacidad_total = reduce(lambda total, habitacion: total + habitacion[3], lista_de_habitaciones, 0)
    print(f"Capacidad total del hotel: {capacidad_total} personas")
    val_datos.pausar_menu()
    return capacidad_total
 
#imprime los numeros de las habitaciones registradas en la lista de habitaciones
 
def obtener_habitaciones_ocupadas(lista_de_habitaciones):
    habitaciones_ocupadas = [habitacion for habitacion in lista_de_habitaciones if habitacion[4] == 'Ocupada']
 
    print("\n--- Habitaciones ocupadas ---")
    if len(habitaciones_ocupadas) == 0:
        print("No hay habitaciones ocupadas.")
    else:
        print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<12}{'Estado':<15}")
        print("-" * 50)
        for habitacion in habitaciones_ocupadas:
            print(f"{habitacion[0]:<5}{habitacion[1]:<10}{habitacion[2]:<12}{habitacion[3]:<12}{habitacion[4]:<15}")
 
    val_datos.pausar_menu()
    return habitaciones_ocupadas
 
 
def buscar_clientes_por_inicial(clientes_lista, letra):
    patron = "^" + letra
    clientes_encontrados = []
    for cliente in clientes_lista:
        if re.match(patron, cliente[1], re.IGNORECASE):
            clientes_encontrados.append(cliente)
    print(f"\n--- Clientes cuyo nombre empieza con '{letra}' ---")
    if len(clientes_encontrados) == 0:
        print("No se encontraron clientes.")
    else:
        for cliente in clientes_encontrados:
            print(cliente)
 
    val_datos.pausar_menu()
    return clientes_encontrados
 
 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Menú de matrices para el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
def menu_matrices(clientes_lista, habitaciones_lista, reservas_lista):
    opcion = -1
 
    while opcion != 0:
        titulo = " Menú Principal > Menú de Matrices "
        print(f"\n{titulo:-^50}")
        print("[1] Ordenar clientes por apellido")
        print("[2] Ordenar habitaciones por número")
        print("[3] Ordenar reservas por fecha de ingreso")
        print("[4] Ver habitaciones disponibles")
        print("[5] Ver capacidad total del hotel")
        print("[6] Ver habitaciones ocupadas")
        print("[7] Buscar clientes por letra inicial")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)
 
        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 7)
 
        if opcion == 1:
            subtitulo = " Clientes ordenados por apellido "
            print(f"\n{subtitulo:-^50}")
            ordenar_por_apellido(clientes_lista)
        elif opcion == 2:
            subtitulo = " Habitaciones ordenadas por número "
            print(f"\n{subtitulo:-^50}")
            ordenar_por_numero(habitaciones_lista)
        elif opcion == 3:
            subtitulo = " Reservas ordenadas por fecha de ingreso "
            print(f"\n{subtitulo:-^50}")
            ordenar_por_fecha_ingreso(reservas_lista)
        elif opcion == 4:
            subtitulo = " Habitaciones disponibles "
            print(f"\n{subtitulo:-^50}")
            ver_habitaciones_disponibles(habitaciones_lista)
        elif opcion == 5:
            subtitulo = " Capacidad total del hotel "
            print(f"\n{subtitulo:-^50}")
            calcular_capacidad_total(habitaciones_lista)
        elif opcion == 6:
            obtener_habitaciones_ocupadas(habitaciones_lista)
        elif opcion == 7:
            letra = input("Ingrese la letra inicial a buscar: ")
            buscar_clientes_por_inicial(clientes_lista, letra)
        else:
            print("Saliendo del menú de matrices...")
