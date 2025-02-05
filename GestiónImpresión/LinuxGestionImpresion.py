import cups
import os

def listar_impresoras():
    # Obtener las impresoras disponibles desde CUPS
    conn = cups.Connection()
    impresoras = conn.getPrinters()
    if not impresoras:
        print("No hay impresoras disponibles.")
    else:
        print("Lista de impresoras disponibles:")
        for idx, (impresora, _) in enumerate(impresoras.items()):
            print(f"{idx + 1}. {impresora}")
    return impresoras

def listar_trabajos_impresion(impresora):
    # Obtener los trabajos en la cola de una impresora específica
    conn = cups.Connection()
    trabajos = conn.getJobs(which_jobs=cups.JOB_PENDING, my_jobs=False)
    if not trabajos:
        print(f"No hay trabajos en la cola de la impresora {impresora}.")
    else:
        print(f"Trabajos en la cola de la impresora {impresora}:")
        for idx, job in trabajos.items():
            if job['printer'] == impresora:
                print(f"{idx}. {job['title']} (ID: {job['id']})")
    return trabajos

def enviar_a_imprimir(impresora, archivo):
    # Enviar un archivo a la impresora
    try:
        conn = cups.Connection()
        job_id = conn.printFile(impresora, archivo, os.path.basename(archivo), {})
        print(f"Archivo {archivo} enviado a la impresora {impresora}. (ID de trabajo: {job_id})")
    except Exception as e:
        print(f"Error al enviar el archivo a imprimir: {e}")

def cancelar_trabajo(impresora, job_id):
    # Cancelar un trabajo en la cola
    try:
        conn = cups.Connection()
        conn.cancelJob(job_id)
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
            trabajos = listar_trabajos_impresion(impresoras[seleccion][0])

        elif opcion == '3':
            if 'impresoras' not in locals() or not impresoras:
                print("Primero debes listar las impresoras.")
                continue
            seleccion = int(input("Selecciona la impresora (por número): ")) - 1
            if seleccion < 0 or seleccion >= len(impresoras):
                print("Opción no válida.")
                continue
            archivo = input("Ingresa la ruta del archivo a imprimir: ")
            enviar_a_imprimir(impresoras[seleccion][0], archivo)

        elif opcion == '4':
            if 'impresoras' not in locals() or not impresoras:
                print("Primero debes listar las impresoras.")
                continue
            seleccion = int(input("Selecciona la impresora (por número): ")) - 1
            if seleccion < 0 or seleccion >= len(impresoras):
                print("Opción no válida.")
                continue
            trabajos = listar_trabajos_impresion(impresoras[seleccion][0])
            if trabajos:
                trabajo_id = int(input("Ingresa el ID del trabajo a cancelar: "))
                cancelar_trabajo(impresoras[seleccion][0], trabajo_id)

        elif opcion == '5':
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
