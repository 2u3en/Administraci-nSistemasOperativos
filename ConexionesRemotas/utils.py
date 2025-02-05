import getpass

# Función para obtener datos de conexión para SSH
def obtener_datos_ssh():
    """Solicita al usuario la información de la conexión SSH."""
    host = input("Introduce la dirección IP o nombre del host remoto: ")
    puerto = input("Introduce el puerto (por defecto es 22): ")
    if not puerto:
        puerto = 22  # Valor por defecto para SSH
    usuario = input("Introduce el nombre de usuario: ")
    clave = getpass.getpass("Introduce la contraseña: ")

    return host, puerto, usuario, clave

# Función para obtener datos de conexión para RDP (Windows)
def obtener_datos_rdp():
    """Solicita al usuario la información de la conexión RDP."""
    host = input("Introduce la dirección IP o nombre del host remoto: ")
    puerto = input("Introduce el puerto (por defecto es 3389): ")
    if not puerto:
        puerto = 3389  # Valor por defecto para RDP
    usuario = input("Introduce el nombre de usuario: ")
    clave = getpass.getpass("Introduce la contraseña: ")

    return host, puerto, usuario, clave