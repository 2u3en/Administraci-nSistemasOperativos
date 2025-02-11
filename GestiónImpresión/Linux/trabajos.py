import cups
import subprocess
from colorama import Fore, Back, Style, init

# Crear una instancia del objeto CUPS
conn = cups.Connection()

# 2. Enviar un trabajo de impresión
def imprimir_documento(impresora, archivo):
    try:
        # Solicitar al usuario el número de copias
        copias = input(f"{Fore.CYAN}Introduce el número de copias a imprimir: {Style.RESET_ALL}")

        # Validar que el número de copias sea un número entero positivo
        while not copias.isdigit() or int(copias) <= 0:
            print(
                f"{Fore.RED}Por favor, ingresa un número válido de copias (un número entero positivo).{Style.RESET_ALL}")
            copias = input(f"{Fore.CYAN}Introduce el número de copias a imprimir: {Style.RESET_ALL}")

        # Ejecutar el comando lp para imprimir el archivo con el número de copias
        print(
            f"{Fore.YELLOW}Enviando el archivo {archivo} a la impresora {impresora} con {copias} copias...{Style.RESET_ALL}")
        subprocess.check_call(["lp", "-d", impresora, "-n", copias, archivo])

        print(
            f"{Fore.GREEN}Trabajo de impresión enviado a la impresora {impresora} con {copias} copias.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al enviar el trabajo de impresión: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")




# 6. Listar trabajos de impresión
def listar_trabajos():
    try:
        # Ejecutar lpstat -W completed para obtener los trabajos completados
        resultado_completados = subprocess.check_output(["lpstat", "-W", "completed"], universal_newlines=True)
        print(f"{Fore.GREEN}Trabajos de impresión completados:{Style.RESET_ALL}")
        if resultado_completados:
            print(f"{Fore.CYAN}{resultado_completados}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No hay trabajos completados.{Style.RESET_ALL}")

        # Ejecutar lpstat -W not-completed para obtener los trabajos no completados
        resultado_no_completados = subprocess.check_output(["lpstat", "-W", "not-completed"], universal_newlines=True)
        print(f"{Fore.GREEN}Trabajos de impresión no completados:{Style.RESET_ALL}")
        if resultado_no_completados:
            print(f"{Fore.CYAN}{resultado_no_completados}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No hay trabajos no completados.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al obtener la lista de trabajos de impresión: {e}{Style.RESET_ALL}")









# 7. Cancelar un trabajo de impresión
def cancelar_trabajo():
    try:
        # Listar trabajos en cola
        listar_trabajos()

        # Solicitar al usuario que ingrese el ID del trabajo a cancelar
        job_id = input(f"{Fore.CYAN}Introduce el ID del trabajo que deseas cancelar: {Style.RESET_ALL}")

        # Cancelar el trabajo seleccionado
        print(f"{Fore.YELLOW}Cancelando el trabajo de impresión {job_id}...{Style.RESET_ALL}")
        conn.cancelJob(job_id)
        print(f"{Fore.GREEN}Trabajo de impresión {job_id} cancelado.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al obtener la lista de trabajos de impresión: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al cancelar el trabajo de impresión: {e}{Style.RESET_ALL}")

