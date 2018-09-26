#!/bin/bash
#
#  Run tests with coverage.
#  Checks if program is on Drone,
#
if [[ $DRONE ]]
  then
  echo '--------------------------------------'
  echo 'Running tests in Drone.'
  echo '--------------------------------------'

  source venv/bin/activate
  py.test --cov-report term-missing \
          --durations=5 \
          --verbose \
          --cov=skill tests/

  else
  echo '------------------------------------'
  echo 'Running tests in local environment.'
  echo '------------------------------------'

  source venv/bin/activate
  py.test --cov-report term-missing \
          --cov-report html \
          --cov=skill tests/

fi