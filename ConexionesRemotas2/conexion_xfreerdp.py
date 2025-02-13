import subprocess

class ConexionRDP:
    def __init__(self, host, puerto, usuario, clave):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave

    def establecer_conexion(self):
        # Comando para establecer la conexión remota usando xfreerdp
        # (puedes usar rdesktop si prefieres)
        comando = [
            'xfreerdp',
            '/v:' + self.host,  # Dirección del servidor RDP
            '/u:' + self.usuario,  # Usuario
            '/p:' + self.clave,  # Contraseña
            '/port:' + str(self.puerto),  # Puerto RDP (por defecto es 3389)
            '/size:600x400'
        ]

        try:
            print("Iniciando la conexión RDP...")
            subprocess.run(comando, check=True)  # Ejecutar el comando
            print(f"Conexión establecida con {self.host}")
        except subprocess.CalledProcessError as e:
            print(f"Error al establecer la conexión: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


# Solicitar los datos al usuario
def solicitar_datos():
    host = input("Ingresa la IP o el nombre del host del servidor RDP: ")
    puerto = input("Ingresa el puerto del servidor RDP (por defecto 3389): ")
    if not puerto:
        puerto = "3389"  # Si no se ingresa puerto, se usa el valor predeterminado.
    usuario = input("Ingresa el nombre de usuario: ")
    clave = input("Ingresa la contraseña: ")

    # Crear la instancia de la conexión RDP
    conexion = ConexionRDP(host, int(puerto), usuario, clave)
    conexion.establecer_conexion()


if __name__ == "__main__":
    print("---¡Bienvenido al script de conexión SSH!---")
    solicitar_datos()
