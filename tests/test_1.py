from utilidades import archivos


def test_linea_a_registro():
    # Linea normal con salto de linea al final: el ID y el DNI se convierten a int.
    assert archivos.linea_a_registro("1;Juan;Pérez;32145678\n", (0, 3)) == [1, "Juan", "Pérez", 32145678]
    # Ultima linea del archivo, sin salto de linea.
    assert archivos.linea_a_registro("2;Ana;López;25412587", (0, 3)) == [2, "Ana", "López", 25412587]
    # Sin columnas enteras, todos los campos quedan como texto.
    assert archivos.linea_a_registro("3;Carlos;Gómez;40123654\n", ()) == ["3", "Carlos", "Gómez", "40123654"]


def test_registro_a_linea():
    """Arma la linea con los campos separados por ';' y el salto de linea."""
    assert archivos.registro_a_linea([1, "Juan", "Pérez", 32145678]) == "1;Juan;Pérez;32145678\n"


def test_ida_y_vuelta_registro():
    """Pasar un registro a linea y volver devuelve el mismo registro."""
    registro = [1, "Juan", "Pérez", 32145678]
    assert archivos.linea_a_registro(archivos.registro_a_linea(registro), (0, 3)) == registro
