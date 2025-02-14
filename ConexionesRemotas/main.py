# ----------------------------------------------------------------------------
# Script: Conexiones Remotas (SSH, MSTSC, XFREERDP, REMMINA)
# Autor: Rubén
# Versión: 1.0.0
# Fecha de creación: 9/02/2025
# Última modificación: 14/02/2025
# Descripción:
#   Este script permite gestionar conexiones remotas entre diferentes sistemas
#   operativos (Windows y Linux), a través de varios métodos.
#   Dependiendo del sistema operativo desde el cual se
#   ejecuta el script, se brindan opciones para conectarse a otros sistemas de
#   forma remota.
# Dependencias:
#   - conexion_ssh.py
#   - conexion_mstsc.py
#   - conexion_xfreerdp.py
#   - conexion_remmina.py
#
# ----------------------------------------------------------------------------

# Importamos las librerías y las clases definidas en los scripts auxiliares para los diferentes tipos de conexión.
import os
import sys
from conexion_ssh import ConexionSSH
from conexion_mstsc import ConexionMSTSC
from conexion_xfreerdp import ConexionRDP
from conexion_remmina import ConexionREMMINA


# Función para determinar el Sistema Operativo desde donde se está ejecutando el script.
def obtener_sistema_operativo():
    """
    Determina el sistema operativo desde el que se ejecuta el script.

    :return: El nombre del sistema operativo ('windows' o 'linux')
    """
    sistema = os.name
    if sistema == "posix":
        return "linux"
    elif sistema == "nt":
        return "windows"
    else:
        print("Sistema no soportado.")
        sys.exit(1)


# Función general para la creación de un menú de selección.
def menu_conexion_origen(sistema_origen):
    """
    Menú para seleccionar el sistema operativo al que se va a conectar,
    dependiendo del sistema desde el cual se ejecuta el script.

    :param sistema_origen: El sistema operativo de origen ('windows' o 'linux')
    :return: El sistema operativo de destino ('windows' o 'linux')
    """
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


# Función para la creación de un menú de selección si el script se ejecuta desde SO Windows hacia Windows.
def opciones_conexion_windows_a_windows():
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


# Función para la creación de un menú de selección si el script se ejecuta desde SO Windows hacia Linux.
def opciones_conexion_windows_a_linux():
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


# Función para la creación de un menú de selección si el script se ejecuta desde SO Linux hacia Windows.
def opciones_conexion_linux_a_windows():
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


# Función para la creación de un menú de selección si el script se ejecuta desde SO Linux hacia Linux.
def opciones_conexion_linux_a_linux():
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


# Función para la solicitud de los datos de conexión al usuario.
def obtener_datos_conexion():
    """Solicitar la IP, puerto, usuario y clave para la conexión."""
    host = input("\nIngresa la IP o nombre de host del servidor: ")
    puerto = input("Ingresa el puerto (por defecto 22 para SSH o 3389 para conexiones gráficas): ")
    puerto = int(puerto) if puerto else 22
    usuario = input("Ingresa el nombre de usuario: ")
    clave = input("Ingresa la contraseña: ")

    return host, puerto, usuario, clave


# Función principal desde donde se instancian las funciones de los menús y de las clases importadas.
def main():
    sistema = obtener_sistema_operativo()  # Obtenemos el tipo de SO

    while True:
        destino = menu_conexion_origen(sistema)  # Llamamos al menú de selección de destino

        if sistema == "windows":
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


# Llamada a la función principal
if __name__ == "__main__":
    main()  # Ejecución de la función principal
