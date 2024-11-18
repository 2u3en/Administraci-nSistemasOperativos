#!/bin/bash

#Propósito:Monitorizar recursos del sistema
#Versión:1.0
#FechadeCreación:09/11/2024
#FechadeModificación:
#Github:
#Autor:Rubén P.

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
# ----- Monitoreo de Recursos (CPU, Memoria y Procesos)
# ========================================================================

# START

# - Registrar el uso de CPU 
# ========================================================================
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " -- Uso de CPU -- " >> $LOG_FILE
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
            
            echo -e "  Usuario (us): ${us}%" >> $LOG_FILE
            echo -e "  Sistema (sy): ${sy}%" >> $LOG_FILE
            echo -e "  Prioridad (ni): ${ni}%" >> $LOG_FILE
            echo -e "  Inactivo (id): ${id}%" >> $LOG_FILE
            echo -e "  Esperando I/O (wa): ${wa}%" >> $LOG_FILE
            echo -e "  Interrupción hardware (hi): ${hi}%" >> $LOG_FILE
            echo -e "  Interrupción software (si): ${si}%" >> $LOG_FILE
            echo -e "  Steal (st): ${st}%" >> $LOG_FILE
            echo "" >> $LOG_FILE


# - Registrar el uso de memoria
# ========================================================================
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " -- Uso de Memoria -- " >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

            mem_fisica=$(top -b -n 1 | grep "MiB Mem")
            mem_swap=$(top -b -n 1 | grep "MiB Intercambio")
          

            echo -e "  Memoria Física" >> "$LOG_FILE"
            echo -e "  $mem_fisica" >> "$LOG_FILE"

            echo "" >> "$LOG_FILE"

            echo -e "  Memoria Swap" >> "$LOG_FILE"
            echo -e "  $mem_swap" >> "$LOG_FILE"


# - Registrar los 5 procesos que más CPU consumen
# ========================================================================
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " -- 5 Procesos que más CPU consumen -- " >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

            echo -e "   PID - %CPU - COMMAND" >> "$LOG_FILE"          
            ps -eo pid,%cpu,comm --sort=-%cpu | head -n 6 | tail -n 5 >> "$LOG_FILE"    

            # ---- Con 'ps' obtenemos los procesos.
            # ---- Con -e(--everyone) indicamos que muestre tanto los procesos del sistema como los de usuario.
            # ---- Con -o personalizamos la salida especificando los campos a mostrar (pid,%cpu,comm)
            # ---- Los ordenamos de mayor a menor uso de cpu con '--sort=-%cpu'
            # ---- Con 'head -n 6' obtenemos las 6 primeras líneas y como la primera es el encabezado, con 'tail -n 5' eliminamos la obtención de este.
            # ---- Por último lo registramos en el fichero.  


# - Registrar los 5 procesos que más memoria consumen
# ========================================================================
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " -- 5 Procesos que más memoria consumen -- " >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

            echo -e "   PID - %MEM - COMMAND" >> "$LOG_FILE"          
            ps -eo pid,%mem,comm --sort=-%mem | head -n 6 | tail -n 5 >> "$LOG_FILE"        


# - Registrar el uso de espacio en disco
# ========================================================================
echo "" >> $LOG_FILE
echo -e "${BY}==============================================" >> $LOG_FILE
echo -e " -- Uso de Espacio en Discos -- " >> $LOG_FILE
echo -e "==============================================${NC}" >> $LOG_FILE

            # ----- Comando para obtener las particiones y el espacio libre
            df -h | grep -vE 'cdrom|S.ficheros' | while read line; do
            
            # Extraer el nombre de la partición, el tamaño, el espacio usado y libre
            partition=$(echo $line | awk '{print $1}')
            size=$(echo $line | awk '{print $2}')
            used=$(echo $line | awk '{print $3}')
            available=$(echo $line | awk '{print $4}')
            use_percent=$(echo $line | awk '{print $5}' | sed 's/%//')
            montado=$(echo $line | awk '{print $6}')

            # Mostrar información de la partición
            echo -e "  Partición: $partition" >> $LOG_FILE
            echo -e "  Tamaño:$size - Usado:$used - Libre:$available - Uso:$use_percent% - Montado en:$montado" >> $LOG_FILE
            echo "" >>"$LOG_FILE"

            # Verificar si el uso de la partición es mayor o igual al 90%
                if [[ $use_percent -ge 90 ]]; then
                    echo -e "¡Advertencia! La partición $partition tiene más del 90% de espacio usado." >> $LOG_FILE
                
                fi
            done


# END