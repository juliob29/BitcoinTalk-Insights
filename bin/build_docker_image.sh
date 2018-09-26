#!/bin/bash
#
#  Builds Docker image of the
#  `skill-bitcointalk-insights` program.
#
VERSION=$1
docker build --tag registry.dataproducts.team/skill-bitcointalk-insights:$VERSION \
             --tag registry.dataproducts.team/skill-bitcointalk-insights:latest \
             .