import os
import paramiko
import subprocess
import time

class ConexionSSH:
    def __init__(self, host, puerto, usuario, clave=None, clave_privada_path=None):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave
        self.clave_privada_path = clave_privada_path  # Ruta de la clave privada
        self.client = None
        self.channel = None

    # Verifica si ya existen claves SSH, si no las genera.
    def generar_claves(self):
        # Ruta por defecto para la clave SSH
        clave_path = os.path.expanduser('~/.ssh/id_rsa')

        # Si ya existe el par de claves, no generamos uno nuevo
        if os.path.exists(clave_path):
            print("Las claves SSH ya existen.")
            return

        # Si no existen, las generamos
        print("Generando par de claves SSH...")
        try:
            # Ejecutamos el comando para generar las claves
            subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', clave_path, '-N', ''], check=True)
            print(f"Claves generadas en {clave_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error al generar las claves: {e}")

    # Copiar la clave pública al servidor remoto
    def copiar_clave_publica(self):
        clave_publica_path = os.path.expanduser('~/.ssh/id_rsa.pub')

        # Verificamos que la clave pública exista
        if not os.path.exists(clave_publica_path):
            print("No se encontró la clave pública para copiar.")
            return

        print("Copiando la clave pública al servidor...")

        try:
            # Ejecutamos ssh-copy-id con la opción para desactivar la verificación del host
            subprocess.run(['ssh-copy-id', '-o', 'StrictHostKeyChecking=no', '-i', clave_publica_path,
                            f'{self.usuario}@{self.host}'], check=True)
            print(f"Clave pública copiada a {self.host}.")
        except subprocess.CalledProcessError as e:
            print(f"Error al copiar la clave pública: {e}")

    # Aceptar automáticamente la clave del servidor si es la primera vez
    def aceptar_clave_servidor(self):
        print(f"Aceptando la clave del servidor {self.host}...")
        try:
            subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', f'{self.usuario}@{self.host}', 'exit'], check=True)
            print(f"Clave del servidor {self.host} aceptada.")
        except subprocess.CalledProcessError as e:
            print(f"Error al aceptar la clave del servidor: {e}")

    # Establece la conexión SSH utilizando una clave privada o contraseña.
    def establecer_conexion(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.clave_privada_path:
                # Autenticación con clave privada
                private_key = paramiko.RSAKey.from_private_key_file(self.clave_privada_path)
                self.client.connect(self.host, port=self.puerto, username=self.usuario, pkey=private_key)
                print(f"Conexión SSH establecida con {self.host} usando clave privada")
            else:
                # Autenticación con contraseña
                self.client.connect(self.host, port=self.puerto, username=self.usuario, password=self.clave)
                print(f"Conexión SSH establecida con {self.host} usando contraseña")

            # Abrir una shell interactiva
            self.channel = self.client.invoke_shell()
            print(f"Shell interactiva abierta con {self.host}")

            # Continuar con la shell hasta que el usuario decida cerrar
            self.interactuar_con_shell()

        except paramiko.AuthenticationException as e:
            print(f"Error de autenticación: {e}")
        except paramiko.SSHException as e:
            print(f"Error en la conexión SSH: {e}")
        except Exception as e:
            print(f"Error al conectar a {self.host}: {e}")
            self.client = None

    def interactuar_con_shell(self):
        while True:
            try:
                # Esperamos datos de la shell remota
                if self.channel.recv_ready():
                    # Lee la salida de la shell
                    salida = self.channel.recv(1024).decode('utf-8')
                    if salida:
                        print(salida, end="")  # Imprime la salida de la shell

                # Espera una entrada del usuario
                comando = input(f"{self.usuario}@{self.host}:~$ ")

                # Comandos para salir
                if comando.lower() in ['exit', 'quit', 'logout']:
                    print("Cerrando la conexión SSH...")
                    self.cerrar_conexion()
                    break

                if comando:
                    # Envia el comando a la shell remota
                    self.channel.send(comando + '\n')

                # Espera corta para dar tiempo al servidor remoto a procesar el comando
                    time.sleep(0.9)  # Puedes ajustar el tiempo según lo necesites

                # Esperamos y leemos los datos de la shell remota
                    if self.channel.recv_ready():
                        salida = self.channel.recv(1024).decode('utf-8')
                        if salida:
                            print(salida, end="")  # Imprime la salida de la shell

            except KeyboardInterrupt:
                print("\nInterrumpido por el usuario.")
                self.cerrar_conexion()
                break
            except Exception as e:
                print(f"Error en la sesión interactiva: {e}")
                break

    def cerrar_conexion(self):
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        print(f"Conexión cerrada con {self.host}")


def obtener_datos_usuario():
    host = input("Introduce la IP o nombre de dominio del servidor: ")
    puerto = int(input("Introduce el puerto SSH (por defecto 22): ") or 22)
    usuario = input("Introduce el nombre de usuario para la conexión: ")
    clave = input("Introduce la contraseña (si usarás clave privada, déjalo vacío): ")

    # Ruta de la clave privada (opcional)
    clave_privada_path = input("Introduce la ruta de tu clave privada (si no, deja vacío): ")
    if not clave_privada_path:
        clave_privada_path = None

    return host, puerto, usuario, clave, clave_privada_path


if __name__ == "__main__":
    print("---¡Bienvenido al script de conexión SSH!---")

    # Obtener datos del usuario
    host, puerto, usuario, clave, clave_privada_path = obtener_datos_usuario()

    # Crear objeto de conexión SSH
    conexion = ConexionSSH(host=host, puerto=puerto, usuario=usuario, clave=clave, clave_privada_path=clave_privada_path)

    # Generar las claves (si no existen)
    conexion.generar_claves()

    # Copiar la clave pública al servidor
    conexion.copiar_clave_publica()

    # Aceptar la clave del servidor si es la primera vez
    conexion.aceptar_clave_servidor()

    # Establecer la conexión SSH
    conexion.establecer_conexion()
