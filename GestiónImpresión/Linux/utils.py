from colorama import Fore, Style

def mostrar_mensaje(color, mensaje):
    # Función para mostrar mensajes con colores personalizados
    print(f"{color}{mensaje}{Style.RESET_ALL}")

def manejar_error(error):
    # Función para manejar errores y mostrar mensajes
    print(f"{Fore.RED}Error: {error}{Style.RESET_ALL}")