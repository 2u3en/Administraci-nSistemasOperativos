    #!/bin/bash
    #Propósito:Monitorizar logs
    #Versión:1.0
    #FechadeCreación:09/11/2024
    #FechadeModificación:
    #Github:
    #Autor:Rubén P.

    # START

    # ----- Colores
        nc='\033[0m'        #Sin color
        r='\033[1;31m'      #Rojo
        g='\033[1;32m'      #Verde
        y='\033[1;33m'      #Amarillo
        b='\033[1;34m'      #Azul


    # ========================================================================
    # ----- Directorios y archivo de salida
    # ========================================================================
    LOG_DIR="/var/log"      # - Directorio raíz
         
    OUTPUT_LOG="/home/ruben/Documentos/scripts/Proyecto2/registro_syslog.log"  # - Archivo donde se registran las acciones


    # ========================================================================
    # ----- Array archivos de logs a analizar
    # ========================================================================
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


    # ========================================================================
    # ----- Función para registrar la información obtenida en el archivo definido.
    # ========================================================================
    
    # ----- Esta función recibe un mensaje como argumento y lo escribe en el archivo establecido en la variable añadiendo la fecha y la hora.

    log_action() {
        local mensaje=$1
        local hora=$2

        if [ "$hora" == "true" ]; then
            echo "$(date +'%Y-%m-%d %H:%M:%S') $mensaje" >> "$OUTPUT_LOG"
        else
            echo "$mensaje" >> "$OUTPUT_LOG"
        fi
        
    }


    # ========================================================================
    # ----- Función de Monitoreo de Recursos (CPU, Memoria y Procesos)
    # ========================================================================

    log_usoCpu(){
        # ----- Obtenemos y guardamos en variable el uso de CPU
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

        # ----- Registramos el uso de CPU con fecha y hora. 
        log_action "Uso de CPU: $cpu_usage%" "true"        
    }

    log_usoMem(){
        # ----- Obtenemos y guardamos en variable el uso de memoria
        local memory_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
        log_action "Uso de memoria: $memory_usage%" "true"

    }
    
    log_masCpu(){
        # ----- 5 procesos que más consumen CPU
        log_action "==== 5 procesos que más consumen CPU ====" "true" 

        echo -e "   PID - %CPU - COMMAND" >> "$OUTPUT_LOG"          
        ps -eo pid,%cpu,comm --sort=-%cpu | head -n 6 | tail -n 5 >> "$OUTPUT_LOG"    

        # ---- Con 'ps' obtenemos los procesos.
        # ---- Con -e(--everyone) indicamos que muestre tanto los procesos del sistema como los de usuario.
        # ---- Con -o personalizamos la salida especificando los campos a mostrar (pid,%cpu,comm)
        # ---- Los ordenamos de mayor a menor uso de cpu con '--sort=-%cpu'
        # ---- Con 'head -n 6' obtenemos las 6 primeras líneas y como la primera es el encabezado, con 'tail -n 5' eliminamos la obtención de este.
        # ---- Por último lo registramos en el fichero.         

    }
    

    log_masMem(){
    # ----- 5 procesos que más consumen Memoria
        log_action "==== 5 procesos que más consumen CPU ====" "true" 

        echo -e "   PID - %CPU - COMMAND" >> "$OUTPUT_LOG" 
        ps -eo pid,%mem,comm --sort=-%mem | head -n 6 | tail -n 5 >> "$OUTPUT_LOG"

    }

    
    log_usoParticiones(){
    # ----- Notificar si una partición tiene menos de un 10% de espacio libre.
        local LIMITE=90 

        echo -e "${b}==== Espacio libre en las particiones ====${nc}" >> "$OUTPUT_LOG"

        # ----- Comando para obtener las particiones y el espacio libre
        df -h --output=source,pcent | grep -vE '^Filesystem|tmpfs|cdrom' | while read line; do

        # ----- Leer la información de la partición y el porcentaje de uso
        particion=$(echo $line | awk '{print $1}')
        porcentaje=$(echo $line | awk '{print $2}' | tr -d '%')

        # ----- Verificar si el porcentaje de uso es mayor que el umbral
            if [ "$porcentaje" -ge $((100 - LIMITE)) ]; then
        # ----- Registrar la alerta
            log_action "${r}ALERTA: La partición '$particion' tiene menos del $LIMITE% de espacio libre.${nc}" "true"
            fi
        done

    }



    # ========================================================================
    # ----- Funciones para Registro de Logs
    # ========================================================================

    # ----- Función para filtrar y registrar logs críticos

    # ----- Esta función recibe como argumento el archivo en el que va a buscar las palabras clave.

    filter_critical_logs() {
        local log_file=$1
        local file_name=$(basename "$log_file")  # ----- Extraemos el nombre del archivo sin la ruta

    # ----- Escribimos en el archivo de registro un mensaje para indicar el archivo registrado.
        log_action "${b}==== Iniciando búsqueda de logs en '$file_name' ====
                            ---------------------------------${nc}"        

    # ----- Iteramos sobre cada palabra clave.
        for keyword in "${KEYWORDS[@]}"; do
     
    # ----- Mensaje que indica que palabra clave se ha registrado en que archivo, ayudando a la visualización.       
            log_action "== Buscando ${r}'$keyword'${y} logs en ${r}'$file_name'${nc} ==${nc}"
            

    # ----- Filtramos los logs que contienen la palabra clave y redirigimos la salida de grep al archvio de log definido.
    # ----- Además ocultamos cualquier mensaje que pueda mostrar 'grep' en terminal.
            grep -i "$keyword" "$log_file" >> "$OUTPUT_LOG" 2>/dev/null

     # ----- Escribimos en el archivo un mensaje para indicar el fin del resgistro de la palabra clave en el archivo.
            log_action "== Fin de '$keyword' logs en '$file_name' ==\n"
            
        done

     # ----- Escribimos en el archivo un mensaje para indicar el fin del resgistro de logs en el fichero.
        log_action "${g}==== Fin de la búsqueda de logs críticos en '$file_name' ====\n${nc}"
        
    }

    
    # ========================================================================
    # ----- Función Principal para Procesar Logs y Recursos
    # ========================================================================

    process_logs() {
        # ----- Registrar el uso de recursos del sistema

        echo "" >> "$OUTPUT_LOG"
        echo -e "${b}==== Uso de CPU y Memoria ====${nc}" >> "$OUTPUT_LOG"

        log_usoCpu
        log_usoMem

        echo -e "${b}=========================\n${nc}" >> "$OUTPUT_LOG"

        log_masCpu

        echo ""
        echo -e "${b}=========================\n${nc}" >> "$OUTPUT_LOG"

        log_masMem

        echo ""
        echo -e "${b}=========================\n${nc}" >> "$OUTPUT_LOG"
        echo ""

        log_usoParticiones        

        # ----- Procesar los archivos de logs
        for log_file in "${SYSLOG_FILES[@]}"; do
            if [ -f "$log_file" ]; then
                filter_critical_logs "$log_file"
            else
                log_action "${y}El archivo '$log_file' no existe o no se puede acceder.${nc}"
            fi
        done
    }

    # ========================================================================
    # ----- Ejecución del Script
    # ========================================================================

    process_logs
    echo -e "${g} - Fin de ejecución - ${nc}"

    # END
