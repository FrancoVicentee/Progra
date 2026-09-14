from paquete_2 import val_datos



"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Funciones para el manejo de habitaciones en el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""


def alta_habitacion(habitaciones_lista):
    titulo = " Alta de habitaciones "
    print(f"\n{titulo:-^50}")
 
 
    numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
 
    numero_existe = existe_numero_habitacion(habitaciones_lista, numero)
    while numero_existe == True:
        print("Error. Ya existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
        numero_existe = existe_numero_habitacion(habitaciones_lista, numero)
 
    tipo = val_datos.pedir_tipo_habitacion("Ingrese el tipo de habitación (Simple/Doble/Suite): ")
 
    capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo)
    capacidad = val_datos.pedir_entero_rango(
        f"Ingrese la capacidad de la habitación ({capacidad_minima}-{capacidad_maxima}): ",
        capacidad_minima, capacidad_maxima
    )
 
    estado = val_datos.pedir_estado_habitacion("Ingrese el estado de la habitación (Disponible/Ocupada/Mantenimiento): ")
 
    id_nuevo = generar_id_habitacion(habitaciones_lista)
 
    habitacion_nueva = [id_nuevo, numero, tipo, capacidad, estado]
    habitaciones_lista.append(habitacion_nueva)
 
    print("Habitación agregada correctamente.")
 
    return habitaciones_lista


def listar_habitaciones(habitaciones_lista):
    titulo = " Listado de habitaciones "
    print(f"\n{titulo:-^55}")
 
    cantidad_habitaciones = len(habitaciones_lista)
 
    if cantidad_habitaciones == 0:
        print("No hay habitaciones cargadas.")
    else:
        print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<13}{'Estado':<15}")
        print(f"{'-' * 55}")
 
        indice = 0
        while indice < cantidad_habitaciones:
            habitacion_actual = habitaciones_lista[indice]
            mostrar_habitacion(habitacion_actual)
            indice += 1
 
        print(f"{'-' * 55}")
        print(f"Cantidad total de habitaciones: {cantidad_habitaciones}")
 
        val_datos.pausar_menu()
    return habitaciones_lista


def baja_habitacion(habitaciones_lista):
    titulo = " Baja de habitacion "
    print(f"\n{titulo:-^50}")
 
    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
    else:
        numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a dar de baja: ", 100, 999)
 
        posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
 
        while posicion == -1:
            print("Error. No existe una habitación con ese número.")
            numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a dar de baja: ", 100, 999)
            posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
 
        print("\nSe encontró la siguiente habitación:")
        mostrar_habitacion(habitaciones_lista[posicion])
 
        confirmacion = val_datos.pedir_entero_rango("¿Confirma la baja? [1] Sí [0] No: ", 0, 1)
 
        if confirmacion == 1:
            habitaciones_lista.pop(posicion)
            print("Habitación eliminada correctamente.")
        else:
            print("Operación cancelada. La habitación no fue eliminada.")
 
    return habitaciones_lista


def modificar_habitacion(habitaciones_lista):
    titulo = " Modificación de habitacion "
    print(f"\n{titulo:-^50}")
 
 
    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
    else:
        numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a modificar: ", 100, 999)
 
        posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
 
        while posicion == -1:
            print("Error. No existe una habitación con ese número.")
            numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a modificar: ", 100, 999)
            posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
 
        print("\nSe encontró la siguiente habitación:")
        mostrar_habitacion(habitaciones_lista[posicion])
 
        print("\n---------------------------")
        print("¿Qué desea modificar?")
        print("[1] Número")
        print("[2] Tipo")
        print("[3] Capacidad")
        print("[4] Estado")
        print("[0] Cancelar")
        print("---------------------------")
 
        opcion_modificar = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)
 
        if opcion_modificar == 1:
            numero_nuevo = val_datos.pedir_entero_rango("Ingrese el nuevo número: ", 100, 999)
 
            numero_existe = existe_numero_en_otra_posicion(habitaciones_lista, numero_nuevo, posicion)
            while numero_existe == True:
                print("Error. Ya existe otra habitación con ese número.")
                numero_nuevo = val_datos.pedir_entero_rango("Ingrese el nuevo número: ", 100, 999)
                numero_existe = existe_numero_en_otra_posicion(habitaciones_lista, numero_nuevo, posicion)
 
            habitaciones_lista[posicion][1] = numero_nuevo
            print("Número modificado correctamente.")
 
        elif opcion_modificar == 2:
            tipo_nuevo = val_datos.pedir_tipo_habitacion("Ingrese el nuevo tipo (Simple/Doble/Suite): ")
 
            habitaciones_lista[posicion][2] = tipo_nuevo
            print("Tipo modificado correctamente.")
 
            capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo_nuevo)
            capacidad_actual = habitaciones_lista[posicion][3]
 
            if capacidad_actual < capacidad_minima or capacidad_actual > capacidad_maxima:
                print(f"La capacidad actual ({capacidad_actual}) no es válida para el tipo {tipo_nuevo}.")
                capacidad_ajustada = val_datos.pedir_entero_rango(
                    f"Ingrese la nueva capacidad ({capacidad_minima}-{capacidad_maxima}): ",
                    capacidad_minima, capacidad_maxima
                )
                habitaciones_lista[posicion][3] = capacidad_ajustada
 
        elif opcion_modificar == 3:
            tipo_actual = habitaciones_lista[posicion][2]
            capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo_actual)
 
            capacidad_nueva = val_datos.pedir_entero_rango(
                f"Ingrese la nueva capacidad ({capacidad_minima}-{capacidad_maxima}): ",
                capacidad_minima, capacidad_maxima
            )
 
            habitaciones_lista[posicion][3] = capacidad_nueva
            print("Capacidad modificada correctamente.")
 
        elif opcion_modificar == 4:
            estado_nuevo = val_datos.pedir_estado_habitacion("Ingrese el nuevo estado (Disponible/Ocupada/Mantenimiento): ")
 
            habitaciones_lista[posicion][4] = estado_nuevo
            print("Estado modificado correctamente.")
 
        else:
            print("Operación cancelada. No se modificó ningún dato.")
 
        print("\nLa habitación quedó así:")
        mostrar_habitacion(habitaciones_lista[posicion])
 
    return habitaciones_lista


def mostrar_habitacion(habitacion):
    id_habitacion = habitacion[0]
    numero_habitacion = habitacion[1]
    tipo_habitacion = habitacion[2]
    capacidad_habitacion = habitacion[3]
    estado_habitacion = habitacion[4]
 
    print(f"{id_habitacion:<5}{numero_habitacion:<10}{tipo_habitacion:<12}{capacidad_habitacion:<12}{estado_habitacion:<15}")


def existe_numero_habitacion(habitaciones_lista, numero):
    existe = False
    for habitacion in habitaciones_lista:
        if habitacion[1] == numero:
            existe = True
    return existe


def existe_numero_en_otra_posicion(habitaciones_lista, numero, posicion_actual):
    existe = False
    indice = 0
    for habitacion in habitaciones_lista:
        if habitacion[1] == numero and indice != posicion_actual:
            existe = True
        indice += 1
    return existe


def buscar_posicion_por_numero(habitaciones_lista, numero):
    posicion = -1
    indice = 0
    for habitacion in habitaciones_lista:
        if habitacion[1] == numero:
            posicion = indice
        indice += 1
    return posicion


def obtener_rango_capacidad(tipo):
    if tipo == "Simple":
        capacidad_minima = 1
        capacidad_maxima = 1
    elif tipo == "Doble":
        capacidad_minima = 1
        capacidad_maxima = 2
    else:
        capacidad_minima = 1
        capacidad_maxima = 6
 
    return capacidad_minima, capacidad_maxima


def generar_id_habitacion(habitaciones_lista):
    id_nuevo = list(map(lambda habitacion: habitacion[0], habitaciones_lista))
    return max(id_nuevo) + 1

def consultar_habitacion(habitaciones_lista):
    titulo = " Consultar habitación "
    print(f"\n{titulo:-^50}")

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación: ", 100, 999)
    posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

    if posicion == -1:
        print("No existe una habitación con ese número.")
    else:
        mostrar_habitacion(habitaciones_lista[posicion])

    val_datos.pausar_menu()
    return habitaciones_lista
 
 

"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Menú de habitaciones para el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""


def menu_habitaciones(habitaciones_lista):
    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Habitaciones "
        print(f"\n{titulo:-^50}")
        print("[1] Alta de habitación")
        print("[2] Listar habitaciones")
        print("[3] Baja de habitación")
        print("[4] Modificar habitación")
        print("[5] Consultar habitación")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                habitaciones_lista = alta_habitacion(habitaciones_lista)
            case 2:
                habitaciones_lista = listar_habitaciones(habitaciones_lista)
            case 3:
                habitaciones_lista = baja_habitacion(habitaciones_lista)
            case 4:
                habitaciones_lista = modificar_habitacion(habitaciones_lista)
            case 5:
                habitaciones_lista = consultar_habitacion(habitaciones_lista)
            case 0:
                print("Saliendo del menú de habitaciones...")

    return habitaciones_lista