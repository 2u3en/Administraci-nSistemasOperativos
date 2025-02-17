# Administración de usuarios

import subprocess
from colorama import Fore, Style

# MENU
def administrar_usuarios():
    try:
        # Solicitar al usuario el nombre de la impresora
        impresora = input(f"{Fore.CYAN}\n\tIntroduce el nombre de la impresora: {Style.RESET_ALL}")

        # Mostrar opciones para administrar usuarios
        print(f"{Fore.CYAN}\n\t1. Permitir acceso a un usuario")
        print(f"{Fore.CYAN}\t2. Denegar acceso a un usuario")
        print(f"{Fore.CYAN}\t3. Volver al menú anterior{Style.RESET_ALL}")

        opcion = input(f"\n\tElige una opción: ")

# CONTROL PARA PERMITIR O DENEGAR ACCESO A IMPRESORAS A USUARI@S

        if opcion == "1":
            # PERMITIR IMPRESION A USUARI@
            usuario = input(f"\n\tIntroduce el nombre del usuario al que deseas permitir acceso: {Style.RESET_ALL}")
            subprocess.check_call(["lpadmin", "-p", impresora, "-u", f"allow:{usuario}"])
            print(f"\t{Fore.GREEN}Acceso permitido al usuario {usuario} para la impresora {impresora}.{Style.RESET_ALL}")

        elif opcion == "2":
            # DENEGAR IMPRESION A USUARI@
            usuario = input(f"\n\tIntroduce el nombre del usuario al que deseas denegar acceso: {Style.RESET_ALL}")
            subprocess.check_call(["lpadmin", "-p", impresora, "-u", f"deny:{usuario}"])
            print(f"\t{Fore.GREEN}Acceso denegado al usuario {usuario} para la impresora {impresora}.{Style.RESET_ALL}")

        elif opcion == "3":
            return  # Volver al menú anterior

        else:
            print(f"{Fore.RED}Opción no válida, por favor elige una opción válida.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al administrar el acceso del usuario: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido al administrar el acceso del usuario: {e}{Style.RESET_ALL}")
