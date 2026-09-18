from paquete_2 import val_datos



def generar_id(clientes_lista):
    """
    Calcula el proximo id para un cliente nuevo utilizando map y max. 
    La funcion devuelve 1 si la lista esta vacia.
    """
    ids = list(map(lambda cliente: cliente[0], clientes_lista))
    if len(ids) == 0:
        return 1
    return max(ids) + 1


def ingresar_cliente(clientes_lista):
    print("\n--- Ingresar cliente ---")
    nombre = val_datos.pedir_nombre("Nombre: ")
    apellido = val_datos.pedir_apellido("Apellido: ")
    dni = val_datos.pedir_entero_rango("DNI: ", 100000, 100000000)
 
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

    if cliente is False:
        print("No existe un cliente con ese ID.")
        return clientes_lista

    print("Deje vacío el campo si no desea modificarlo.")

    nuevo_nombre = input(f"Nombre ({cliente[1]}): ")
    if nuevo_nombre != "":
        while val_datos.es_texto(nuevo_nombre) == False:
            print("Error. El nombre solo puede contener letras.")
            nuevo_nombre = input(f"Nombre ({cliente[1]}): ")
        cliente[1] = nuevo_nombre

    nuevo_apellido = input(f"Apellido ({cliente[2]}): ")
    if nuevo_apellido != "":
        while val_datos.es_texto(nuevo_apellido) == False:
            print("Error. El apellido solo puede contener letras.")
            nuevo_apellido = input(f"Apellido ({cliente[2]}): ")
        cliente[2] = nuevo_apellido

    nuevo_dni = input(f"DNI ({cliente[3]}): ")
    if nuevo_dni != "":
        while val_datos.es_entero(nuevo_dni) == False or int(nuevo_dni) < 100000 or int(nuevo_dni) > 100000000:
            print("Error. Ingrese un DNI válido (100000-100000000).")
            nuevo_dni = input(f"DNI ({cliente[3]}): ")
        cliente[3] = int(nuevo_dni)

    print("Cliente modificado correctamente.")
    return clientes_lista

def consultar_cliente(clientes_lista):
    print("\n--- Consultar cliente ---")
    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        return clientes_lista

    id_consulta = val_datos.pedir_entero_rango("Ingrese el ID del cliente: ", 1, generar_id(clientes_lista) - 1)
    cliente = buscar_cliente_por_id(clientes_lista, id_consulta)

    if cliente is False:
        print("No existe un cliente con ese ID.")
    else:
        print(f"ID: {cliente[0]}")
        print(f"Nombre: {cliente[1]}")
        print(f"Apellido: {cliente[2]}")
        print(f"DNI: {cliente[3]}")

    val_datos.pausar_menu()
    return clientes_lista




def menu_clientes(clientes_lista):
    """
    Menu principal para gestionar las habitaciones.
    """
    opcion = -1
    while opcion != 0:
        titulo = " Menú Principal > Menú de Clientes "
        print(f"\n{titulo:-^50}")
        print("[1] Ingresar cliente")
        print("[2] Listar clientes")
        print("[3] Baja de cliente")
        print("[4] Modificar cliente")
        print("[5] Consultar cliente")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                clientes_lista = ingresar_cliente(clientes_lista)
            case 2:
                clientes_lista = listar_clientes(clientes_lista)
            case 3:
                clientes_lista = baja_cliente(clientes_lista)
            case 4:
                clientes_lista = modificar_cliente(clientes_lista)
            case 5:
                clientes_lista = consultar_cliente(clientes_lista)
            case 0:
                print("Saliendo del menú de clientes...")

    return clientes_lista