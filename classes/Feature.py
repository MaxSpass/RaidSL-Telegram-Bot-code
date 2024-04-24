from classes.EventDispatcher import EventDispatcher
from classes.Duration import Duration
from helpers.common import close_popup_recursive, log


class Feature:
    def __init__(self, name, app, report_predicate=None):
        self.NAME = name
        self.app = app
        self.report_predicate = report_predicate
        self.update = None
        self.context = None
        self.terminate = False
        self.completed = False
        self.event_dispatcher = EventDispatcher()
        self.duration = Duration()

        self.event_dispatcher.subscribe('finish', lambda data, *args: {
            self.update.message.reply_text(f"Done: {self.NAME} | Duration: {data['duration']}")
        })

    # def report(self):
    #     report = self.report_predicate() if self.report_predicate else None
    #     if report:
    #         if len(self.duration.durations):
    #             report += f"\nDuration: {self.duration.get_last()}"
    #
    #     return report


    def log(self, msg):
        log(f'{self.NAME} | {msg}')
        self.event_dispatcher.publish('log')

    def enter(self):
        close_popup_recursive()
        self.event_dispatcher.publish('enter')

    def finish(self):
        close_popup_recursive()
        self.duration.end()
        self.log(f"Done: {self.NAME}")
        
        self.event_dispatcher.publish('finish', {
            'duration': self.duration.get_last()
        })

    def run(self, upd, ctx, *args):
        self.terminate = False
        self.update = upd
        self.context = ctx

        if not self.completed:
            self.duration.start()

            self.enter()
            self.event_dispatcher.publish('run', *args)
            self.finish()
        else:
            self.log('is already completed')
