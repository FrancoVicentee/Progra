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
        print("[8] Ver tipos de habitación utilizados")
        print("[9] Ver clientes sin reservas")
        print("[10] Listar apellidos de clientes")
        print("[11] Promedio general de capacidad")
        print("[12] Promedio de capacidad por tipo")
        print("[13] Conteo de habitaciones por estado")
        print("[14] Porcentaje de ocupación")
        print("[15] Habitación con mayor y menor capacidad")
        print("[16] Resumen estadístico general")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 16)

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
        elif opcion == 8:
            tipos_de_habitacion_utilizados(habitaciones_lista)
        elif opcion == 9:
            clientes_sin_reserva(clientes_lista, reservas_lista)
        elif opcion == 10:
            listar_apellidos_clientes(clientes_lista)
        elif opcion == 11:
            promedio_capacidad_habitaciones(habitaciones_lista)
        elif opcion == 12:
            promedio_capacidad_por_tipo(habitaciones_lista)
        elif opcion == 13:
            conteo_habitaciones_por_estado(habitaciones_lista)
        elif opcion == 14:
            porcentaje_ocupacion(habitaciones_lista)
        elif opcion == 15:
            habitacion_capacidad_max_min(habitaciones_lista)
        elif opcion == 16:
            resumen_estadistico(clientes_lista, habitaciones_lista, reservas_lista)
        else:
            print("Saliendo del menú de matrices...")


def tipos_de_habitacion_utilizados(lista_de_habitaciones):
    print("\n--- Tipos de habitación utilizados ---")
    tipos = {habitacion[2] for habitacion in lista_de_habitaciones}
    print("Tipos de habitación en uso:", tipos)
    val_datos.pausar_menu()
    return tipos


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


def listar_apellidos_clientes(clientes_lista):
    print("\n--- Apellidos de los clientes ---")
    apellidos = list(map(lambda cliente: cliente[2], clientes_lista))
    print(apellidos)
    val_datos.pausar_menu()
    return apellidos

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


def promedio_capacidad_por_tipo(habitaciones_lista):
    print("\n--- Promedio de capacidad por tipo ---")
    tipos = {habitacion[2] for habitacion in habitaciones_lista}

    if len(tipos) == 0:
        print("No hay habitaciones cargadas.")
        return {}

    promedios = {}
    for tipo in tipos:
        capacidades_tipo = [habitacion[3] for habitacion in habitaciones_lista if habitacion[2] == tipo]
        promedios[tipo] = sum(capacidades_tipo) / len(capacidades_tipo)

    for tipo, promedio in promedios.items():
        print(f"{tipo}: {promedio:.2f}")

    val_datos.pausar_menu()
    return promedios


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