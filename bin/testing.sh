#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR=${DIR}/..

for plugin in redis_chain_store; do
    echo "Starting tests for ${plugin}"
    celery -E -A celery_task_plugins.${plugin}.tests.celery_app --broker=amqp://rabbitmq_user:rabbitmq_password@rabbitmq:5672 worker -c 2 &
    pytest -sv ${ROOT_DIR}/celery_task_plugins/${plugin}
    pkill -9 -f 'celery'  &> /dev/null
done
