from paquete_2 import val_datos
 
def menu_habitaciones(habitaciones_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE HABITACIONES")
        print("---------------------------")
        print("[1] Alta de habitación")
        print("[2] Listar habitaciones")
        print("[3] Baja de habitación")
        print("[4] Modificar habitación")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")
 
        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)
 
        if opcion == 1:
            habitaciones_lista = alta_habitacion(habitaciones_lista)
        elif opcion == 2:
            habitaciones_lista = listar_habitaciones(habitaciones_lista)
        elif opcion == 3:
            habitaciones_lista = baja_habitacion(habitaciones_lista)
        elif opcion == 4:
            habitaciones_lista = modificar_habitacion(habitaciones_lista)
 
    return habitaciones_lista
 
 
def alta_habitacion(habitaciones_lista):
    print("\n---------------------------")
    print("ALTA DE HABITACIÓN")
    print("---------------------------")
 
    numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
 
    numero_existe = existe_numero_habitacion(habitaciones_lista, numero)
    while numero_existe == True:
        print("Error. Ya existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
        numero_existe = existe_numero_habitacion(habitaciones_lista, numero)
 
    tipo = input("Ingrese el tipo de habitación (Simple/Doble/Suite): ")
    while es_tipo_valido(tipo) == False:
        print("Error. Debe ingresar Simple, Doble o Suite.")
        tipo = input("Ingrese el tipo de habitación (Simple/Doble/Suite): ")
 
    capacidad = val_datos.pedir_entero_rango("Ingrese la capacidad de la habitación: ", 1, 10)
 
    estado = input("Ingrese el estado de la habitación (Disponible/Ocupada/Mantenimiento): ")
    while es_estado_valido(estado) == False:
        print("Error. Debe ingresar Disponible, Ocupada o Mantenimiento.")
        estado = input("Ingrese el estado de la habitación (Disponible/Ocupada/Mantenimiento): ")
 
    id_nuevo = generar_id_habitacion(habitaciones_lista)
 
    habitacion_nueva = [id_nuevo, numero, tipo, capacidad, estado]
    habitaciones_lista.append(habitacion_nueva)
 
    print("Habitación agregada correctamente.")
 
    return habitaciones_lista
 
 
def listar_habitaciones(habitaciones_lista):
    print("\n---------------------------")
    print("LISTADO DE HABITACIONES")
    print("---------------------------")
 
    cantidad_habitaciones = len(habitaciones_lista)
 
    if cantidad_habitaciones == 0:
        print("No hay habitaciones cargadas.")
    else:
        print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<12}{'Estado':<15}")
        print("---------------------------------------------------")
 
        indice = 0
        while indice < cantidad_habitaciones:
            habitacion_actual = habitaciones_lista[indice]
            mostrar_habitacion(habitacion_actual)
            indice += 1
 
        print("---------------------------------------------------")
        print(f"Cantidad total de habitaciones: {cantidad_habitaciones}")
 
        print("\n---------------------------")
        val_datos.pedir_entero_rango("Presione 0 para volver al menú de habitaciones: ", 0, 0)
 
    return habitaciones_lista
 
 
def baja_habitacion(habitaciones_lista):
    print("\n---------------------------")
    print("BAJA DE HABITACIÓN")
    print("---------------------------")
 
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
    print("\n---------------------------")
    print("MODIFICAR HABITACIÓN")
    print("---------------------------")
 
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
            tipo_nuevo = input("Ingrese el nuevo tipo (Simple/Doble/Suite): ")
            while es_tipo_valido(tipo_nuevo) == False:
                print("Error. Debe ingresar Simple, Doble o Suite.")
                tipo_nuevo = input("Ingrese el nuevo tipo (Simple/Doble/Suite): ")
 
            habitaciones_lista[posicion][2] = tipo_nuevo
            print("Tipo modificado correctamente.")
 
        elif opcion_modificar == 3:
            capacidad_nueva = val_datos.pedir_entero_rango("Ingrese la nueva capacidad: ", 1, 10)
 
            habitaciones_lista[posicion][3] = capacidad_nueva
            print("Capacidad modificada correctamente.")
 
        elif opcion_modificar == 4:
            estado_nuevo = input("Ingrese el nuevo estado (Disponible/Ocupada/Mantenimiento): ")
            while es_estado_valido(estado_nuevo) == False:
                print("Error. Debe ingresar Disponible, Ocupada o Mantenimiento.")
                estado_nuevo = input("Ingrese el nuevo estado (Disponible/Ocupada/Mantenimiento): ")
 
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
 
 
def es_tipo_valido(tipo):
    es_valido = False
    if tipo == "Simple" or tipo == "Doble" or tipo == "Suite":
        es_valido = True
    return es_valido
 
 
def es_estado_valido(estado):
    es_valido = False
    if estado == "Disponible" or estado == "Ocupada" or estado == "Mantenimiento":
        es_valido = True
    return es_valido
 
 
def generar_id_habitacion(habitaciones_lista):
    if len(habitaciones_lista) == 0:
        id_nuevo = 1
    else:
        id_maximo = habitaciones_lista[0][0]
        for habitacion in habitaciones_lista:
            if habitacion[0] > id_maximo:
                id_maximo = habitacion[0]
        id_nuevo = id_maximo + 1
 
    return id_nuevo