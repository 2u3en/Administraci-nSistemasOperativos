import os
import sys

# Importar los scripts de conexión SSH y RDP
from conexion_ssh import ConexionSSH  # Asumiendo que el script de SSH está en un archivo llamado 'conexion_ssh.py'
from conexion_xfreerdp import ConexionRDP  # Asumiendo que el script de RDP está en un archivo llamado 'conexion_rdp.py'


def menu():
    """Mostrar el menú principal para seleccionar el sistema operativo del servidor."""
    print("\nSeleccione el sistema operativo del servidor al que desea conectarse:")
    print("1. Conectar a un servidor Linux (SSH)")
    print("2. Conectar a un servidor Windows (RDP)")
    print("3. Salir")

    try:
        opcion = int(input("Ingrese su opción (1/2/3): "))
    except ValueError:
        print("Opción no válida. Debe ingresar un número.")
        return None

    if opcion == 1:
        return "linux"
    elif opcion == 2:
        return "windows"
    elif opcion == 3:
        print("Saliendo del programa...")
        sys.exit(0)  # Salir del programa
    else:
        print("Opción no válida.")
        return None


def main():
    while True:
        # Mostrar el menú y capturar la elección del usuario
        eleccion = menu()

        if eleccion == "linux":
            print("\nConectando a un servidor Linux via SSH...")
            host = input("Ingresa la IP o nombre de host del servidor Linux: ")
            puerto = input("Ingresa el puerto (por defecto 22): ")
            usuario = input("Ingresa el nombre de usuario: ")
            clave = input("Ingresa la contraseña: ")

            # Crear y establecer la conexión SSH
            conexion_ssh = ConexionSSH(host, int(puerto) if puerto else 22, usuario, clave)
            conexion_ssh.establecer_conexion()

        elif eleccion == "windows":
            print("\nConectando a un servidor Windows via RDP...")
            host = input("Ingresa la IP o nombre de host del servidor Windows: ")
            puerto = input("Ingresa el puerto (por defecto 3389): ")
            usuario = input("Ingresa el nombre de usuario: ")
            clave = input("Ingresa la contraseña: ")

            # Crear y establecer la conexión RDP
            conexion_rdp = ConexionRDP(host, int(puerto) if puerto else 3389, usuario, clave)
            conexion_rdp.establecer_conexion()


if __name__ == "__main__":
    main()
