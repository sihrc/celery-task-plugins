import logging
import os

from celery_task_plugins.context_logger.task import ContextLoggerPlugin, LoggerContext
from celery_task_plugins.base import combined_task_plugins
from celery_task_plugins.testing_utils.celery_app import get_testing_app

MyContext = LoggerContext(
    "[%(asctime)s] %(name)s <U:%(user)s>: %(message)s", extras_default={"user": None}
)


test_logger = logging.getLogger("test")
test_logger.addHandler(logging.FileHandler("/tmp/context_logger_test.log"))

app = get_testing_app(
    task_cls=combined_task_plugins(
        ContextLoggerPlugin(MyContext, base_logger=test_logger, stdout=True)
    ),
    worker_hijack_root_logger=False,
)


@app.task(bind=True)
def task_1(self):
    self.request.logger.info("Inside Task 1")


@app.task(bind=True)
def task_2(self, *args):
    self.request.logger.info("Inside Task 2")
