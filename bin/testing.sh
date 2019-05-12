#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR=${DIR}/..

plugins=("redis_chain_store" "context_logger")
for plugin in ${plugins[@]}; do
    echo "Starting tests for ${plugin}"
    celery -E -A celery_task_plugins.${plugin}.tests.celery_app --broker=amqp://rabbitmq_user:rabbitmq_password@rabbitmq:5672 worker -c 2 --pidfile /tmp/celery.pid &
    pytest -sv ${ROOT_DIR}/celery_task_plugins/${plugin}
    kill -9 $(cat /tmp/celery.pid)  &> /dev/null
done
