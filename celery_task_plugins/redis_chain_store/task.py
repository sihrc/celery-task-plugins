import threading
from contextlib import contextmanager

import redis
from celery.task import Task
from kombu import serialization


def CeleryChainPlugin(
    redis_host,
    redis_port=6379,
    redis_db=1,
    base_exc_class=Exception,
    read_kwarg="_read_chain_results",
    store_kwarg="_store_chain_results",
    store_expires=3600,
):
    class CeleryChainTask(Task):
        store_chain_results = False
        read_chain_results = False
        typing = False

        thread_context = threading.local()
        thread_context.redis_chain_store = redis.ConnectionPool(
            host=redis_host, port=redis_port, db=redis_db
        )
        chain_store = redis.Redis(connection_pool=thread_context.redis_chain_store)

        class ResultNotFound(base_exc_class):
            pass

        def read_results(self, task_id, delete=True, raise_if_missing=True):
            if self.chain_store.exists(task_id):
                serializer = self.app.conf["result_serializer"]
                content_type, content_encoding, _ = serialization.registry._encoders[
                    serializer
                ]
                chained_arg = self.chain_store.get(task_id)
                chained_arg = serialization.loads(
                    chained_arg, content_type, content_encoding, accept={content_type}
                )

                if delete:
                    self.chain_store.delete(task_id)

                return chained_arg
            else:
                if raise_if_missing:
                    raise self.ResultNotFound(f"Can't find result for task {task_id}")
                else:
                    return task_id

        @contextmanager
        def with_chain_args(self, args, kwarg_override=False):
            if not self.read_chain_results or kwarg_override:
                yield args
            else:
                result_id = args[0]
                try:
                    arg = self.read_results(
                        result_id, delete=False, raise_if_missing=False
                    )
                    args = (arg,) + args[1:]
                    yield args
                except Exception:
                    raise
                else:
                    self.chain_store.delete(result_id)

        def __call__(self, *args, **kwargs):
            self.read_chain_results = kwargs.pop(read_kwarg, self.read_chain_results)
            self.store_chain_results = kwargs.pop(store_kwarg, self.store_chain_results)

            with self.with_chain_args(args) as args:
                result = super(CeleryChainTask, self).__call__(*args, **kwargs)

            if (self.request.chain or self.request.group) and self.store_chain_results:
                _, _, data = serialization.dumps(
                    result, self.app.conf["result_serializer"]
                )
                self.chain_store.set(self.request.id, data, ex=store_expires)
                result = self.request.id

            return result

    return CeleryChainTask
