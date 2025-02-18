# ----------------------------------------------------------------------------
# Script: Gestión de impresión en Windows
# Autor: Rubén
# Versión: 1.0.0
# Fecha de creación: 9/02/2025
# Última modificación: 18/02/2025
#
# Descripción:
#   Este script permite la administración de impresoras y colas de trabajos
#   en un sistema Windows con impresoras virtuales mediante PDFCreator.
# ----------------------------------------------------------------------------

from colorama import Fore, Style, init
from informacion_impresoras import listar_impresoras, estado_servicio, detalles_impresora, impresora_predeterminada
from gestion_colas import mostrar_cola_impresora, imprimir_documento, cancelar_trabajo_impresion

# Inicializar colorama
init(autoreset=True)

def menu():
    while True:
        print(Fore.YELLOW + "\nMenú de opciones:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Información impresoras" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Gestión de colas" + Style.RESET_ALL)
        print(Fore.RED + "3. Salir" + Style.RESET_ALL)
        opcion = input(Fore.GREEN + "Elige una opción (1-3): " + Style.RESET_ALL)

        if opcion == '1':
            menu_informacion_impresoras()
        elif opcion == '2':
            menu_gestion_colas()
        elif opcion == '3':
            print(Fore.MAGENTA + "Saliendo del programa... ¡Hasta luego!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

def menu_informacion_impresoras():
    while True:
        print(Fore.YELLOW + "\nMenú Información Impresoras:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Listar impresoras" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Ver estado del servicio de impresión" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Ver detalles de una impresora" + Style.RESET_ALL)
        print(Fore.RED + "4. Volver al menú principal" + Style.RESET_ALL)
        opcion = input(Fore.GREEN + "Elige una opción (1-4): " + Style.RESET_ALL)

        if opcion == '1':
            listar_impresoras()
        elif opcion == '2':
            estado_servicio()
        elif opcion == '3':
            nombre_impresora = input(Fore.GREEN + "Introduce el nombre de la impresora: " + Style.RESET_ALL)
            detalles_impresora(nombre_impresora)
        elif opcion == '4':
            impresora_predeterminada()
        elif opcion == '5':
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

def menu_gestion_colas():
    while True:
        print(Fore.YELLOW + "\nMenú Gestión de Colas:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Mostrar cola de impresión" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Imprimir documento" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Cancelar trabajo de impresión" + Style.RESET_ALL)
        print(Fore.CYAN + "4. Ver trabajos de una impresora" + Style.RESET_ALL)
        print(Fore.CYAN + "5. Ver impresora predeterminada" + Style.RESET_ALL)
        print(Fore.RED + "6. Volver al menú principal" + Style.RESET_ALL)
        opcion = input(Fore.GREEN + "Elige una opción (1-6): " + Style.RESET_ALL)

        if opcion == '1':
            mostrar_cola_impresora()
        elif opcion == '2':
            imprimir_documento()
        elif opcion == '3':
            cancelar_trabajo_impresion()
        elif opcion == '4':
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

if __name__ == "__main__":
    menu()
