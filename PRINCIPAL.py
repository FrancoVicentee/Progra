# MÓDULOS

from paquete_1 import Clientes
from paquete_1 import Habitaciones
from paquete_1 import Reservas
from paquete_2 import matriz
from paquete_2 import val_datos
    
# FUNCIONES DE VALIDACIÓN Y LOGIN (Inspiradas en el sistema de estacionamiento)

def login():
    usuario_valido = "Admin"
    contraseña_valida = "Hotel123"
    
    usuario_try = input("Ingrese el usuario: ")
    while usuario_try != usuario_valido:
        print("Este usuario no existe. Intente nuevamente.")
        usuario_try = input("Ingrese el usuario: ")
        
    intentos_contra = 3
    acceso_concedido = False
    
    while intentos_contra > 0 and acceso_concedido == False:
        contraseña_try = input("Ingrese la contraseña: ")
        if contraseña_try == contraseña_valida:
            print("¡Has iniciado sesión correctamente!")
            acceso_concedido = True
        else:
            intentos_contra -= 1
            if intentos_contra > 0:
                print("Contraseña incorrecta. Le quedan", intentos_contra, "intentos.")
            else:
                print("Has llegado al límite de intentos, tu sesión ha sido bloqueada.")
                
    return acceso_concedido

def menu_principal():

    # DATOS HARDCODEADOS

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
    ]

    opcion = -1
    while opcion != 0:
        print("---------------------------")
        print("MENÚ PRINCIPAL")
        print("---------------------------")
        print("[1] Gestión de clientes")
        print("[2] Gestión de habitaciones")
        print("[3] Gestión de reservas")
        print("[4] Matrices - Ordenar y consultar datos")
        print("---------------------------")
        print("[0] Salir del programa")
        print("---------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        match opcion:
            case 1:
                clientes = Clientes.menu_clientes(clientes)
            case 2:
                habitaciones = Habitaciones.menu_habitaciones(habitaciones)
            case 3:
                reservas = Reservas.menu_reservas(reservas, clientes, habitaciones)
            case 4:
                matriz.menu_matrices(clientes, habitaciones, reservas)
            case 0:
                print("Saliendo del programa, ¡Hasta luego!")


if __name__ == "__main__":
    if login():
        menu_principal()