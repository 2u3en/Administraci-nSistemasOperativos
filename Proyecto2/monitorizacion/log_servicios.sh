#!/bin/bash

#Propósito:Monitorizar servicios
#Versión:1.0
#FechadeCreación:09/11/2024
#FechadeModificación:
#Github:
#Autor:Rubén P.

# START

# - 

NC='\033[0m'
BR='\033[1;31m'
BG='\033[1;32m'
BY='\033[1;33m'
BB='\033[1;34m'
BP='\033[1;35m'
BW='\033[1;37m'



# ========================================================================
# ----- Array archivos de logs a analizar
# ========================================================================

    LOG_DIR="/var/log"
    SYSLOG_FILES=(

        "$LOG_DIR/syslog"       # - Registro de logs generales del sistema.
        "$LOG_DIR/auth.log"     # - Registro de las actividades que implican autenticación.
        "$LOG_DIR/dmesg"        # - Registro con información del hardware.
        #"$LOG_DIR/kern.log"
        "$LOG_DIR/messages"     # - Registro de errores en arranque no relacionados con el Kernel.Con él controlaremos los servicios.


        #"$LOG_DIR/btmp"        # - Registro de intentos fallidos de login (Seguridad ante ataque de fuerza bruta).
        "$LOG_DIR/ufw.log"      # - Registro de logs del firewall.
        "$LOG_DIR/daemon.log"   # - Registro de logs generados por servicios en segundo plano. 
    )   

# ========================================================================
# ----- Palabras clave para filtrar
# ========================================================================
        KEYWORDS=("error" "fail" "critical" "warn" "alert" "panic")


# - Definir archivo de log
LOG_FILE="$1"

# - Comprobar si se proporcionó el archivo de log
if [ -z "$LOG_FILE" ]; then
    echo "Se debe proporcionar un archivo de log como argumento."
    exit 1
fi



# ========================================================================
# ----- Monitoreo del estado de todos los servicios
# ========================================================================

# - Registrar el estado de los servicios
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e "Estado de todos los servicios del sistema:" >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

        systemctl list-units --type=service >> $LOG_FILE
        echo "" >> $LOG_FILE





# ========================================================================
# ----- Funciones para Registro de Logs
# ========================================================================
    # ----- Función para filtrar y registrar logs críticos
    # ----- Esta función recibe como argumento el archivo en el que va a buscar las palabras clave.


      # Iteramos sobre los archivos de log
for log_file in "${SYSLOG_FILES[@]}"; do
    # Verificamos si el archivo existe
    if [ -f "$log_file" ]; then
        file_name=$(basename "$log_file")  # Extraemos solo el nombre del archivo sin la ruta

        # Escribimos en el archivo de registro un mensaje indicando que comenzamos la búsqueda
        echo -e "${BY}==== Iniciando búsqueda de logs en '$file_name' ====${NC}"  >> "$LOG_FILE"
        
        # Variable para verificar si encontramos resultados
        found_logs=false

        # Iteramos sobre cada palabra clave para buscar
        for keyword in "${KEYWORDS[@]}"; do
            # Filtramos los logs que contienen la palabra clave
            results=$(grep -i "$keyword" "$log_file" 2>/dev/null)

            if [ -n "$results" ]; then
                # Si encontramos resultados, los registramos en el archivo de log
                echo -e "${BY}== Buscando ${BR}'$keyword'${BY} logs en ${BR}'$file_name'${NY} =="${NC} >> "$LOG_FILE"
                echo -e "$results" >> "$LOG_FILE"
                echo -e "${BY}== Fin de '$keyword' logs en '$file_name' ==\n${NC}" >> "$LOG_FILE"
                found_logs=true
            fi
        done

        # Si no se encontraron logs para ninguna palabra clave, mostramos un mensaje
        if ! $found_logs; then
            echo -e "${BR}  No se encontraron logs para las palabras clave en '$file_name'.${NC}" >> "$LOG_FILE"
        fi

        # Escribimos en el archivo un mensaje para indicar que hemos terminado con este archivo
        echo -e "${BY}==== Fin de la búsqueda de logs críticos en '$file_name' ====\n${NC}" >> "$LOG_FILE"

    else
        # Si el archivo no existe, lo indicamos en el archivo de log
        echo -e "${BR}El archivo '$log_file' no existe o no se puede acceder.${NC}" >> "$LOG_FILE"
    fi
done


# END