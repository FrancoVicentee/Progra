def es_entero(cadena):

    if cadena == "":
        return False
    inicio = 1 if cadena[0] == "-" else 0
    if inicio == 1 and len(cadena) == 1:
        return False
    for i in range(inicio, len(cadena)):
        if cadena[i] < "0" or cadena[i] > "9":
            return False
    return True


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
