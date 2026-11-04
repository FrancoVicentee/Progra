import os
from utilidades import archivos
from gestion import Reservas


RUTA_TXT = "tests/prueba_temp.txt"
RUTA_JSON = "tests/prueba_temp.json"


def crear_reservas_temporal():
    """Crea un archivo de reservas de prueba con una sola reserva."""
    arch = open(RUTA_TXT, "w", encoding="UTF-8")
    arch.write("1;1;3;01/09/2026;15/09/2026\n")
    arch.close()


def test_registro_a_linea():
    """Arma la linea con los campos separados por ';' y el salto de linea."""
    assert archivos.registro_a_linea([1, "Juan", "Pérez", 32145678]) == "1;Juan;Pérez;32145678\n"


def test_ida_y_vuelta_registro():
    """Pasar un registro a linea y volver devuelve el mismo registro."""
    registro = [1, "Juan", "Pérez", 32145678]
    assert archivos.linea_a_registro(archivos.registro_a_linea(registro), (0, 3)) == registro


def test_leer_json_archivo_inexistente():
    """Sin valor por defecto, un JSON que no existe devuelve None."""
    assert archivos.leer_json(RUTA_JSON) is None


def test_leer_json_inexistente_con_valor_por_defecto():
    """Con valor por defecto, un JSON que no existe devuelve ese valor."""
    assert archivos.leer_json(RUTA_JSON, {}) == {}


def test_leer_json_roto():
    """Un JSON con formato invalido devuelve None."""
    arch = open(RUTA_JSON, "w", encoding="UTF-8")
    arch.write("{roto")
    arch.close()
    resultado = archivos.leer_json(RUTA_JSON)
    os.remove(RUTA_JSON)
    assert resultado is None


def test_grabar_y_leer_json():
    """Grabar un diccionario y volver a leerlo devuelve el mismo diccionario."""
    datos = {"100": {"nombre": "Ana", "sueldo": 150000}}
    grabado = archivos.grabar_json(RUTA_JSON, datos)
    leido = archivos.leer_json(RUTA_JSON)
    os.remove(RUTA_JSON)
    assert grabado is True
    assert leido == datos


def test_solapamiento_fechas_que_se_pisan():
    """Misma habitacion con fechas que se pisan hay solapamiento."""
    crear_reservas_temporal()
    resultado = Reservas.existe_solapamiento(2, 3, "10/09/2026", "20/09/2026", -1, RUTA_TXT)
    os.remove(RUTA_TXT)
    assert resultado is True


def test_solapamiento_egreso_igual_a_ingreso():
    """Si el ingreso nuevo es igual al egreso existente no hay solapamiento."""
    crear_reservas_temporal()
    resultado = Reservas.existe_solapamiento(2, 3, "15/09/2026", "20/09/2026", -1, RUTA_TXT)
    os.remove(RUTA_TXT)
    assert resultado is False


def test_solapamiento_excluyendo_la_propia_reserva():
    """Al excluir la reserva existente no choca consigo misma."""
    crear_reservas_temporal()
    resultado = Reservas.existe_solapamiento(2, 3, "10/09/2026", "20/09/2026", 1, RUTA_TXT)
    os.remove(RUTA_TXT)
    assert resultado is False