        #!/bin/bash

        #Propósito:Monitorizar servicios
        #FechadeCreación:09/11/2024
        #FechadeModificación:25/11/2024
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


        export PATH=$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/sbin

        # - Definir archivo de log
       
        LOG_FILE=$1
      
        # ========================================================================
        # ----- Monitoreo del estado de todos los servicios(Systemd)
        # ========================================================================

        {

        # - Registrar el estado de los servicios cargados en sistema
        echo -e "${BY}============================================================================" 
        echo -e "Lista de todos los servicios activos cargados del sistema y sus dependencias:" 
        echo -e "============================================================================${NC}"

                systemctl list-dependencies

                echo "" 

        # - Registro detallado del estado de los servicios críticos
        echo -e "${BY}=============================================="
        echo -e "Logs de estado servicios criticos:" 
        echo -e "==============================================${NC}" 


        SERVICIOS=("apache2" "mysql" "ssh" "docker" "cron")  # -- Ejemplo de algunos servicios criticos del servidor. 

                # Comprobar el estado de cada servicio
                for SERVICIO in "${SERVICIOS[@]}"; do
                    # Obtener el estado del servicio
                    ESTADO=$(systemctl is-active "$SERVICIO")


                    # Registrar el estado del servicio
                    if [ "$ESTADO" == "active" ]; then
                        echo "Servicio '$SERVICIO' está CORRECTO (activo)." 
                        logger -t "info_monitor" -p local0.info  "Servicio ${SERVICIO} está CORRECTO (activo)"
                    else
                        echo "ALERTA: El servicio '$SERVICIO' no está activo o tiene problemas. Estado: $ESTADO" 
                        logger -t "warn_monitor" -p local0.warn  "Servicio ${SERVICIO} no está activo o tiene problemas. Estado: ${ESTADO}"
                    fi

                    # Obtener el estado detallado del servicio (usando systemctl status)
                    echo "Estado detallado del servicio '$SERVICIO':"
                    systemctl status "$SERVICIO" 2>/dev/null | tail -n 3 

                    # Obtener los últimos registros del servicio (usando journalctl)
                    echo "Últimos registros del servicio '$SERVICIO':"
                    journalctl -u "$SERVICIO" 2>/dev/null | tail -n 3 
                    
                    # Línea en blanco para separar cada servicio
                    echo "" 

                done

        # - Registro de servicios fallidos o con algún problema durante su ejecución
        echo -e "${BY}==============================================" 
        echo -e "Lista de servicios con problemas durante su ejecución:" 
        echo -e "==============================================${NC}" 

                systemctl --failed --type=service 

        } | tee -a "$LOG_FILE" 

        # END