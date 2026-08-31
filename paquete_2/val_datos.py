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
