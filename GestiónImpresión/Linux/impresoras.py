import subprocess
from colorama import Fore, Back, Style, init
import cups
import time

# Inicializar colorama para que funcione correctamente en Windows y Linux
init(autoreset=True)

# Crear una instancia del objeto CUPS
conn = cups.Connection()


# 1. Listar las impresoras disponibles
def listar_impresoras():
    impresoras = conn.getPrinters()
    if not impresoras:
        print(f"{Fore.RED}No se encontraron impresoras disponibles.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.GREEN}\n\tImpresoras disponibles:{Style.RESET_ALL}")
        for impresora in impresoras:
            print(f"\t  - {Fore.MAGENTA}{impresora}{Style.RESET_ALL}")


# 2. Verificar el estado de la impresora
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


# 3. Mostrar la impresora predeterminada
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


# 4. Establecer la impresora predeterminada
def establecer_impresora_default():
    try:
        # Listar las impresoras disponibles
        listar_impresoras()

        # Solicitar al usuario la impresora que quiere establecer como predeterminada
        impresora = input(
            f"\n{Fore.YELLOW}Introduce el nombre de la impresora que deseas establecer como predeterminada (o 'cancelar' para cancelar): {Style.RESET_ALL}")

        if impresora.lower() == "cancelar":
            print(f"{Fore.RED}Acción cancelada.{Style.RESET_ALL}")
            return

        # Verificar la impresora predeterminada antes de cambiarla
        print(f"\n\t{Fore.CYAN}La impresora predeterminada actual es: {Style.RESET_ALL}")
        mostrar_impresora_default()

        # Establecer la impresora seleccionada como predeterminada con lpoptions
        print(f"\n{Fore.YELLOW}Estableciendo la impresora {impresora} como predeterminada...{Style.RESET_ALL}")
        resultado = subprocess.run(["lpoptions", "-d", impresora], text=True, capture_output=True)

        # Comprobar si el comando fue exitoso
        if resultado.returncode == 0:
            print(f"{Fore.GREEN}La impresora {impresora} ha sido establecida como la impresora predeterminada.{Style.RESET_ALL}")

            # Esperar un momento para asegurar que la configuración se haya actualizado
            time.sleep(1)

            # Verificar la impresora predeterminada después del cambio
            print(f"{Fore.CYAN}Verificando la impresora predeterminada después del cambio: {Style.RESET_ALL}")
            mostrar_impresora_default()

        else:
            print(
                f"{Fore.RED}Error al establecer la impresora {impresora} como predeterminada: {resultado.stderr}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")


# 5. Deshabilitar una impresora
def disable_impresora(impresora):
    try:
        print(f"\n\t{Fore.YELLOW}Deshabilitando la impresora {impresora}...{Style.RESET_ALL}")
        conn.disablePrinter(impresora)
        print(f"\t{Fore.GREEN}Impresora {impresora} deshabilitada.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al deshabilitar la impresora {impresora}: {e}{Style.RESET_ALL}")


# 6. Habilitar una impresora
def enable_impresora(impresora):
    try:
        print(f"\n\t{Fore.YELLOW}Habilitando impresora {impresora}...{Style.RESET_ALL}")
        conn.enablePrinter(impresora)
        print(f"\t{Fore.GREEN}Impresora {impresora} habilitada.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al habilitar la impresora {impresora}: {e}{Style.RESET_ALL}")









