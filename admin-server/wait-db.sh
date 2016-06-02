echo ">> Waiting for oracle database to start"
while true; do
    result="$(tnsping $DB_HOST:$DB_PORT/$DB_NAME)"
    echo "$result"
    if [ "$result" == 'OK' ]; then
        break
    fi
    sleep 10
done
echo "Database started!"
