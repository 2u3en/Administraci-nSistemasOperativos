import win32print
import win32serviceutil
from colorama import Fore, Style

# Lista todas las impresoras disponibles conectadas al sistema.
def listar_impresoras():
    try:
        impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        if not impresoras:
            print(Fore.RED + "No se encontraron impresoras." + Style.RESET_ALL)
            return
        print(Fore.GREEN + "Impresoras disponibles:" + Style.RESET_ALL)
        for printer in impresoras:
            print(f"{printer[2]} - Estado: {get_estado_impresora(printer[2])}")
    except Exception as e:
        print(Fore.RED + f"Error al listar las impresoras: {e}" + Style.RESET_ALL)

# Muestra la impresora predeterminada del sistema.
def impresora_predeterminada():

    try:
        default_printer = win32print.GetDefaultPrinter()
        print(Fore.GREEN + f"Impresora predeterminada: {default_printer}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error al obtener la impresora predeterminada: {e}" + Style.RESET_ALL)

#Obtiene el estado de una impresora.
def get_estado_impresora(nombre_impresora):
    try:
        hprinter = win32print.OpenPrinter(nombre_impresora)
        info_impresora = win32print.GetPrinter(hprinter, 2)
        status = info_impresora['Status']
        win32print.ClosePrinter(hprinter)
        return status
    except Exception as e:
        return f"Error: {str(e)}"

#    Verifica si el servicio de impresión está activo.
def estado_servicio():

    try:
        # Verifica si el servicio de cola de impresión está en estado 'Running'
        servicio_impresion = "Spooler"  # El servicio de impresión en Windows se llama "Spooler"
        estado_servicio = win32serviceutil.QueryServiceStatus(servicio_impresion)[1]

        if estado_servicio == 4:  # Estado 4 significa que el servicio está en 'Running'
            print(Fore.GREEN + "El servicio de impresión está activo." + Style.RESET_ALL)
        else:
            print(Fore.RED + "El servicio de impresión no está activo." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error al verificar el servicio: {e}" + Style.RESET_ALL)

# Muestra detalles completos de una impresora específica.
def detalles_impresora(nombre_impresora):

    try:
        hprinter = win32print.OpenPrinter(nombre_impresora)
        info_impresora = win32print.GetPrinter(hprinter, 2)
        print(Fore.GREEN + f"Detalles de la impresora {nombre_impresora}:" + Style.RESET_ALL)
        print(f"Nombre: {info_impresora['pPrinterName']}")
        print(f"Puerto: {info_impresora['pPortName']}")
        print(f"Controlador: {info_impresora['pDriverName']}")
        print(f"Estado: {info_impresora['Status']}")
        win32print.ClosePrinter(hprinter)
    except Exception as e:
        print(Fore.RED + f"Error al obtener los detalles de la impresora: {e}" + Style.RESET_ALL)
