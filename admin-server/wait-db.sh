echo ">> Waiting for oracle database to start"
while true; do
    tnsping $DB_HOST:$DB_PORT/$DB_NAME < /dev/null
    echo $?;
    if [ $? -eq "OK" ]; then
        break
    fi
    sleep 10
done
echo "Database started!"
