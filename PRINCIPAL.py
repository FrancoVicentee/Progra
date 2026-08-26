encabezados_clientes = ['Id_cliente', 'Nombre', 'Apellido', 'DNI']
clientes = [
    [1, 'Juan', 'Pérez', 32145678],
    [2, 'Ana', 'López', 25412587],
    [3, 'Carlos', 'Gómez', 40123654],
    [4, 'María', 'Fernández', 35147852],
    [5, 'Lucía', 'Martínez', 38741256],
]

encabezados_habitaciones = ['Id_hab', 'Numero', 'Tipo', 'Capacidad', 'Estado']
habitaciones = [
    [1, 101, 'Simple', 1, 'Disponible'],
    [2, 102, 'Simple', 1, 'Ocupada'],
    [3, 201, 'Doble', 2, 'Disponible'],
    [4, 202, 'Doble', 2, 'Mantenimiento'],
    [5, 301, 'Suite', 4, 'Disponible'],
]

encabezados_reservas = ['Id_reserva', 'Id_cliente', 'Id_hab', 'Fecha_ingreso', 'Fecha_egreso']
reservas = [
    [1, 1, 3, '01/09/2026', '15/09/2026'],
    [2, 2, 1, '28/08/2026', '02/09/2026'],
    [3, 3, 2, '05/09/2026', '10/09/2026'],
    [4, 5, 5, '02/09/2026', '08/09/2026'],
    [5, 4, 4, '07/09/2026', '12/09/2026'],
]