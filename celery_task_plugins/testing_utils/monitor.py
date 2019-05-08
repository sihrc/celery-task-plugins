import time
import threading
from contextlib import contextmanager


@contextmanager
def celery_monitor(app, event):
    state = app.events.State()

    tasks = []

    def print_event(event):
        state.event(event)
        task = state.tasks.get(event["uuid"])
        tasks.append(task)

    def listen():
        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={event: print_event})
            recv.capture(limit=None, timeout=None, wakeup=True)

    t = threading.Thread(target=listen)
    t.daemon = True
    t.start()
    yield tasks
    time.sleep(1)
