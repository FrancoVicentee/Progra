from paquete_2 import val_datos

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

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        if opcion == 1:
            print("Ingresar cliente")
        elif opcion == 2:
            print("Listar clientes")
        elif opcion == 3:
            print("Baja de cliente")
        elif opcion == 4:
            print("Modificar cliente")

    return clientes_lista
