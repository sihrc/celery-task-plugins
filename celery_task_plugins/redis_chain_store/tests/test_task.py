from celery import chain

from celery_task_plugins.testing_utils.monitor import celery_monitor

from .celery_app import app, task_1, task_2


def test_chain_task(celery_worker):
    with celery_monitor(app, "task-sent") as tasks:
        chained_task = chain(task_1.s(10000), task_2.s())
        result_task = chained_task.delay()
        result = result_task.get()

    assert tasks[1].args == str(object=(tasks[0].id,))
    assert len(result) == 20000
