import uuid
import queue
import threading
import traceback
from telegram.error import NetworkError
from classes.EventDispatcher import EventDispatcher
from helpers.common import log_save, log

MAX_RETRIES = 3
DELAY = 1


EMULATE_NETWORK_ERROR = False

class Task:
    def __init__(self, name, callback, props=None):
        self.name = name
        self.callback = callback
        self.id = str(uuid.uuid4())

        self.onDone = props['onDone'] if 'onDone' in props else None
        self.onError = props['onError'] if 'onError' in props else None
        self.event_id_done = f'onDone-{self.id}'
        self.event_id_error = f'onError-{self.id}'


class TaskManager:
    def __init__(self):
        self.event_dispatcher = EventDispatcher()
        self.queue = queue.Queue()
        self.listener = threading.Thread(target=self.listen, args=(self.queue,))
        self.listener.start()

    def add(self, name, cb, props):
        task = Task(name, cb, props)
        _type = props['type'] if 'type' in props else 'sync'

        if bool(task.onDone):
            self.event_dispatcher.subscribe(task.event_id_done, task.onDone)
        if bool(task.onError):
            self.event_dispatcher.subscribe(task.event_id_error, task.onError)

        if _type == 'aside':
            self.queue.put(lambda: self.run(task))
        elif _type == 'sync':
            self.run(task)

    # def run(self, task):
    #     res = task.callback()
    #
    #     # @TODO Temp (Requires Preset Feature)
    #     if bool(res) and type(res) is str:
    #         self.event_dispatcher.publish(task.event_id_done, res)

    def run(self, task, retry=True):
        global EMULATE_NETWORK_ERROR

        try:
            if EMULATE_NETWORK_ERROR:
                EMULATE_NETWORK_ERROR = False
                raise NetworkError("Emulated network error from TaskManager")

            res = task.callback()

            # @TODO Temp (Requires Preset Feature)
            if bool(res) and type(res) is str:
                self.event_dispatcher.publish(task.event_id_done, res)

        except NetworkError as e:
            error = f"NetworkError: {e}"
            log(error)
            if retry:
                self.run(task, retry=False)

        #     # @TODO Temp, should be removed
        #     self.event_dispatcher.publish(task.event_id_error, error)

        except NetworkError as e:
            error = f"NetworkError: {e}"
            log(error)
            pass

        except Exception as e:
            error = traceback.format_exc()
            log_save(error)
            self.event_dispatcher.publish(task.event_id_error, str(e))

        finally:
            self.event_dispatcher.unsubscribe(task.event_id_done, task.callback)
            self.event_dispatcher.unsubscribe(task.event_id_error, task.callback)

    def listen(self, queue):
        while True:
            # Check if there are updates in the queue
            if not queue.empty():
                task = queue.get()
                task()
