echo "LISTEN_PORT=$1" >> .env
echo "RUNNER_TYPE=$2" >> .env
echo "MODEL_URL=$3" >> .env
echo "BASE=$4" >> .env

gunicorn --timeout 300 -b :$1 app:app
