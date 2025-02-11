import win32print
import win32api
import time

def listar_impresoras():
    # Listar todas las impresoras disponibles
    impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    if not impresoras:
        print("No hay impresoras disponibles.")
    else:
        print("Lista de impresoras disponibles:")
        for idx, impresora in enumerate(impresoras):
            print(f"{idx + 1}. {impresora[2]}")
    return impresoras

def listar_trabajos_impresion(impresora):
    # Mostrar trabajos en cola de impresión de una impresora específica
    try:
        trabajos = win32print.EnumJobs(impresora, 0, 99, 1)
        if not trabajos:
            print("No hay trabajos en la cola de impresión.")
        else:
            print(f"Trabajos en la cola de la impresora {impresora}:")
            for idx, trabajo in enumerate(trabajos):
                print(f"{idx + 1}. {trabajo['pDocument']} (ID: {trabajo['JobId']})")
        return trabajos
    except Exception as e:
        print(f"Error al listar los trabajos: {e}")
        return []

def enviar_a_imprimir(impresora, archivo):
    # Enviar un archivo a la impresora
    try:
        win32api.ShellExecute(0, "print", archivo, f'/d:"{impresora}"', ".", 0)
        print(f"Archivo {archivo} enviado a la impresora {impresora}.")
    except Exception as e:
        print(f"Error al enviar el archivo a imprimir: {e}")

def cancelar_trabajo(impresora, job_id):
    # Cancelar un trabajo en cola
    try:
        win32print.SetJob(impresora, job_id, 0, None, win32print.JOB_CONTROL_CANCEL)
        print(f"Trabajo con ID {job_id} cancelado.")
    except Exception as e:
        print(f"Error al cancelar el trabajo: {e}")

def menu():
    while True:
        print("\nGestión de Impresoras")
        print("1. Listar Impresoras")
        print("2. Ver trabajos de impresión")
        print("3. Enviar archivo a imprimir")
        print("4. Cancelar trabajo")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            impresoras = listar_impresoras()

        elif opcion == '2':
            if 'impresoras' not in locals() or not impresoras:
                print("Primero debes listar las impresoras.")
                continue
            seleccion = int(input("Selecciona la impresora (por número): ")) - 1
            if seleccion < 0 or seleccion >= len(impresoras):
                print("Opción no válida.")
                continue
            trabajos = listar_trabajos_impresion(impresoras[seleccion][2])

        elif opcion == '3':
            if 'impresoras' not in locals() or not impresoras:
                print("Primero debes listar las impresoras.")
                continue
            seleccion = int(input("Selecciona la impresora (por número): ")) - 1
            if seleccion < 0 or seleccion >= len(impresoras):
                print("Opción no válida.")
                continue
            archivo = input("Ingresa la ruta del archivo a imprimir: ")
            enviar_a_imprimir(impresoras[seleccion][2], archivo)

        elif opcion == '4':
            if 'impresoras' not in locals() or not impresoras:
                print("Primero debes listar las impresoras.")
                continue
            seleccion = int(input("Selecciona la impresora (por número): ")) - 1
            if seleccion < 0 or seleccion >= len(impresoras):
                print("Opción no válida.")
                continue
            trabajos = listar_trabajos_impresion(impresoras[seleccion][2])
            if trabajos:
                trabajo_id = int(input("Ingresa el ID del trabajo a cancelar: "))
                cancelar_trabajo(impresoras[seleccion][2], trabajo_id)

        elif opcion == '5':
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
