import os
from utilidades import val_datos


"""""""""""""""""""""""""""""""""""""""""""""""""""

Constantes de archivos.

"""""""""""""""""""""""""""""""""""""""""""""""""""

# Caracter que separa los campos de cada linea del archivo.
SEPARADOR = ";"

# Archivo auxiliar para las bajas y modificaciones. Existe solo mientras se reescribe el original.
RUTA_TEMPORAL = "datos/temp.txt"


"""""""""""""""""""""""""""""""""""""""""""""""""""

Conversion entre lineas del archivo y registros.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def linea_a_registro(linea, columnas_enteras):
    """
    Pasa una linea del archivo a una lista. Por ejemplo, '1;Juan;Pérez;32145678' queda como
    [1, 'Juan', 'Pérez', 32145678]. Las posiciones que vienen en columnas_enteras se pasan a int
    (si alguna no es un numero, salta un ValueError).
    """

    datos = linea.strip().split(SEPARADOR)
    for indice in columnas_enteras:
        datos[indice] = int(datos[indice])
    return datos


def registro_a_linea(registro):
    """Hace lo contrario: arma la linea con los campos separados por ';' y le agrega el salto de linea."""

    campos = [str(campo) for campo in registro]
    return SEPARADOR.join(campos) + "\n"


def leer_registro_de_linea(linea, columnas_enteras):
    """
    Igual que linea_a_registro, pero si la linea esta vacia o mal escrita no rompe el programa:
    avisa y devuelve una lista vacia. Asi una linea rota no frena todo el recorrido del archivo.
    """

    registro = []
    if linea.strip() != "":
        try:
            registro = linea_a_registro(linea, columnas_enteras)
        except (ValueError, IndexError):
            val_datos.imprimir_error(f"Se omite una línea con formato inválido: {linea.strip()}")
    return registro


"""""""""""""""""""""""""""""""""""""""""""""""""""

Busquedas en el archivo (se lee de a una linea, sin cargarlo entero en memoria).

"""""""""""""""""""""""""""""""""""""""""""""""""""


def buscar_registro(ruta, id_buscado, columnas_enteras):
    """
    Busca en el archivo el registro que tiene ese ID. Lee de a una linea y corta apenas lo encuentra.
    Si no esta, devuelve una lista vacia.
    """

    registro_encontrado = []
    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "" and len(registro_encontrado) == 0:
            registro = leer_registro_de_linea(linea, columnas_enteras)
            if len(registro) > 0 and registro[0] == id_buscado:
                registro_encontrado = registro
            linea = arch.readline()
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {ruta}.")
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return registro_encontrado


def existe_valor(ruta, columna, valor, id_excluido, columnas_enteras):
    """
    Se fija si algun registro del archivo ya tiene ese valor en esa columna (por ejemplo, para no repetir
    un DNI). El registro con id_excluido no se cuenta, asi al modificar un cliente no choca consigo mismo.
    """

    encontrado = False
    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "" and encontrado == False:
            registro = leer_registro_de_linea(linea, columnas_enteras)
            if len(registro) > columna and registro[columna] == valor and registro[0] != id_excluido:
                encontrado = True
            linea = arch.readline()
    except FileNotFoundError:
        # Si el archivo todavia no existe, no puede haber nada repetido.
        pass
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return encontrado


def obtener_proximo_id(ruta, columnas_enteras):
    """
    Recorre el archivo guardando el ID mas alto y devuelve el que sigue.
    Si el archivo no existe o esta vacio, arranca en 1.
    """

    mayor_id = 0
    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "":
            registro = leer_registro_de_linea(linea, columnas_enteras)
            if len(registro) > 0 and registro[0] > mayor_id:
                mayor_id = registro[0]
            linea = arch.readline()
    except FileNotFoundError:
        # Si el archivo todavia no existe, el primer ID es 1.
        pass
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return mayor_id + 1


"""""""""""""""""""""""""""""""""""""""""""""""""""

Alta, baja y modificacion sobre el archivo.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def agregar_registro(ruta, registro):
    """
    Alta: escribe el registro al final del archivo (modo 'a'). Si el archivo no existe, se crea.
    Devuelve True si se pudo grabar.
    """

    grabado = False
    try:
        arch = open(ruta, "at", encoding="UTF-8")
        arch.write(registro_a_linea(registro))
        grabado = True
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo grabar en el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return grabado


def reemplazar_registro(ruta, id_buscado, registro_nuevo, columnas_enteras):
    """
    Sirve para la baja y para la modificacion. Copiamos el archivo linea por linea a uno temporal y,
    cuando aparece el ID buscado, no lo copiamos (baja, registro_nuevo en None) o escribimos el registro
    nuevo en su lugar (modificacion). Al final borramos el original y renombramos el temporal.
    Devuelve True si encontro el ID y pudo guardar los cambios.
    """

    encontrado = False
    copia_completa = False

    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        aux = open(RUTA_TEMPORAL, "wt", encoding="UTF-8")

        linea = arch.readline()
        while linea != "":
            registro = leer_registro_de_linea(linea, columnas_enteras)
            if len(registro) > 0 and registro[0] == id_buscado:
                encontrado = True
                if registro_nuevo is not None:
                    aux.write(registro_a_linea(registro_nuevo))
            else:
                aux.write(linea)
            linea = arch.readline()

        copia_completa = True
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {ruta}.")
    except OSError as error:
        val_datos.imprimir_error(f"Error en el acceso al archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
            aux.close()
        except NameError:
            pass

    actualizado = False
    if encontrado and copia_completa:
        try:
            os.remove(ruta)
            os.rename(RUTA_TEMPORAL, ruta)
            actualizado = True
        except OSError as error:
            val_datos.imprimir_error(f"Error al reemplazar el archivo {ruta}: {error}")
    else:
        # Si no se encontro el ID o algo fallo, el original queda como estaba y el temporal se borra.
        try:
            os.remove(RUTA_TEMPORAL)
        except OSError:
            pass

    return actualizado


"""""""""""""""""""""""""""""""""""""""""""""""""""

Carga completa del archivo.

"""""""""""""""""""""""""""""""""""""""""""""""""""


def cargar_matriz(ruta, columnas_enteras):
    """
    Arma una matriz con todos los registros del archivo. No la usamos para el ABM: queda solo para
    los menus que necesitan todos los datos juntos, como ordenar o sacar estadisticas.
    """

    matriz = []
    try:
        arch = open(ruta, "rt", encoding="UTF-8")
        linea = arch.readline()
        while linea != "":
            registro = leer_registro_de_linea(linea, columnas_enteras)
            if len(registro) > 0:
                matriz.append(registro)
            linea = arch.readline()
    except FileNotFoundError:
        val_datos.imprimir_error(f"No se encontró el archivo {ruta}. Ejecute el programa desde la carpeta del proyecto.")
    except OSError as error:
        val_datos.imprimir_error(f"No se pudo leer el archivo {ruta}: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

    return matriz
