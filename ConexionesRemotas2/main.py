import os
import sys
import platform
from conexion_ssh import ConexionSSH
from conexion_xfreerdp import ConexionRDP
from conexion_mstsc import ConexionMSTSC
from conexion_vnc_x11 import ConexionVNC_X11  # Script de VNC o X11


def menu():
    """Mostrar el menú principal para seleccionar el sistema operativo del servidor."""
    print("\nSeleccione el sistema operativo del servidor al que desea conectarse:")
    print("1. Conectar a un servidor Linux")
    print("2. Conectar a un servidor Windows")
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
        sys.exit(0)
    else:
        print("Opción no válida.")
        return None


def elegir_conexion_linux():
    """Si estamos en Linux, le damos la opción al usuario de conectarse a Linux o Windows."""
    print("\n¿A qué sistema desea conectarse?")
    print("1. Conectar a un servidor Linux")
    print("2. Conectar a un servidor Windows")
    print("3. Volver al menú principal")

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
        return "main"
    else:
        print("Opción no válida.")
        return None


def elegir_conexion_windows():
    """Si estamos en Windows, le damos las opciones de conexión adecuadas."""
    print("\n¿A qué sistema desea conectarse desde Windows?")
    print("1. Conectar a un servidor Linux (solo SSH)")
    print("2. Conectar a un servidor Windows (RDP o SSH)")
    print("3. Volver al menú principal")

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
        return "main"
    else:
        print("Opción no válida.")
        return None


def main():
    sistema_actual = platform.system().lower()

    while True:
        if sistema_actual == "linux":
            eleccion = elegir_conexion_linux()

            if eleccion == "linux":
                print("\nConectando a un servidor Linux...")
                host = input("Ingresa la IP o nombre de host: ")
                puerto = input("Ingresa el puerto (por defecto 22): ")
                usuario = input("Ingresa el nombre de usuario: ")
                clave = input("Ingresa la contraseña: ")

                # Conexión SSH
                conexion_ssh = ConexionSSH(host, int(puerto) if puerto else 22, usuario, clave)
                conexion_ssh.establecer_conexion()

            elif eleccion == "windows":
                print("\nConectando a un servidor Windows...")
                host = input("Ingresa la IP o nombre de host: ")
                puerto = input("Ingresa el puerto (por defecto 3389): ")
                usuario = input("Ingresa el nombre de usuario: ")
                clave = input("Ingresa la contraseña: ")

                # Opción gráfica usando xfreerdp o por terminal usando SSH
                print("¿Cómo deseas conectarte a Windows?")
                print("1. Conexión gráfica (xfreerdp)")
                print("2. Conexión por terminal (SSH)")
                opcion = int(input("Seleccione la opción (1/2): "))

                if opcion == 1:
                    # Conexión gráfica usando xfreerdp
                    conexion_rdp = ConexionRDP(host, int(puerto) if puerto else 3389, usuario, clave)
                    conexion_rdp.establecer_conexion()

                elif opcion == 2:
                    # Conexión SSH
                    conexion_ssh = ConexionSSH(host, int(puerto) if puerto else 22, usuario, clave)
                    conexion_ssh.establecer_conexion()

        elif sistema_actual == "windows":
            eleccion = elegir_conexion_windows()

            if eleccion == "linux":
                print("\nConectando a un servidor Linux vía SSH...")
                host = input("Ingresa la IP o nombre de host: ")
                puerto = input("Ingresa el puerto (por defecto 22): ")
                usuario = input("Ingresa el nombre de usuario: ")
                clave = input("Ingresa la contraseña: ")

                # Conexión SSH
                conexion_ssh = ConexionSSH(host, int(puerto) if puerto else 22, usuario, clave)
                conexion_ssh.establecer_conexion()

            elif eleccion == "windows":
                print("\nConectando a un servidor Windows...")
                host = input("Ingresa la IP o nombre de host: ")
                puerto = input("Ingresa el puerto (por defecto 3389): ")
                usuario = input("Ingresa el nombre de usuario: ")
                clave = input("Ingresa la contraseña: ")

                # Conexión gráfica usando RDP (mstsc) o por terminal SSH
                print("¿Cómo deseas conectarte a Windows?")
                print("1. Conexión gráfica (mstsc)")
                print("2. Conexión por terminal (SSH)")
                opcion = int(input("Seleccione la opción (1/2): "))

                if opcion == 1:
                    # Conexión gráfica usando mstsc (RDP)
                    conexion_rdp = ConexionMSTSC(host, int(puerto) if puerto else 3389, usuario, clave)
                    conexion_rdp.establecer_conexion()

                elif opcion == 2:
                    # Conexión SSH
                    conexion_ssh = ConexionSSH(host, int(puerto) if puerto else 22, usuario, clave)
                    conexion_ssh.establecer_conexion()


if __name__ == "__main__":
    main()
