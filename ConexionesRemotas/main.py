import os
import sys
from conexion_ssh import ConexionSSH
from conexion_mstsc import ConexionMSTSC
from conexion_xfreerdp import ConexionRDP
from conexion_remmina import ConexionREMMINA  # Nueva clase para Remmina


def obtener_sistema_operativo():
    """Determinar el sistema operativo desde el que se ejecuta el script."""
    sistema = os.name
    if sistema == "posix":
        return "linux"
    elif sistema == "nt":
        return "windows"
    else:
        print("Sistema no soportado.")
        sys.exit(1)


def menu_conexion_windows():
    """Menú de opciones para conexión en Windows."""
    print("\n¿A qué sistema operativo te vas a conectar?")
    print("1. Windows")
    print("2. Linux")

    try:
        opcion = int(input("Ingrese su opción (1/2): "))
    except ValueError:
        print("Opción no válida. Debe ingresar un número.")
        return None

    if opcion == 1:
        return "windows"
    elif opcion == 2:
        return "linux"
    else:
        print("Opción no válida.")
        return None


def menu_conexion_linux():
    """Menú de opciones para conexión en Linux."""
    print("\n¿A qué sistema operativo te vas a conectar?")
    print("1. Windows")
    print("2. Linux")

    try:
        opcion = int(input("Ingrese su opción (1/2): "))
    except ValueError:
        print("Opción no válida. Debe ingresar un número.")
        return None

    if opcion == 1:
        return "windows"
    elif opcion == 2:
        return "linux"
    else:
        print("Opción no válida.")
        return None


def opciones_conexion_windows_a_windows():
    """Conexión desde Windows a Windows."""
    print("\n¿Quieres conectarte a través de SSH o MSTSC?")
    print("1. Conectar por SSH")
    print("2. Conectar gráficamente (MSTSC)")

    try:
        opcion = int(input("Ingrese su opción (1/2): "))
    except ValueError:
        print("Opción no válida.")
        return None

    if opcion == 1:
        return "ssh"
    elif opcion == 2:
        return "mstsc"
    else:
        print("Opción no válida.")
        return None


def opciones_conexion_windows_a_linux():
    """Conexión desde Windows a Linux."""
    print("\n¿Quieres conectarte a través de SSH?")
    print("1. Conectar por SSH")

    try:
        opcion = int(input("Ingrese su opción (1): "))
    except ValueError:
        print("Opción no válida.")
        return None

    if opcion == 1:
        return "ssh"
    else:
        print("Opción no válida.")
        return None


def opciones_conexion_linux_a_windows():
    """Conexión desde Linux a Windows."""
    print("\n¿Quieres conectarte a través de SSH o XFREERDP?")
    print("1. Conectar por SSH")
    print("2. Conectar gráficamente (XFREERDP)")

    try:
        opcion = int(input("Ingrese su opción (1/2): "))
    except ValueError:
        print("Opción no válida.")
        return None

    if opcion == 1:
        return "ssh"
    elif opcion == 2:
        return "xfreerdp"
    else:
        print("Opción no válida.")
        return None


def opciones_conexion_linux_a_linux():
    """Conexión desde Linux a Linux."""
    print("\n¿Quieres conectarte a través de SSH o REMMINA?")
    print("1. Conectar por SSH")
    print("2. Conectar gráficamente (REMMINA)")

    try:
        opcion = int(input("Ingrese su opción (1/2): "))
    except ValueError:
        print("Opción no válida.")
        return None

    if opcion == 1:
        return "ssh"
    elif opcion == 2:
        return "remmina"
    else:
        print("Opción no válida.")
        return None


def obtener_datos_conexion():
    """Solicitar la IP, puerto, usuario y clave para la conexión."""
    host = input("\nIngresa la IP o nombre de host del servidor: ")
    puerto = input("Ingresa el puerto (por defecto 22 para SSH o 3389 para conexiones gráficas): ")
    puerto = int(puerto) if puerto else 22
    usuario = input("Ingresa el nombre de usuario: ")
    clave = input("Ingresa la contraseña: ")

    return host, puerto, usuario, clave


def main():
    sistema = obtener_sistema_operativo()

    while True:
        if sistema == "windows":
            destino = menu_conexion_windows()

            if destino == "windows":
                metodo = opciones_conexion_windows_a_windows()
                if metodo == "ssh":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_ssh = ConexionSSH(host, puerto, usuario, clave)
                    conexion_ssh.establecer_conexion()
                elif metodo == "mstsc":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_mstsc = ConexionMSTSC(host, puerto, usuario, clave)
                    conexion_mstsc.establecer_conexion()

            elif destino == "linux":
                metodo = opciones_conexion_windows_a_linux()
                if metodo == "ssh":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_ssh = ConexionSSH(host, puerto, usuario, clave)
                    conexion_ssh.establecer_conexion()

        elif sistema == "linux":
            destino = menu_conexion_linux()

            if destino == "windows":
                metodo = opciones_conexion_linux_a_windows()
                if metodo == "ssh":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_ssh = ConexionSSH(host, puerto, usuario, clave)
                    conexion_ssh.establecer_conexion()
                elif metodo == "xfreerdp":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_xfreerdp = ConexionRDP(host, puerto, usuario, clave)
                    conexion_xfreerdp.establecer_conexion()

            elif destino == "linux":
                metodo = opciones_conexion_linux_a_linux()
                if metodo == "ssh":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_ssh = ConexionSSH(host, puerto, usuario, clave)
                    conexion_ssh.establecer_conexion()
                elif metodo == "remmina":
                    host, puerto, usuario, clave = obtener_datos_conexion()
                    conexion_remmina = ConexionREMMINA(host, puerto, usuario, clave)
                    conexion_remmina.establecer_conexion()


if __name__ == "__main__":
    main()
