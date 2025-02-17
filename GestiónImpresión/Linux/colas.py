# Colas de impresión

import os
import subprocess
from colorama import Fore, Style

# ----------------------------------------------------------
# LISTAR COLA DE TRABAJOS DE UNA IMPRESORA
def listar_trabajos(impresora):
    try:
        # Ejecutar lpstat -W completed para obtener los trabajos completados
        resultado_completados = subprocess.check_output(
            ["lpstat", "-W", "completed", "-d", impresora], universal_newlines=True)
        print(f"\n\t{Fore.GREEN}Trabajos de impresión completados para la impresora {impresora}:{Style.RESET_ALL}")

        if resultado_completados.strip():  # Si hay resultados
            # Agregar una cabecera para los trabajos completados
            print(f"\t{Fore.CYAN}{'ID':<10}{'Usuario':<15}{'Tamaño':<10}{'Fecha'}{Style.RESET_ALL}")

            for linea in resultado_completados.splitlines():

                # Filtrar la línea que contiene el texto 'destino predeterminado'
                if "destino predeterminado del sistema" not in linea:
                    # Separar los campos por espacio, ajustando el formato
                    campos = linea.split()
                    job_id = campos[0]
                    usuario = campos[1]
                    tamanio = campos[2]
                    fecha = " ".join(campos[3:])

                    # Imprimir los trabajos con un formato adecuado
                    print(f"\t{Fore.YELLOW}{job_id:<10}{usuario:<15}{tamanio:<10}{fecha}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No hay trabajos completados.{Style.RESET_ALL}")

        print()  # Salto de línea

        # Ejecutar lpstat -W not-completed para obtener los trabajos no completados
        resultado_no_completados = subprocess.check_output(["lpstat", "-W", "not-completed", "-d", impresora], universal_newlines=True)
        print(f"\t{Fore.GREEN}Trabajos de impresión no completados para la impresora {impresora}:{Style.RESET_ALL}")

        if resultado_no_completados.strip():  # Si hay resultados
            # Agregar una cabecera para los trabajos no completados
            print(f"\t{Fore.CYAN}{'ID':<10}{'Usuario':<15}{'Tamaño':<10}{'Fecha'}{Style.RESET_ALL}")

            for linea in resultado_no_completados.splitlines():
                # Filtrar la línea que contiene el texto 'destino predeterminado'
                if "destino predeterminado del sistema" not in linea:

                    # Separar los campos por espacio, ajustando el formato
                    campos = linea.split()
                    job_id = campos[0]
                    usuario = campos[1]
                    tamanio = campos[2]
                    fecha = " ".join(campos[3:])

                    # Imprimir los trabajos con un formato adecuado
                    print(f"\t{Fore.YELLOW}{job_id:<10}{usuario:<15}{tamanio:<10}{fecha}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No hay trabajos no completados.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al obtener la lista de trabajos de impresión: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# CANCELAR UN TRABAJO DE UNA IMPRESORA
def cancelar_trabajo():
    try:
        # Solicitar al usuario que ingrese el nombre de la impresora
        impresora_seleccionada = input(f"\n\t{Fore.CYAN}Introduce el nombre de la impresora: {Style.RESET_ALL}")

        # Listar los trabajos en cola para la impresora seleccionada
        listar_trabajos(impresora_seleccionada)  # Aquí pasa la impresora seleccionada como parámetro

        # Solicitar al usuario que ingrese el ID del trabajo a cancelar
        job_id = input(f"\n\t{Fore.CYAN}Introduce el ID del trabajo que deseas cancelar: {Style.RESET_ALL}")

        # Cancelar el trabajo seleccionado usando el comando cancel
        print(f"\n\t{Fore.GREEN}Cancelando el trabajo de impresión {job_id} de la impresora {impresora_seleccionada}...{Style.RESET_ALL}")
        subprocess.check_call(["cancel", job_id])

        print(f"\t{Fore.GREEN}Trabajo de impresión {job_id} cancelado de la impresora {impresora_seleccionada}.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al cancelar el trabajo de impresión {job_id}: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error desconocido al cancelar el trabajo: {e}{Style.RESET_ALL}")


# ----------------------------------------------------------
# MOVER UN TRABAJO
def mover_trabajo():
    try:
        # Solicitar el nombre de las impresoras y el ID del trabajo
        impresora_origen = input(f"\n\t{Fore.CYAN}Introduce el nombre de la impresora de origen: {Style.RESET_ALL}")
        impresora_destino = input(f"\n\t{Fore.CYAN}Introduce el nombre de la impresora de destino: {Style.RESET_ALL}")
        job_id = input(f"\n\t{Fore.CYAN}Introduce el ID del trabajo a mover: {Style.RESET_ALL}")

        # Ejecutar el comando lpmove para mover el trabajo de una impresora a otra
        print(f"\n\t{Fore.YELLOW}Moviendo el trabajo {job_id} de la impresora {impresora_origen} a la impresora {impresora_destino}...{Style.RESET_ALL}")
        subprocess.check_call(["lpmove", job_id, impresora_destino])

        print(f"\n\t{Fore.GREEN}Trabajo {job_id} movido de la impresora {impresora_origen} a la impresora {impresora_destino}.{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"\n\t{Fore.RED}Error al mover el trabajo: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\t{Fore.RED}Error desconocido: {e}{Style.RESET_ALL}")

# ----------------------------------------------------------
# ELIMINAR TODOS LOS TRABAJOS DE UNA COLA DE UNA IMPRESORA
def eliminar_todos_los_trabajos():
    try:
        impresora = input(f"\n\t{Fore.CYAN}Introduce el nombre de la impresora de la que deseas eliminar los trabajos: {Style.RESET_ALL}")
        subprocess.check_call(["cancel", "-a", impresora])
        print(f"\n\t{Fore.GREEN}Todos los trabajos en la cola de la impresora {impresora} han sido eliminados. {Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"\n\t{Fore.RED}Error al eliminar los trabajos de la cola de la impresora {impresora}: {e}{Style.RESET_ALL}")
