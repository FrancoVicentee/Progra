from paquete_2 import val_datos


"""""""""""""""""""""""""""""""""""""""""""""""""""

Funciones para el manejo de clientes en el sistema.

"""""""""""""""""""""""""""""""""""""""""""""""""""



def generar_id(clientes_lista):
    if len(clientes_lista) == 0:
        return 1
    ids = [cliente[0] for cliente in clientes_lista]
    return max(ids) + 1


def ingresar_cliente(clientes_lista):
    print("\n--- Ingresar cliente ---")
    nombre = val_datos.pedir_nombre("Nombre: ")
    apellido = val_datos.pedir_apellido("Apellido: ")
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

    print(f"{encabezados_clientes[0]:<10}{encabezados_clientes[1]:<15}{encabezados_clientes[2]:<15}{encabezados_clientes[3]:<12}")
    print("-" * 50)
    for cliente in clientes_lista:
        print(f"{cliente[0]:<10}{cliente[1]:<15}{cliente[2]:<15}{cliente[3]:<12}")
        
    val_datos.pausar_menu()
    return clientes_lista


def buscar_cliente_por_id(clientes_lista, id_buscado):
    for cliente in clientes_lista:
        if cliente[0] == id_buscado:
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
        print(f"Cliente {cliente[1]} {cliente[2]} eliminado.")

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
    nuevo_nombre = input(f"Nombre ({cliente[1]}): ")
    nuevo_apellido = input(f"Apellido ({cliente[2]}): ")
    nuevo_dni = val_datos.pedir_entero_rango(f"DNI ({cliente[3]}): ", 100000, 99999999)

    if nuevo_nombre != "":
        cliente[1] = nuevo_nombre
    if nuevo_apellido != "":
        cliente[2] = nuevo_apellido
    if nuevo_dni != "":
        cliente[3] = int(nuevo_dni)

    print("Cliente modificado correctamente.")
    return clientes_lista




"""""""""""""""""""""""""""""""""""""""""""""""""""

Menú de clientes para el sistema.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def menu_clientes(clientes_lista):
    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Clientes "
        print(f"\n{titulo:-^50}")
        print("[1] Ingresar cliente")
        print("[2] Listar clientes")
        print("[3] Baja de cliente")
        print("[4] Modificar cliente")
        print("[0] Volver al menú anterior")
        print("-" * 50)

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
