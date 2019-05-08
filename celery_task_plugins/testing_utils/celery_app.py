from celery import Celery

DEFAULT_CELERY_CONFIGURATIONS = {
    "task_serializer": "json",
    "result_serializer": "json",
    "enable_utc": True,
    "task_always_eager": False,
    "accept_content": ["application/json"],
    "redis_port": 6379,
    "redis_host": "celery-redis",
    "result_backend": "redis",
    "task_send_sent_event": True,
    "broker_url": "amqp://rabbitmq_user:rabbitmq_password@rabbitmq:5672",
}


def get_testing_app(**celery_options):
    options = dict(DEFAULT_CELERY_CONFIGURATIONS)
    options.update(celery_options)
    app = Celery(**options)
    app.conf.update(options)
    app.set_default()
    return app
