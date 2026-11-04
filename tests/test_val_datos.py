from utilidades import val_datos


def test_es_entero():
    """Acepta solo cadenas de digitos, con o sin espacios en los extremos."""
    assert val_datos.es_entero("123") is True
    assert val_datos.es_entero(" 45 ") is True
    assert val_datos.es_entero("12a") is False
    assert val_datos.es_entero("-5") is False
    assert val_datos.es_entero("") is False


def test_es_entero_en_rango():
    """Controla que el entero este dentro del rango, incluyendo los extremos."""
    assert val_datos.es_entero_en_rango("100", 100, 999) is True
    assert val_datos.es_entero_en_rango("999", 100, 999) is True
    assert val_datos.es_entero_en_rango("99", 100, 999) is False
    assert val_datos.es_entero_en_rango("abc", 100, 999) is False


def test_es_bisiesto():
    """Detecta años bisiestos, incluyendo las reglas de 100 y 400."""
    assert val_datos.es_bisiesto(2024) is True
    assert val_datos.es_bisiesto(2026) is False
    assert val_datos.es_bisiesto(1900) is False
    assert val_datos.es_bisiesto(2000) is True


def test_dias_del_mes():
    """Devuelve los dias de cada mes, con febrero segun el año."""
    assert val_datos.dias_del_mes(1, 2026) == 31
    assert val_datos.dias_del_mes(4, 2026) == 30
    assert val_datos.dias_del_mes(2, 2026) == 28
    assert val_datos.dias_del_mes(2, 2024) == 29


def test_validar_fecha():
    """Acepta fechas reales dd/mm/aaaa y rechaza formatos o dias inexistentes."""
    assert val_datos.validar_fecha("15/09/2026") is True
    assert val_datos.validar_fecha("29/02/2024") is True
    assert val_datos.validar_fecha("29/02/2026") is False
    assert val_datos.validar_fecha("31/04/2026") is False
    assert val_datos.validar_fecha("15-09-2026") is False
    assert val_datos.validar_fecha("15/13/2026") is False


def test_convertir_fecha_a_numero():
    """Pasa dd/mm/aaaa al numero aaaammdd."""
    assert val_datos.convertir_fecha_a_numero("05/09/2026") == 20260905
    assert val_datos.convertir_fecha_a_numero("31/12/1999") == 19991231


def test_normalizar_nombre():
    """Quita espacios sobrantes y pone mayuscula inicial en cada palabra."""
    assert val_datos.normalizar_nombre("  juan   carlos ") == "Juan Carlos"
    assert val_datos.normalizar_nombre("PÉREZ") == "Pérez"


def test_es_texto():
    """Acepta solo letras (con tildes) y espacios entre palabras."""
    assert val_datos.es_texto("María José") is True
    assert val_datos.es_texto("Juan2") is False
    assert val_datos.es_texto("") is False
    assert val_datos.es_texto("   ") is False


def test_tipo_y_estado_validos():
    """Acepta tipos y estados de habitacion sin importar mayusculas."""
    assert val_datos.es_tipo_valido("suite") is True
    assert val_datos.es_tipo_valido("  DOBLE ") is True
    assert val_datos.es_tipo_valido("triple") is False
    assert val_datos.es_estado_valido("mantenimiento") is True
    assert val_datos.es_estado_valido("libre") is False