FROM tmp-oracle-soa-domain

MAINTAINER Jorge Quilcate <jorge.quilcate at sysco.no>

ENV DOMAIN_HOME /opt/oraclefmw/config/domains/domain1
ENV DB_HOST soa-database
ENV DB_PORT 1521
ENV DB_NAME orcl

USER oraclefmw

WORKDIR $DOMAIN_HOME

ADD wait-db.sh .

EXPOSE 7001

CMD sh wait-db.sh && sh startWebLogic.sh -Djava.security.egd=file:///dev/./urandom
