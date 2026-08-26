
# MÓDULOS

"no usamos todavia"
    
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


def es_entero(cadena):
    if cadena == "":
        return False
    inicio = 1 if cadena[0] == "-" else 0
    if inicio == 1 and len(cadena) == 1:
        return False
    for i in range(inicio, len(cadena)):
        if cadena[i] < "0" or cadena[i] > "9":
            return False
    return True


def es_float(cadena):
    if cadena == "":
        return False
    inicio = 1 if cadena[0] == "-" else 0
    if inicio == 1 and len(cadena) == 1:
        return False
    puntos = 0
    for i in range(inicio, len(cadena)):
        if cadena[i] == ".":
            puntos += 1
        elif cadena[i] < "0" or cadena[i] > "9":
            return False
    if puntos > 1:
        return False
    return True


def pedir_entero_rango(mensaje, desde, hasta):
    valor_valido = False
    valor = None
    while valor_valido == False:
        entrada = input(mensaje)
        if es_entero(entrada):
            valor = int(entrada)
            if valor >= desde and valor <= hasta:
                valor_valido = True
            else:
                print("Error. Ingrese un valor entre", desde, "y", hasta)
        else:
            print("Error. Debe ingresar un número entero.")
    return valor


# MENÚS MODULARIZADOS


def menu_clientes(clientes_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE CLIENTES")
        print("---------------------------")
        print("[1] Ingresar cliente")
        print("[2] Listar clientes")
        print("[3] Baja de cliente")
        print("[4] Modificar cliente")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")
        
        opcion = pedir_entero_rango("Seleccione una opción: ", 0, 4)
        
        if opcion == 1:
            print("Dando de alta al cliente...")
        elif opcion == 2:
            print("Listando clientes...")
        elif opcion == 3:
            print("baja de cliente...")
        elif opcion == 4:
            print("modificando cliente...")
            
    return clientes_lista


def menu_habitaciones(habitaciones_Lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE HABITACIONES")
        print("---------------------------")
        print("[1] Alta de habitación")
        print("[2] Listar habitaciones")
        print("[3] Baja de habitación")
        print("[4] modificar habitación")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")
        
        opcion = pedir_entero_rango("Seleccione una opción: ", 0, 4)
        
        if opcion == 1:
            print("Dando de alta la habitación...")
        elif opcion == 2:
            print("Listando habitaciones...")
        elif opcion == 3:
            print("Bajando la habitación...")
        elif opcion == 4:
            print("Modificando la habitación...")
            
    return habitaciones_Lista


def menu_reservas(reservas_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE RESERVAS")
        print("---------------------------")
        print("[1] Alta de reserva")
        print("[2] Listar reservas")
        print("[3] Baja de reserva")
        print("[4] modificar reserva")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")
        
        opcion = pedir_entero_rango("Seleccione una opción: ", 0, 4)
        
        if opcion == 1:
            print("Dando de alta la reserva...")
        elif opcion == 2:
            print("Listando reservas...")
        elif opcion == 3:
            print("Bajando la reserva...")
        elif opcion == 4:
            print("Modificando la reserva...")
            
    return reservas_lista


def menu_matrices(clientes_lista, habitaciones_Lista, reservas_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE MATRICES")
        print("---------------------------")
        print("[1] Ordenar clientes")
        print("[2] Ordenar habitaciones")
        print("[3] Ordenar reservas")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")
        
        opcion = pedir_entero_rango("Seleccione una opción: ", 0, 3)
        
        if opcion == 1:
            print("Ordenando clientes...")
        elif opcion == 2:
            print("Ordenando habitaciones...")
        elif opcion == 3:
            print("Ordenando reservas...")
            
    return clientes_lista, habitaciones_Lista, reservas_lista

def main():
    
    # DATOS HARDCODEADOS
    

    encabezados_clientes = ['Id_cliente', 'Nombre', 'Apellido', 'DNI']
    clientes = [
        [1, 'Juan', 'Pérez', 32145678],
        [2, 'Ana', 'López', 25412587],
        [3, 'Carlos', 'Gómez', 40123654],
        [4, 'María', 'Fernández', 35147852],
        [5, 'Lucía', 'Martínez', 38741256],
    ]

    encabezados_habitaciones = ['Id_hab', 'Numero', 'Tipo', 'Capacidad', 'Estado']
    habitaciones = [
        [1, 101, 'Simple', 1, 'Disponible'],
        [2, 102, 'Simple', 1, 'Ocupada'],
        [3, 201, 'Doble', 2, 'Disponible'],
        [4, 202, 'Doble', 2, 'Mantenimiento'],
        [5, 301, 'Suite', 4, 'Disponible'],
    ]

    encabezados_reservas = ['Id_reserva', 'Id_cliente', 'Id_hab', 'Fecha_ingreso', 'Fecha_egreso']
    reservas = [
        [1, 1, 3, '01/09/2026', '15/09/2026'],
        [2, 2, 1, '28/08/2026', '02/09/2026'],
        [3, 3, 2, '05/09/2026', '10/09/2026'],
        [4, 5, 5, '02/09/2026', '08/09/2026'],
        [5, 4, 4, '07/09/2026', '12/09/2026'],
    ]
    
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL")
        print("---------------------------")
        print("[1] Gestión de clientes")
        print("[2] Gestión de habitaciones")
        print("[3] Gestión de reservas")
        print("[4] Matrices - Ordenar datos")
        print("[5] Facturación - Ficha de servicio")
        print("---------------------------")
        print("[0] Salir del programa")
        print("---------------------------")

        opcion = pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                clientes = menu_clientes(clientes)
            case 2:
                habitaciones = menu_habitaciones(habitaciones)
            case 3:
                reservas = menu_reservas(reservas)
            case 4:
                clientes, habitaciones, reservas = menu_matrices(clientes, habitaciones, reservas)
            case 5:
                print("Generando ficha de servicio...")
            case 0:
                print("Saliendo del programa, Hasta luego!")
         

if login():
    main()