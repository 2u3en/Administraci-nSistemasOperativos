        #!/bin/bash

        #Propósito:Monitorizar estado servicios indicados
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

        # - Variable de entorno exportada para el uso de cron y at
        export PATH=$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/sbin

       # - Archivo de log personal, que será proporcionado por el script principal, en el que se guardarán los mensajes de log.
        LOG_FILE=$1
      
        # ========================================================================
        # ----- Monitoreo del estado de todos los servicios(Systemd)
        # ========================================================================

        {

        # - Registrar el estado de los servicios cargados en sistema
        # ========================================================================
        echo -e "${BY}============================================================================" 
        echo -e "Lista de todos los servicios activos cargados del sistema y sus dependencias:"         # - Cabecera
        echo -e "============================================================================${NC}"

                # - Listamos todos los servicios en el sistema y sus dependencias, pudiendo ver cuales están activos y cuales no.
                systemctl list-dependencies
                echo "" 


        # - Registro detallado del estado de los servicios críticos
        # ========================================================================
        echo -e "${BY}=============================================="
        echo -e "Logs de estado servicios criticos:"                                                    # - Cabecera
        echo -e "==============================================${NC}" 

        # -- Establecemos algunos servicios criticos del servidor en un array. 
        SERVICIOS=("apache2" "mysql" "ssh" "docker" "cron")  

                # - Comprobamos el estado de cada "SERVICIO" iterando por cada servicio del array "SERVICIOS"
                # - "@" es un carácter comodín para referirnos a todos los elementos del array.

                for SERVICIO in "${SERVICIOS[@]}"; do

                    # - Con "systemctl is-active" obtenemos el estado del servicio iterado.
                    ESTADO=$(systemctl is-active "$SERVICIO")

                    # - Si el estado del servicio es activo, lo registramos en el fichero de log personal y en nuestro logger
                    # con el mensaje del estado del servicio.
                    if [ "$ESTADO" == "active" ]; then
                        echo "Servicio '$SERVICIO' está CORRECTO (activo)." 
                        logger -t "info_monitor" -p local0.info  "Servicio ${SERVICIO} está CORRECTO (activo)"

                    # - Si el servicio no está activo, registramos en el fichero de log personal y en el logger el mensaje.
                    # - En este caso en el logger con un mensaje de warning.
                    else
                        echo "ALERTA: El servicio '$SERVICIO' no está activo o tiene problemas. Estado: $ESTADO" 
                        logger -t "warn_monitor" -p local0.warn  "Servicio ${SERVICIO} no está activo o tiene problemas. Estado: ${ESTADO}"
                    fi

                    # - Obtenemos las 3 últimas líneas de información en detalle del servicio.
                    echo "Estado detallado del servicio '$SERVICIO':"
                    systemctl status "$SERVICIO" 2>/dev/null | tail -n 3   # - Con "2>/dev/null"  evitamos que muestre información por terminal           

                    # Obtenemos los últimos registros del servicio usando journalctl
                    echo "Últimos registros del servicio '$SERVICIO':"
                    journalctl -u "$SERVICIO" 2>/dev/null | tail -n 3 
                    
                    # Línea en blanco para separar cada servicio
                    echo "" 

                done

        # - Registro de servicios fallidos o con algún problema durante su ejecución
        # ========================================================================
        echo -e "${BY}==============================================" 
        echo -e "Lista de servicios con problemas durante su ejecución:"        # - Cabecera
        echo -e "==============================================${NC}" 

        # - Registramos si algún servicio ha fallado o ha tenido algún problema.
        # - Filtramos la salida de "systemctl" con --failed (para servicios fallidos) y --type=service para que muestre solo los servcicios.
        # - Si no filtraramos por service, aparecerían otras unidades como dispositivos.
                systemctl --failed --type=service 


        # - Registramos todo los que están entre {} en nuestro fichero personal de logs.
        } | tee -a "$LOG_FILE" 

        # END