#!/bin/bash

NC='\033[0m'
BR='\033[1;31m'
BG='\033[1;32m'
BY='\033[1;33m'
BB='\033[1;34m'
BP='\033[1;35m'
BW='\033[1;37m'

# - Definir archivo de log
LOG_FILE="$1"

# - Comprobar si se proporcionó el archivo de log
if [ -z "$LOG_FILE" ]; then
    echo -e "Se debe proporcionar un archivo de log como argumento."
    exit 1
fi

# ========================================================================
# ----- Función de Monitoreo de Recursos (CPU, Memoria y Procesos)
# ========================================================================

# - Registrar el uso de CPU 
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " Uso de CPU" >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

             cpu_info=$(top -bn1 | grep "Cpu(s)" | sed "s/Cpu(s): *//")

            # Asignar valores a cada etiqueta
            us=$(echo "$cpu_info" | awk '{print $1}' | sed 's/%//')
            sy=$(echo "$cpu_info" | awk '{print $3}' | sed 's/%//')
            ni=$(echo "$cpu_info" | awk '{print $5}' | sed 's/%//')
            id=$(echo "$cpu_info" | awk '{print $9}' | sed 's/%//')
            wa=$(echo "$cpu_info" | awk '{print $11}' | sed 's/%//')
            hi=$(echo "$cpu_info" | awk '{print $13}' | sed 's/%//')
            si=$(echo "$cpu_info" | awk '{print $15}' | sed 's/%//')
            st=$(echo "$cpu_info" | awk '{print $17}' | sed 's/%//')

            # Mostrar los resultados en formato de lista con etiquetas
            
            echo -e "Usuario (us): ${us}%" >> $LOG_FILE
            echo -e "Sistema (sy): ${sy}%" >> $LOG_FILE
            echo -e "Prioridad (ni): ${ni}%" >> $LOG_FILE
            echo -e "Inactivo (id): ${id}%" >> $LOG_FILE
            echo -e "Esperando I/O (wa): ${wa}%" >> $LOG_FILE
            echo -e "Interrupción hardware (hi): ${hi}%" >> $LOG_FILE
            echo -e "Interrupción software (si): ${si}%" >> $LOG_FILE
            echo -e "Steal (st): ${st}%" >> $LOG_FILE
            echo "" >> $LOG_FILE


# - Registrar el uso de memoria
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e "Uso de Memoria" >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

    # Leer el archivo /proc/meminfo y extraer algunas líneas clave
    total_mem=$(grep MemTotal /proc/meminfo | awk '{print $2,$3}')
    free_mem=$(grep MemFree /proc/meminfo | awk '{print $2,$3}')
    buffers_mem=$(grep Buffers /proc/meminfo | awk '{print $2,$3}')
    cached_mem=$(grep Cached /proc/meminfo | awk '{print $2,$3}')

    # Verificar si alguna línea no tiene datos válidos (por ejemplo, si el valor está vacío)
    if [[ -z "$total_mem" || -z "$free_mem" || -z "$buffers_mem" || -z "$cached_mem" ]]; then
    echo "Error: No se pudo obtener la información de la memoria" >> $LOG_FILE
    exit 1
    fi
    
    # Mostrar los resultados 
    echo -e "Total: ${total_mem}" >> $LOG_FILE
    echo -e "Libre: ${free_mem}" >> $LOG_FILE
    echo -e "Buffers: ${buffers_mem}" >> $LOG_FILE
    echo -e "Caché: ${cached_mem}" >> $LOG_FILE



# - Registrar el uso de espacio en disco
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e "Uso de Espacio en Disco" >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE
df -h >> $LOG_FILE
echo "" >> $LOG_FILE

# - Registrar la carga del sistema (load averages)
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e "Carga del Sistema (load averages)" >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE
uptime >> $LOG_FILE
echo "" >> $LOG_FILE