import subprocess

class ConexionMSTSC:
    def __init__(self, host, puerto, usuario, clave):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave
        self.rdp_file = "conexion_rdp.rdp"  # Archivo RDP temporal

    def crear_archivo_rdp(self):
        """Crea un archivo RDP con las configuraciones necesarias."""
        contenido = f"""
full address:s:{self.host}:{self.puerto}
username:s:{self.usuario}
password 51:b:{self.clave.encode().hex()}
screen mode id:i:2
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
compression:i:1
winposstr:s:0,3,50,50,1024,768
use multimon:i:0
"""
        try:
            with open(self.rdp_file, "w") as archivo_rdp:
                archivo_rdp.write(contenido)
            print(f"Archivo RDP creado en {self.rdp_file}")
        except Exception as e:
            print(f"Error al crear el archivo RDP: {e}")

    def establecer_conexion(self):
        """Establece la conexión RDP usando el archivo RDP."""
        try:
            # Crear el archivo RDP temporal
            self.crear_archivo_rdp()

            # Usar el comando mstsc para establecer la conexión con el archivo RDP
            subprocess.run(["mstsc", self.rdp_file], check=True)
            print(f"Conexión RDP establecida a {self.host} con usuario {self.usuario}")

        except subprocess.CalledProcessError as e:
            print(f"Error al intentar conectar mediante RDP: {e}")
        except Exception as e:
            print(f"Error inesperado al intentar conectar mediante RDP: {e}")

        # Limpiar el archivo RDP después de su uso
        try:
            subprocess.run(["del", self.rdp_file], shell=True)
            print("Archivo RDP temporal eliminado.")
        except Exception as e:
            print(f"Error al eliminar el archivo RDP temporal: {e}")
