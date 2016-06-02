FROM tmp-oracle-soa-domain

MAINTAINER Jorge Quilcate <jorge.quilcate at sysco.no>

ENV DOMAIN_HOME /opt/oraclefmw/config/domains/domain1
ENV ADMIN_SERVER_HOST admin-server
ENV ADMIN_SERVER_PORT 7001
ENV MANAGED_SERVER_NAME server1
ENV MANAGED_SERVER_PORT 7003

USER oraclefmw

WORKDIR $DOMAIN_HOME

ADD wait-admin-server.sh .

EXPOSE $MANAGED_SERVER_PORT

CMD sh wait-admin-server.sh && \
    sh bin/startManagedWebLogic.sh $MANAGED_SERVER_NAME t3://$ADMIN_SERVER_HOST:$ADMIN_SERVER_PORT -Djava.security.egd=file:///dev/./urandom
