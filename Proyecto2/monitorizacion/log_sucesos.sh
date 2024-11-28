    #!/bin/bash

    #Propósito:Monitorizar logs de syslog y dmesg
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


    # ========================================================================
    # ----- Array archivos de logs a analizar
    # ========================================================================

        LOG_DIR="/var/log"          # - Variable para reducir la ruta
        

        SYSLOG_FILES=(              # - Array

            "$LOG_DIR/syslog"       # - Registro de logs generales del sistema.      
            "$LOG_DIR/dmesg"        # - Registro con información del hardware.
            

            # - Ejemplo de mensajes de logs de sistema que sería conveniente agregar en la monitorización de un servidor


            #"$LOG_DIR/kern.log"
            #"$LOG_DIR/messages"     # - Registro de errores en arranque no relacionados con el Kernel.Con él controlaremos los servicios.
            #"$LOG_DIR/btmp"         # - Registro de intentos fallidos de login (Seguridad ante ataque de fuerza bruta).
            #"$LOG_DIR/ufw.log"      # - Registro de logs del firewall.
            #"$LOG_DIR/daemon.log"   # - Registro de logs generados por servicios en segundo plano. 
        )   

    # ========================================================================
    # ----- Palabras clave para filtrar
    # ========================================================================

        # - Palabras clave que utilizaremos para filtrar los mensajes de log
            KEYWORDS=("error" "fail" "critical" "warn" "alert" "panic")

    
    # - Definir archivo de log personal, que será proporcionado por el script principal, en el que se guardarán los mensajes de log.
    LOG_FILE=$1
   

    # - Comprobar si se proporcionó el archivo de log personal.
    if [ -z "$LOG_FILE" ]; then
        echo "Se debe proporcionar un archivo de log como argumento."
        exit 1
    fi


    # ========================================================================
    # ----- Funciones para Registro de Logs
    # ========================================================================
        # ----- Función para filtrar y registrar logs críticos
        # ----- Esta función recibe como argumento el directorio en el que va a buscar las palabras clave.

        # - Iteramos sobre los archivos de log indicados.

    for log_file in "${SYSLOG_FILES[@]}"; do

        # - Verificación de la existencia del archivo de log indicado en el array.
        if [ -f "$log_file" ]; then

            file_name=$(basename "$log_file")  # - Extraemos el nombre del archivo sin la ruta

            echo -e "${BB}==============================================" >> $LOG_FILE                      
            echo -e " -- BÚSQUEDA DE LOGS --"  >> "$LOG_FILE"                                               # - Cabecera 
            echo -e "==============================================${NC}" >> $LOG_FILE

            # - Escribimos en el fichero de registro indicado en el script principal un mensaje indicando que comenzamos la búsqueda de logs en el fichero iterado
            echo -e "${BY}==== Iniciando búsqueda de logs en '$file_name' ====${NC}"  >> "$LOG_FILE"
            
            # - Variable para verificar si encontramos resultados
            found_logs=false

            # - Iteramos sobre cada palabra clave para buscar

            for keyword in "${KEYWORDS[@]}"; do

                # - Filtramos los logs que contienen las palabras clave indicadas

                results=$(grep -i "$keyword" "$log_file" 2>/dev/null | tail -n 3) 

                # - Si se encuentran resultados,es decir, en el fichero iterado, se encuentran palabras clave, registramos la información en el fichero de log personal.

                if [ -n "$results" ]; then      # - Si la variable no esta vacía
                    
                    echo -e "${BY}== Buscando ${BR}'$keyword'${BY} logs en ${BR}'$file_name'${NY} =="${NC} >> "$LOG_FILE"  # - Cabecera con la palabra clave y el fichero de log 
                    
                    echo -e "$results" >> "$LOG_FILE"               # - Registro de los resultados de la iteración de la palabra clave en el fichero, en el fichero personal 

                    echo -e "${BY}== Fin de '$keyword' logs en '$file_name' ==\n${NC}" >> "$LOG_FILE"    # - Cabecera para indicar fin de la búsqueda de la palabra en el fichero  

                    found_logs=true
                fi
            done


            # - Mensaje de que no se encontraron logs para ninguna palabra clave en un fichero indicado.
            if ! $found_logs; then
                echo -e "${BR}  No se encontraron logs para las palabras clave en '$file_name'.${NC}" >> "$LOG_FILE"
            fi

            # - Mensaje para indicar que hemos terminado con ese archivo.
            echo -e "${BY}==== Fin de la búsqueda de logs críticos en '$file_name' ====\n${NC}" >> "$LOG_FILE"

        else
            # - Mensaje de que uno de los archivos indicados en el array no existe.
            echo -e "${BR}El archivo '$log_file' no existe o no se puede acceder.${NC}" >> "$LOG_FILE"
        fi
    done

    # END