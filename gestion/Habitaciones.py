from utilidades import val_datos, archivos
from gestion import Reservas

RUTA_HABITACIONES = "datos/habitaciones.txt"
COLUMNAS_HABITACIONES = [0, 1, 3]


def alta_habitacion(habitaciones_lista):
    """Solicita los datos validados al usuario y registra una nueva habitación en el sistema."""

    val_datos.imprimir_titulo("Alta de habitaciones")

    numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)
    while archivos.existe_valor(RUTA_HABITACIONES, 1, numero, -1, COLUMNAS_HABITACIONES):
        val_datos.imprimir_error("Error. Ya existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango("Ingrese el número de habitación: ", 100, 999)

    tipo = val_datos.pedir_tipo_habitacion("Ingrese el tipo de habitación (Simple/Doble/Suite): ")

    capacidad_minima, capacidad_maxima = obtener_rango_capacidad(tipo)
    capacidad = val_datos.pedir_entero_rango(
        f"Ingrese la capacidad de la habitación ({capacidad_minima}-{capacidad_maxima}): ",
        capacidad_minima, capacidad_maxima
    )

    estado = val_datos.pedir_estado_habitacion("Ingrese el estado de la habitación (Disponible/Ocupada/Mantenimiento): ")

    id_nuevo = archivos.obtener_proximo_id(RUTA_HABITACIONES, COLUMNAS_HABITACIONES)

    habitacion_nueva = [id_nuevo, numero, tipo, capacidad, estado]
    if archivos.agregar_registro(RUTA_HABITACIONES, habitacion_nueva):
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

def imprimir_habitaciones_recursivo(arch):
    """
    Imprime las habitaciones del archivo y devuelve cuantas hay.
    Caso base: readline() devuelve "" (fin del archivo) y devuelve 0.
    Caso recursivo: lee una linea, la imprime y se llama de nuevo con el mismo archivo.
    Reduccion del dominio: el cursor avanza una linea por llamada, asi queda una linea menos por leer.
    """

    linea = arch.readline()
    if linea == "":
        return 0
    registro = archivos.leer_registro_de_linea(linea, COLUMNAS_HABITACIONES)
    if len(registro) == 0:
        return imprimir_habitaciones_recursivo(arch)
    mostrar_habitacion(registro)
    return 1 + imprimir_habitaciones_recursivo(arch)


def listar_habitaciones(habitaciones_lista):
    """Imprime en pantalla todas las habitaciones del archivo con formato de tabla (lectura recursiva)."""

    val_datos.imprimir_titulo("Listado de habitaciones")

    try:
        arch = open(RUTA_HABITACIONES, "rt", encoding="UTF-8")
        mostrar_encabezado_habitaciones()
        cantidad_habitaciones = imprimir_habitaciones_recursivo(arch)
        print("-" * 54)
        if cantidad_habitaciones == 0:
            print("No hay habitaciones cargadas.")
        else:
            print(f"Cantidad total de habitaciones: {cantidad_habitaciones}")
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {RUTA_HABITACIONES}.")
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {RUTA_HABITACIONES}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    val_datos.pausar_menu()
    return habitaciones_lista


def pedir_numero_existente(mensaje):
    """Pide un numero de habitacion hasta que exista en el archivo y devuelve el registro completo."""

    numero = val_datos.pedir_entero_rango(mensaje, 100, 999)
    habitacion = buscar_habitacion_por_numero(numero)

    while len(habitacion) == 0:
        val_datos.imprimir_error("Error. No existe una habitación con ese número.")
        numero = val_datos.pedir_entero_rango(mensaje, 100, 999)
        habitacion = buscar_habitacion_por_numero(numero)

    return habitacion



def baja_habitacion(habitaciones_lista, reservas_lista, clientes_lista):
    """
    Da de baja una habitacion previa confirmacion. Para mantener la integridad referencial,
    no permite eliminar una habitacion que tenga reservas asociadas (se muestran para que el usuario las elimine primero).
    """

    val_datos.imprimir_titulo("Baja de habitación")

    if len(archivos.cargar_matriz(RUTA_HABITACIONES, COLUMNAS_HABITACIONES)) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    habitacion = pedir_numero_existente("Ingrese el número de la habitación a dar de baja: ")


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
            if archivos.reemplazar_registro(RUTA_HABITACIONES, habitacion[0], None, COLUMNAS_HABITACIONES):
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

    if len(archivos.cargar_matriz(RUTA_HABITACIONES, COLUMNAS_HABITACIONES)) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    habitacion = pedir_numero_existente("Ingrese el número de la habitación a modificar: ")


    print("\nSe encontró la siguiente habitación:")
    mostrar_encabezado_habitaciones()
    mostrar_habitacion(habitacion)

    print("\nDeje vacío el campo si no desea modificarlo.")

    entrada_numero = input(f"Número ({habitacion[1]}): ").strip()
    if entrada_numero != "":
        while (val_datos.es_entero_en_rango(entrada_numero, 100, 999) == False
               or archivos.existe_valor(RUTA_HABITACIONES, 1, int(entrada_numero), habitacion[0], COLUMNAS_HABITACIONES)):
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

    if archivos.reemplazar_registro(RUTA_HABITACIONES, habitacion[0], habitacion, COLUMNAS_HABITACIONES):
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

    if len(archivos.cargar_matriz(RUTA_HABITACIONES, COLUMNAS_HABITACIONES)) == 0:
        print("No hay habitaciones cargadas.")
        return habitaciones_lista

    numero = val_datos.pedir_entero_rango("Ingrese el número de la habitación: ", 100, 999)
    habitacion = buscar_habitacion_por_numero(numero)

    if len(habitacion) == 0:
        val_datos.imprimir_error("No existe una habitación con ese número.")
    else:
        mostrar_encabezado_habitaciones()
        mostrar_habitacion(habitacion)

        reservas_de_la_habitacion = Reservas.obtener_reservas_por_habitacion(reservas_lista, habitacion[0])

        print(f"\nHistorial de reservas de la habitación {habitacion[1]}:")
        if len(reservas_de_la_habitacion) == 0:
            print("La habitación no tiene reservas registradas.")
        else:
            Reservas.mostrar_reservas_detalladas(reservas_de_la_habitacion, clientes_lista, habitaciones_lista)
            print(f"\nTotal de reservas: {len(reservas_de_la_habitacion)} | Total de noches reservadas: {val_datos.total_noches(reservas_de_la_habitacion)}")

    val_datos.pausar_menu()
    return habitaciones_lista


def buscar_habitacion_por_numero(numero):
    """Devuelve el registro de la habitacion con ese numero leyendo el archivo, o una lista vacia si no existe."""

    encontrada = []
    try:
        arch = open(RUTA_HABITACIONES, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "" and len(encontrada) == 0:
            registro = archivos.leer_registro_de_linea(linea, COLUMNAS_HABITACIONES)
            if len(registro) > 0 and registro[1] == numero:
                encontrada = registro
            linea = arch.readline()
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {RUTA_HABITACIONES}.")
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {RUTA_HABITACIONES}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return encontrada



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