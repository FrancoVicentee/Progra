import os
from utilidades import archivos, estadisticas
from gestion import Reservas


RUTA_TXT = "tests/prueba_temp.txt"
RUTA_JSON = "tests/prueba_temp.json"


def test_grabar_y_leer_json():
    """Grabar un diccionario y volver a leerlo devuelve el mismo diccionario."""
    datos = {"100": {"nombre": "Ana", "sueldo": 150000}}
    grabado = archivos.grabar_json(RUTA_JSON, datos)
    leido = archivos.leer_json(RUTA_JSON)
    os.remove(RUTA_JSON)
    assert grabado is True
    assert leido == datos


def test_solapamiento_fechas():
    """Detecta si las fechas nuevas se pisan con una reserva existente de la misma habitacion."""
    arch = open(RUTA_TXT, "w", encoding="UTF-8")
    arch.write("1;1;3;01/09/2026;15/09/2026\n")
    arch.close()

    se_pisan = Reservas.existe_solapamiento(2, 3, "10/09/2026", "20/09/2026", -1, RUTA_TXT)
    # Si el ingreso nuevo es el mismo dia del egreso existente, no se pisan.
    egreso_igual_a_ingreso = Reservas.existe_solapamiento(2, 3, "15/09/2026", "20/09/2026", -1, RUTA_TXT)
    # Al modificar la reserva 1 no tiene que chocar consigo misma.
    excluyendo_la_propia = Reservas.existe_solapamiento(2, 3, "10/09/2026", "20/09/2026", 1, RUTA_TXT)
    os.remove(RUTA_TXT)

    assert se_pisan is True
    assert egreso_igual_a_ingreso is False
    assert excluyendo_la_propia is False


def test_contar_reservas_de_cliente():
    """Cuenta recursivamente las reservas de un cliente."""
    reservas = [
        [1, 1, 101, "01/09/2026", "03/09/2026"],
        [2, 2, 102, "10/09/2026", "15/09/2026"],
        [3, 1, 103, "20/09/2026", "22/09/2026"],
    ]
    assert estadisticas.contar_reservas_de_cliente(reservas, 1) == 2
    assert estadisticas.contar_reservas_de_cliente(reservas, 99) == 0
    # Caso base: lista vacia.
    assert estadisticas.contar_reservas_de_cliente([], 1) == 0
