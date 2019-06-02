from celery_task_plugins.base import combined_task_plugins
from celery_task_plugins.redis_chain_store.task import CeleryChainPlugin
from celery_task_plugins.testing_utils.celery_app import get_testing_app

app = get_testing_app(task_cls=CeleryChainPlugin(redis_host="celery-redis"))


@app.task(store_chain_results=True, bind=True)
def task_1(self, length):
    return list(range(length))


@app.task(read_chain_results=True, bind=True)
def task_2(self, task_1_response):
    return task_1_response * 2


@app.task
def task_3(length):
    return list(range(length))


@app.task
def task_4(task_3_response):
    return task_3_response * 2

