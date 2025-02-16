import subprocess
from colorama import Fore, Style


def imprimir_documento():
    try:
        # Solicitar el nombre de la impresora
        impresora = input(f"{Fore.CYAN}\n\tIntroduce el nombre de la impresora: {Style.RESET_ALL}")

        # Solicitar la ruta del archivo a imprimir
        archivo = input(f"{Fore.CYAN}\n\tIntroduce la ruta del archivo a imprimir: {Style.RESET_ALL}")

        # Solicitar el número de copias
        while True:
            try:
                copias = int(input(f"{Fore.CYAN}\n\tIntroduce el número de copias: {Style.RESET_ALL}"))
                if copias > 0:
                    break
                else:
                    print(
                        f"{Fore.RED}Por favor, ingresa un número válido de copias (un número entero positivo).{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor, ingresa un número válido para las copias.{Style.RESET_ALL}")

        # Ejecutar el comando lp para imprimir el archivo con el número de copias
        print(
            f"\n\t{Fore.GREEN}Enviando el archivo {archivo} a la impresora {impresora} con {copias} copias...{Style.RESET_ALL}")
        subprocess.check_call(["lp", "-d", impresora, "-n", str(copias), archivo],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(
            f"\n\t{Fore.GREEN}Trabajo de impresión enviado a la impresora {impresora} con {copias} copias.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al enviar el trabajo de impresión: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")





