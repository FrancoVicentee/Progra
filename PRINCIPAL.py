# MÓDULOS

from gestion import Clientes, Administrador, Reservas, Habitaciones
from utilidades import estadisticas, matriz, val_datos, archivos


RUTA_USUARIOS = "datos/usuarios.json"


def cargar_usuarios():
    """Lee los usuarios del JSON y pasa cada lista (contraseña, rol) a tupla."""

    datos = archivos.leer_json(RUTA_USUARIOS)
    usuarios = {}
    if datos is not None:
        for usuario, credenciales in datos.items():
            usuarios[usuario] = tuple(credenciales)
    return usuarios


def login(usuarios):
    """Pide usuario y contraseña con 3 intentos. Devuelve si entró y con qué rol."""

    intentos = 3
    acceso_concedido = False
    rol_usuario = ""

    while intentos > 0 and acceso_concedido == False:
        # El usuario no distingue mayusculas ni espacios en los extremos; la contraseña si.
        usuario_try = input("\nIngrese el usuario: ").strip().lower()
        contrasena_try = input("Ingrese la contraseña: ")

        if usuario_try in usuarios and usuarios[usuario_try][0] == contrasena_try:
            val_datos.imprimir_exito(f"\n¡Sesión iniciada correctamente como {usuarios[usuario_try][1]}!")
            acceso_concedido = True
            rol_usuario = usuarios[usuario_try][1]
        else:
            intentos -= 1
            if intentos > 0:
                val_datos.imprimir_error(f"Credenciales incorrectas. Intentos restantes: {intentos}")
            else:
                val_datos.imprimir_error("Has llegado al límite de intentos, tu sesión ha sido bloqueada.")

    return acceso_concedido, rol_usuario


def cargar_datos():
    """Lee los archivos de clientes, habitaciones y reservas y devuelve una tupla (clientes, habitaciones, reservas)."""

    clientes = Clientes.cargar_clientes()
    habitaciones = archivos.cargar_matriz(Habitaciones.RUTA_HABITACIONES, Habitaciones.COLUMNAS_HABITACIONES)
    reservas = archivos.cargar_matriz(Reservas.RUTA_RESERVAS, Reservas.COLUMNAS_RESERVAS)
    return clientes, habitaciones, reservas


def menu_principal_admin():
    """Función para mostrar el menú principal para administradores. Permite gestionar clientes, habitaciones, reservas,
    matrices, estadísticas del hotel y empleados. Devuelve True si el usuario eligió cerrar el programa."""

    menu_activo = True
    salir_del_programa = False

    while menu_activo == True:
        titulo = " Menú Principal (ADMIN) "
        print(f"\n{titulo:-^50}")
        print("[1] Gestión de clientes")
        print("[2] Gestión de habitaciones")
        print("[3] Gestión de reservas")
        print("[4] Matrices - Ordenar y consultar datos")
        print("[5] Ver estadísticas del hotel")
        print("[6] Menú de Administración (Empleados)")
        print("-" * 50)
        print("[7] Cerrar sesión (Volver al login)")
        print("[0] Cerrar el programa definitivamente")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 7)

        # Se leen los archivos en cada opcion para trabajar siempre con los datos actualizados.
        if opcion >= 1 and opcion <= 5:
            clientes, habitaciones, reservas = cargar_datos()

        match opcion:
            case 1:
                Clientes.menu_clientes(reservas, habitaciones)
            case 2:
                Habitaciones.menu_habitaciones(habitaciones, reservas, clientes)
            case 3:
                Reservas.menu_reservas(reservas, clientes, habitaciones)
            case 4:
                matriz.menu_matrices(clientes, habitaciones, reservas)
            case 5:
                estadisticas.menu_estadisticas(clientes, habitaciones, reservas)
            case 6:
                Administrador.menu_admin()
            case 7:
                print("\nCerrando sesión... Volviendo a la pantalla de inicio.")
                menu_activo = False
            case 0:
                menu_activo = False
                salir_del_programa = True

    return salir_del_programa


def menu_principal_empleados():
    """Función para mostrar el menú principal para empleados. Permite gestionar clientes, habitaciones, reservas,
    matrices y estadísticas del hotel. Devuelve True si el usuario eligió cerrar el programa."""

    menu_activo = True
    salir_del_programa = False

    while menu_activo == True:
        titulo = " Menú Principal (EMPLEADO) "
        print(f"\n{titulo:-^50}")
        print("[1] Gestión de clientes")
        print("[2] Gestión de habitaciones")
        print("[3] Gestión de reservas")
        print("[4] Matrices - Ordenar y consultar datos")
        print("[5] Ver estadísticas del hotel")
        print("-" * 50)
        print("[6] Cerrar sesión (Volver al login)")
        print("[0] Cerrar el programa definitivamente")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 6)

        # Se leen los archivos en cada opcion para trabajar siempre con los datos actualizados.
        if opcion >= 1 and opcion <= 5:
            clientes, habitaciones, reservas = cargar_datos()

        match opcion:
            case 1:
                Clientes.menu_clientes(reservas, habitaciones)
            case 2:
                Habitaciones.menu_habitaciones(habitaciones, reservas, clientes)
            case 3:
                Reservas.menu_reservas(reservas, clientes, habitaciones)
            case 4:
                matriz.menu_matrices(clientes, habitaciones, reservas)
            case 5:
                estadisticas.menu_estadisticas(clientes, habitaciones, reservas)
            case 6:
                print("\nCerrando sesión... Volviendo a la pantalla de inicio.")
                menu_activo = False
            case 0:
                menu_activo = False
                salir_del_programa = True

    return salir_del_programa


if __name__ == "__main__":

    try:
        usuarios = cargar_usuarios()

        if len(usuarios) == 0:
            val_datos.imprimir_error("No hay usuarios cargados para iniciar sesión. Revise el archivo " + RUTA_USUARIOS + ".")
        else:
            sesion_activa = True
            while sesion_activa == True:
                acceso, rol = login(usuarios)

                if acceso == True:
                    salir = False
                    if rol == "ADMIN":
                        salir = menu_principal_admin()
                    elif rol == "EMPLEADO":
                        salir = menu_principal_empleados()
                    if salir == True:
                        sesion_activa = False
                else:
                    sesion_activa = False
    except KeyboardInterrupt:
        # Ctrl+C cierra el programa sin mostrar el error de Python.
        val_datos.imprimir_error("\n\nPrograma interrumpido por el usuario.")

    print("\nSaliendo del programa, ¡Hasta luego!")
