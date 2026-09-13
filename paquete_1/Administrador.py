from paquete_2 import val_datos
 
 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Funciones de administrador para el manejo de empleados en el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
 
def alta_empleado(empleados_dict):
    print("\n--- Alta de Empleado ---")
    legajo = val_datos.pedir_entero_rango("Ingrese legajo (100-999): ", 100, 999)
    
    if legajo not in empleados_dict:
        nombre = val_datos.pedir_nombre_empleado("Nombre del empleado: ")
        sueldo = val_datos.pedir_entero_rango("Sueldo: $", 100000, 9999999)
        empleados_dict[legajo] = {"nombre": nombre, "sueldo": sueldo}
        print("Empleado registrado correctamente.")
    else:
        print("Error. El legajo ya existe.")
        
    return empleados_dict
 
 
def listar_empleados(empleados_dict):
    print("\n--- Listado de Empleados ---")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados.")
    else:
        print(f"{'Legajo':<10}{'Nombre':<20}{'Sueldo':<10}")
        print("-" * 35)
        
        claves = list(empleados_dict.keys())
        indice = 0
        while indice < len(claves):
            leg = claves[indice]
            datos = empleados_dict[leg]
            print(f"{leg:<10}{datos['nombre']:<20}${datos['sueldo']:<10}")
            indice += 1
            
    val_datos.pausar_menu()
    return empleados_dict
 
 
def baja_empleado(empleados_dict):
    print("\n--- Baja de Empleado ---")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para dar de baja.")
    else:
        legajo = val_datos.pedir_entero_rango("Ingrese legajo a dar de baja (100-999): ", 100, 999)
        
        if legajo in empleados_dict:
            print(f"Empleado encontrado: {empleados_dict[legajo]['nombre']}")
            confirmacion = val_datos.pedir_entero_rango("¿Confirma la baja? [1] Sí [0] No: ", 0, 1)
            
            if confirmacion == 1:
                empleados_dict.pop(legajo)
                print("Empleado eliminado correctamente.")
            else:
                print("Operación cancelada.")
        else:
            print("Empleado no encontrado.")
            
    return empleados_dict
 
 
def modificar_sueldo(empleados_dict):
    print("\n--- Modificar Sueldo de Empleado ---")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados para modificar.")
    else:
        legajo = val_datos.pedir_entero_rango("Ingrese legajo a modificar (100-999): ", 100, 999)
        
        if legajo in empleados_dict:
            print(f"Empleado actual: {empleados_dict[legajo]['nombre']} - Sueldo: ${empleados_dict[legajo]['sueldo']}")
            nuevo_sueldo = val_datos.pedir_entero_rango("Nuevo sueldo: $", 100000, 9999999)
            empleados_dict[legajo]["sueldo"] = nuevo_sueldo
            print("Sueldo actualizado correctamente.")
        else:
            print("Empleado no encontrado.")
            
    return empleados_dict
 
 
 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
Menú de administración para el sistema.
 
"""""""""""""""""""""""""""""""""""""""""""""""""""
 
 
def menu_admin(empleados_dict):
    opcion = -1
    while opcion != 0:
        titulo = " Menú Administración "
        print(f"\n{titulo:-^50}")
        print("[1] Alta de empleado")
        print("[2] Listar empleados")
        print("[3] Baja de empleado")
        print("[4] Modificar sueldo empleado")
        print("[5] Consultar empleado")
        print("-" * 50)
        print("[0] Cerrar menú de administración")
        print("-" * 50)

        opcion = val_datos.pedir_entero_rango("Seleccione una opción: ", 0, 5)

        match opcion:
            case 1:
                empleados_dict = alta_empleado(empleados_dict)
            case 2:
                empleados_dict = listar_empleados(empleados_dict)
            case 3:
                empleados_dict = baja_empleado(empleados_dict)
            case 4:
                empleados_dict = modificar_sueldo(empleados_dict)
            case 5:
                empleados_dict = consultar_empleado(empleados_dict)
            case 0:
                print("Cerrando menú de administración.")

    return empleados_dict

def consultar_empleado(empleados_dict):
    print("\n--- Consultar empleado ---")
    if len(empleados_dict) == 0:
        print("No hay empleados registrados.")
        return empleados_dict

    legajo = val_datos.pedir_entero_rango("Ingrese legajo a consultar (100-999): ", 100, 999)

    if legajo in empleados_dict:
        datos = empleados_dict[legajo]
        print(f"Legajo: {legajo}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Sueldo: ${datos['sueldo']}")
    else:
        print("No existe un empleado con ese legajo.")

    val_datos.pausar_menu()
    return empleados_dict