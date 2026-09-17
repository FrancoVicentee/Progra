# MÓDULOS
 
from paquete_1 import Clientes, Administrador, Reservas, Habitaciones
from paquete_2 import estadisticas, matriz, val_datos

def login():
    
    usuarios = {
        "admin": ("hotel123", "ADMIN"),
        "recepcion": ("emp123", "EMPLEADO"),
    }
    
    intentos = 3
    acceso_concedido = False
    rol_usuario = ""
    
    while intentos > 0 and acceso_concedido == False:
        usuario_try = input("\nIngrese el usuario: ")
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
 
def menu_principal_admin(clientes, habitaciones, reservas, empleados_dict):
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
 
        match opcion:
            case 1:
                clientes = Clientes.menu_clientes(clientes)
            case 2:
                habitaciones = Habitaciones.menu_habitaciones(habitaciones)
            case 3:
                reservas = Reservas.menu_reservas(reservas, clientes, habitaciones)
            case 4:
                matriz.menu_matrices(clientes, habitaciones, reservas)
            case 5:
                estadisticas.menu_estadisticas(clientes, habitaciones, reservas)
            case 6:
                empleados_dict = Administrador.menu_admin(empleados_dict)
            case 7:
                print("\nCerrando sesión... Volviendo a la pantalla de inicio.")
                menu_activo = False
            case 0:
                menu_activo = False
                salir_del_programa = True
 
    return salir_del_programa
 
def menu_principal_empleados(clientes, habitaciones, reservas):
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
 
        match opcion:
            case 1:
                clientes = Clientes.menu_clientes(clientes)
            case 2:
                habitaciones = Habitaciones.menu_habitaciones(habitaciones)
            case 3:
                reservas = Reservas.menu_reservas(reservas, clientes, habitaciones)
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
    
    empleados_dict = {
        101: {"nombre": "Fran Cino", "sueldo": 550000},
        102: {"nombre": "Benicio Beaudean", "sueldo": 670000}
    }
    
    clientes = [
        [1, 'Juan', 'Pérez', 32145678],
        [2, 'Ana', 'López', 25412587],
        [3, 'Carlos', 'Gómez', 40123654],
        [4, 'María', 'Fernández', 35147852],
        [5, 'Lucía', 'Martínez', 38741256],
    ]
 
    habitaciones = [
        [1, 101, 'Simple', 1, 'Disponible'],
        [2, 102, 'Simple', 1, 'Ocupada'],
        [3, 201, 'Doble', 2, 'Disponible'],
        [4, 202, 'Doble', 2, 'Mantenimiento'],
        [5, 301, 'Suite', 4, 'Disponible'],
    ]
 
    reservas = [
        [1, 1, 3, '01/09/2026', '15/09/2026'],
        [2, 2, 1, '28/08/2026', '02/09/2026'],
        [3, 3, 2, '05/09/2026', '10/09/2026'],
        [4, 5, 5, '02/09/2026', '08/09/2026'],
        [5, 4, 4, '07/09/2026', '12/09/2026'],
        [6, 2, 3, '10/03/2026', '15/03/2026'],
    ]
    
    sesion_activa = True
    while sesion_activa == True:
        acceso, rol = login()
        
        if acceso == True:
            salir = False
            if rol == "ADMIN":
                salir = menu_principal_admin(clientes, habitaciones, reservas, empleados_dict)
            elif rol == "EMPLEADO":
                salir = menu_principal_empleados(clientes, habitaciones, reservas)    
            if salir == True:
                sesion_activa = False 
        else:
            sesion_activa = False 
            
    print("\nSaliendo del programa, ¡Hasta luego!")