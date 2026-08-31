from paquete_2 import val_datos

def menu_reservas(reservas_lista, clientes_lista, habitaciones_lista):

    opcion = -1
    while opcion != 0:
        print("\n---------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE RESERVAS")
        print("---------------------------")
        print("[1] Alta de reserva")
        print("[2] Listar reservas")
        print("[3] Baja de reserva")
        print("[4] Modificar reserva")
        print("---------------------------")
        print("[0] Volver al menú anterior")
        print("---------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        if opcion == 1:
            print("Alta de reserva")
        elif opcion == 2:
            print("Listar reservas")
        elif opcion == 3:
            print("Baja de reserva")
        elif opcion == 4:
            print("Modificar reserva")

    return reservas_lista