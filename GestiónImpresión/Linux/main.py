from impresoras import listar_impresoras,estado_impresora, mostrar_impresora_default,disable_impresora,enable_impresora,establecer_impresora_default
from trabajos import listar_trabajos, cancelar_trabajo, imprimir_documento
from utils import mostrar_mensaje, manejar_error
from colorama import Fore, Style


# Función para el menú principal
def menu_principal():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de gestión de impresoras y trabajos de impresión:")
        print("\n\t1. Administración de impresoras")
        print("\t2. Gestión de trabajos de impresión")
        print("\t3. Salir\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            menu_impresoras()
        elif opcion == "2":
            menu_trabajos()
        elif opcion == "3":
            mostrar_mensaje(Fore.GREEN, "\n\t\tSaliendo del programa...")
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el menú de administración de impresoras
def menu_impresoras():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de administración de impresoras:")
        print("\n\t1. Listar impresoras disponibles")
        print("\t2. Estado impresora")
        print("\t3. Ver impresora predeterminada")
        print("\t4. Establecer impresora predeterminada")
        print("\t5. Deshabilitar impresora")
        print("\t6. Habilitar impresora")
        print("\t7. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            listar_impresoras()
        elif opcion == "2":
            estado_impresora()
        elif opcion == "3":
            mostrar_impresora_default()
        elif opcion == "4":
            establecer_impresora_default()
        elif opcion == "5":
            impresora = input(f"\n\t{Fore.YELLOW}Nombre de la impresora a deshabilitar: ")
            disable_impresora(impresora)
        elif opcion == "6":
            impresora = input(f"\n\t{Fore.YELLOW}Nombre de la impresora a habilitar: ")
            enable_impresora(impresora)
        elif opcion == "7":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


# Función para el menú de gestión de trabajos de impresión
def menu_trabajos():
    while True:
        mostrar_mensaje(Fore.CYAN, "\n\t\t\t\tMenú de gestión de trabajos de impresión:")
        print("\n\t1. Listar trabajos en cola")
        print("\t2. Cancelar un trabajo")
        print("\t3. Enviar trabajo de impresión")
        print("\t4. Volver\n")

        opcion = input("\tElige una opción: ")

        if opcion == "1":
            listar_trabajos()
        elif opcion == "2":
            job_id = input("\tIntroduce el ID del trabajo a cancelar: ")
            cancelar_trabajo(job_id)
        elif opcion == "3":
            impresora = input("\tIntroduce el nombre de la impresora: ")
            archivo = input("\tIntroduce la ruta del archivo a imprimir: ")
            copias = int(input("\tIntroduce el número de copias: "))
            imprimir_documento(impresora, archivo, copias)
        elif opcion == "4":
            break
        else:
            manejar_error("\tOpción no válida, intenta de nuevo.\n")


if __name__ == "__main__":
    menu_principal()
