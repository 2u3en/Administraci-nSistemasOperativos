#!/bin/bash

# - Definir archivo de log
LOG_FILE="$1"

# - Comprobar si se proporcionó el archivo de log
if [ -z "$LOG_FILE" ]; then
    echo "Se debe proporcionar un archivo de log como argumento."
    exit 1
fi

# Registrar el estado de los servicios
echo "==============================================" >> $LOG_FILE
echo "Estado de los Servicios:" >> $LOG_FILE
systemctl list-units --type=service --state=running >> $LOG_FILE
echo "" >> $LOG_FILE