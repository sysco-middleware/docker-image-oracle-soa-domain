#Loop determining state of WLS
echo ">>> Waiting for WebLogic server to get started"
while true; do
    status="$(lwp-request http://$ADMIN_SERVER_HOST:$ADMIN_SERVER_PORT | grep 'Connection refused')"
    echo "$status"
    if [ -z "$status" ]; then
        break
    fi
    sleep 10
done
echo -e "\nWebLogic Server has started\n"
