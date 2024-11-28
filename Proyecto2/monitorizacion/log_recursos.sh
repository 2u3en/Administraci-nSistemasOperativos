    #!/bin/bash

    #Propósito:Monitorizar recursos del sistema(CPU,memoria,procesos)
    #FechadeCreación:09/11/2024
    #FechadeModificación:28/11/2024
    #Github:https://github.com/2u3en/Administraci-nSistemasOperativos/tree/f4c79599a213210279e5828ddb569a04041e6e53/Proyecto2/monitorizacion
    #Autor:Rubén P.

    # START

    NC='\033[0m'
    BR='\033[1;31m'
    BG='\033[1;32m'
    BY='\033[1;33m'
    BB='\033[1;34m'
    BP='\033[1;35m'
    BW='\033[1;37m'

    # - Archivo de log personal, que será proporcionado por el script principal, en el que se guardarán los mensajes de log.
    LOG_FILE=$1
   

    # - Comprobar si se proporcionó el archivo de log personal.
    if [ -z "$LOG_FILE" ]; then
        echo -e "Se debe proporcionar un archivo de log como argumento."
        exit 1
    fi

    # ========================================================================
    # ----- Monitoreo de Recursos (CPU, Memoria y Procesos)
    # ========================================================================

    # - Tiempo en funcionamiento del sistema 
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- Tiempo en funcionamiento del sistema -- " >> $LOG_FILE             # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE

    # - En una variable guardamos, con "awk" la columna 3 de la salida del comando "uptime" y borramos la coma del final con "sed"

                timeup=$(uptime -bn1 | awk '{print $3}' | sed 's/,//g')

    # - Registramos en el fichero de log personal la variable con el tiempo en funcionamiento del sistema.
                echo -e "  Tiempo en uso : $timeup" >> $LOG_FILE


    # - Registrar el uso de CPU 
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- Uso de CPU -- " >> $LOG_FILE                                        # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE

    # - En una variable guardamos, con "grep "Cpu(s), la salida del comando "top -bnl", este útlimo con los atributos:
    # -b para ejecutarlo en modo batch, es decir que no se actualice en tiempo real y muestre la salida completa.
    # -n1 para establecer el número de interacciones.
    # - Con "grep "Cpu(s) capturamos la línea y con "sed" eliminamos el principio de la línea

                 cpu_info=$(top -bn1 | grep "Cpu(s)" | sed "s/Cpu(s): *//")


                # Asignar valores a cada etiqueta
    # - Almacenamos en variables cada columna, con "awk", de la línea antes obtenida.
                us=$(echo "$cpu_info" | awk '{print $1}' | sed 's/%//')
                sy=$(echo "$cpu_info" | awk '{print $3}' | sed 's/%//')
                ni=$(echo "$cpu_info" | awk '{print $5}' | sed 's/%//')
                id=$(echo "$cpu_info" | awk '{print $9}' | sed 's/%//')
                wa=$(echo "$cpu_info" | awk '{print $11}' | sed 's/%//')
                hi=$(echo "$cpu_info" | awk '{print $13}' | sed 's/%//')
                si=$(echo "$cpu_info" | awk '{print $15}' | sed 's/%//')
                st=$(echo "$cpu_info" | awk '{print $17}' | sed 's/%//')

                # - Registramos los resultados en formato de lista con etiquetas en el fichero personal.
                echo -e "  Usuario (us): ${us}%" >> $LOG_FILE
                echo -e "  Sistema (sy): ${sy}%" >> $LOG_FILE
                echo -e "  Prioridad (ni): ${ni}%" >> $LOG_FILE
                echo -e "  Inactivo (id): ${id}%" >> $LOG_FILE
                echo -e "  Esperando I/O (wa): ${wa}%" >> $LOG_FILE
                echo -e "  Interrupción hardware (hi): ${hi}%" >> $LOG_FILE
                echo -e "  Interrupción software (si): ${si}%" >> $LOG_FILE
                echo -e "  Steal (st): ${st}%" >> $LOG_FILE
                echo "" >> $LOG_FILE

    # - Enviamos a nuestro fichero de logger creado en exclusiva la información extraída, el cual es diferente al fichero personal de log.
                logger -t "server_monitor" -p local0.info  "Uso de CPU registrado. Usuario (us): ${us}%, Sistema (sy): ${sy}%, Inactivo (id): ${id}%."


    # - Registrar el uso de memoria
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- Uso de Memoria -- " >> $LOG_FILE                                           # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE

    # - Guardamos en variables la salida del comando "top", filtrando las líneas que empiezan por  "MiB Mem" y "MiB Intercambio"
                mem_fisica=$(top -bn1 | grep "MiB Mem")
                mem_swap=$(top -bn1 | grep "MiB Intercambio")
              
    # - Registramos en el fichero personal de log cada variable con la información

                echo -e "  Memoria Física" >> "$LOG_FILE"
                echo -e "  $mem_fisica" >> "$LOG_FILE"

                echo "" >> "$LOG_FILE"

                echo -e "  Memoria Swap" >> "$LOG_FILE"
                echo -e "  $mem_swap" >> "$LOG_FILE"

    # - También enviamos a nuestro fichero de logger la información.
                logger -t "server_monitor" -p local0.info  "Uso de memoria física : ${mem_fisica}, Uso de memoria swap: ${mem_swap} "



    # - Registrar los 5 procesos que más CPU consumen
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- 5 Procesos que más CPU consumen -- " >> $LOG_FILE                          # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE

                # - Creamos una cabecera para indicar los valores.
                echo -e "   PID - %CPU - COMMAND" >> "$LOG_FILE"       

                # ---- Con 'ps' obtenemos los procesos.
                # ---- Con -e(--everyone) indicamos que muestre tanto los procesos del sistema como los de usuario.
                # ---- Con -o personalizamos la salida especificando los campos a mostrar (pid,%cpu,comm)
                # ---- Los ordenamos de mayor a menor uso de cpu con '--sort=-%cpu'
                # ---- Con 'head -n 6' obtenemos las 6 primeras líneas y como la primera es el encabezado, con 'tail -n 5' eliminamos la obtención de este.
                # ---- Por último lo registramos en el fichero.

                ps -eo pid,%cpu,comm --sort=-%cpu | head -n 6 | tail -n 5 >> "$LOG_FILE"    

                  
    # - Registrar los 5 procesos que más memoria consumen
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- 5 Procesos que más memoria consumen -- " >> $LOG_FILE                      # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE


    # - Creamos una cabecera para indicar los valores.
                echo -e "   PID - %MEM - COMMAND" >> "$LOG_FILE"

            # - Esta línea funciona igual que la anterior, pero con el campo de memoria.          
                ps -eo pid,%mem,comm --sort=-%mem | head -n 6 | tail -n 5 >> "$LOG_FILE"        


    # - Registrar el uso de espacio en disco
    # ========================================================================
    echo "" >> $LOG_FILE
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e " -- Uso de Espacio en Discos -- " >> $LOG_FILE                                 # - Cabecera
    echo -e "==============================================${NC}" >> $LOG_FILE

                # - Comando para obtener las particiones y el espacio libre.
                # - Con "df" obtenemos el espacio de disco usado.
                # - Con -h hacemos que la salida sea más fácil de leer 
                # - Con "grep" filtramos la salida de df.
                # - Con -v invertimos el patrón de coincidencia, es decir, indicamos lo que no queremos capturar.
                # - con -E utilizamos expresiones regulares. 

                # - El bucle iterará por cada pertición, guardando en una variable la información de cada columna indicada con "awk".
                df -h | grep -vE 'cdrom|S.ficheros' | while read line; do
                
                # - Extraer el nombre de la partición, el tamaño, el espacio usado y libre
                partition=$(echo $line | awk '{print $1}')
                size=$(echo $line | awk '{print $2}')
                used=$(echo $line | awk '{print $3}')
                available=$(echo $line | awk '{print $4}')
                use_percent=$(echo $line | awk '{print $5}' | sed 's/%//')
                montado=$(echo $line | awk '{print $6}')

                # - Registramos la información de la partición iterada en el fichero personal de log.
                echo -e "  Partición: $partition" >> $LOG_FILE
                echo -e "  Tamaño:$size - Usado:$used - Libre:$available - Uso:$use_percent% - Montado en:$montado" >> $LOG_FILE
                echo "" >>"$LOG_FILE"

                # - Verificamos si el uso de la partición es mayor o igual al 90%

                    # - Si el uso es superior al 90% registramos el mensaje en nuestro fichero personal de log.
                    # - Además registramos en nuestro logger el mensaje de tipo "warning". 
                    if [[ $use_percent -ge 90 ]]; then
                        echo -e "¡Advertencia! La partición $partition tiene más del 90% de espacio usado." >> $LOG_FILE
                        
                        logger -t "server_monitor" -p local0.warn "¡Advertencia! La partición ${partition} tiene más del 90% de espacio usado."

                    fi
                done


    # END