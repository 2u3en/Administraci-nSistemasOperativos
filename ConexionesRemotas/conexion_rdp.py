import subprocess


def crear_conexion_mstsc(host, puerto, usuario, clave):
    """Crea la conexión remota utilizando MSTSC (Remote Desktop)."""
    archivo_rdp = f"{host}:{puerto}"

    # Crear un archivo RDP temporal con los datos de configuración
    rdp_file_content = f"""
    full address:s:{archivo_rdp}
    username:s:{usuario}
    password 51:b:{clave.encode('utf-16le').hex()}
    """

    # Guardamos el archivo .rdp temporal
    with open('conexion_remota.rdp', 'w') as file:
        file.write(rdp_file_content)

    print("\nConexión RDP configurada. Abriendo cliente MSTSC...")

    # Llamamos a MSTSC para abrir la conexión
    subprocess.run(["mstsc", "conexion_remota.rdp"])