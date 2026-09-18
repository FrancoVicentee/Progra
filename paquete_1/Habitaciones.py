from paquete_2 import val_datos
 
 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Funciones para el manejo de habitaciones en el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
 
def alta_habitacion(habitaciones_lista):
    """Solicita los datos validados al usuario y registra una nueva habitación en el sistema."""

    titulo = " Alta de habitaciones "
    print(f"\n{titulo:-^50}")
 
 
    numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 1000)
 
    numero_existe = existe_numero_habitacion(habitaciones_lista, numero)
    while numero_existe == True:
        print("Error. Ya existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 1000)
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
    """Imprime en pantalla todas las habitaciones registradas con formato de tabla."""
    
    titulo = " Listado de habitaciones "
    print(f"\n{titulo:-^50}")

    cantidad_habitaciones = len(habitaciones_lista)

    if cantidad_habitaciones == 0:
        print("No hay habitaciones cargadas.")
    else:
        print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<13}{'Estado':<15}")
        print("-" * 50)

        indice = 0
        while indice < cantidad_habitaciones:
            habitacion_actual = habitaciones_lista[indice]
            mostrar_habitacion(habitacion_actual)
            indice += 1

        print("-" * 50)
        print(f"Cantidad total de habitaciones: {cantidad_habitaciones}")

        val_datos.pausar_menu()
    return habitaciones_lista
 
 
def baja_habitacion(habitaciones_lista):
    titulo = " Baja de habitacion "
    print(f"\n{titulo:-^50}")
 
    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
    else:
        numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a dar de baja: ", 100, 1000)
 
        posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
 
        while posicion == -1:
            print("Error. No existe una habitación con ese número.")
            numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a dar de baja: ", 100, 1000)
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
        numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a modificar: ", 100, 1000)

        posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

        while posicion == -1:
            print("Error. No existe una habitación con ese número.")
            numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación a modificar: ", 100, 1000)
            posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

        print("\nSe encontró la siguiente habitación:")
        mostrar_habitacion(habitaciones_lista[posicion])

        print("Deje vacío el campo si no desea modificarlo.")

        numero_actual = habitaciones_lista[posicion][1]
        entrada_numero = input(f"Número ({numero_actual}): ")
        if entrada_numero != "":
            while val_datos.es_entero(entrada_numero) == False or int(entrada_numero) < 100 or int(entrada_numero) > 999 or existe_numero_en_otra_posicion(habitaciones_lista, int(entrada_numero), posicion):
                print("Error. Ingrese un número entre 100 y 999 que no esté en uso.")
                entrada_numero = input(f"Número ({numero_actual}): ")
            habitaciones_lista[posicion][1] = int(entrada_numero)

        tipo_actual = habitaciones_lista[posicion][2]
        entrada_tipo = input(f"Tipo ({tipo_actual}): ")
        if entrada_tipo != "":
            while val_datos.es_tipo_valido(entrada_tipo) == False:
                print("Error. Debe ingresar Simple, Doble o Suite.")
                entrada_tipo = input(f"Tipo ({tipo_actual}): ")
            habitaciones_lista[posicion][2] = val_datos.normalizar_capitalizado(entrada_tipo)

        tipo_vigente = habitaciones_lista[posicion][2]
        capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo_vigente)
        capacidad_actual = habitaciones_lista[posicion][3]
        entrada_capacidad = val_datos.pedir_entero_rango(f"Capacidad ({capacidad_actual}, rango {capacidad_minima}-{capacidad_maxima}): ", capacidad_minima, capacidad_maxima)
        if entrada_capacidad != "":
            while val_datos.es_entero(entrada_capacidad) == False or int(entrada_capacidad) < capacidad_minima or int(entrada_capacidad) > capacidad_maxima:
                print(f"Error. Ingrese un valor entre {capacidad_minima} y {capacidad_maxima}.")
                entrada_capacidad = val_datos.pedir_entero_rango(f"Capacidad ({capacidad_actual}, rango {capacidad_minima}-{capacidad_maxima}): ", capacidad_minima, capacidad_maxima)
            habitaciones_lista[posicion][3] = int(entrada_capacidad)
        elif capacidad_actual < capacidad_minima or capacidad_actual > capacidad_maxima:
            print(f"La capacidad actual ({capacidad_actual}) no es válida para el tipo {tipo_vigente}.")
            capacidad_ajustada = val_datos.pedir_entero_rango(
                f"Ingrese la nueva capacidad ({capacidad_minima}-{capacidad_maxima}): ",
                capacidad_minima, capacidad_maxima
            )
            habitaciones_lista[posicion][3] = capacidad_ajustada

        estado_actual = habitaciones_lista[posicion][4]
        entrada_estado = input(f"Estado ({estado_actual}): ")
        if entrada_estado != "":
            while val_datos.es_estado_valido(entrada_estado) == False:
                print("Error. Debe ingresar Disponible, Ocupada o Mantenimiento.")
                entrada_estado = input(f"Estado ({estado_actual}): ")
            habitaciones_lista[posicion][4] = val_datos.normalizar_capitalizado(entrada_estado)

        print("Habitación modificada correctamente.")

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
    if len(habitaciones_lista) == 0:
        id_nuevo = 1
    else:
        ids = list(map(lambda habitacion: habitacion[0], habitaciones_lista))
        id_nuevo = max(ids) + 1
 
    return id_nuevo
 
 
 
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
                print("Volviendo al menú anterior...")

    return habitaciones_lista

def consultar_habitacion(habitaciones_lista):
    titulo = " Consultar habitación "
    print(f"\n{titulo:-^50}")

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación: ", 100, 1000)
    posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

    if posicion == -1:
        print("No existe una habitación con ese número.")
    else:
        mostrar_habitacion(habitaciones_lista[posicion])

    val_datos.pausar_menu()
    return habitaciones_lista