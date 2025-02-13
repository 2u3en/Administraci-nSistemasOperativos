import subprocess
import platform

class ConexionVNC_X11:
    def __init__(self, host, puerto, usuario, clave, metodo="vnc"):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave
        self.metodo = metodo  # "vnc" o "x11"

    def conexion_vnc(self):
        """Conexión utilizando VNC (usando el cliente vncviewer)."""
        try:
            # Ejecutar el comando VNC
            comando = f"vncviewer {self.host}:{self.puerto}"
            print(f"Conectando mediante VNC a {self.host}:{self.puerto}")
            subprocess.run(comando, shell=True, check=True)
            print(f"Conexión VNC establecida con {self.host}:{self.puerto}")
        except subprocess.CalledProcessError as e:
            print(f"Error al intentar conectar mediante VNC: {e}")
        except Exception as e:
            print(f"Error inesperado al intentar conectar mediante VNC: {e}")

    def conexion_x11(self):
        """Conexión utilizando X11 forwarding (usando ssh -X)."""
        try:
            # Ejecutar la conexión SSH con X11 forwarding
            comando = f"ssh -X {self.usuario}@{self.host} -p {self.puerto}"
            print(f"Conectando mediante X11 forwarding a {self.host}")
            subprocess.run(comando, shell=True, check=True)
            print(f"Conexión X11 establecida con {self.host}")
        except subprocess.CalledProcessError as e:
            print(f"Error al intentar conectar mediante X11: {e}")
        except Exception as e:
            print(f"Error inesperado al intentar conectar mediante X11: {e}")

    def establecer_conexion(self):
        """Establece la conexión dependiendo del método elegido."""
        if self.metodo == "vnc":
            self.conexion_vnc()
        elif self.metodo == "x11":
            self.conexion_x11()
        else:
            print("Método no soportado. Elige 'vnc' o 'x11'.")
