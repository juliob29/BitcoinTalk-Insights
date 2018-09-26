#!/bin/sh
#
#  Copy the file 'postgresql.locl.conf' (which contains custom
#  configuration settings for the database) to its intended
#  location /var/lib/postgresql/data/postgresql.conf, and add
#  a line to the main postgres configuration file at
#  /var/lib/postgresql/data/postgresql.conf to include it.
#
#  We have to do things in this roundabout way because the
#  postgres Docker container mounts an external volume to
#  the directory /var/lib/postgresql/data/. Therefore we
#  can't copy anything to this directory in the Dockerfile
#  directly because the change won't take effect.
#
#
#  Pre-loaded libraries at startup. The libraries
#  `cstore_fdw` and `pg_cron` need to be installed
#  in order for the following lines to run.
#
# printf "\nshared_preload_libraries = 'cstore_fdw'" >> /var/lib/postgresql/data/postgresql.conf
#
#  Changes the acceptance of connections
#  to all.
#
printf "\nlisten_addresses = '*'" >> /var/lib/postgresql/data/postgresql.conf