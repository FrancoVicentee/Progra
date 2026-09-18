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
    lista_de_reservas.sort(key=lambda reserva: val_datos.convertir_fecha_a_numero(reserva[3]))
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


def clientes_sin_reserva(clientes_lista, reservas_lista):
    print("\n--- Clientes sin reservas ---")
    ids_clientes = {cliente[0] for cliente in clientes_lista}
    ids_con_reserva = {reserva[1] for reserva in reservas_lista}
    ids_sin_reserva = ids_clientes - ids_con_reserva

    if len(ids_sin_reserva) == 0:
        print("Todos los clientes tienen al menos una reserva.")
    else:
        for cliente in clientes_lista:
            if cliente[0] in ids_sin_reserva:
                print(cliente)
    val_datos.pausar_menu()
    return ids_sin_reserva

def habitaciones_reservadas_ambos_semestres(habitaciones_lista, reservas_lista):
    """
    Funcion que crea dos conjuntos que se separan en habitaciones reservadas en el 
    primer semestre y habitaciones reservadas en el segundo semestre. 
    Luego hace la interseccion de ambos conjuntos para ver que habitaciones estan reservadas en ambos semestres.
    """
    print("\n--- Habitaciones reservadas en ambos semestres ---")
    
    habitaciones_semestre_1 = {reserva[2] for reserva in reservas_lista if 1 <= int(reserva[3][3:5]) <= 6}
    habitaciones_semestre_2 = {reserva[2] for reserva in reservas_lista if 7 <= int(reserva[3][3:5]) <= 12}
    
    habitaciones_ambos_semestres = habitaciones_semestre_1.intersection(habitaciones_semestre_2)

    if len(habitaciones_ambos_semestres) == 0:
        print("No hay habitaciones reservadas en ambos semestres.")
    else:
        print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<12}{'Estado':<15}")
        print("-" * 54)
        for habitacion in habitaciones_lista:
            if habitacion[0] in habitaciones_ambos_semestres:
                print(f"{habitacion[0]:<5}{habitacion[1]:<10}{habitacion[2]:<12}{habitacion[3]:<12}{habitacion[4]:<15}")

    val_datos.pausar_menu()
    return habitaciones_ambos_semestres


def listar_nombres_mayusculas(clientes_lista):
    """
    Funcion que utiliza map para crear una lista de 
    nombres de clientes en mayusculas.
    """
    nombres_mayusculas = list(map(lambda cliente: cliente[1].upper(), clientes_lista))
    
    for nombre in nombres_mayusculas:
        print(nombre)
    val_datos.pausar_menu()




 
def menu_matrices(clientes_lista, habitaciones_lista, reservas_lista):
    """
    Menu principal para gestionar las matrices del sistema.
    """
    opcion = -1

    while opcion != 0:
        titulo = " Menú Principal > Menú de Matrices "
        print(f"\n{titulo:-^50}")
        print("[1] Ordenar clientes por apellido")
        print("[2] Ordenar habitaciones por número")
        print("[3] Ordenar reservas por fecha de ingreso")
        print("[4] Ver habitaciones disponibles")
        print("[5] Buscar clientes por letra inicial")
        print("[6] Ver habitaciones reservadas en ambos semestres")
        print("[7] Ver clientes sin reservas")
        print("[8] Listar nombres en mayúsculas")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 8)
        
        match opcion:
            case 1:
                subtitulo = " Clientes ordenados por apellido "
                print(f"\n{subtitulo:-^50}")
                ordenar_por_apellido(clientes_lista)
            case 2:
                subtitulo = " Habitaciones ordenadas por número "
                print(f"\n{subtitulo:-^50}")
                ordenar_por_numero(habitaciones_lista)
            case 3:
                subtitulo = " Reservas ordenadas por fecha de ingreso "
                print(f"\n{subtitulo:-^50}")
                ordenar_por_fecha_ingreso(reservas_lista)
            case 4:
                subtitulo = " Habitaciones disponibles "
                print(f"\n{subtitulo:-^50}")
                ver_habitaciones_disponibles(habitaciones_lista)
            case 5:
                letra = input("Ingrese la letra inicial a buscar: ")
                buscar_clientes_por_inicial(clientes_lista, letra)
            case 6:
                subtitulo = " Habitaciones reservadas en ambos semestres "
                print(f"\n{subtitulo:-^50}")
                habitaciones_reservadas_ambos_semestres(habitaciones_lista, reservas_lista)
            case 7:
                subtitulo = " Clientes sin reservas "
                print(f"\n{subtitulo:-^50}")
                clientes_sin_reserva(clientes_lista, reservas_lista)
            case 8:
                subtitulo = " Nombres de clientes en mayúsculas "
                print(f"\n{subtitulo:-^50}")
                listar_nombres_mayusculas(clientes_lista)
            case 0:
                print("Saliendo del menú de matrices...")