import re
from utilidades import val_datos
from gestion import Clientes, Habitaciones, Reservas


def ordenar_por_apellido(lista_de_clientes):
    """Ordena la matriz de clientes por apellido (y nombre ante empates), sin distinguir mayusculas, y la muestra."""

    lista_de_clientes.sort(key=lambda cliente: (cliente[2].lower(), cliente[1].lower()))
    Clientes.mostrar_encabezado_clientes()
    for cliente in lista_de_clientes:
        Clientes.mostrar_cliente(cliente)
    val_datos.pausar_menu()
    return lista_de_clientes


def ordenar_por_numero(lista_de_habitaciones):
    """Ordena la matriz de habitaciones por numero de habitacion y la muestra."""

    lista_de_habitaciones.sort(key=lambda habitacion: habitacion[1])
    Habitaciones.mostrar_encabezado_habitaciones()
    for habitacion in lista_de_habitaciones:
        Habitaciones.mostrar_habitacion(habitacion)
    val_datos.pausar_menu()
    return lista_de_habitaciones


def ordenar_por_fecha_ingreso(lista_de_reservas, clientes_lista, habitaciones_lista):
    """Ordena la matriz de reservas por fecha de ingreso (convirtiendo la fecha a numero aaaammdd) y la muestra."""

    lista_de_reservas.sort(key=lambda reserva: val_datos.convertir_fecha_a_numero(reserva[3]))
    Reservas.mostrar_reservas_detalladas(lista_de_reservas, clientes_lista, habitaciones_lista)
    val_datos.pausar_menu()
    return lista_de_reservas


def ver_habitaciones_disponibles(lista_de_habitaciones):
    """Muestra solo las habitaciones cuyo estado es 'Disponible' (usando comprension de listas)."""

    habitaciones_disponibles = [habitacion for habitacion in lista_de_habitaciones if habitacion[4] == "Disponible"]

    if len(habitaciones_disponibles) == 0:
        print("No hay habitaciones disponibles.")
    else:
        Habitaciones.mostrar_encabezado_habitaciones()
        for habitacion in habitaciones_disponibles:
            Habitaciones.mostrar_habitacion(habitacion)
        print(f"\nHabitaciones disponibles: {len(habitaciones_disponibles)} de {len(lista_de_habitaciones)}")

    val_datos.pausar_menu()
    return habitaciones_disponibles


def buscar_clientes_por_inicio(clientes_lista, texto_buscado):
    """
    Busca los clientes cuyo nombre o apellido empiece con el texto buscado, sin distinguir mayusculas.
    El texto se valida antes con una expresion regular que solo admite letras, por lo que no puede
    contener metacaracteres que alteren el patron. El patron usa el ancla ^ y la bandera IGNORECASE.
    """

    patron = "^" + texto_buscado
    clientes_encontrados = []
    for cliente in clientes_lista:
        if re.match(patron, cliente[1], re.IGNORECASE) or re.match(patron, cliente[2], re.IGNORECASE):
            clientes_encontrados.append(cliente)

    print(f"\nClientes cuyo nombre o apellido empieza con '{texto_buscado}':")
    if len(clientes_encontrados) == 0:
        print("No se encontraron clientes.")
    else:
        Clientes.mostrar_encabezado_clientes()
        for cliente in clientes_encontrados:
            Clientes.mostrar_cliente(cliente)

    val_datos.pausar_menu()
    return clientes_encontrados


def buscar_reservas_por_periodo(reservas_lista, clientes_lista, habitaciones_lista, mes, anio):
    """
    Busca las reservas cuya fecha de ingreso cae en el mes y año indicados, usando una expresion regular
    con clase de caracteres y cuantificador para el dia: ^[0-9]{2}/mm/aaaa$.
    """

    patron = rf"^[0-9]{{2}}/{mes:02d}/{anio}$"
    reservas_encontradas = [reserva for reserva in reservas_lista if re.match(patron, reserva[3])]

    print(f"\nReservas con ingreso en {mes:02d}/{anio}:")
    if len(reservas_encontradas) == 0:
        print("No se encontraron reservas en ese período.")
    else:
        Reservas.mostrar_reservas_detalladas(reservas_encontradas, clientes_lista, habitaciones_lista)
        print(f"\nCantidad de reservas encontradas: {len(reservas_encontradas)}")

    val_datos.pausar_menu()
    return reservas_encontradas


def clientes_sin_reserva(clientes_lista, reservas_lista):
    """Muestra los clientes que no tienen ninguna reserva, usando la diferencia entre conjuntos de IDs."""

    ids_clientes = {cliente[0] for cliente in clientes_lista}
    ids_con_reserva = {reserva[1] for reserva in reservas_lista}
    ids_sin_reserva = ids_clientes - ids_con_reserva

    if len(ids_sin_reserva) == 0:
        print("Todos los clientes tienen al menos una reserva.")
    else:
        Clientes.mostrar_encabezado_clientes()
        for cliente in clientes_lista:
            if cliente[0] in ids_sin_reserva:
                Clientes.mostrar_cliente(cliente)
    val_datos.pausar_menu()
    return ids_sin_reserva


def habitaciones_reservadas_ambos_semestres(habitaciones_lista, reservas_lista):
    """
    Funcion que crea dos conjuntos que se separan en habitaciones reservadas en el
    primer semestre y habitaciones reservadas en el segundo semestre.
    Luego hace la interseccion de ambos conjuntos para ver que habitaciones estan reservadas en ambos semestres.
    """

    habitaciones_semestre_1 = {reserva[2] for reserva in reservas_lista if 1 <= int(reserva[3][3:5]) <= 6}
    habitaciones_semestre_2 = {reserva[2] for reserva in reservas_lista if 7 <= int(reserva[3][3:5]) <= 12}

    habitaciones_ambos_semestres = habitaciones_semestre_1.intersection(habitaciones_semestre_2)

    if len(habitaciones_ambos_semestres) == 0:
        print("No hay habitaciones reservadas en ambos semestres.")
    else:
        Habitaciones.mostrar_encabezado_habitaciones()
        for habitacion in habitaciones_lista:
            if habitacion[0] in habitaciones_ambos_semestres:
                Habitaciones.mostrar_habitacion(habitacion)

    val_datos.pausar_menu()
    return habitaciones_ambos_semestres


def listar_nombres_mayusculas(clientes_lista):
    """
    Funcion que utiliza map para crear una lista con el apellido en mayusculas
    y el nombre de cada cliente (formato 'APELLIDO, Nombre').
    """

    nombres_formateados = list(map(lambda cliente: f"{cliente[2].upper()}, {cliente[1]}", clientes_lista))

    for nombre in nombres_formateados:
        print(nombre)
    val_datos.pausar_menu()
    return nombres_formateados


def menu_matrices(clientes_lista, habitaciones_lista, reservas_lista):
    """
    Menu principal para gestionar las matrices del sistema.
    """
    opcion = -1

    while opcion != 0:
        titulo = " Menú Principal > Menú de Matrices "
        print(f"\n{titulo:-^50}")
        print("[1] Ordenar clientes por apellido")
        print("[2] Ordenar habitaciones por número")
        print("[3] Ordenar reservas por fecha de ingreso")
        print("[4] Ver habitaciones disponibles")
        print("[5] Buscar clientes por inicio de nombre o apellido")
        print("[6] Ver habitaciones reservadas en ambos semestres")
        print("[7] Ver clientes sin reservas")
        print("[8] Listar nombres en mayúsculas")
        print("[9] Buscar reservas por mes y año de ingreso")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 9)

        match opcion:
            case 1:
                val_datos.imprimir_titulo("Clientes ordenados por apellido")
                ordenar_por_apellido(clientes_lista)
            case 2:
                val_datos.imprimir_titulo("Habitaciones ordenadas por número")
                ordenar_por_numero(habitaciones_lista)
            case 3:
                val_datos.imprimir_titulo("Reservas ordenadas por fecha de ingreso")
                ordenar_por_fecha_ingreso(reservas_lista, clientes_lista, habitaciones_lista)
            case 4:
                val_datos.imprimir_titulo("Habitaciones disponibles")
                ver_habitaciones_disponibles(habitaciones_lista)
            case 5:
                val_datos.imprimir_titulo("Buscar clientes")
                texto = val_datos.pedir_texto("Ingrese la letra o el texto inicial a buscar: ", "texto de búsqueda")
                buscar_clientes_por_inicio(clientes_lista, texto)
            case 6:
                val_datos.imprimir_titulo("Habitaciones reservadas en ambos semestres")
                habitaciones_reservadas_ambos_semestres(habitaciones_lista, reservas_lista)
            case 7:
                val_datos.imprimir_titulo("Clientes sin reservas")
                clientes_sin_reserva(clientes_lista, reservas_lista)
            case 8:
                val_datos.imprimir_titulo("Nombres de clientes en mayúsculas")
                listar_nombres_mayusculas(clientes_lista)
            case 9:
                val_datos.imprimir_titulo("Buscar reservas por período")
                mes = val_datos.pedir_entero_rango("Ingrese el mes (1-12): ", 1, 12)
                anio = val_datos.pedir_entero_rango("Ingrese el año (2000-2100): ", 2000, 2100)
                buscar_reservas_por_periodo(reservas_lista, clientes_lista, habitaciones_lista, mes, anio)
            case 0:
                print("Saliendo del menú de matrices...")
