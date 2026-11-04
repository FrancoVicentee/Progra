from utilidades import val_datos


def test_calcular_noches_mismo_mes():
    """Calcula las noches entre dos fechas del mismo mes."""
    assert val_datos.calcular_noches("01/09/2026", "15/09/2026") == 14


def test_calcular_noches_cruzando_mes():
    """Calcula las noches cuando la reserva cruza de un mes al siguiente."""
    assert val_datos.calcular_noches("28/08/2026", "02/09/2026") == 5


def test_calcular_noches_febrero_bisiesto():
    """En un año bisiesto febrero tiene 29 dias, asi que hay 2 noches."""
    assert val_datos.calcular_noches("28/02/2024", "01/03/2024") == 2


def test_calcular_noches_febrero_no_bisiesto():
    """En un año no bisiesto febrero tiene 28 dias, asi que hay 1 noche."""
    assert val_datos.calcular_noches("28/02/2026", "01/03/2026") == 1


def test_calcular_noches_cruzando_anio():
    """Calcula las noches cuando la reserva cruza de un año al siguiente."""
    assert val_datos.calcular_noches("30/12/2026", "02/01/2027") == 3


def test_total_noches_lista_vacia():
    """Caso base: sin reservas el total de noches es 0."""
    assert val_datos.total_noches([]) == 0


def test_total_noches_dos_reservas():
    """Suma las noches de dos reservas (14 + 5)."""
    reservas = [
        [1, 1, 101, "01/09/2026", "15/09/2026"],
        [2, 2, 102, "28/08/2026", "02/09/2026"],
    ]
    assert val_datos.total_noches(reservas) == 19


def test_total_noches_tres_reservas():
    """Suma las noches de tres reservas (2 + 5 + 2, una de ellas en febrero bisiesto)."""
    reservas = [
        [1, 1, 101, "01/09/2026", "03/09/2026"],
        [2, 2, 102, "10/09/2026", "15/09/2026"],
        [3, 1, 103, "28/02/2024", "01/03/2024"],
    ]
    assert val_datos.total_noches(reservas) == 9


def test_comparar_fechas_posterior():
    """Devuelve 1 cuando la primera fecha es posterior a la segunda."""
    assert val_datos.comparar_fechas("02/09/2026", "01/09/2026") == 1
    # El año pesa mas que el dia y el mes.
    assert val_datos.comparar_fechas("01/01/2027", "31/12/2026") == 1


def test_comparar_fechas_anterior():
    """Devuelve -1 cuando la primera fecha es anterior a la segunda."""
    assert val_datos.comparar_fechas("01/09/2026", "02/09/2026") == -1
    assert val_datos.comparar_fechas("31/12/2026", "01/01/2027") == -1


def test_comparar_fechas_iguales():
    """Devuelve 0 cuando las dos fechas son iguales."""
    assert val_datos.comparar_fechas("15/09/2026", "15/09/2026") == 0
