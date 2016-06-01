export SLEEPTIME=5

#Loop determining state of WLS
function check_wls {
    ACTION=$1
    while true
    do
        echo -e "***** Waiting for WebLogic server to get $ACTION *****"
        sleep $SLEEPTIME
        status=`lwp-request http://$ADMIN_SERVER_HOST:$ADMIN_SERVER_PORT | grep "500 Can't connect"`
        if [ "$ACTION" == "started" ] && [ -z "$status" ]; then
            break
        elif [ "$ACTION" == "shutdown" ] && [ ! -z "$status" ]; then
            break
        fi
    done
    echo -e "\nWebLogic Server has $ACTION\n"
}
