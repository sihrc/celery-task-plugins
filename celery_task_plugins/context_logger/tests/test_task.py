import os
from celery import chain

from .celery_app import app, task_1, task_2


def test_chain_task(celery_worker):
    try:
        chained_task = chain(task_1.s(_logging_extras={"user": "user_812"}), task_2.s())
        result_task = chained_task.delay()
        result_task.get()

        with open("/tmp/context_logger_test.log", "r") as f:
            contents = f.read()

        for line in contents.split("\n"):
            if line:
                assert "user_812" in line
    finally:
        os.remove("/tmp/context_logger_test.log")

