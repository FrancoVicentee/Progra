from utilidades import val_datos


LEGAJO_MINIMO = 100
LEGAJO_MAXIMO = 999
SUELDO_MINIMO = 100000
SUELDO_MAXIMO = 10000000


def pedir_legajo(mensaje):
    """Pide un numero de legajo dentro del rango permitido y lo devuelve."""

    return val_datos.pedir_entero_rango(f"{mensaje} ({LEGAJO_MINIMO}-{LEGAJO_MAXIMO}): ", LEGAJO_MINIMO, LEGAJO_MAXIMO)


def alta_empleado(empleados_dict):
    """Registra un empleado nuevo en el diccionario si el legajo ingresado no existe."""

    val_datos.imprimir_titulo("Alta de empleado")
    legajo = pedir_legajo("Ingrese legajo")

    if legajo not in empleados_dict:
        nombre = val_datos.pedir_nombre("Nombre del empleado: ")
        sueldo = val_datos.pedir_entero_rango("Sueldo: $", SUELDO_MINIMO, SUELDO_MAXIMO)
        empleados_dict[legajo] = {"nombre": nombre, "sueldo": sueldo}
        val_datos.imprimir_exito("Empleado registrado correctamente.")
    else:
        val_datos.imprimir_error("Error. El legajo ya existe.")

    return empleados_dict


def listar_empleados(empleados_dict):
    """Imprime todos los empleados registrados con formato de tabla."""

    val_datos.imprimir_titulo("Listado de empleados")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados.")
    else:
        print(f"{'Legajo':<10}{'Nombre':<25}{'Sueldo':<12}")
        print("-" * 47)

        for legajo, datos in empleados_dict.items():
            print(f"{legajo:<10}{datos['nombre']:<25}${datos['sueldo']:<11}")

        print("-" * 47)
        print(f"Cantidad total de empleados: {len(empleados_dict)}")

    val_datos.pausar_menu()
    return empleados_dict


def baja_empleado(empleados_dict):
    """Elimina un empleado del diccionario previa confirmacion."""

    val_datos.imprimir_titulo("Baja de empleado")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para dar de baja.")
    else:
        legajo = pedir_legajo("Ingrese legajo a dar de baja")

        if legajo in empleados_dict:
            print(f"Empleado encontrado: {empleados_dict[legajo]['nombre']}")

            if val_datos.pedir_confirmacion("¿Confirma la baja?"):
                empleados_dict.pop(legajo)
                val_datos.imprimir_exito("Empleado eliminado correctamente.")
            else:
                print("Operación cancelada.")
        else:
            val_datos.imprimir_error("Empleado no encontrado.")

    return empleados_dict


def modificar_sueldo(empleados_dict):
    """Modifica el sueldo de un empleado existente."""

    val_datos.imprimir_titulo("Modificar sueldo de empleado")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para modificar.")
    else:
        legajo = pedir_legajo("Ingrese legajo a modificar")

        if legajo in empleados_dict:
            print(f"Empleado actual: {empleados_dict[legajo]['nombre']} - Sueldo: ${empleados_dict[legajo]['sueldo']}")
            nuevo_sueldo = val_datos.pedir_entero_rango("Nuevo sueldo: $", SUELDO_MINIMO, SUELDO_MAXIMO)
            empleados_dict[legajo]["sueldo"] = nuevo_sueldo
            val_datos.imprimir_exito("Sueldo actualizado correctamente.")
        else:
            val_datos.imprimir_error("Empleado no encontrado.")

    return empleados_dict


def consultar_empleado(empleados_dict):
    """Consulta un empleado por legajo y muestra sus datos."""

    val_datos.imprimir_titulo("Consultar empleado")
    if len(empleados_dict) == 0:
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
    return empleados_dict


def menu_admin(empleados_dict):
    """
    Menu principal para gestionar las operaciones de administración de empleados.
    """
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
                empleados_dict = alta_empleado(empleados_dict)
            case 2:
                empleados_dict = listar_empleados(empleados_dict)
            case 3:
                empleados_dict = baja_empleado(empleados_dict)
            case 4:
                empleados_dict = modificar_sueldo(empleados_dict)
            case 5:
                empleados_dict = consultar_empleado(empleados_dict)
            case 0:
                print("Cerrando menú de administración.")

    return empleados_dict
