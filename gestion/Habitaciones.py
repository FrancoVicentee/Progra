from utilidades import val_datos
from gestion import Reservas


def alta_habitacion(habitaciones_lista):
    """Solicita los datos validados al usuario y registra una nueva habitación en el sistema."""

    val_datos.imprimir_titulo("Alta de habitaciones")

    numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
    while existe_numero_habitacion(habitaciones_lista, numero):
        val_datos.imprimir_error("Error. Ya existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)

    tipo = val_datos.pedir_tipo_habitacion("Ingrese el tipo de habitación (Simple/Doble/Suite): ")

    capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo)
    capacidad = val_datos.pedir_entero_rango(
        f"Ingrese la capacidad de la habitación ({capacidad_minima}-{capacidad_maxima}): ",
        capacidad_minima, capacidad_maxima
    )

    estado = val_datos.pedir_estado_habitacion("Ingrese el estado de la habitación (Disponible/Ocupada/Mantenimiento): ")

    id_nuevo = val_datos.generar_id(habitaciones_lista)

    habitacion_nueva = [id_nuevo, numero, tipo, capacidad, estado]
    habitaciones_lista.append(habitacion_nueva)

    val_datos.imprimir_exito(f"Habitación agregada correctamente con ID {id_nuevo}.")

    return habitaciones_lista


def mostrar_encabezado_habitaciones():
    """Imprime el encabezado de la tabla de habitaciones."""

    print(f"{'ID':<5}{'Número':<10}{'Tipo':<12}{'Capacidad':<12}{'Estado':<15}")
    print("-" * 54)


def mostrar_habitacion(habitacion):
    """Imprime una fila de la tabla de habitaciones con los datos de la habitacion recibida."""

    id_habitacion = habitacion[0]
    numero_habitacion = habitacion[1]
    tipo_habitacion = habitacion[2]
    capacidad_habitacion = habitacion[3]
    estado_habitacion = habitacion[4]

    print(f"{id_habitacion:<5}{numero_habitacion:<10}{tipo_habitacion:<12}{capacidad_habitacion:<12}{estado_habitacion:<15}")


def listar_habitaciones(habitaciones_lista):
    """Imprime en pantalla todas las habitaciones registradas con formato de tabla."""

    val_datos.imprimir_titulo("Listado de habitaciones")

    cantidad_habitaciones = len(habitaciones_lista)

    if cantidad_habitaciones == 0:
        print("No hay habitaciones cargadas.")
    else:
        mostrar_encabezado_habitaciones()

        indice = 0
        while indice < cantidad_habitaciones:
            mostrar_habitacion(habitaciones_lista[indice])
            indice += 1

        print("-" * 54)
        print(f"Cantidad total de habitaciones: {cantidad_habitaciones}")

    val_datos.pausar_menu()
    return habitaciones_lista


def pedir_numero_existente(habitaciones_lista, mensaje):
    """Pide un numero de habitacion hasta que corresponda a una habitacion cargada y devuelve su posicion en la matriz."""

    numero = val_datos.pedir_entero_rango(mensaje, 100, 999)
    posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

    while posicion == -1:
        val_datos.imprimir_error("Error. No existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango(mensaje, 100, 999)
        posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

    return posicion


def baja_habitacion(habitaciones_lista, reservas_lista, clientes_lista):
    """
    Da de baja una habitacion previa confirmacion. Para mantener la integridad referencial,
    no permite eliminar una habitacion que tenga reservas asociadas (se muestran para que el usuario las elimine primero).
    """

    val_datos.imprimir_titulo("Baja de habitación")

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    posicion = pedir_numero_existente(habitaciones_lista, "Ingrese el número de la habitación a dar de baja: ")
    habitacion = habitaciones_lista[posicion]

    reservas_de_la_habitacion = Reservas.obtener_reservas_por_habitacion(reservas_lista, habitacion[0])

    if len(reservas_de_la_habitacion) > 0:
        val_datos.imprimir_error(f"No se puede dar de baja la habitación {habitacion[1]}: "
                                 f"tiene {len(reservas_de_la_habitacion)} reserva(s) asociada(s).")
        print("Elimine primero estas reservas desde el menú de reservas:\n")
        Reservas.mostrar_reservas_detalladas(reservas_de_la_habitacion, clientes_lista, habitaciones_lista)
    else:
        print("\nSe encontró la siguiente habitación:")
        mostrar_encabezado_habitaciones()
        mostrar_habitacion(habitacion)

        if val_datos.pedir_confirmacion("¿Confirma la baja?"):
            habitaciones_lista.pop(posicion)
            val_datos.imprimir_exito("Habitación eliminada correctamente.")
        else:
            print("Operación cancelada. La habitación no fue eliminada.")

    return habitaciones_lista


def modificar_habitacion(habitaciones_lista):
    """
    Permite modificar numero, tipo, capacidad y estado de una habitacion. Los campos que se dejan vacios
    no se modifican. Si cambia el tipo, se controla que la capacidad siga siendo valida para el nuevo tipo.
    """

    val_datos.imprimir_titulo("Modificación de habitación")

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    posicion = pedir_numero_existente(habitaciones_lista, "Ingrese el número de la habitación a modificar: ")
    habitacion = habitaciones_lista[posicion]

    print("\nSe encontró la siguiente habitación:")
    mostrar_encabezado_habitaciones()
    mostrar_habitacion(habitacion)

    print("\nDeje vacío el campo si no desea modificarlo.")

    entrada_numero = input(f"Número ({habitacion[1]}): ").strip()
    if entrada_numero != "":
        while (val_datos.es_entero_en_rango(entrada_numero, 100, 999) == False
               or existe_numero_en_otra_posicion(habitaciones_lista, int(entrada_numero), posicion)):
            val_datos.imprimir_error("Error. Ingrese un número entre 100 y 999 que no esté en uso.")
            entrada_numero = input(f"Número ({habitacion[1]}): ").strip()
        habitacion[1] = int(entrada_numero)

    entrada_tipo = input(f"Tipo ({habitacion[2]}): ").strip()
    if entrada_tipo != "":
        while val_datos.es_tipo_valido(entrada_tipo) == False:
            val_datos.imprimir_error("Error. Debe ingresar Simple, Doble o Suite.")
            entrada_tipo = input(f"Tipo ({habitacion[2]}): ")
        habitacion[2] = val_datos.normalizar_capitalizado(entrada_tipo)

    capacidad_minima, capacidad_maxima = obtener_rango_capacidad(habitacion[2])
    capacidad_actual = habitacion[3]
    mensaje_capacidad = f"Capacidad ({capacidad_actual}, rango {capacidad_minima}-{capacidad_maxima}): "
    entrada_capacidad = input(mensaje_capacidad).strip()
    if entrada_capacidad != "":
        while val_datos.es_entero_en_rango(entrada_capacidad, capacidad_minima, capacidad_maxima) == False:
            val_datos.imprimir_error(f"Error. Ingrese un valor entre {capacidad_minima} y {capacidad_maxima}.")
            entrada_capacidad = input(mensaje_capacidad).strip()
        habitacion[3] = int(entrada_capacidad)
    elif capacidad_actual < capacidad_minima or capacidad_actual > capacidad_maxima:
        val_datos.imprimir_error(f"La capacidad actual ({capacidad_actual}) no es válida para el tipo {habitacion[2]}.")
        habitacion[3] = val_datos.pedir_entero_rango(f"Ingrese la nueva capacidad ({capacidad_minima}-{capacidad_maxima}): ",
                                                     capacidad_minima, capacidad_maxima)

    entrada_estado = input(f"Estado ({habitacion[4]}): ").strip()
    if entrada_estado != "":
        while val_datos.es_estado_valido(entrada_estado) == False:
            val_datos.imprimir_error("Error. Debe ingresar Disponible, Ocupada o Mantenimiento.")
            entrada_estado = input(f"Estado ({habitacion[4]}): ")
        habitacion[4] = val_datos.normalizar_capitalizado(entrada_estado)

    val_datos.imprimir_exito("Habitación modificada correctamente.")

    print("\nLa habitación quedó así:")
    mostrar_encabezado_habitaciones()
    mostrar_habitacion(habitacion)

    return habitaciones_lista


def consultar_habitacion(habitaciones_lista, reservas_lista, clientes_lista):
    """
    Consulta una habitacion por numero y muestra sus datos junto con su historial de reservas
    (cliente, fechas y noches), ademas del total de noches reservadas.
    """

    val_datos.imprimir_titulo("Consultar habitación")

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación: ", 100, 999)
    posicion = buscar_posicion_por_numero(habitaciones_lista, numero)

    if posicion == -1:
        val_datos.imprimir_error("No existe una habitación con ese número.")
    else:
        habitacion = habitaciones_lista[posicion]
        mostrar_encabezado_habitaciones()
        mostrar_habitacion(habitacion)

        reservas_de_la_habitacion = Reservas.obtener_reservas_por_habitacion(reservas_lista, habitacion[0])

        print(f"\nHistorial de reservas de la habitación {habitacion[1]}:")
        if len(reservas_de_la_habitacion) == 0:
            print("La habitación no tiene reservas registradas.")
        else:
            Reservas.mostrar_reservas_detalladas(reservas_de_la_habitacion, clientes_lista, habitaciones_lista)
            noches = [val_datos.calcular_noches(reserva[3], reserva[4]) for reserva in reservas_de_la_habitacion]
            print(f"\nTotal de reservas: {len(reservas_de_la_habitacion)} | Total de noches reservadas: {sum(noches)}")

    val_datos.pausar_menu()
    return habitaciones_lista


def existe_numero_habitacion(habitaciones_lista, numero):
    """Devuelve True si ya existe una habitacion con el numero indicado."""

    return buscar_posicion_por_numero(habitaciones_lista, numero) != -1


def existe_numero_en_otra_posicion(habitaciones_lista, numero, posicion_actual):
    """Devuelve True si el numero ya lo usa una habitacion distinta a la que esta en posicion_actual."""

    posicion = buscar_posicion_por_numero(habitaciones_lista, numero)
    return posicion != -1 and posicion != posicion_actual


def buscar_posicion_por_numero(habitaciones_lista, numero):
    """Devuelve la posicion en la matriz de la habitacion con el numero indicado, o -1 si no existe."""

    posicion = -1
    indice = 0
    for habitacion in habitaciones_lista:
        if habitacion[1] == numero:
            posicion = indice
        indice += 1
    return posicion


def obtener_rango_capacidad(tipo):
    """Devuelve una tupla (capacidad_minima, capacidad_maxima) permitida para el tipo de habitacion."""

    return val_datos.RANGOS_CAPACIDAD[tipo]


def menu_habitaciones(habitaciones_lista, reservas_lista, clientes_lista):
    """
    Menu principal para gestionar las habitaciones.
    """

    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Habitaciones "
        print(f"\n{titulo:-^50}")
        print("[1] Alta de habitación")
        print("[2] Listar habitaciones")
        print("[3] Baja de habitación")
        print("[4] Modificar habitación")
        print("[5] Consultar habitación e historial de reservas")
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
                habitaciones_lista = baja_habitacion(habitaciones_lista, reservas_lista, clientes_lista)
            case 4:
                habitaciones_lista = modificar_habitacion(habitaciones_lista)
            case 5:
                habitaciones_lista = consultar_habitacion(habitaciones_lista, reservas_lista, clientes_lista)
            case 0:
                print("Volviendo al menú anterior...")

    return habitaciones_lista
