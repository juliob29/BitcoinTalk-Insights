#
#  Crypto POSTGRES
#  --------------
#  PostgreSQL instance for Crypto configured
#  to use TimescaleDB.
#
#
FROM timescale/timescaledb:0.10.1-pg10
MAINTAINER Julio Ballista <juliob@stanford.edu>

#
#  General environment variables. Most importantly,
#  these are used for managing locale configuration.
#
ENV POSTGRES_DB=crypto
ENV POSTGRES_USER=crypto
ENV LC_ALL=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

#
#  CONFIGURATION
#  -------------
#
#  We import configuration files to the
#  database here. These build the database schema.
#
RUN mkdir -p /docker-entrypoint-initdb.d

#
#  Add local data to PostgreSQL data ingestion
#  directory. Files in that directory will be
#  ingested by PostgreSQL on build-time.
#
ADD ./sql/* /docker-entrypoint-initdb.d/
ADD ./build/* /docker-entrypoint-initdb.d/

ENV POSTGRES_PASSWORD=

EXPOSE 5432
