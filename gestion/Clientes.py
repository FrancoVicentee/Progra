from utilidades import val_datos
from gestion import Reservas



def mostrar_encabezado_clientes():
    """Imprime el encabezado de la tabla de clientes."""

    encabezados_clientes = ("ID", "Nombre", "Apellido", "DNI")
    print(f"{encabezados_clientes[0]:<10}{encabezados_clientes[1]:<15}{encabezados_clientes[2]:<15}{encabezados_clientes[3]:<12}")
    print("-" * 52)


def mostrar_cliente(cliente):
    """Imprime una fila de la tabla de clientes con los datos del cliente recibido."""

    print(f"{cliente[0]:<10}{cliente[1]:<15}{cliente[2]:<15}{cliente[3]:<12}")


def existe_dni(clientes_lista, dni, id_excluido):
    """Devuelve True si el DNI ya esta cargado en otro cliente (se ignora el cliente con id_excluido)."""

    coincidencias = [cliente for cliente in clientes_lista if cliente[3] == dni and cliente[0] != id_excluido]
    return len(coincidencias) > 0


def ingresar_cliente(clientes_lista):
    """Solicita los datos validados de un cliente nuevo y lo agrega a la matriz de clientes."""

    val_datos.imprimir_titulo("Ingresar cliente")
    nombre = val_datos.pedir_nombre("Nombre: ")
    apellido = val_datos.pedir_apellido("Apellido: ")

    dni = val_datos.pedir_dni("DNI: ")
    while existe_dni(clientes_lista, dni, -1):
        val_datos.imprimir_error("Error. Ya existe un cliente con ese DNI.")
        dni = val_datos.pedir_dni("DNI: ")

    nuevo_id = val_datos.generar_id(clientes_lista)
    nuevo_cliente = [nuevo_id, nombre, apellido, dni]

    clientes_lista.append(nuevo_cliente)
    val_datos.imprimir_exito(f"Cliente agregado con ID {nuevo_id}.")
    return clientes_lista


def listar_clientes(clientes_lista):
    """Imprime en pantalla todos los clientes registrados con formato de tabla."""

    val_datos.imprimir_titulo("Listado de clientes")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
    else:
        mostrar_encabezado_clientes()
        for cliente in clientes_lista:
            mostrar_cliente(cliente)
        print("-" * 52)
        print(f"Cantidad total de clientes: {len(clientes_lista)}")

    val_datos.pausar_menu()
    return clientes_lista


def buscar_cliente_por_id(clientes_lista, id_buscado):
    """Devuelve el cliente con el ID indicado, o False si no existe."""

    for cliente in clientes_lista:
        if cliente[0] == id_buscado:
            return cliente
    return False


def baja_cliente(clientes_lista, reservas_lista, habitaciones_lista):
    """
    Da de baja un cliente previa confirmacion. Para mantener la integridad referencial,
    no permite eliminar un cliente que tenga reservas asociadas (se muestran para que el usuario las elimine primero).
    """

    val_datos.imprimir_titulo("Baja de cliente")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_baja = val_datos.pedir_entero_rango("Ingrese el ID del cliente a dar de baja: ", 1, val_datos.generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_baja)

    if cliente is False:
        val_datos.imprimir_error("No existe un cliente con ese ID.")
        return clientes_lista

    reservas_del_cliente = Reservas.obtener_reservas_por_cliente(reservas_lista, id_baja)

    if len(reservas_del_cliente) > 0:
        val_datos.imprimir_error(f"No se puede dar de baja a {cliente[1]} {cliente[2]}: "
                                 f"tiene {len(reservas_del_cliente)} reserva(s) asociada(s).")
        print("Elimine primero estas reservas desde el menú de reservas:\n")
        Reservas.mostrar_reservas_detalladas(reservas_del_cliente, clientes_lista, habitaciones_lista)
    else:
        print("\nSe encontró el siguiente cliente:")
        mostrar_encabezado_clientes()
        mostrar_cliente(cliente)
        if val_datos.pedir_confirmacion("¿Confirma la baja?"):
            clientes_lista.remove(cliente)
            val_datos.imprimir_exito(f"Cliente {cliente[1]} {cliente[2]} eliminado.")
        else:
            print("Operación cancelada. El cliente no fue eliminado.")

    return clientes_lista


def modificar_cliente(clientes_lista):
    """Permite modificar nombre, apellido y DNI de un cliente. Los campos que se dejan vacios no se modifican."""

    val_datos.imprimir_titulo("Modificar cliente")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_mod = val_datos.pedir_entero_rango("Ingrese el ID del cliente a modificar: ", 1, val_datos.generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_mod)

    if cliente is False:
        val_datos.imprimir_error("No existe un cliente con ese ID.")
        return clientes_lista

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
               or existe_dni(clientes_lista, int(nuevo_dni), cliente[0])):
            val_datos.imprimir_error(f"Error. Ingrese un DNI válido ({val_datos.DNI_MINIMO}-{val_datos.DNI_MAXIMO}) "
                                     f"que no pertenezca a otro cliente.")
            nuevo_dni = input(f"DNI ({cliente[3]}): ").strip()
        cliente[3] = int(nuevo_dni)

    val_datos.imprimir_exito("Cliente modificado correctamente.")
    return clientes_lista


def consultar_cliente(clientes_lista, reservas_lista, habitaciones_lista):
    """
    Consulta un cliente por ID y muestra sus datos junto con todas sus reservas asociadas
    (habitacion, fechas y noches), ademas de un pequeño resumen de su historial.
    """

    val_datos.imprimir_titulo("Consultar cliente")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_consulta = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, val_datos.generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_consulta)

    if cliente is False:
        val_datos.imprimir_error("No existe un cliente con ese ID.")
    else:
        print(f"ID:       {cliente[0]}")
        print(f"Nombre:   {cliente[1]}")
        print(f"Apellido: {cliente[2]}")
        print(f"DNI:      {cliente[3]}")

        reservas_del_cliente = Reservas.obtener_reservas_por_cliente(reservas_lista, id_consulta)

        print(f"\nReservas de {cliente[1]} {cliente[2]}:")
        if len(reservas_del_cliente) == 0:
            print("El cliente no tiene reservas registradas.")
        else:
            Reservas.mostrar_reservas_detalladas(reservas_del_cliente, clientes_lista, habitaciones_lista)
            noches = [val_datos.calcular_noches(reserva[3], reserva[4]) for reserva in reservas_del_cliente]
            print(f"\nTotal de reservas: {len(reservas_del_cliente)} | Total de noches: {sum(noches)}")

    val_datos.pausar_menu()
    return clientes_lista


def menu_clientes(clientes_lista, reservas_lista, habitaciones_lista):
    """
    Menu principal para gestionar los clientes.
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
                clientes_lista = ingresar_cliente(clientes_lista)
            case 2:
                clientes_lista = listar_clientes(clientes_lista)
            case 3:
                clientes_lista = baja_cliente(clientes_lista, reservas_lista, habitaciones_lista)
            case 4:
                clientes_lista = modificar_cliente(clientes_lista)
            case 5:
                clientes_lista = consultar_cliente(clientes_lista, reservas_lista, habitaciones_lista)
            case 0:
                print("Saliendo del menú de clientes...")

    return clientes_lista