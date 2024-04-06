import uuid
import queue
import threading
import traceback
from datetime import datetime
from classes.EventDispatcher import EventDispatcher
from helpers.common import log_save


class Task:
    def __init__(self, name, callback, props=None):
        self.name = name
        self.callback = callback
        self.id = str(uuid.uuid4())

        self.event_id_done = f'onDone-{self.id}'
        self.event_id_error = f'onError-{self.id}'

        if props is not None:
            if 'onDone' in props:
                self.onDone = props['onDone']
            if 'onError' in props:
                self.onError = props['onError']


class TaskManager:
    def __init__(self):
        self.event_dispatcher = EventDispatcher()
        self.queue = queue.Queue()
        self.listener = threading.Thread(target=self._listen, args=(self.queue,))
        self.listener.start()

    def add(self, name, cb, props):
        task = Task(name, cb, props)
        _type = props['type'] if 'type' in props else 'sync'
        if task.onDone:
            self.event_dispatcher.subscribe(task.event_id_done, task.onDone)
        if task.onError:
            self.event_dispatcher.subscribe(task.event_id_error, task.onError)

        if _type == 'aside':
            self.queue.put(task)
        elif _type == 'sync':
            self._exec(task)

    def _exec(self, task):
        self.start_time = datetime.now()

        try:
            res = task.callback()
            status = "Done" if bool(res) or res is None else "Error"
            duration_str = f"Duration: {str(datetime.now() - self.start_time).split('.')[0]}"
            message = f'{status}: {task.name} | {duration_str}'
            self.event_dispatcher.publish(task.event_id_done, message)
        except Exception as e:
            error = traceback.format_exc()
            log_save(error)
            self.event_dispatcher.publish(task.event_id_error, str(e))
        finally:
            self.event_dispatcher.unsubscribe(task.event_id_done, task.callback)
            self.event_dispatcher.unsubscribe(task.event_id_error, task.callback)

    def _listen(self, queue):
        while True:
            # Check if there are updates in the queue
            if not queue.empty():
                task = queue.get()
                self._exec(task)
