from copy import deepcopy
import logging
import sys
import time

from celery.task import Task


class LoggerContext(object):
    def __init__(
        self,
        format_str="[%(name)s][%(levelname)s] %(asctime)-15s %(filename)s:%(lineno)d Message: %(message)s",
        extras_default=None,
    ):
        self.formatter = logging.Formatter(format_str, datefmt="%m/%d/%y-%I:%M:%S%p")
        self.extras_default = extras_default or {}


def ContextLoggerPlugin(
    logger_context, base_logger=None, level=logging.INFO, stdout=False
):
    if base_logger is None:
        base_logger = logging.getLogger("task")
        stream = logging.StreamHandler(stream=sys.stdout)
        base_logger.addHandler(stream)

    # Set Logger Configurations
    base_logger.setLevel(level)
    base_logger.propagate = True
    if stdout:
        base_logger.addHandler(logging.StreamHandler(sys.stdout))
    for handler in base_logger.handlers:
        handler.setLevel(level)
        handler.setFormatter(logger_context.formatter)

    class CeleryContextLogger(Task):
        typing = False

        def __call__(self, *args, **kwargs):
            start_time = time.clock()

            logging_extras = deepcopy(logger_context.extras_default)
            logging_extras.update(getattr(self.request, "_logging_extras", {}))
            # TODO: Consider adding a new 'option'
            logging_extras.update(kwargs.pop("_logging_extras", {}))

            child_logger = base_logger.getChild("name")

            self.request.logger = logging.LoggerAdapter(child_logger, logging_extras)
            self.request.logger.info(f"Began {self.request.id}")

            try:
                result = self.run(*args, **kwargs)
                if self.request.chain:
                    for task in self.request.chain:
                        task["kwargs"]["_logging_extras"] = dict(
                            **task["kwargs"].get("_logging_extras", {}),
                            **logging_extras,
                        )
            except Exception:
                self.request.logger.exception("Exception was raised in task.")
                raise
            else:
                self.request.logger.info(
                    f"Completed {self.request.id} in {time.clock() - start_time}s"
                )
                return result

    return CeleryContextLogger
