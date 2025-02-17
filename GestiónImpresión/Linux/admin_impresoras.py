# Administración de impresoras

import subprocess
from colorama import Fore, Back, Style, init
import cups
import time
from info_impresoras import listar_impresoras,mostrar_impresora_default

# Inicializar colorama
init(autoreset=True)

# Crear una instancia del objeto CUPS
conn = cups.Connection()

# ----------------------------------------------------------
# ESTABLECER IMPRESORA PREDETERMINADA
def establecer_impresora_default():
    try:
        # Listar las impresoras disponibles
        listar_impresoras()

        # Solicitar al usuario  el nombre de la impresora a establecer como predeterminada
        impresora = input(f"\n{Fore.YELLOW}Introduce el nombre de la impresora que deseas establecer como predeterminada (o 'cancelar' para cancelar): {Style.RESET_ALL}")

        if impresora.lower() == "cancelar":
            print(f"{Fore.RED}Acción cancelada.{Style.RESET_ALL}")
            return

        # Verificar la impresora predeterminada antes de cambiarla
        print(f"\n\t{Fore.CYAN}La impresora predeterminada actual es: {Style.RESET_ALL}")
        mostrar_impresora_default()

        # Establecer la impresora seleccionada como predeterminada con lpoptions
        print(f"\n{Fore.YELLOW}Estableciendo la impresora {impresora} como predeterminada...{Style.RESET_ALL}")
        resultado = subprocess.run(["lpoptions", "-d", impresora], text=True, capture_output=True)

        # Comprobar ejecución del comando
        if resultado.returncode == 0:
            print(f"{Fore.GREEN}La impresora {impresora} ha sido establecida como la impresora predeterminada.{Style.RESET_ALL}")

            # Esperar para asegurar que la configuración se haya actualizado
            time.sleep(1)

            # Verificar la impresora predeterminada después del cambio
            print(f"{Fore.CYAN}Verificando la impresora predeterminada después del cambio: {Style.RESET_ALL}")
            mostrar_impresora_default()

        else:
            print(f"{Fore.RED}Error al establecer la impresora {impresora} como predeterminada: {resultado.stderr}{Style.RESET_ALL}")

    # Captura de errores
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# DESHABILITAR IMPRESORA
def disable_impresora(impresora):
    try:
        print(f"\n\t{Fore.YELLOW}Deshabilitando la impresora {impresora}...{Style.RESET_ALL}")
        conn.disablePrinter(impresora)
        print(f"\t{Fore.GREEN}Impresora {impresora} deshabilitada.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al deshabilitar la impresora {impresora}: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# HABILITAR IMPRESORA
def enable_impresora(impresora):
    try:
        print(f"\n\t{Fore.YELLOW}Habilitando impresora {impresora}...{Style.RESET_ALL}")
        conn.enablePrinter(impresora)
        print(f"\t{Fore.GREEN}Impresora {impresora} habilitada.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error al habilitar la impresora {impresora}: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# ESTABLECER LIMITE DE PÁGINAS
def establecer_limite_paginas():
    try:
        # Solicitar al usuario que ingrese el nombre de la impresora
        impresora = input(f"{Fore.CYAN}\n\tIntroduce el nombre de la impresora: {Style.RESET_ALL}")

        # Solicitar al usuario si desea establecer un límite de páginas
        limite_paginas = input(f"{Fore.CYAN}\n\t¿Deseas establecer un límite de páginas? (s/n): ")
        if limite_paginas.lower() == 's':
            limite = int(input(f"{Fore.CYAN}\n\tIntroduce el límite de páginas por trabajo: "))
        else:
            limite = None  # No hay límite de páginas

        # Preparar el comando de configuración para establecer el límite de páginas
        if limite is not None:
            print(f"\n\t{Fore.GREEN}Estableciendo un límite de {limite} páginas para la impresora {impresora}...{Style.RESET_ALL}")
            subprocess.check_call(["lpadmin", "-p", impresora, "-o", f"job-page-limit={limite}"])
            print(f"\t{Fore.GREEN}Límite de {limite} páginas establecido para la impresora {impresora}.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No se estableció límite de páginas.{Style.RESET_ALL}")

    # Captura de errores
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al establecer el límite de páginas: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido al establecer el límite de páginas: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# AGREGAR IMPRESORA
def agregar_impresora():
    try:
        # Solicitar el nombre de la impresora
        nombre_impresora = input(f"{Fore.CYAN}\n\tIntroduce el nombre de la impresora: {Style.RESET_ALL}")

        # Solicitar el URI del dispositivo (por ejemplo, usb://EPSON/PrinterModel)
        device_uri = input(f"{Fore.CYAN}\n\tIntroduce el URI del dispositivo (por ejemplo, IPP://EPSON/PrinterModel): {Style.RESET_ALL}")

        # Crear el comando lpadmin para agregar la impresora
        comando = ["sudo", "lpadmin", "-p", nombre_impresora, "-E", "-v", device_uri]

        # Ejecutar el comando
        subprocess.check_call(comando)

        # Mensaje de confirmación
        print(f"{Fore.GREEN}\n\tLa impresora {nombre_impresora} ha sido agregada correctamente.{Style.RESET_ALL}")

    # Captura de erroes
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al agregar la impresora: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# ELIMINAR IMPRESORA
def eliminar_impresora():
    try:
        # Solicitar nombre de la impresora
        impresora = input(f"{Fore.CYAN}\n\tIntroduce el nombre de la impresora que deseas eliminar: {Style.RESET_ALL}")

        # Ejecutar el comando para eliminar la impresora
        print(f"\n\t{Fore.GREEN}Eliminando la impresora {impresora}...{Style.RESET_ALL}")
        subprocess.check_call(["lpadmin", "-x", impresora])

        # Confirmar la eliminación
        print(f"\t{Fore.GREEN}La impresora {impresora} ha sido eliminada correctamente.{Style.RESET_ALL}")

    # Captura de errores
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al eliminar la impresora {impresora}: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido al eliminar la impresora: {e}{Style.RESET_ALL}")






