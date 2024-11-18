#!/bin/bash

# - Definir archivo de log
LOG_FILE="$1"

# - Comprobar si se proporcionó el archivo de log
if [ -z "$LOG_FILE" ]; then
    echo "Se debe proporcionar un archivo de log como argumento."
    exit 1
fi

# - Registrar los procesos en ejecución
echo "==============================================" >> $LOG_FILE
echo "Procesos en Ejecución:" >> $LOG_FILE
ps aux --sort=-%cpu | head -n 20 >> $LOG_FILE
echo "" >> $LOG_FILE