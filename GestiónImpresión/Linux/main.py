# main.py

from info_impresoras import(
    listar_impresoras,
    estado_impresora,
    mostrar_impresora_default,
    estado_servicio)

from admin_impresoras import(
    establecer_impresora_default,
    disable_impresora,
    enable_impresora,
    establecer_limite_paginas,
    agregar_impresora,
    eliminar_impresora)

from trabajos import imprimir_documento
from colas import listar_trabajos, cancelar_trabajo, mover_trabajo, eliminar_todos_los_trabajos
from usuarios import administrar_usuarios
from colorama import Fore, Style


# Función para mostrar mensajes
def mostrar_mensaje(color, mensaje):
    print(f"{color}{mensaje}{Style.RESET_ALL}")

# Función para manejar errores
def manejar_error(mensaje):
    print(f"{Fore.RED}{mensaje}{Style.RESET_ALL}")


# Función para el menú principal
def menu_principal():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de gestión de impresoras y trabajos de impresión:")
        print("\n\t1. Administración de impresoras")
        print("\t2. Gestión de trabajos de impresión")
        print("\t3. Gestión de colas de impresión")
        print("\t4. Administración de usuarios")  # Nueva opción para la administración de usuarios
        print("\t5. Salir\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            menu_admin_impresoras()  # Aquí es donde se maneja la administración de impresoras
        elif opcion == "2":
            menu_trabajos()
        elif opcion == "3":
            menu_colas()
        elif opcion == "4":
            administrar_usuarios()  # Llamada a la función de administración de usuarios
        elif opcion == "5":
            mostrar_mensaje(Fore.GREEN, "\n\t\tSaliendo del programa...")
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el menú de administración de impresoras
def menu_admin_impresoras():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de administración de impresoras:")
        print("\n\t1. Administrar impresoras")
        print("\t2. Información de impresoras")
        print("\t3. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            menu_administrar_impresoras()
        elif opcion == "2":
            menu_info_impresoras()
        elif opcion == "3":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el submenú de administración de impresoras
def menu_administrar_impresoras():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tSubmenú de Administración de impresoras:")
        print("\n\t1. Establecer impresora predeterminada")
        print("\t2. Deshabilitar impresora")
        print("\t3. Habilitar impresora")
        print("\t4. Establecer límite de páginas")
        print("\t5. Agregar impresora")
        print("\t6. Eliminar impresora")
        print("\t7. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            establecer_impresora_default()
        elif opcion == "2":
            impresora = input(f"\n\t{Fore.YELLOW}Nombre de la impresora a deshabilitar: ")
            disable_impresora(impresora)
        elif opcion == "3":
            impresora = input(f"\n\t{Fore.YELLOW}Nombre de la impresora a habilitar: ")
            enable_impresora(impresora)
        elif opcion == "4":
            establecer_limite_paginas()
        elif opcion == "5":
            agregar_impresora()
        elif opcion == "6":
            eliminar_impresora()
        elif opcion == "7":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el submenú de información de impresoras
def menu_info_impresoras():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tSubmenú de Información de impresoras:")
        print("\n\t1. Listar impresoras disponibles")
        print("\t2. Estado impresora")
        print("\t3. Ver impresora predeterminada")
        print("\t4. Estado del servicio")
        print("\t5. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            listar_impresoras()
        elif opcion == "2":
            estado_impresora()
        elif opcion == "3":
            mostrar_impresora_default()
        elif opcion == "4":
            estado_servicio()
        elif opcion == "5":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el menú de gestión de trabajos de impresión
def menu_trabajos():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de gestión de trabajos de impresión:")
        print("\n\t1. Enviar trabajo de impresión")
        print("\t2. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            imprimir_documento()
        elif opcion == "2":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el menú de gestión de colas de impresión
def menu_colas():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de gestión de colas de impresión:")
        print("\n\t1. Listar trabajos en cola")
        print("\t2. Cancelar trabajo de impresión")
        print("\t3. Mover trabajo a otra impresora")
        print("\t4. Eliminar todos los trabajos de la impresora")
        print("\t5. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            impresora = input(f"\n\t{Fore.CYAN}Introduce el nombre de la impresora: {Style.RESET_ALL}")
            listar_trabajos(impresora)
        elif opcion == "2":
            cancelar_trabajo()
        elif opcion == "3":
            mover_trabajo()  # Llamamos a la función de mover trabajo
        elif opcion == "4":
            eliminar_todos_los_trabajos()  # Llamamos a la función de eliminar todos los trabajos
        elif opcion == "5":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


if __name__ == "__main__":
    menu_principal()
