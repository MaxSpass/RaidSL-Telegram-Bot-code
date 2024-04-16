from classes.EventDispatcher import EventDispatcher
from helpers.common import close_popup_recursive


class Feature:
    def __init__(self, feature_name, app):
        self.FEATURE_NAME = feature_name
        self.app = app
        self.update = None
        self.context = None
        self.terminate = False
        self.event_dispatcher = EventDispatcher()

    def log(self, msg):
        print(f'{self.FEATURE_NAME} | {msg}')
        self.event_dispatcher.publish('log')

    def enter(self):
        close_popup_recursive()
        self.event_dispatcher.publish('enter')

    def finish(self):
        close_popup_recursive()
        self.event_dispatcher.publish('finish')
        self.log('Done')

    def run(self, upd, ctx, *args):
        self.terminate = False
        self.update = upd
        self.context = ctx

        self.enter()
        self.event_dispatcher.publish('run', *args)
        self.finish()
