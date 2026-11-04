from utilidades import estadisticas


RESERVAS = [
    [1, 1, 101, "01/09/2026", "03/09/2026"],
    [2, 2, 102, "10/09/2026", "15/09/2026"],
    [3, 1, 103, "20/09/2026", "22/09/2026"],
]


def test_contar_reservas_de_cliente_con_reservas():
    """Un cliente con 2 reservas devuelve 2."""
    assert estadisticas.contar_reservas_de_cliente(RESERVAS, 1) == 2


def test_contar_reservas_de_cliente_sin_reservas():
    """Un cliente sin reservas devuelve 0, y una lista vacia tambien."""
    assert estadisticas.contar_reservas_de_cliente(RESERVAS, 99) == 0
    assert estadisticas.contar_reservas_de_cliente([], 1) == 0