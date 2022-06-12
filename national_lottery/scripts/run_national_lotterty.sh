. ../project.envs

echo "Starting"

. ${HOME}/flask_venv/bin/activate

echo "Running command: flask run"
flask run >> ${HOME}/WS/projects/flask_dev/logs/flask_server.log 2>&1 &
rv=$?

exit ${rv}
