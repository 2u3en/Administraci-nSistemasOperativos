#!/bin/bash

#Propósito:Monitorizar logs
#Versión:1.0
#FechadeCreación:09/11/2024
#FechadeModificación:
#Github:
#Autor:Rubén P.

# START

NC='\033[0m'
BR='\033[1;31m'
BG='\033[1;32m'
BY='\033[1;33m'
BB='\033[1;34m'
BP='\033[1;35m'
BW='\033[1;37m'

# - Directorio para los logs
LOG_DIR="/home/ruben/Documentos/scripts/Proyecto2/scripts_monitorizacion/registroLogs"
DATE=$(date "+%Y-%m-%d_%H:%M:%S")
LOG_FILE="${LOG_DIR}/server_monitor_${DATE}.log"

# - Creación del directorio de logs si no existe
mkdir -p $LOG_DIR

# - Función para registrar la cabecera con la fecha y hora
log_header() {
    echo -e "${BY}==============================================" >> $LOG_FILE
    echo -e "Monitorización del Servidor - $DATE" >> $LOG_FILE
    echo -e "Fecha y Hora: $(date)" >> $LOG_FILE
    echo -e "==============================================${NC}" >> $LOG_FILE
}

# - Llamada a los scripts individuales
log_header
./log_recursos_sistema.sh $LOG_FILE
./log_servicios.sh $LOG_FILE
./log_procesos.sh $LOG_FILE



#./log_network_connections.sh $LOG_FILE

# END