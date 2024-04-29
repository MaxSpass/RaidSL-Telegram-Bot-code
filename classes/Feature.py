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
        self.run_counter = 0

    def report(self):
        report_list = self.report_predicate() if self.report_predicate else []

        if len(self.duration.durations):
            report_list.append(f"Duration: {self.duration.get_total()}")

        if self.run_counter:
            report_list.append(f"Runs counter: {str(self.run_counter)}")

        if len(report_list):
            report_list = [f"***{self.NAME}***"] + report_list

        return '\n'.join(report_list)

    def log(self, msg):
        log(f'{self.NAME} | {msg}')
        self.event_dispatcher.publish('log')

    def enter(self):
        close_popup_recursive()
        self.event_dispatcher.publish('enter')

    def finish(self):
        close_popup_recursive()
        self.duration.end()
        message_done = f"Done: {self.NAME} | Duration: {self.duration.get_last()}"

        self.log(message_done)
        self.event_dispatcher.publish('finish')
        self.update.message.reply_text(message_done)

    def run(self, upd, ctx, *args):
        if self.completed:
            self.log('is already completed')
            return

        self.update = upd
        self.context = ctx
        self.terminate = False
        self.run_counter += 1
        self.duration.start()

        self.enter()
        self.event_dispatcher.publish('run', *args)
        self.finish()
