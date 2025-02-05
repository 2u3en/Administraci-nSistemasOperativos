import paramiko


class ConexionSSH:
    def __init__(self, host, puerto, usuario, clave):
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.clave = clave
        self.client = None
        self.channel = None

    def establecer_conexion(self):
        """Establece la conexión SSH y abre una shell interactiva."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, port=self.puerto, username=self.usuario, password=self.clave)
            print(f"Conexión SSH establecida con {self.host}")

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
        """Mantiene la sesión de shell abierta hasta que el usuario decida salir."""
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
                if comando.lower() in ['exit', 'quit', 'logout']:  # Comandos para salir
                    print("Cerrando la conexión SSH...")
                    self.cerrar_conexion()
                    break
                if comando:
                    # Envia el comando a la shell remota
                    self.channel.send(comando + '\n')

            except KeyboardInterrupt:
                print("\nInterrumpido por el usuario.")
                self.cerrar_conexion()
                break
            except Exception as e:
                print(f"Error en la sesión interactiva: {e}")
                break

    def cerrar_conexion(self):
        """Cierra la conexión SSH y la shell."""
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        print(f"Conexión cerrada con {self.host}")