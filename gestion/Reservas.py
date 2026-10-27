from utilidades import val_datos, archivos


RUTA_RESERVAS = "datos/reservas.txt"
RUTA_CLIENTES = "datos/clientes.txt"
RUTA_HABITACIONES = "datos/habitaciones.txt"
COLUMNAS_RESERVAS = [0, 1, 2]
COLUMNAS_CLIENTES = [0, 3]
COLUMNAS_HABITACIONES = [0, 1, 3]


def obtener_reservas_por_cliente(reservas_lista, id_cliente):
    """
    Devuelve una lista con todas las reservas del archivo asociadas al cliente indicado, usando filter y lambda.
    El parametro reservas_lista se mantiene para no romper las llamadas de Clientes.py, pero ya no se usa.
    """

    reservas_archivo = archivos.cargar_matriz(RUTA_RESERVAS, COLUMNAS_RESERVAS)
    return list(filter(lambda reserva: reserva[1] == id_cliente, reservas_archivo))


def obtener_reservas_por_habitacion(reservas_lista, id_habitacion):
    """Devuelve una lista con todas las reservas asociadas a la habitacion indicada, usando filter y lambda."""

    return list(filter(lambda reserva: reserva[2] == id_habitacion, reservas_lista))


def mostrar_reservas_detalladas(reservas_a_mostrar, clientes_lista, habitaciones_lista):
    """
    Imprime en formato de tabla las reservas recibidas, reemplazando los IDs de cliente y habitacion
    por el nombre del cliente y el numero/tipo de la habitacion. Tambien muestra las noches de cada reserva.
    """

    print(f"{'ID':<5}{'Cliente':<22}{'Hab.':<6}{'Tipo':<8}{'Ingreso':<12}{'Egreso':<12}{'Noches':<6}")
    print("-" * 71)

    for reserva in reservas_a_mostrar:
        cliente = archivos.buscar_registro(RUTA_CLIENTES, reserva[1], COLUMNAS_CLIENTES)
        habitacion = archivos.buscar_registro(RUTA_HABITACIONES, reserva[2], COLUMNAS_HABITACIONES)

        nombre_cliente = "(sin datos)"
        if len(cliente) > 0:
            nombre_cliente = f"{cliente[1]} {cliente[2]}"

        numero_hab = "-"
        tipo_hab = "-"
        if len(habitacion) > 0:
            numero_hab = habitacion[1]
            tipo_hab = habitacion[2]

        noches = val_datos.calcular_noches(reserva[3], reserva[4])

        # Se recorta el nombre con slicing para no romper la alineacion de la tabla.
        print(f"{reserva[0]:<5}{nombre_cliente[:21]:<22}{numero_hab:<6}{tipo_hab:<8}"
              f"{reserva[3]:<12}{reserva[4]:<12}{noches:<6}")


def alta_reserva(reservas_lista, clientes_lista, habitaciones_lista):
    """
    Registra una nueva reserva en el archivo de reservas. Valida que el cliente y la habitacion
    existan en sus archivos y que las fechas no se superpongan con otra reserva del mismo cliente
    o de la misma habitacion. El ID nuevo se calcula leyendo el archivo.
    """

    val_datos.imprimir_titulo("Alta de reserva")

    hay_clientes = len(archivos.cargar_matriz(RUTA_CLIENTES, COLUMNAS_CLIENTES)) > 0
    hay_habitaciones = len(archivos.cargar_matriz(RUTA_HABITACIONES, COLUMNAS_HABITACIONES)) > 0
    if hay_clientes == False or hay_habitaciones == False:
        val_datos.imprimir_error("Debe existir al menos un cliente y una habitación registrados para crear una reserva.")
        return reservas_lista

    id_cliente = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, 1000)
    while len(archivos.buscar_registro(RUTA_CLIENTES, id_cliente, COLUMNAS_CLIENTES)) == 0:
        val_datos.imprimir_error("No existe un cliente con ese ID.")
        id_cliente = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, 1000)

    id_hab = val_datos.pedir_entero_rango("Ingrese el ID de la habitación: ", 1, 1000)
    while len(archivos.buscar_registro(RUTA_HABITACIONES, id_hab, COLUMNAS_HABITACIONES)) == 0:
        val_datos.imprimir_error("No existe una habitación con ese ID.")
        id_hab = val_datos.pedir_entero_rango("Ingrese el ID de la habitación: ", 1, 1000)

    fecha_ingreso, fecha_egreso = pedir_fechas_reserva(id_cliente, id_hab, -1)

    nuevo_id = archivos.obtener_proximo_id(RUTA_RESERVAS, COLUMNAS_RESERVAS)
    if archivos.agregar_registro(RUTA_RESERVAS, [nuevo_id, id_cliente, id_hab, fecha_ingreso, fecha_egreso]):
        val_datos.imprimir_exito(f"Reserva agregada correctamente con ID {nuevo_id}.")
    return reservas_lista


def listar_reservas(reservas_lista, clientes_lista, habitaciones_lista):
    """Imprime todas las reservas registradas, leyendolas del archivo, con los datos del cliente y de la habitacion."""

    val_datos.imprimir_titulo("Listado de reservas")
    reservas_archivo = archivos.cargar_matriz(RUTA_RESERVAS, COLUMNAS_RESERVAS)
    if len(reservas_archivo) == 0:
        print("No hay reservas registradas.")
    else:
        mostrar_reservas_detalladas(reservas_archivo, clientes_lista, habitaciones_lista)
        print(f"\nCantidad total de reservas: {len(reservas_archivo)}")
    return reservas_lista


def buscar_reserva_por_id(reservas_lista, id_reserva):
    """
    Busca una reserva por su ID en el archivo de reservas. Devuelve una tupla (encontrado, reserva):
    encontrado es True/False y reserva es la fila encontrada (o una lista vacia).
    """

    reserva = archivos.buscar_registro(RUTA_RESERVAS, id_reserva, COLUMNAS_RESERVAS)
    return len(reserva) > 0, reserva


def existe_solapamiento(indice_columna, id_valor, fecha_ingreso, fecha_egreso, id_reserva_excluida, ruta=RUTA_RESERVAS):
    """
    Se fija si las fechas nuevas se cruzan con una reserva que ya existe en el archivo de reservas.
    Lee el archivo de a una linea. Sirve tanto para chequear el cliente como la habitacion, dependiendo
    que columna se le pase (1 para cliente, 2 para habitacion). La reserva con id_reserva_excluida no se
    cuenta, asi al modificar una reserva no choca consigo misma. Si el archivo no existe, no hay solapamiento.
    Devuelve True si se superponen las fechas, False si no.
    """

    ingreso_nuevo = val_datos.convertir_fecha_a_numero(fecha_ingreso)
    egreso_nuevo = val_datos.convertir_fecha_a_numero(fecha_egreso)

    hay_solapamiento = False

    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "" and hay_solapamiento == False:
            reserva = archivos.leer_registro_de_linea(linea, COLUMNAS_RESERVAS)
            if len(reserva) == 5 and reserva[indice_columna] == id_valor and reserva[0] != id_reserva_excluida:
                ingreso_existente = val_datos.convertir_fecha_a_numero(reserva[3])
                egreso_existente = val_datos.convertir_fecha_a_numero(reserva[4])
                if ingreso_nuevo < egreso_existente and ingreso_existente < egreso_nuevo:
                    hay_solapamiento = True
            linea = arch.readline()
    except FileNotFoundError:
        # Si el archivo todavia no existe, no hay reservas con las que chocar.
        pass
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return hay_solapamiento


def pedir_fechas_reserva(id_cliente, id_hab, id_reserva_excluida):
    """
    Pide la fecha de ingreso y egreso y no deja seguir hasta que sean
    validas, osea que el egreso sea despues del ingreso y que no se pisen
    con otra reserva del archivo del mismo cliente o la misma habitacion.
    Devuelve una tupla (fecha_ingreso, fecha_egreso).
    """

    fechas_validas = False
    fecha_ingreso = ""
    fecha_egreso = ""

    while fechas_validas == False:
        fecha_ingreso = val_datos.pedir_fecha_valida("Ingrese la fecha de ingreso (dd/mm/aaaa): ")
        fecha_egreso = val_datos.pedir_fecha_valida("Ingrese la fecha de egreso (dd/mm/aaaa): ")

        if val_datos.comparar_fechas(fecha_egreso, fecha_ingreso) != 1:
            val_datos.imprimir_error("Error. La fecha de egreso debe ser posterior a la fecha de ingreso.")
        elif existe_solapamiento(1, id_cliente, fecha_ingreso, fecha_egreso, id_reserva_excluida):
            val_datos.imprimir_error("Error. El cliente ya tiene una reserva registrada que se superpone con esas fechas.")
        elif existe_solapamiento(2, id_hab, fecha_ingreso, fecha_egreso, id_reserva_excluida):
            val_datos.imprimir_error("Error. La habitación ya tiene una reserva registrada que se superpone con esas fechas.")
        else:
            fechas_validas = True

    return fecha_ingreso, fecha_egreso


def baja_reserva(reservas_lista, clientes_lista, habitaciones_lista):
    """Muestra las reservas del archivo, pide el ID de la que se quiere eliminar y la elimina previa confirmacion."""

    val_datos.imprimir_titulo("Baja de reserva")
    reservas_archivo = archivos.cargar_matriz(RUTA_RESERVAS, COLUMNAS_RESERVAS)
    if len(reservas_archivo) == 0:
        print("No hay reservas registradas.")
        return reservas_lista

    mostrar_reservas_detalladas(reservas_archivo, clientes_lista, habitaciones_lista)
    id_reserva = val_datos.pedir_entero_rango("\nIngrese el ID de la reserva: ", 1, 1000)
    encontrado = buscar_reserva_por_id(reservas_lista, id_reserva)[0]

    if encontrado:
        if val_datos.pedir_confirmacion(f"¿Confirma la baja de la reserva {id_reserva}?"):
            if archivos.reemplazar_registro(RUTA_RESERVAS, id_reserva, None, COLUMNAS_RESERVAS):
                val_datos.imprimir_exito("Reserva eliminada correctamente.")
        else:
            print("Operación cancelada.")
    else:
        val_datos.imprimir_error("No existe una reserva con ese ID.")
    return reservas_lista


def modificar_reserva(reservas_lista, clientes_lista, habitaciones_lista):
    """
    Permite modificar cliente, habitacion y fechas de una reserva del archivo. Los campos que se dejan vacios
    no se modifican. Los cambios solo se guardan si las nuevas fechas son validas y no se superponen.
    """

    val_datos.imprimir_titulo("Modificación de reserva")
    reservas_archivo = archivos.cargar_matriz(RUTA_RESERVAS, COLUMNAS_RESERVAS)
    if len(reservas_archivo) == 0:
        print("No hay reservas registradas.")
        return reservas_lista

    mostrar_reservas_detalladas(reservas_archivo, clientes_lista, habitaciones_lista)

    id_reserva = val_datos.pedir_entero_rango("\nIngrese el ID de la reserva: ", 1, 1000)
    encontrado, reserva = buscar_reserva_por_id(reservas_lista, id_reserva)

    if encontrado:
        print("Deje vacío el campo si no desea modificarlo.")

        id_cliente_nuevo = reserva[1]
        entrada_cliente = input(f"ID de cliente ({reserva[1]}): ").strip()
        if entrada_cliente != "":
            while (val_datos.es_entero(entrada_cliente) == False
                   or len(archivos.buscar_registro(RUTA_CLIENTES, int(entrada_cliente), COLUMNAS_CLIENTES)) == 0):
                val_datos.imprimir_error("Error. Debe ingresar un ID de cliente existente.")
                entrada_cliente = input(f"ID de cliente ({reserva[1]}): ").strip()
            id_cliente_nuevo = int(entrada_cliente)

        id_hab_nuevo = reserva[2]
        entrada_hab = input(f"ID de habitación ({reserva[2]}): ").strip()
        if entrada_hab != "":
            while (val_datos.es_entero(entrada_hab) == False
                   or len(archivos.buscar_registro(RUTA_HABITACIONES, int(entrada_hab), COLUMNAS_HABITACIONES)) == 0):
                val_datos.imprimir_error("Error. Debe ingresar un ID de habitación existente.")
                entrada_hab = input(f"ID de habitación ({reserva[2]}): ").strip()
            id_hab_nuevo = int(entrada_hab)

        fecha_ingreso_nueva = reserva[3]
        entrada_ingreso = input(f"Fecha de ingreso ({reserva[3]}): ").strip()
        if entrada_ingreso != "":
            while val_datos.validar_fecha(entrada_ingreso) == False:
                val_datos.imprimir_error("Error. Fecha inválida. Use el formato dd/mm/aaaa con una fecha existente.")
                entrada_ingreso = input(f"Fecha de ingreso ({reserva[3]}): ").strip()
            fecha_ingreso_nueva = entrada_ingreso

        fecha_egreso_nueva = reserva[4]
        entrada_egreso = input(f"Fecha de egreso ({reserva[4]}): ").strip()
        if entrada_egreso != "":
            while val_datos.validar_fecha(entrada_egreso) == False:
                val_datos.imprimir_error("Error. Fecha inválida. Use el formato dd/mm/aaaa con una fecha existente.")
                entrada_egreso = input(f"Fecha de egreso ({reserva[4]}): ").strip()
            fecha_egreso_nueva = entrada_egreso

        if val_datos.comparar_fechas(fecha_egreso_nueva, fecha_ingreso_nueva) != 1:
            val_datos.imprimir_error("Error. La fecha de egreso debe ser posterior al ingreso. No se modificó la reserva.")
        elif existe_solapamiento(1, id_cliente_nuevo, fecha_ingreso_nueva, fecha_egreso_nueva, id_reserva):
            val_datos.imprimir_error("Error. El cliente ya tiene una reserva que se superpone con esas fechas. No se modificó la reserva.")
        elif existe_solapamiento(2, id_hab_nuevo, fecha_ingreso_nueva, fecha_egreso_nueva, id_reserva):
            val_datos.imprimir_error("Error. La habitación ya tiene una reserva que se superpone con esas fechas. No se modificó la reserva.")
        else:
            reserva_nueva = [id_reserva, id_cliente_nuevo, id_hab_nuevo, fecha_ingreso_nueva, fecha_egreso_nueva]
            if archivos.reemplazar_registro(RUTA_RESERVAS, id_reserva, reserva_nueva, COLUMNAS_RESERVAS):
                val_datos.imprimir_exito("Reserva modificada correctamente.")
    else:
        val_datos.imprimir_error("No existe una reserva con ese ID.")
    return reservas_lista


def info_reservas(reservas_lista, clientes_lista, habitaciones_lista):
    """Consulta una reserva por ID y muestra su informacion completa junto con los datos del cliente y la habitacion."""

    val_datos.imprimir_titulo("Información completa de reserva")
    if len(archivos.cargar_matriz(RUTA_RESERVAS, COLUMNAS_RESERVAS)) == 0:
        print("No hay reservas registradas.")
        return reservas_lista

    id_consulta = val_datos.pedir_entero_rango("Ingrese el ID de la reserva: ", 1, 1000)
    encontrado, reserva = buscar_reserva_por_id(reservas_lista, id_consulta)

    if encontrado == False:
        val_datos.imprimir_error("No existe una reserva con ese ID.")
    else:
        cliente = archivos.buscar_registro(RUTA_CLIENTES, reserva[1], COLUMNAS_CLIENTES)
        habitacion = archivos.buscar_registro(RUTA_HABITACIONES, reserva[2], COLUMNAS_HABITACIONES)

        print(f"ID de reserva: {reserva[0]}")
        if len(cliente) > 0:
            print(f"Cliente:       {cliente[1]} {cliente[2]} (ID {cliente[0]} - DNI {cliente[3]})")
        if len(habitacion) > 0:
            print(f"Habitación:    {habitacion[1]} - {habitacion[2]} - capacidad {habitacion[3]} - {habitacion[4]}")
        print(f"Ingreso:       {reserva[3]}")
        print(f"Egreso:        {reserva[4]}")
        print(f"Noches:        {val_datos.calcular_noches(reserva[3], reserva[4])}")

    val_datos.pausar_menu()
    return reservas_lista


def menu_reservas(reservas_lista, clientes_lista, habitaciones_lista):
    """
    Menu principal para gestionar las reservas.
    """
    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Reservas "
        print(f"\n{titulo:-^50}")
        print("[1] Alta de reserva")
        print("[2] Listar reservas")
        print("[3] Baja de reserva")
        print("[4] Modificar reserva")
        print("[5] Consultar información por reserva")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                reservas_lista = alta_reserva(reservas_lista, clientes_lista, habitaciones_lista)
            case 2:
                reservas_lista = listar_reservas(reservas_lista, clientes_lista, habitaciones_lista)
                val_datos.pausar_menu()
            case 3:
                reservas_lista = baja_reserva(reservas_lista, clientes_lista, habitaciones_lista)
            case 4:
                reservas_lista = modificar_reserva(reservas_lista, clientes_lista, habitaciones_lista)
            case 5:
                reservas_lista = info_reservas(reservas_lista, clientes_lista, habitaciones_lista)
            case 0:
                print("Saliendo del menú de reservas...")

    return reservas_lista
