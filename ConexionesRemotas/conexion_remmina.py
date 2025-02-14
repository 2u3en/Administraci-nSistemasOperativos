import subprocess


class ConexionREMMINA:
    def __init__(self, host, puerto, usuario, clave):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave

    def establecer_conexion(self):
        # Creamos el comando para iniciar Remmina
        comando = ['remmina', '--connect', f'rdp://{self.usuario}:{self.clave}@{self.host}:{self.puerto}']

        try:
            subprocess.run(comando, check=True)
            print("Conexión establecida con éxito.")
        except subprocess.CalledProcessError as e:
            print(f"Ocurrió un error al intentar conectar: {e}")
        except FileNotFoundError:
            print("Remmina no está instalado. Instálalo para usar esta función.")
