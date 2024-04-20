import uuid
import queue
import threading
import traceback
from datetime import datetime
from classes.EventDispatcher import EventDispatcher
from helpers.common import log_save
from telegram.error import NetworkError
from helpers.common import log, sleep

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
        self.listener = threading.Thread(target=self._listen, args=(self.queue,))
        self.listener.start()

    def add(self, name, cb, props):
        task = Task(name, cb, props)
        _type = props['type'] if 'type' in props else 'sync'
        if bool(task.onDone):
            self.event_dispatcher.subscribe(task.event_id_done, task.onDone)
        if bool(task.onError):
            self.event_dispatcher.subscribe(task.event_id_error, task.onError)

        if _type == 'aside':
            self.queue.put(lambda: self._exec(task))
        elif _type == 'sync':
            self._exec(task)

    def _exec(self, task):
        global EMULATE_NETWORK_ERROR

        retries = 0
        while retries < MAX_RETRIES:
            try:
                if EMULATE_NETWORK_ERROR:
                    EMULATE_NETWORK_ERROR = False
                    raise NetworkError("Emulated network error")

                self.start_time = datetime.now()
                res = task.callback()
                status = "Done" if bool(res) or res is None else "Error"
                duration_str = f"Duration: {str(datetime.now() - self.start_time).split('.')[0]}"
                message = f'{status}: {task.name} | {duration_str}'

                if bool(res):
                    # Prepares readable response
                    if res and type(res) is str:
                        message += f'\n{res}'

                self.event_dispatcher.publish(task.event_id_done, message)
                return  # Exit the function if message is sent successfully

            except NetworkError as e:
                # Workaround for telegram package idle bug
                log(f"NetworkError: {e}")
                retries += 1
                log(f"Retrying ({retries}/{MAX_RETRIES})...")
                sleep(DELAY)

                # @TODO Test
                if task.name == 'test_feature':
                    self.event_dispatcher.publish(task.event_id_error, str(e))

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
                task()
