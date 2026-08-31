from paquete_2 import val_datos

def menu_habitaciones(habitaciones_lista):
    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE HABITACIONES")
        print("---------------------------")
        print("[1] Alta de habitación")
        print("[2] Listar habitaciones")
        print("[3] Baja de habitación")
        print("[4] Modificar habitación")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        if opcion == 1:
            print("Alta de habitación")
        elif opcion == 2:
            print("Listar habitaciones")
        elif opcion == 3:
            print("Baja de habitación")
        elif opcion == 4:
            print("Modificar habitación")

    return habitaciones_lista
