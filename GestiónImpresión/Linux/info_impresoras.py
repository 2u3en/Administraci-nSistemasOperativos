# Información de impresoras

import subprocess
from colorama import Fore, Style
import cups

# Crear una instancia del objeto CUPS
conn = cups.Connection()

# Listar las impresoras disponibles
def listar_impresoras():
    impresoras = conn.getPrinters()
    if not impresoras:
        print(f"{Fore.RED}No se encontraron impresoras disponibles.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.GREEN}\n\tImpresoras disponibles:{Style.RESET_ALL}")
        for impresora in impresoras:
            print(f"\t  - {Fore.MAGENTA}{impresora}{Style.RESET_ALL}")

# Mostrar la impresora predeterminada
def mostrar_impresora_default():
    try:
        # Ejecutar lpstat -d para obtener la impresora predeterminada
        resultado = subprocess.run(["lpstat", "-d"], text=True, capture_output=True)

        # Verificar si la ejecución fue exitosa
        if resultado.returncode == 0:
            # Revisar si la salida contiene "destino predeterminado del sistema"
            if "destino predeterminado del sistema" in resultado.stdout:
                # Extraer el nombre de la impresora predeterminada
                impresora_default = resultado.stdout.split(":")[1].strip()
                print(f"{Fore.GREEN}\n\tLa impresora por defecto actual es:")
                print(f"\t  - {Fore.MAGENTA}{impresora_default}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No se pudo encontrar la impresora por defecto.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error al ejecutar el comando lpstat: {resultado.stderr}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")

# Verificar el estado de la impresora
def estado_impresora():
    try:
        # Ejecutar lpstat -t y capturar la salida
        resultado = subprocess.check_output(["lpstat", "-t"], universal_newlines=True)

        # Filtrar la información para mostrar el estado de todas las impresoras
        lines = resultado.splitlines()
        impresoras_estado = [line for line in lines if "impresora" in line]  # Filtra por líneas que contienen "printer"

        if impresoras_estado:
            print(f"{Fore.GREEN}\n\tEstado de las impresoras:{Style.RESET_ALL}")
            for linea in impresoras_estado:
                print(f"\t  - {Fore.MAGENTA}{linea}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No se encontró información sobre las impresoras.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al obtener el estado de las impresoras: {e}{Style.RESET_ALL}")

# Mostrar estado del servicio CUPS
def estado_servicio():
    try:
        print(f"\n\t{Fore.CYAN}Estado del servicio CUPS{Style.RESET_ALL}")
        resultado = subprocess.check_output(["lpstat", "-r"],universal_newlines=True,encoding='utf-8')
        print(f"\t{Fore.GREEN}{resultado}{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al comprobar el estado del servicio de impresión: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")
