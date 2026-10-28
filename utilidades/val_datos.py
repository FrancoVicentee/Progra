import re


"""""""""""""""""""""""""""""""""""""""""""""""""""

Constantes del sistema (tuplas inmutables y patrones de expresiones regulares).

"""""""""""""""""""""""""""""""""""""""""""""""""""

TIPOS_HABITACION = ("Simple", "Doble", "Suite")
ESTADOS_HABITACION = ("Disponible", "Ocupada", "Mantenimiento")

# Rango de capacidad (minima, maxima) permitido para cada tipo de habitacion.
RANGOS_CAPACIDAD = {
    "Simple": (1, 1),
    "Doble": (1, 2),
    "Suite": (1, 6),
}

# Cantidad de dias de cada mes en un año no bisiesto (enero = posicion 0).
DIAS_POR_MES = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

DNI_MINIMO = 100000
DNI_MAXIMO = 100000000

# Solo digitos del 0 al 9, al menos uno.
PATRON_ENTERO = r"^[0-9]+$"

# Una o mas palabras formadas solo por letras, separadas por un unico espacio.
PATRON_TEXTO = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+( [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"

# Fecha dd/mm/aaaa. Cada grupo captura dia, mes y año respectivamente.
PATRON_FECHA = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"


"""""""""""""""""""""""""""""""""""""""""""""""""""

Validaciones numericas.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def es_entero(cadena):
    """Devuelve True si la cadena (sin espacios en los extremos) esta formada solo por digitos."""

    return re.match(PATRON_ENTERO, cadena.strip()) is not None


def pedir_entero_rango(mensaje, desde, hasta):
    """Pide un numero entero por teclado hasta que se ingrese uno valido dentro del rango [desde, hasta]."""

    valor_valido = False
    valor = None
    while valor_valido == False:
        entrada = input(mensaje)
        if es_entero(entrada):
            valor = int(entrada)
            if valor >= desde and valor <= hasta:
                valor_valido = True
            else:
                imprimir_error(f"Error. Ingrese un valor entre {desde} y {hasta}.")
        else:
            imprimir_error("Error. Debe ingresar un número entero.")
    return valor


def es_entero_en_rango(cadena, desde, hasta):
    """Devuelve True si la cadena es un entero valido y su valor esta dentro del rango [desde, hasta]."""

    return es_entero(cadena) and desde <= int(cadena) <= hasta


def pedir_confirmacion(mensaje):
    """Pide al usuario que confirme una operacion. Devuelve True si responde 1 (Si) y False si responde 0 (No)."""

    respuesta = pedir_entero_rango(f"{mensaje} [1] Sí [0] No: ", 0, 1)
    return respuesta == 1


"""""""""""""""""""""""""""""""""""""""""""""""""""

Validaciones y operaciones con fechas.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def es_bisiesto(anio):
    """Devuelve True si el año recibido es bisiesto."""

    return (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0


def dias_del_mes(mes, anio):
    """Devuelve la cantidad de dias que tiene el mes indicado (1-12) en el año indicado."""

    if mes == 2 and es_bisiesto(anio):
        return 29
    return DIAS_POR_MES[mes - 1]


def validar_fecha(fecha):
    """
    Valida una fecha en formato dd/mm/aaaa usando una expresion regular con grupos.
    Ademas del formato, controla que el dia exista en ese mes
    (por ejemplo, rechaza 31/04 o 29/02 en años no bisiestos).
    """

    coincidencia = re.match(PATRON_FECHA, fecha.strip())
    if coincidencia is None:
        return False

    dia = int(coincidencia.group(1))
    mes = int(coincidencia.group(2))
    anio = int(coincidencia.group(3))

    return dia <= dias_del_mes(mes, anio)


def pedir_fecha_valida(mensaje):
    """Pide una fecha por teclado hasta que tenga formato dd/mm/aaaa y sea una fecha real."""

    fecha = input(mensaje).strip()
    while validar_fecha(fecha) == False:
        imprimir_error("Error. Fecha inválida. Use el formato dd/mm/aaaa con una fecha existente.")
        fecha = input(mensaje).strip()
    return fecha


def separar_fecha(fecha):
    """Separa una fecha dd/mm/aaaa y devuelve una tupla de enteros (dia, mes, anio)."""

    partes = fecha.strip().split("/")
    return int(partes[0]), int(partes[1]), int(partes[2])


def convertir_fecha_a_numero(fecha):
    """
    Toma una fecha en formato dd/mm/aaaa y la pasa a un numero
    tipo aaaammdd. Lo hacemos asi para poder comparar fechas
    facil con mayor o menor, en vez de comparar el texto y asi poder ordenarlas mas facil.
    """

    dia = fecha[0:2]
    mes = fecha[3:5]
    anio = fecha[6:10]
    return int(anio + mes + dia)


def comparar_fechas(fecha1, fecha2):
    """Compara dos fechas dd/mm/aaaa. Devuelve 1 si fecha1 es posterior, -1 si es anterior y 0 si son iguales."""

    numero1 = convertir_fecha_a_numero(fecha1)
    numero2 = convertir_fecha_a_numero(fecha2)
    if numero1 > numero2:
        return 1
    elif numero1 < numero2:
        return -1
    else:
        return 0


def fecha_a_dias(fecha):
    """
    Convierte una fecha dd/mm/aaaa en la cantidad de dias transcurridos desde el 01/01/0001.
    Sirve para poder restar dos fechas y obtener la cantidad de noches de una reserva.
    """

    dia, mes, anio = separar_fecha(fecha)
    anios_previos = anio - 1
    dias = anios_previos * 365 + anios_previos // 4 - anios_previos // 100 + anios_previos // 400

    mes_actual = 1
    while mes_actual < mes:
        dias += dias_del_mes(mes_actual, anio)
        mes_actual += 1

    return dias + dia


def calcular_noches(fecha_ingreso, fecha_egreso):
    """Devuelve la cantidad de noches que hay entre la fecha de ingreso y la fecha de egreso."""

    return fecha_a_dias(fecha_egreso) - fecha_a_dias(fecha_ingreso)


"""""""""""""""""""""""""""""""""""""""""""""""""""

Funciones genericas sobre matrices (listas de listas cuyo primer elemento es el ID).

"""""""""""""""""""""""""""""""""""""""""""""""""""


def generar_id(lista):
    """Calcula el proximo ID libre de una matriz usando map y max. Devuelve 1 si la matriz esta vacia."""

    if len(lista) == 0:
        return 1
    ids = list(map(lambda registro: registro[0], lista))
    return max(ids) + 1


def existe_id(lista, id_valor):
    """Devuelve True si existe un registro en la matriz cuyo ID (posicion 0) coincida con id_valor."""

    coincidencias = list(filter(lambda registro: registro[0] == id_valor, lista))
    return len(coincidencias) > 0


def buscar_por_id(lista, id_valor, indice=0):
    """
    Devuelve el registro de la matriz con el ID indicado, o una lista vacia si no existe.
    Caso base 1: indice >= len(lista), se recorrio todo y no esta: devuelve [].
    Caso base 2: lista[indice][0] == id_valor: lo encontro y lo devuelve.
    Caso recursivo: busca de nuevo desde indice + 1. El dominio se reduce en un elemento por llamada.
    """

    if indice >= len(lista):
        return []
    if lista[indice][0] == id_valor:
        return lista[indice]
    return buscar_por_id(lista, id_valor, indice + 1)


def total_noches(reservas, indice=0):
    """
    Devuelve el total de noches de una matriz de reservas.
    Caso base: indice >= len(reservas): no quedan reservas y devuelve 0.
    Caso recursivo: noches de la reserva actual + total_noches desde indice + 1.
    El dominio se reduce en una reserva por llamada.
    """

    if indice >= len(reservas):
        return 0
    return calcular_noches(reservas[indice][3], reservas[indice][4]) + total_noches(reservas, indice + 1)


def pausar_menu():
    """Detiene la ejecucion hasta que el usuario ingrese 0, para que pueda leer la informacion en pantalla."""

    pedir_entero_rango("\nPresione 0 para volver: ", 0, 0)


"""""""""""""""""""""""""""""""""""""""""""""""""""

Validaciones de texto (nombres, apellidos y DNI).

"""""""""""""""""""""""""""""""""""""""""""""""""""


def normalizar_espacios(texto):
    """Elimina los espacios de los extremos y deja un unico espacio entre palabras."""

    return " ".join(texto.strip().split())


def normalizar_nombre(texto):
    """Normaliza un nombre propio: quita espacios sobrantes y pone en mayuscula la inicial de cada palabra."""

    return normalizar_espacios(texto).title()


def es_texto(texto):
    """Devuelve True si el texto contiene solo letras (con o sin tildes) y espacios entre palabras."""

    return re.match(PATRON_TEXTO, normalizar_espacios(texto)) is not None


def pedir_texto(mensaje, campo):
    """Pide un texto formado solo por letras y lo devuelve normalizado. 'campo' se usa en el mensaje de error."""

    texto = input(mensaje)
    while es_texto(texto) == False:
        imprimir_error(f"Error. El {campo} solo puede contener letras.")
        texto = input(mensaje)
    return normalizar_nombre(texto)


def pedir_nombre(mensaje):
    """Pide un nombre valido por teclado y lo devuelve normalizado."""

    return pedir_texto(mensaje, "nombre")


def pedir_apellido(mensaje):
    """Pide un apellido valido por teclado y lo devuelve normalizado."""

    return pedir_texto(mensaje, "apellido")


def pedir_dni(mensaje):
    """Pide un DNI por teclado dentro del rango permitido y lo devuelve como entero."""

    return pedir_entero_rango(mensaje, DNI_MINIMO, DNI_MAXIMO)


"""""""""""""""""""""""""""""""""""""""""""""""""""

Validaciones de habitaciones (tipo y estado).

"""""""""""""""""""""""""""""""""""""""""""""""""""


def normalizar_capitalizado(texto):
    """Quita los espacios de los extremos y deja solo la primera letra en mayuscula."""

    return texto.strip().capitalize()


def es_tipo_valido(tipo):
    """Devuelve True si el tipo de habitacion ingresado es Simple, Doble o Suite (sin importar mayusculas)."""

    return normalizar_capitalizado(tipo) in TIPOS_HABITACION


def pedir_tipo_habitacion(mensaje):
    """Pide un tipo de habitacion valido y lo devuelve capitalizado."""

    tipo = input(mensaje)
    while es_tipo_valido(tipo) == False:
        imprimir_error("Error. Debe ingresar Simple, Doble o Suite (mayúsculas o minúsculas).")
        tipo = input(mensaje)
    return normalizar_capitalizado(tipo)


def es_estado_valido(estado):
    """Devuelve True si el estado ingresado es Disponible, Ocupada o Mantenimiento (sin importar mayusculas)."""

    return normalizar_capitalizado(estado) in ESTADOS_HABITACION


def pedir_estado_habitacion(mensaje):
    """Pide un estado de habitacion valido y lo devuelve capitalizado."""

    estado = input(mensaje)
    while es_estado_valido(estado) == False:
        imprimir_error("Error. Debe ingresar Disponible, Ocupada o Mantenimiento (mayúsculas o minúsculas).")
        estado = input(mensaje)
    return normalizar_capitalizado(estado)


"""""""""""""""""""""""""""""""""""""""""""""""""""

Funciones para imprimir mensajes en color (éxito / error) y titulos.

"""""""""""""""""""""""""""""""""""""""""""""""""""

COLOR_ROJO = "\033[91m"
COLOR_VERDE = "\033[92m"
COLOR_RESET = "\033[0m"


def imprimir_error(mensaje):
    """Imprime un mensaje de error en color rojo."""

    print(f"{COLOR_ROJO}{mensaje}{COLOR_RESET}")


def imprimir_exito(mensaje):
    """Imprime un mensaje de exito en color verde."""

    print(f"{COLOR_VERDE}{mensaje}{COLOR_RESET}")


def imprimir_titulo(texto):
    """Imprime un titulo centrado entre guiones con un ancho de 50 caracteres."""

    titulo = f" {texto} "
    print(f"\n{titulo:-^50}")
