from celery.task import Task


def combined_task_plugins(*plugins):
    plugins += (Task,)
    return type("CombinedPluginsTask", tuple(plugins), {})
