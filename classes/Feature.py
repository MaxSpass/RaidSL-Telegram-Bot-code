from classes.EventDispatcher import EventDispatcher
from helpers.common import close_popup_recursive, log
from datetime import datetime

class Feature:
    def __init__(self, feature_name, app):
        self.FEATURE_NAME = feature_name
        self.app = app
        self.update = None
        self.context = None
        self.terminate = False
        self.event_dispatcher = EventDispatcher()

        self.start_time = None

        self.event_dispatcher.subscribe('finish', lambda data, *args: {
            self.update.message.reply_text(f"Done: {self.FEATURE_NAME} | Duration: {data['duration']}")
        })

    def log(self, msg):
        log(f'{self.FEATURE_NAME} | {msg}')
        self.event_dispatcher.publish('log')

    def enter(self):
        close_popup_recursive()
        self.event_dispatcher.publish('enter')

    def finish(self):
        close_popup_recursive()
        duration = str(datetime.now() - self.start_time).split('.')[0]
        self.log(f"Done: {self.FEATURE_NAME}")
        self.event_dispatcher.publish('finish', {'duration': duration})


    def run(self, upd, ctx, *args):
        self.terminate = False
        self.update = upd
        self.context = ctx

        self.start_time = datetime.now()

        self.enter()
        self.event_dispatcher.publish('run', *args)
        self.finish()
