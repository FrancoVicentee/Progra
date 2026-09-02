from paquete_2 import val_datos

def alta_reserva(reservas_lista, clientes_lista, habitaciones_lista):

    print("\n--- Alta de reserva ---")

    if len(clientes_lista) == 0 or len(habitaciones_lista) == 0:
        print("Debe existir al menos un cliente y una habitación registrados para crear una reserva.")
        return reservas_lista

    nuevo_id = reservas_lista[-1][0] + 1 if len(reservas_lista) > 0 else 1

    id_cliente = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, clientes_lista[-1][0])
    while val_datos.existe_id(clientes_lista, id_cliente) == False:
        print("No existe un cliente con ese ID.")
        id_cliente = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, clientes_lista[-1][0])

    id_hab = val_datos.pedir_entero_rango("Ingrese el ID de la habitación: ", 1, habitaciones_lista[-1][0])
    while val_datos.existe_id(habitaciones_lista, id_hab) == False:
        print("No existe una habitación con ese ID.")
        id_hab = val_datos.pedir_entero_rango("Ingrese el ID de la habitación: ", 1, habitaciones_lista[-1][0])

    fecha_ingreso, fecha_egreso = pedir_fechas_reserva(reservas_lista, id_cliente, id_hab, -1)

    reservas_lista.append([nuevo_id, id_cliente, id_hab, fecha_ingreso, fecha_egreso])
    print("Reserva agregada correctamente.")
    return reservas_lista


def listar_reservas(reservas_lista):

    print("\n--- Listado de reservas ---")
    if len(reservas_lista) == 0:
        print("No hay reservas registradas.")
    else:
        print(f"{'ID':<5}{'Id_cliente':<12}{'Id_hab':<10}{'Ingreso':<15}{'Egreso':<15}")
        for reserva in reservas_lista:
            print(
                f"{reserva[0]:<5}{reserva[1]:<12}{reserva[2]:<10}"
                f"{reserva[3]:<15}{reserva[4]:<15}"
            )
    return reservas_lista


def buscar_reserva_por_id(reservas_lista, id_reserva):

    encontrado = False
    reserva_encontrada = []
    for reserva in reservas_lista:
        if reserva[0] == id_reserva:
            encontrado = True
            reserva_encontrada = reserva
    return encontrado, reserva_encontrada


def existe_solapamiento(reservas_lista, indice_columna, id_valor, fecha_ingreso, fecha_egreso, id_reserva_excluida):
 
    ingreso_nuevo = val_datos.convertir_fecha_a_numero(fecha_ingreso)
    
    egreso_nuevo = val_datos.convertir_fecha_a_numero(fecha_egreso)

    hay_solapamiento = False

    for reserva in reservas_lista:
        if reserva[indice_columna] == id_valor and reserva[0] != id_reserva_excluida:
            ingreso_existente = val_datos.convertir_fecha_a_numero(reserva[3])
            egreso_existente = val_datos.convertir_fecha_a_numero(reserva[4])
            if ingreso_nuevo < egreso_existente and ingreso_existente < egreso_nuevo:
                hay_solapamiento = True

    return hay_solapamiento


def pedir_fechas_reserva(reservas_lista, id_cliente, id_hab, id_reserva_excluida):

    fechas_validas = False
    fecha_ingreso = ""
    fecha_egreso = ""

    while fechas_validas == False:
        fecha_ingreso = val_datos.pedir_fecha_valida("Ingrese la fecha de ingreso (dd/mm/aaaa): ")
        fecha_egreso = val_datos.pedir_fecha_valida("Ingrese la fecha de egreso (dd/mm/aaaa): ")

        if val_datos.comparar_fechas(fecha_egreso, fecha_ingreso) != 1:
            print("Error. La fecha de egreso debe ser posterior a la fecha de ingreso.")
        elif existe_solapamiento(reservas_lista, 1, id_cliente, fecha_ingreso, fecha_egreso, id_reserva_excluida):
            print("Error. El cliente ya tiene una reserva registrada que se superpone con esas fechas.")
        elif existe_solapamiento(reservas_lista, 2, id_hab, fecha_ingreso, fecha_egreso, id_reserva_excluida):
            print("Error. La habitación ya tiene una reserva registrada que se superpone con esas fechas.")
        else:
            fechas_validas = True

    return [fecha_ingreso, fecha_egreso]


def baja_reserva(reservas_lista):

    print("\n--- Baja de reserva ---")
    if len(reservas_lista) == 0:
        print("No hay reservas registradas.")
        return reservas_lista

    listar_reservas(reservas_lista)
    id_reserva = val_datos.pedir_entero_rango(
        "Ingrese el ID de la reserva a eliminar: ", 1, reservas_lista[-1][0]
    )
    encontrado, reserva = buscar_reserva_por_id(reservas_lista, id_reserva)

    if encontrado:
        reservas_lista.remove(reserva)
        print("Reserva eliminada correctamente.")
    else:
        print("No existe una reserva con ese ID.")
    return reservas_lista


def modificar_reserva(reservas_lista, clientes_lista, habitaciones_lista):
 
    print("\n--- Modificación de reserva ---")
    if len(reservas_lista) == 0:
        print("No hay reservas registradas.")
        return reservas_lista

    listar_reservas(reservas_lista)

    id_reserva = val_datos.pedir_entero_rango(
        "Ingrese el ID de la reserva a modificar: ", 1, reservas_lista[-1][0]
    )
    encontrado, reserva = buscar_reserva_por_id(reservas_lista, id_reserva)

    if encontrado:
        id_cliente = val_datos.pedir_entero_rango("Ingrese el nuevo ID de cliente: ", 1, clientes_lista[-1][0])
        while val_datos.existe_id(clientes_lista, id_cliente) == False:
            print("No existe un cliente con ese ID.")
            id_cliente = val_datos.pedir_entero_rango("Ingrese el nuevo ID de cliente: ", 1, clientes_lista[-1][0])

        id_hab = val_datos.pedir_entero_rango("Ingrese el nuevo ID de habitación: ", 1, habitaciones_lista[-1][0])
        while val_datos.existe_id(habitaciones_lista, id_hab) == False:
            print("No existe una habitación con ese ID.")
            id_hab = val_datos.pedir_entero_rango("Ingrese el nuevo ID de habitación: ", 1, habitaciones_lista[-1][0])

        reserva[1] = id_cliente
        reserva[2] = id_hab
        fecha_ingreso, fecha_egreso = pedir_fechas_reserva(reservas_lista, id_cliente, id_hab, id_reserva)
        reserva[3] = fecha_ingreso
        reserva[4] = fecha_egreso
        print("Reserva modificada correctamente.")
    else:
        print("No existe una reserva con ese ID.")
    return reservas_lista


def menu_reservas(reservas_lista, clientes_lista, habitaciones_lista):

    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE RESERVAS")
        print("---------------------------")
        print("[1] Alta de reserva")
        print("[2] Listar reservas")
        print("[3] Baja de reserva")
        print("[4] Modificar reserva")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        if opcion == 1:
            reservas_lista = alta_reserva(reservas_lista, clientes_lista, habitaciones_lista)
        elif opcion == 2:
            reservas_lista = listar_reservas(reservas_lista)
        elif opcion == 3:
            reservas_lista = baja_reserva(reservas_lista)
        elif opcion == 4:
            reservas_lista = modificar_reserva(reservas_lista, clientes_lista, habitaciones_lista)

    return reservas_lista