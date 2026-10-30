from utilidades import val_datos, archivos
from gestion import Reservas


RUTA_CLIENTES = "datos/clientes.txt"
COLUMNAS_ENTERAS_CLIENTES = (0, 3)


def cargar_clientes():
    """Devuelve la matriz con todos los clientes del archivo. Solo la usan los menus que necesitan todos juntos."""

    return archivos.cargar_matriz(RUTA_CLIENTES, COLUMNAS_ENTERAS_CLIENTES)


def buscar_cliente(id_cliente):
    """Busca el cliente en el archivo. Devuelve el registro, o una lista vacia si no existe."""

    return archivos.buscar_registro(RUTA_CLIENTES, id_cliente, COLUMNAS_ENTERAS_CLIENTES)


def mostrar_encabezado_clientes():
    """Imprime el encabezado de la tabla de clientes."""

    encabezados_clientes = ("ID", "Nombre", "Apellido", "DNI")
    print(f"{encabezados_clientes[0]:<10}{encabezados_clientes[1]:<15}{encabezados_clientes[2]:<15}{encabezados_clientes[3]:<12}")
    print("-" * 52)


def mostrar_cliente(cliente):
    """Imprime una fila de la tabla de clientes con los datos del cliente recibido."""

    print(f"{cliente[0]:<10}{cliente[1]:<15}{cliente[2]:<15}{cliente[3]:<12}")


def existe_dni(dni, id_excluido):
    """Devuelve True si el DNI ya esta cargado en otro cliente (se ignora el cliente con id_excluido)."""

    return archivos.existe_valor(RUTA_CLIENTES, 3, dni, id_excluido, COLUMNAS_ENTERAS_CLIENTES)


def pedir_cliente_existente(mensaje):
    """Pide el ID de un cliente y lo busca en el archivo. Devuelve el cliente, o una lista vacia si no esta."""

    cliente = []
    ultimo_id = archivos.obtener_proximo_id(RUTA_CLIENTES, COLUMNAS_ENTERAS_CLIENTES) - 1

    if ultimo_id == 0:
        print("No hay clientes cargados.")
    else:
        id_cliente = val_datos.pedir_entero_rango(mensaje, 1, ultimo_id)
        cliente = buscar_cliente(id_cliente)
        if len(cliente) == 0:
            val_datos.imprimir_error("No existe un cliente con ese ID.")

    return cliente


def ingresar_cliente():
    """Solicita los datos validados de un cliente nuevo y lo agrega al final del archivo de clientes."""

    val_datos.imprimir_titulo("Ingresar cliente")
    nombre = val_datos.pedir_nombre("Nombre: ")
    apellido = val_datos.pedir_apellido("Apellido: ")

    dni = val_datos.pedir_dni("DNI: ")
    while existe_dni(dni, -1):
        val_datos.imprimir_error("Error. Ya existe un cliente con ese DNI.")
        dni = val_datos.pedir_dni("DNI: ")

    nuevo_id = archivos.obtener_proximo_id(RUTA_CLIENTES, COLUMNAS_ENTERAS_CLIENTES)
    nuevo_cliente = [nuevo_id, nombre, apellido, dni]

    if archivos.agregar_registro(RUTA_CLIENTES, nuevo_cliente):
        val_datos.imprimir_exito(f"Cliente agregado con ID {nuevo_id}.")


def listar_clientes():
    """Imprime en pantalla todos los clientes del archivo con formato de tabla."""

    val_datos.imprimir_titulo("Listado de clientes")
    cantidad = 0

    try:
        arch = open(RUTA_CLIENTES, "r", encoding="UTF-8")
        mostrar_encabezado_clientes()
        for linea in arch:
            cliente = archivos.leer_registro_de_linea(linea, COLUMNAS_ENTERAS_CLIENTES)
            if len(cliente) > 0:
                mostrar_cliente(cliente)
                cantidad += 1
        print("-" * 52)
        print(f"Cantidad total de clientes: {cantidad}")
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {RUTA_CLIENTES}.")
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {RUTA_CLIENTES}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    val_datos.pausar_menu()


def baja_cliente(reservas_lista, habitaciones_lista):
    """
    Da de baja un cliente previa confirmacion. Para mantener la integridad referencial,
    no permite eliminar un cliente que tenga reservas asociadas (se muestran para que el usuario las elimine primero).
    """

    val_datos.imprimir_titulo("Baja de cliente")
    cliente = pedir_cliente_existente("Ingrese el ID del cliente a dar de baja: ")
    if len(cliente) == 0:
        return

    reservas_del_cliente = Reservas.obtener_reservas_por_cliente(reservas_lista, cliente[0])

    if len(reservas_del_cliente) > 0:
        val_datos.imprimir_error(f"No se puede dar de baja a {cliente[1]} {cliente[2]}: "
                                 f"tiene {len(reservas_del_cliente)} reserva(s) asociada(s).")
        print("Elimine primero estas reservas desde el menú de reservas:\n")
        Reservas.mostrar_reservas_detalladas(reservas_del_cliente, [cliente], habitaciones_lista)
    else:
        print("\nSe encontró el siguiente cliente:")
        mostrar_encabezado_clientes()
        mostrar_cliente(cliente)
        if val_datos.pedir_confirmacion("¿Confirma la baja?"):
            if archivos.reemplazar_registro(RUTA_CLIENTES, cliente[0], None, COLUMNAS_ENTERAS_CLIENTES):
                val_datos.imprimir_exito(f"Cliente {cliente[1]} {cliente[2]} eliminado.")
        else:
            print("Operación cancelada. El cliente no fue eliminado.")


def modificar_cliente():
    """Permite modificar nombre, apellido y DNI de un cliente. Los campos que se dejan vacios no se modifican."""

    val_datos.imprimir_titulo("Modificar cliente")
    cliente = pedir_cliente_existente("Ingrese el ID del cliente a modificar: ")
    if len(cliente) == 0:
        return

    print("Deje vacío el campo si no desea modificarlo.")

    nuevo_nombre = input(f"Nombre ({cliente[1]}): ").strip()
    if nuevo_nombre != "":
        while val_datos.es_texto(nuevo_nombre) == False:
            val_datos.imprimir_error("Error. El nombre solo puede contener letras.")
            nuevo_nombre = input(f"Nombre ({cliente[1]}): ")
        cliente[1] = val_datos.normalizar_nombre(nuevo_nombre)

    nuevo_apellido = input(f"Apellido ({cliente[2]}): ").strip()
    if nuevo_apellido != "":
        while val_datos.es_texto(nuevo_apellido) == False:
            val_datos.imprimir_error("Error. El apellido solo puede contener letras.")
            nuevo_apellido = input(f"Apellido ({cliente[2]}): ")
        cliente[2] = val_datos.normalizar_nombre(nuevo_apellido)

    nuevo_dni = input(f"DNI ({cliente[3]}): ").strip()
    if nuevo_dni != "":
        while (val_datos.es_entero_en_rango(nuevo_dni, val_datos.DNI_MINIMO, val_datos.DNI_MAXIMO) == False
               or existe_dni(int(nuevo_dni), cliente[0])):
            val_datos.imprimir_error(f"Error. Ingrese un DNI válido ({val_datos.DNI_MINIMO}-{val_datos.DNI_MAXIMO}) "
                                     f"que no pertenezca a otro cliente.")
            nuevo_dni = input(f"DNI ({cliente[3]}): ").strip()
        cliente[3] = int(nuevo_dni)

    if archivos.reemplazar_registro(RUTA_CLIENTES, cliente[0], cliente, COLUMNAS_ENTERAS_CLIENTES):
        val_datos.imprimir_exito("Cliente modificado correctamente.")


def consultar_cliente(reservas_lista, habitaciones_lista):
    """
    Consulta un cliente por ID y muestra sus datos junto con todas sus reservas asociadas
    (habitacion, fechas y noches), ademas de un pequeño resumen de su historial.
    """

    val_datos.imprimir_titulo("Consultar cliente")
    cliente = pedir_cliente_existente("Ingrese el ID del cliente: ")

    if len(cliente) > 0:
        print(f"ID:       {cliente[0]}")
        print(f"Nombre:   {cliente[1]}")
        print(f"Apellido: {cliente[2]}")
        print(f"DNI:      {cliente[3]}")

        reservas_del_cliente = Reservas.obtener_reservas_por_cliente(reservas_lista, cliente[0])

        print(f"\nReservas de {cliente[1]} {cliente[2]}:")
        if len(reservas_del_cliente) == 0:
            print("El cliente no tiene reservas registradas.")
        else:
            Reservas.mostrar_reservas_detalladas(reservas_del_cliente, [cliente], habitaciones_lista)

            print(f"\nTotal de reservas: {len(reservas_del_cliente)} | Total de noches: {val_datos.total_noches(reservas_del_cliente)}")

    val_datos.pausar_menu()


def menu_clientes(reservas_lista, habitaciones_lista):
    """
    Menu principal para gestionar los clientes
    """
    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Clientes "
        print(f"\n{titulo:-^50}")
        print("[1] Ingresar cliente")
        print("[2] Listar clientes")
        print("[3] Baja de cliente")
        print("[4] Modificar cliente")
        print("[5] Consultar cliente y sus reservas")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                ingresar_cliente()
            case 2:
                listar_clientes()
            case 3:
                baja_cliente(reservas_lista, habitaciones_lista)
            case 4:
                modificar_cliente()
            case 5:
                consultar_cliente(reservas_lista, habitaciones_lista)
            case 0:
                print("Saliendo del menú de clientes...")
