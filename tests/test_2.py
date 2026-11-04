from utilidades import val_datos


def test_validar_fecha():
    """Acepta fechas reales dd/mm/aaaa y rechaza formatos o dias inexistentes."""
    assert val_datos.validar_fecha("15/09/2026") is True
    assert val_datos.validar_fecha("29/02/2024") is True
    assert val_datos.validar_fecha("29/02/2026") is False
    assert val_datos.validar_fecha("31/04/2026") is False
    assert val_datos.validar_fecha("15-09-2026") is False
    assert val_datos.validar_fecha("15/13/2026") is False


def test_calcular_noches():
    """Calcula las noches entre dos fechas, cruzando meses, años y febrero."""
    assert val_datos.calcular_noches("01/09/2026", "15/09/2026") == 14
    assert val_datos.calcular_noches("28/08/2026", "02/09/2026") == 5
    assert val_datos.calcular_noches("30/12/2026", "02/01/2027") == 3
    # Febrero bisiesto tiene 29 dias y el no bisiesto 28.
    assert val_datos.calcular_noches("28/02/2024", "01/03/2024") == 2
    assert val_datos.calcular_noches("28/02/2026", "01/03/2026") == 1


def test_total_noches():
    """Suma recursivamente las noches de una lista de reservas."""
    reservas = [
        [1, 1, 101, "01/09/2026", "15/09/2026"],
        [2, 2, 102, "28/08/2026", "02/09/2026"],
    ]
    assert val_datos.total_noches(reservas) == 19
    # Caso base: sin reservas el total es 0.
    assert val_datos.total_noches([]) == 0
