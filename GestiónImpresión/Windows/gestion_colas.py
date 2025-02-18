# Gestion de colas de trabajo
import win32print
import os
from colorama import Fore, Style

# Muestra los trabajos en la cola de impresión de una impresora especificada
def mostrar_cola_impresora():
    nombre_impresora = input("Introduce el nombre de la impresora para ver la cola de impresión: ")
    try:
        hprinter = win32print.OpenPrinter(nombre_impresora)
        jobs = win32print.EnumJobs(hprinter, 0, 999, 1)  # Ver todos los trabajos de impresión
        if not jobs:
            print(Fore.RED + "No hay trabajos en la cola de impresión." + Style.RESET_ALL)
            return
        print(Fore.GREEN + f"Trabajos de impresión en cola para {nombre_impresora}:" + Style.RESET_ALL)
        for job in jobs:
            print(f"Trabajo ID: {job['JobId']} - Usuario: {job['pUserName']} - Estado: {job['Status']}")
        win32print.ClosePrinter(hprinter)
    except Exception as e:
        print(Fore.RED + f"Error al obtener los trabajos de impresión: {e}" + Style.RESET_ALL)

# Envía a una impresora indicada una trabajo.
def imprimir_documento():
    try:
        nombre_impresora = input("Introduce el nombre de la impresora a la que quieres enviar el documento: ")
        ruta_documento = input("Introduce la ruta completa del documento a imprimir: ")

        # Verificar si el archivo existe
        if not os.path.isfile(ruta_documento):
            print(Fore.RED + "El archivo no existe. Por favor, verifica la ruta." + Style.RESET_ALL)
            return

        # Abrir la impresora
        printer_handle = win32print.OpenPrinter(nombre_impresora)

        # Crear un trabajo de impresión
        devmode = win32print.GetPrinter(printer_handle, 2)['pDevMode']
        job_id = win32print.StartDocPrinter(printer_handle, 1, (ruta_documento, None, "RAW"))

        # Abrir el archivo para imprimir
        with open(ruta_documento, "rb") as file:
            file_data = file.read()
            win32print.WritePrinter(printer_handle, file_data)

        # Finalizar el trabajo de impresión
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)

        print(Fore.GREEN + f"Documento {ruta_documento} enviado a la impresora {nombre_impresora}." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error al imprimir el documento: {e}" + Style.RESET_ALL)

# Cancelar un trabajo en cola por su ID
def cancelar_trabajo_impresion():
    try:
        nombre_impresora = input("Introduce el nombre de la impresora: ")
        trabajo_id = int(input("Introduce el ID del trabajo de impresión que deseas cancelar: "))

        hprinter = win32print.OpenPrinter(nombre_impresora)

        # Usamos SetJob para cancelar el trabajo de impresión
        win32print.SetJob(hprinter, trabajo_id, 0, None, win32print.JOB_CONTROL_CANCEL)

        win32print.ClosePrinter(hprinter)
        print(Fore.GREEN + f"Trabajo ID {trabajo_id} cancelado exitosamente." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error al cancelar el trabajo de impresión: {e}" + Style.RESET_ALL)


