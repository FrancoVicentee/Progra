from functools import reduce
from utilidades import val_datos



def calcular_promedio(valores):
    """Devuelve el promedio de una lista de numeros, o 0 si la lista esta vacia."""

    if len(valores) == 0:
        return 0
    return sum(valores) / len(valores)


def calcular_porcentaje(parte, total):
    """Devuelve el porcentaje que representa 'parte' sobre 'total', o 0 si el total es 0."""

    if total == 0:
        return 0
    return parte / total * 100


def contar_por_categoria(lista, indice_columna, categorias):
    """
    Cuenta cuantos registros de la matriz tienen cada categoria en la columna indicada.
    Devuelve un diccionario {categoria: cantidad}. Usa filter y lambda.
    """

    conteo = {}
    for categoria in categorias:
        conteo[categoria] = len(list(filter(lambda registro: registro[indice_columna] == categoria, lista)))
    return conteo


def calcular_noches_reserva(reserva):
    """Devuelve la cantidad de noches de una reserva."""

    return val_datos.calcular_noches(reserva[3], reserva[4])


def obtener_tipo_de_reserva(reserva, habitaciones_lista):
    """Devuelve el tipo de la habitacion asociada a la reserva, o una cadena vacia si la habitacion no existe."""

    habitacion = val_datos.buscar_por_id(habitaciones_lista, reserva[2])
    if len(habitacion) == 0:
        return ""
    return habitacion[2]


def contar_reservas_por_cliente(clientes_lista, reservas_lista):
    """Devuelve un diccionario {id_cliente: cantidad_de_reservas} con todos los clientes (incluso los que tienen 0)."""

    conteo = {}
    for cliente in clientes_lista:
        conteo[cliente[0]] = 0
    for reserva in reservas_lista:
        if reserva[1] in conteo:
            conteo[reserva[1]] += 1
    return conteo


def imprimir_tabla_categorias(titulo_columna, conteo, total):
    """Imprime una tabla con cantidad y porcentaje sobre el total de cada categoria del diccionario conteo."""

    print(f"{titulo_columna:<16}{'Cantidad':>10}{'Porcentaje':>14}")
    print("-" * 40)
    for categoria, cantidad in conteo.items():
        porcentaje = calcular_porcentaje(cantidad, total)
        print(f"{categoria:<16}{cantidad:>10}{porcentaje:>13.1f}%")
    print("-" * 40)
    print(f"{'Total':<16}{total:>10}{calcular_porcentaje(total, total):>13.1f}%")


"""""""""""""""""""""""""""""""""""""""""""""""""""

Estadisticas de habitaciones.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def calcular_capacidad_total(habitaciones_lista):
    """Calcula y muestra la suma total de las capacidades de todas las habitaciones utilizando la función reduce."""

    capacidad_total = reduce(lambda total, habitacion: total + habitacion[3], habitaciones_lista, 0)
    print(f"Capacidad total del hotel: {capacidad_total} personas")
    print(f"Cantidad de habitaciones: {len(habitaciones_lista)}")
    val_datos.pausar_menu()
    return capacidad_total


def promedio_capacidad_habitaciones(habitaciones_lista):
    """Muestra el promedio general de capacidad y el promedio de capacidad por tipo de habitacion (categoria)."""

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        val_datos.pausar_menu()
        return {}

    capacidades = [habitacion[3] for habitacion in habitaciones_lista]
    promedio_general = calcular_promedio(capacidades)
    print(f"Promedio general de capacidad: {promedio_general:.2f} personas\n")

    promedios_por_tipo = {}
    print(f"{'Tipo':<12}{'Habitaciones':>14}{'Promedio capacidad':>22}")
    print("-" * 48)
    for tipo in val_datos.TIPOS_HABITACION:
        capacidades_tipo = [habitacion[3] for habitacion in habitaciones_lista if habitacion[2] == tipo]
        promedios_por_tipo[tipo] = calcular_promedio(capacidades_tipo)
        print(f"{tipo:<12}{len(capacidades_tipo):>14}{promedios_por_tipo[tipo]:>22.2f}")

    val_datos.pausar_menu()
    return promedios_por_tipo


def conteo_habitaciones_por_estado(habitaciones_lista):
    """Muestra la cantidad de habitaciones de cada estado y su porcentaje sobre el total (incluye el % de ocupación)."""

    total = len(habitaciones_lista)
    conteo = contar_por_categoria(habitaciones_lista, 4, val_datos.ESTADOS_HABITACION)

    imprimir_tabla_categorias("Estado", conteo, total)
    print(f"\nPorcentaje de ocupación del hotel: {calcular_porcentaje(conteo['Ocupada'], total):.1f}%")

    val_datos.pausar_menu()
    return conteo


def conteo_habitaciones_por_tipo(habitaciones_lista):
    """Muestra la cantidad de habitaciones de cada tipo y su porcentaje sobre el total."""

    total = len(habitaciones_lista)
    conteo = contar_por_categoria(habitaciones_lista, 2, val_datos.TIPOS_HABITACION)

    imprimir_tabla_categorias("Tipo", conteo, total)

    val_datos.pausar_menu()
    return conteo


def habitacion_capacidad_max_min(habitaciones_lista):
    """Identifica y muestra las habitaciones con la mayor y menor capacidad utilizando funciones lambda."""

    if len(habitaciones_lista) == 0:
        print("No hay habitaciones cargadas.")
        val_datos.pausar_menu()
        return

    mayor = max(habitaciones_lista, key=lambda habitacion: habitacion[3])
    menor = min(habitaciones_lista, key=lambda habitacion: habitacion[3])
    print(f"Mayor capacidad: habitación {mayor[1]} ({mayor[2]}) con {mayor[3]} persona(s)")
    print(f"Menor capacidad: habitación {menor[1]} ({menor[2]}) con {menor[3]} persona(s)")
    val_datos.pausar_menu()


"""""""""""""""""""""""""""""""""""""""""""""""""""

Estadisticas de reservas y clientes.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def estadisticas_reservas(reservas_lista, habitaciones_lista):
    """
    Muestra estadisticas calculadas a partir de las reservas: total de noches, noches promedio,
    reserva mas larga y mas corta, y por tipo de habitacion la cantidad de reservas,
    su porcentaje sobre el total y el promedio de noches.
    """

    total_reservas = len(reservas_lista)
    if total_reservas == 0:
        print("No hay reservas registradas.")
        val_datos.pausar_menu()
        return

    total_noches = reduce(lambda acumulado, reserva: acumulado + calcular_noches_reserva(reserva), reservas_lista, 0)
    mas_larga = max(reservas_lista, key=lambda reserva: calcular_noches_reserva(reserva))
    mas_corta = min(reservas_lista, key=lambda reserva: calcular_noches_reserva(reserva))

    print(f"Total de reservas: {total_reservas}")
    print(f"Total de noches reservadas: {total_noches}")
    print(f"Promedio de noches por reserva: {total_noches / total_reservas:.2f}")
    print(f"Reserva más larga: ID {mas_larga[0]} ({calcular_noches_reserva(mas_larga)} noches, "
          f"{mas_larga[3]} al {mas_larga[4]})")
    print(f"Reserva más corta: ID {mas_corta[0]} ({calcular_noches_reserva(mas_corta)} noches, "
          f"{mas_corta[3]} al {mas_corta[4]})")

    print(f"\n{'Tipo':<12}{'Reservas':>10}{'Porcentaje':>13}{'Noches prom.':>15}")
    print("-" * 50)
    for tipo in val_datos.TIPOS_HABITACION:
        reservas_tipo = [reserva for reserva in reservas_lista if obtener_tipo_de_reserva(reserva, habitaciones_lista) == tipo]
        noches_tipo = list(map(calcular_noches_reserva, reservas_tipo))
        porcentaje = calcular_porcentaje(len(reservas_tipo), total_reservas)
        print(f"{tipo:<12}{len(reservas_tipo):>10}{porcentaje:>12.1f}%{calcular_promedio(noches_tipo):>15.2f}")

    val_datos.pausar_menu()


def clientes_con_mas_reservas(clientes_lista, reservas_lista):
    """
    Muestra un ranking de clientes ordenado por cantidad de reservas (de mayor a menor),
    el porcentaje de reservas que representa cada uno y el porcentaje de clientes con al menos una reserva.
    """

    if len(clientes_lista) == 0:
        print("No hay clientes cargados.")
        val_datos.pausar_menu()
        return {}

    conteo = contar_reservas_por_cliente(clientes_lista, reservas_lista)
    total_reservas = len(reservas_lista)

    ranking = sorted(clientes_lista, key=lambda cliente: conteo[cliente[0]], reverse=True)

    print(f"{'Puesto':<8}{'Cliente':<25}{'Reservas':>10}{'% del total':>14}")
    print("-" * 57)
    puesto = 1
    for cliente in ranking:
        nombre_completo = f"{cliente[1]} {cliente[2]}"
        porcentaje = calcular_porcentaje(conteo[cliente[0]], total_reservas)
        print(f"{puesto:<8}{nombre_completo[:24]:<25}{conteo[cliente[0]]:>10}{porcentaje:>13.1f}%")
        puesto += 1

    clientes_con_reserva = {reserva[1] for reserva in reservas_lista}
    porcentaje_activos = calcular_porcentaje(len(clientes_con_reserva), len(clientes_lista))
    print(f"\nClientes con al menos una reserva: {len(clientes_con_reserva)} de {len(clientes_lista)} "
          f"({porcentaje_activos:.1f}%)")

    val_datos.pausar_menu()
    return conteo


def resumen_estadistico(clientes_lista, habitaciones_lista, reservas_lista):
    """Muestra un resumen general con totales, promedios, maximos, minimos y conteos especificos del sistema."""

    val_datos.imprimir_titulo("Resumen estadístico general")
    print(f"Total de clientes: {len(clientes_lista)}")
    print(f"Total de habitaciones: {len(habitaciones_lista)}")
    print(f"Total de reservas: {len(reservas_lista)}")

    if len(habitaciones_lista) > 0:
        capacidades = [habitacion[3] for habitacion in habitaciones_lista]
        conteo_estados = contar_por_categoria(habitaciones_lista, 4, val_datos.ESTADOS_HABITACION)

        print("\nCapacidad de habitaciones:")
        print(f"  Total: {sum(capacidades)} | Promedio: {calcular_promedio(capacidades):.2f} | "
              f"Máxima: {max(capacidades)} | Mínima: {min(capacidades)}")

        print("\nHabitaciones por estado:")
        for estado, cantidad in conteo_estados.items():
            print(f"  {estado}: {cantidad} ({calcular_porcentaje(cantidad, len(habitaciones_lista)):.1f}%)")

    if len(reservas_lista) > 0:
        noches = list(map(calcular_noches_reserva, reservas_lista))

        print("\nNoches por reserva:")
        print(f"  Total: {sum(noches)} | Promedio: {calcular_promedio(noches):.2f} | "
              f"Máxima: {max(noches)} | Mínima: {min(noches)}")

    if len(clientes_lista) > 0:
        ids_clientes = {cliente[0] for cliente in clientes_lista}
        ids_con_reserva = {reserva[1] for reserva in reservas_lista}
        print("\nClientes:")
        print(f"  Con reservas: {len(ids_clientes & ids_con_reserva)} | Sin reservas: {len(ids_clientes - ids_con_reserva)}")

    val_datos.pausar_menu()


def menu_estadisticas(clientes_lista, habitaciones_lista, reservas_lista):
    """
    Menu principal para consultar las estadísticas del sistema.
    """
    opcion = -1

    while opcion != 0:
        titulo = " Menú Principal > Menú de Estadísticas "
        print(f"\n{titulo:-^50}")
        print("[1] Ver capacidad total del hotel")
        print("[2] Promedio de capacidad (general y por tipo)")
        print("[3] Habitaciones por estado (cantidad y %)")
        print("[4] Habitaciones por tipo (cantidad y %)")
        print("[5] Habitación con mayor y menor capacidad")
        print("[6] Estadísticas de reservas")
        print("[7] Clientes con más reservas")
        print("[8] Resumen estadístico general")
        print("-" * 50)
        print("[0] Volver al menú anterior")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 8)

        match opcion:
            case 1:
                val_datos.imprimir_titulo("Capacidad total del hotel")
                calcular_capacidad_total(habitaciones_lista)
            case 2:
                val_datos.imprimir_titulo("Promedio de capacidad")
                promedio_capacidad_habitaciones(habitaciones_lista)
            case 3:
                val_datos.imprimir_titulo("Habitaciones por estado")
                conteo_habitaciones_por_estado(habitaciones_lista)
            case 4:
                val_datos.imprimir_titulo("Habitaciones por tipo")
                conteo_habitaciones_por_tipo(habitaciones_lista)
            case 5:
                val_datos.imprimir_titulo("Habitación con mayor y menor capacidad")
                habitacion_capacidad_max_min(habitaciones_lista)
            case 6:
                val_datos.imprimir_titulo("Estadísticas de reservas")
                estadisticas_reservas(reservas_lista, habitaciones_lista)
            case 7:
                val_datos.imprimir_titulo("Clientes con más reservas")
                clientes_con_mas_reservas(clientes_lista, reservas_lista)
            case 8:
                resumen_estadistico(clientes_lista, habitaciones_lista, reservas_lista)
            case 0:
                print("Saliendo del menú de estadísticas...")