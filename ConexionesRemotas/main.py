import platform
from conexion_ssh import ConexionSSH
from conexion_rdp import crear_conexion_mstsc
from utils import obtener_datos_ssh, obtener_datos_rdp


def gestionar_conexion_ssh(host, puerto, usuario, clave):
    """Gestiona la conexión SSH y abre una shell interactiva."""
    conexion = ConexionSSH(host, puerto, usuario, clave)
    conexion.establecer_conexion()


def main():
    sistema_operativo = platform.system()

    if sistema_operativo == 'Windows':
        print("Sistema operativo detectado: Windows")

        # Obtener los datos de la conexión RDP desde el usuario
        host, puerto, usuario, clave = obtener_datos_rdp()

        # Crear la conexión RDP usando MSTSC
        crear_conexion_mstsc(host, puerto, usuario, clave)

    elif sistema_operativo == 'Linux':
        print("Sistema operativo detectado: Linux (Ubuntu)")

        # Obtener los datos de la conexión SSH desde el usuario
        host, puerto, usuario, clave = obtener_datos_ssh()

        # Establecer y gestionar la conexión SSH interactiva
        gestionar_conexion_ssh(host, puerto, usuario, clave)

    else:
        print(f"Sistema operativo no soportado: {sistema_operativo}")
        return


if __name__ == '__main__':
    main()