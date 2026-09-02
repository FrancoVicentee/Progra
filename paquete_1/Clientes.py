from paquete_2 import val_datos

def menu_clientes(clientes_lista):
    opcion = -1
    while opcion != 0:
        print("\n------------------------------------")
        print("MENÚ PRINCIPAL > MENÚ DE CLIENTES")
        print("------------------------------------")
        print("[1] Ingresar cliente")
        print("[2] Listar clientes")
        print("[3] Baja de cliente")
        print("[4] Modificar cliente")
        print("----------------------------")
        print("[0] Volver al menú anterior")
        print("----------------------------")

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 4)

        if opcion == 1:
            clientes_lista = ingresar_cliente(clientes_lista)
        elif opcion == 2:
            clientes_lista = listar_clientes(clientes_lista)
        elif opcion == 3:
            clientes_lista = baja_cliente(clientes_lista)
        elif opcion == 4:
            clientes_lista = modificar_cliente(clientes_lista)

    return clientes_lista



""""""""""""""""""""""""""""""""""""""""""""""""""""

Funciones para el manejo de clientes en el sistema.

""""""""""""""""""""""""""""""""""""""""""""""""""""


ID = 0
NOMBRE = 1
APELLIDO = 2
DNI = 3


def generar_id(clientes_lista):
    if len(clientes_lista) == 0:
        return 1
    ids = [cliente[ID] for cliente in clientes_lista]
    return max(ids) + 1


def ingresar_cliente(clientes_lista):
    print("\n--- Ingresar cliente ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = val_datos.pedir_entero_rango("DNI: ", 100000, 99999999)

    nuevo_id = generar_id(clientes_lista)
    nuevo_cliente = [nuevo_id, nombre, apellido, dni]

    clientes_lista.append(nuevo_cliente)
    print(f"Cliente agregado con ID {nuevo_id}.")
    return clientes_lista


def listar_clientes(clientes_lista):
    encabezados_clientes = ['ID', 'Nombre', 'Apellido', 'DNI']
    titulo = " Listado de clientes "
    print(f"\n{titulo:-^50}")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    print(f"{encabezados_clientes[ID]:<10}{encabezados_clientes[NOMBRE]:<15}{encabezados_clientes[APELLIDO]:<15}{encabezados_clientes[DNI]:<12}")
    print("-" * 50)
    for cliente in clientes_lista:
        print(f"{cliente[ID]:<10}{cliente[NOMBRE]:<15}{cliente[APELLIDO]:<15}{cliente[DNI]:<12}")

    return clientes_lista


def buscar_cliente_por_id(clientes_lista, id_buscado):
    for cliente in clientes_lista:
        if cliente[ID] == id_buscado:
            return cliente
    return False


def baja_cliente(clientes_lista):
    print("\n--- Baja de cliente ---")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_baja = val_datos.pedir_entero_rango("Ingrese el ID del cliente a dar de baja: ", 1, generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_baja)

    if cliente is False:
        print("No existe un cliente con ese ID.")
    else:
        clientes_lista.remove(cliente)
        print(f"Cliente {cliente[NOMBRE]} {cliente[APELLIDO]} eliminado.")

    return clientes_lista


def modificar_cliente(clientes_lista):
    print("\n--- Modificar cliente ---")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_mod = val_datos.pedir_entero_rango("Ingrese el ID del cliente a modificar: ", 1, generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_mod)

    if cliente is None:
        print("No existe un cliente con ese ID.")
        return clientes_lista

    print("Deje vacío el campo si no desea modificarlo.")
    nuevo_nombre = input(f"Nombre ({cliente[NOMBRE]}): ")
    nuevo_apellido = input(f"Apellido ({cliente[APELLIDO]}): ")
    nuevo_dni = val_datos.pedir_entero_rango(f"DNI ({cliente[DNI]}): ", 100000, 99999999)

    if nuevo_nombre != "":
        cliente[NOMBRE] = nuevo_nombre
    if nuevo_apellido != "":
        cliente[APELLIDO] = nuevo_apellido
    if nuevo_dni != "":
        cliente[DNI] = int(nuevo_dni)

    print("Cliente modificado correctamente.")
    return clientes_lista