#!/bin/bash

. ../../env.national_lottery

echo "Starting"

. ${HOME}/flask_venv/bin/activate

echo "Running command: flask run"
flask run >> ${LOG_DIR}/flask_server.log 2>&1 &
rv=$?

exit ${rv}
