from utilidades import val_datos, archivos


RUTA_EMPLEADOS = "datos/empleados.json"

LEGAJO_MINIMO = 100
LEGAJO_MAXIMO = 999
SUELDO_MINIMO = 100000
SUELDO_MAXIMO = 10000000


def cargar_empleados():
    """Lee los empleados del JSON y pasa los legajos de texto a int."""

    datos = archivos.leer_json(RUTA_EMPLEADOS)
    if datos is None:
        return None

    empleados_dict = {}
    for legajo, empleado in datos.items():
        empleados_dict[int(legajo)] = empleado
    return empleados_dict


def guardar_empleados(empleados_dict):
    """Graba los empleados en el JSON."""

    return archivos.grabar_json(RUTA_EMPLEADOS, empleados_dict)


def pedir_legajo(mensaje):
    """Pide un legajo válido."""

    return val_datos.pedir_entero_rango(f"{mensaje} ({LEGAJO_MINIMO}-{LEGAJO_MAXIMO}): ", LEGAJO_MINIMO, LEGAJO_MAXIMO)


def alta_empleado():
    """Da de alta un empleado si el legajo no existe."""

    val_datos.imprimir_titulo("Alta de empleado")
    empleados_dict = cargar_empleados()
    if empleados_dict is None:
        return

    legajo = pedir_legajo("Ingrese legajo")

    if legajo not in empleados_dict:
        nombre = val_datos.pedir_nombre("Nombre del empleado: ")
        sueldo = val_datos.pedir_entero_rango("Sueldo: $", SUELDO_MINIMO, SUELDO_MAXIMO)
        empleados_dict[legajo] = {"nombre": nombre, "sueldo": sueldo}
        if guardar_empleados(empleados_dict):
            val_datos.imprimir_exito("Empleado registrado correctamente.")
    else:
        val_datos.imprimir_error("Error. El legajo ya existe.")


def listar_empleados():
    """Muestra todos los empleados en una tabla."""

    val_datos.imprimir_titulo("Listado de empleados")
    empleados_dict = cargar_empleados()

    if empleados_dict is None:
        pass
    elif len(empleados_dict) == 0:
        print("No hay empleados registrados.")
    else:
        print(f"{'Legajo':<10}{'Nombre':<25}{'Sueldo':<12}")
        print("-" * 47)

        for legajo, datos in empleados_dict.items():
            print(f"{legajo:<10}{datos['nombre']:<25}${datos['sueldo']:<11}")

        print("-" * 47)
        print(f"Cantidad total de empleados: {len(empleados_dict)}")

    val_datos.pausar_menu()


def baja_empleado():
    """Da de baja un empleado, previa confirmación."""

    val_datos.imprimir_titulo("Baja de empleado")
    empleados_dict = cargar_empleados()

    if empleados_dict is None:
        return
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para dar de baja.")
        return

    legajo = pedir_legajo("Ingrese legajo a dar de baja")

    if legajo in empleados_dict:
        print(f"Empleado encontrado: {empleados_dict[legajo]['nombre']}")

        if val_datos.pedir_confirmacion("¿Confirma la baja?"):
            empleados_dict.pop(legajo)
            if guardar_empleados(empleados_dict):
                val_datos.imprimir_exito("Empleado eliminado correctamente.")
        else:
            print("Operación cancelada.")
    else:
        val_datos.imprimir_error("Empleado no encontrado.")


def modificar_sueldo():
    """Modifica el sueldo de un empleado."""

    val_datos.imprimir_titulo("Modificar sueldo de empleado")
    empleados_dict = cargar_empleados()

    if empleados_dict is None:
        return
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para modificar.")
        return

    legajo = pedir_legajo("Ingrese legajo a modificar")

    if legajo in empleados_dict:
        print(f"Empleado actual: {empleados_dict[legajo]['nombre']} - Sueldo: ${empleados_dict[legajo]['sueldo']}")
        nuevo_sueldo = val_datos.pedir_entero_rango("Nuevo sueldo: $", SUELDO_MINIMO, SUELDO_MAXIMO)
        empleados_dict[legajo]["sueldo"] = nuevo_sueldo
        if guardar_empleados(empleados_dict):
            val_datos.imprimir_exito("Sueldo actualizado correctamente.")
    else:
        val_datos.imprimir_error("Empleado no encontrado.")


def consultar_empleado():
    """Muestra los datos de un empleado por legajo."""

    val_datos.imprimir_titulo("Consultar empleado")
    empleados_dict = cargar_empleados()

    if empleados_dict is None:
        pass
    elif len(empleados_dict) == 0:
        print("No hay empleados registrados para consultar.")
    else:
        legajo = pedir_legajo("Ingrese legajo a consultar")

        if legajo in empleados_dict:
            empleado = empleados_dict[legajo]
            print(f"Legajo: {legajo}")
            print(f"Nombre: {empleado['nombre']}")
            print(f"Sueldo: ${empleado['sueldo']}")
        else:
            val_datos.imprimir_error("Empleado no encontrado.")

    val_datos.pausar_menu()


def menu_admin():
    """Menú de administración de empleados."""
    opcion = -1
    while opcion != 0:
        titulo = " Menú Administración "
        print(f"\n{titulo:-^50}")
        print("[1] Alta de empleado")
        print("[2] Listar empleados")
        print("[3] Baja de empleado")
        print("[4] Modificar sueldo empleado")
        print("[5] Consultar empleado")
        print("-" * 50)
        print("[0] Cerrar menú de administración")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                alta_empleado()
            case 2:
                listar_empleados()
            case 3:
                baja_empleado()
            case 4:
                modificar_sueldo()
            case 5:
                consultar_empleado()
            case 0:
                print("Cerrando menú de administración.")
