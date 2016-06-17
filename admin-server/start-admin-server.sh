#sed -i "s/%hostname%/$HOSTNAME/g" "${LISTENERS_ORA}" &&
#sed -i "s/%port%/1521/g" "${LISTENERS_ORA}" &&
# [/name = 'AdminServer']
xmlstarlet sel -N x=http://xmlns.oracle.com/weblogic/domain -t -c "x:domain/x:server/x:listen-address" config/config.xml &&
xmlstarlet ed -O -L -N x=http://xmlns.oracle.com/weblogic/domain  -u "x:domain/x:server/x:listen-address" -v $HOSTNAME config/config.xml &&
xmlstarlet sel -N x=http://xmlns.oracle.com/weblogic/domain -t -c "x:domain/x:server/x:listen-address" config/config.xml &&
sh wait-db.sh &&
sh startWebLogic.sh -Djava.security.egd=file:///dev/./urandom
