    #!/bin/bash

    #Propósito:Monitorizar recursos,sucesos y servicios del sistema
    #Versión:2.0
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


    # - Variables de entorno exportadas para el uso de cron y at
    export PATH=$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/sbin
    export HOME=/home/ruben/Documentos/scripts/Proyecto2/monitorizacion/

    # - Directorio para los logs
    DATE=$(date "+%Y-%m-%d_%H:%M:%S") # - Variable para fecha y hora
    LOG_FILE="/var/log/SERVERMONITOR/server_monitor_${DATE}.log"  # - Creamos un fichero personal de logs con el nombre "server_monitor" junto a la fecha y hora
    LOG_DIR="/var/log/SERVERMONITOR" # - Creamos el directorio personal de log

    # - Creación del directorio de logs si no existe
        if [ ! -d "$LOG_DIR" ]; then
            # - Si no existe, creamos el directorio
             mkdir -p "$LOG_DIR"
            # - Cambiamos el propietario del directorio para que sea accesible
             chown $(whoami):$(whoami) "$LOG_DIR"
            #  - Configuramos permisos de lectura, escritura y ejecución
             chmod 755 "$LOG_DIR"    
        fi


    # - Función para registrar la cabecera con la fecha y hora
    header() {
        echo -e "${BG}======================================================" >> $LOG_FILE
        echo -e " SCRIPT SUPERVISIÓN INTEGRAL DE UN SERVIDOR LINUX " >> $LOG_FILE
        echo -e "Fecha y Hora: $(date)" >> $LOG_FILE
        echo -e "======================================================${NC}" >> $LOG_FILE
    }

    cabecera_recursos(){
        echo -e "${BB}===================================================" >> $LOG_FILE
        echo -e " -- RECURSOS DEL SISTEMA -- $(date)" >> $LOG_FILE
        echo -e "========================================================${NC}" >> $LOG_FILE
    }

    cabecera_servicios(){
        echo -e "${BB}===================================================" >> $LOG_FILE
        echo -e " -- SERVICIOS DEL SISTEMA -- $(date)" >> $LOG_FILE
        echo -e "========================================================${NC}" >> $LOG_FILE
    }

    cabecera_sucesos(){
        echo -e "${BB}=======================================================" >> $LOG_FILE
        echo -e " -- LOGS DE SISTEMA -- $(date)" >> $LOG_FILE
        echo -e "=======================================================${NC}" >> $LOG_FILE
    }

        
        

        # - Llamada a los scripts individuales y sus cabeceras.
        # ========================================================================

        # - Invocamos a los scripts individuales con la ruta absoluta para no tener problemas a la hora de su ejecución con CRON o AT
        # - Con $LOG_FILE le indicamos a los scripts cual es el fichero donde han de guardar la información que obtiene.
        # - Además registramos en el logger personal la finalización de su ejecución.

        # - Registro en el logger personal del inicio de la monitorización
        logger -t "server_monitor" -p local0.info "INICIO DE LA MONITORIZACION DEL SERVIDOR"

        header

        cabecera_recursos

        /home/ruben/Documentos/scripts/Proyecto2/monitorizacion/log_recursos.sh $LOG_FILE 
        logger -p local0.info -t "server_monitor" "Recursos del sistema registrados"


        cabecera_sucesos
        /home/ruben/Documentos/scripts/Proyecto2/monitorizacion/log_sucesos.sh $LOG_FILE 
        logger -p local0.info -t "server_monitor" "Sucesos del sistema registrados"

        cabecera_servicios
        /home/ruben/Documentos/scripts/Proyecto2/monitorizacion/log_servicios.sh $LOG_FILE >/dev/null
        logger -p local0.info -t "server_monitor" "Estado servicios criticos registrados" 

        # - Registro en el logger personal del fin de la monitorización
        logger -t "server_monitor" -p local0.info "FIN DE LA MONITORIZACION DEL SERVIDOR"
        

    # END