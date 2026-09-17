import re
 
def es_entero(cadena):
    return cadena.isnumeric()
 
 
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
                print(f"Error. Ingrese un valor entre {desde} y {hasta}.")
        else:
            print("Error. Debe ingresar un número entero.")
    return valor




def validar_fecha(fecha):
 
    if len(fecha) != 10:
        return False
    if fecha[2] != "/" or fecha[5] != "/":
        return False
 
    dia = fecha[0:2]
    mes = fecha[3:5]
    anio = fecha[6:10]
 
    if es_entero(dia) == False or es_entero(mes) == False or es_entero(anio) == False:
        return False
 
    dia_numero = int(dia)
    mes_numero = int(mes)
 
    if dia_numero < 1 or dia_numero > 31:
        return False
    if mes_numero < 1 or mes_numero > 12:
        return False
 
    return True
 
 
def pedir_fecha_valida(mensaje):
 
    fecha_valida = False
    fecha = ""
    while fecha_valida == False:
        fecha = input(mensaje).strip()
        if validar_fecha(fecha):
            fecha_valida = True
        else:
            print("Error. Formato de fecha inválido. Use dd/mm/aaaa.")
    return fecha
 
 
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
    numero1 = convertir_fecha_a_numero(fecha1)
    numero2 = convertir_fecha_a_numero(fecha2)
    if numero1 > numero2:
        return 1
    elif numero1 < numero2:
        return -1
    else:
        return 0
 
 
def existe_id(lista, id_valor):
    coincidencias = list(filter(lambda registro: registro[0] == id_valor, lista))
    return len(coincidencias) > 0
 
 
def pausar_menu():
    opcion = -1
    while opcion != 0:
        opcion = pedir_entero_rango("\nPresione 0 para volver: ", 0, 0)
 
 
def es_texto(texto):
    if texto == "":
        return False
    if texto.isspace():
        return False
    if not texto.replace(" ", "").isalpha():
        return False
    return True
 
 
def pedir_nombre(mensaje):
    nombre = input(mensaje)
    while es_texto(nombre) == False:
        print("Error. El nombre solo puede contener letras.")
        nombre = input(mensaje)
    return nombre
 
 

 
 
def pedir_apellido(mensaje):
    apellido = input(mensaje)
    while es_texto(apellido) == False:
        print("Error. El apellido solo puede contener letras.")
        apellido = input(mensaje)
    return apellido
 

 
 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Validaciones de habitaciones (tipo y estado).
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
 
def normalizar_capitalizado(texto):
    return texto.strip().capitalize()
 
 
def es_tipo_valido(tipo):
    tipos_validos = ("Simple", "Doble", "Suite")
    return normalizar_capitalizado(tipo) in tipos_validos
 
 
def pedir_tipo_habitacion(mensaje):
    tipo = input(mensaje)
    while es_tipo_valido(tipo) == False:
        print("Error. Debe ingresar Simple, Doble o Suite (mayúsculas o minúsculas).")
        tipo = input(mensaje)
    return normalizar_capitalizado(tipo)
 
 
def es_estado_valido(estado):
    estados_validos = ("Disponible", "Ocupada", "Mantenimiento")
    return normalizar_capitalizado(estado) in estados_validos
 
 
def pedir_estado_habitacion(mensaje):
    estado = input(mensaje)
    while es_estado_valido(estado) == False:
        print("Error. Debe ingresar Disponible, Ocupada o Mantenimiento (mayúsculas o minúsculas).")
        estado = input(mensaje)
    return normalizar_capitalizado(estado)


"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Funciones para imprimir mensajes en color (éxito / error).
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
COLOR_ROJO = "\033[91m"
COLOR_VERDE = "\033[92m"
COLOR_RESET = "\033[0m"
 
 
def imprimir_error(mensaje):
    print(f"{COLOR_ROJO}{mensaje}{COLOR_RESET}")
 
 
def imprimir_exito(mensaje):
    print(f"{COLOR_VERDE}{mensaje}{COLOR_RESET}")
 