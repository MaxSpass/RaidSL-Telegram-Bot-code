from classes.EventDispatcher import EventDispatcher
from classes.Duration import Duration
from classes.Foundation import Foundation
from classes.Debug import Debug
from helpers.common import close_popup_recursive, log, find_popup_error_detector
from datetime import datetime

LOCATIONS_WITH_STORAGE = [
    'Arena Classic',
    'Arena Tag',
    'Arena Live',
]


class Location(Foundation):
    def __init__(self, name, app, report_predicate=None):
        Foundation.__init__(self, name=name)

        self.NAME = name
        self.app = app
        self.report_predicate = report_predicate
        self.update = None
        self.context = None
        self.terminate = False
        self.completed = False
        self.event_dispatcher = EventDispatcher()
        self.duration = Duration()
        self.debug = Debug(app=app, name=name)
        self.run_counter = 0
        self.results = None
        self.refill = 0

        self.E_TERMINATE = {
            "name": "Terminate",
            "interval": 3,
            "expect": lambda: self.terminate
        }

    # @TODO Temp commented
    #     # @TODO Should add time
    #     if self.NAME in LOCATIONS_WITH_STORAGE:
    #         records = self.app.storage.get_entries(days=0, title=self.NAME)
    #         self.results = []
    #         for i in range(len(records)):
    #             record = records[i]
    #             results_record = record['data']['results_record']
    #             duration_record = record['data']['duration_record']
    #
    #             # @TODO Refactor
    #             if self.NAME in ['Arena Live']:
    #                 for j in range(len(results_record)):
    #                     rec = results_record[j]
    #                     self.results.append(rec)
    #             elif self.NAME in ['Arena Classic', 'Arena Tag']:
    #                 self.results.append(results_record)
    #
    #             duration_record = list(map(lambda d: datetime.fromisoformat(d), duration_record))
    #             self.duration.durations.append(duration_record)
    #
    #     self.event_dispatcher.subscribe('update_results', self.update_storage)
    #
    # def update_storage(self):
    #     if self.NAME in LOCATIONS_WITH_STORAGE:
    #         results_record = self.results[len(self.results) - 1]
    #         duration_record = list(map(
    #             lambda x: x.isoformat(),
    #             self.duration.durations[len(self.duration.durations) - 1]
    #         ))
    #
    #         self.app.storage.add(
    #             title=self.NAME,
    #             data={
    #                 'results_record': results_record,
    #                 'duration_record': duration_record
    #             }
    #         )

    def send_message(self, text):
        if self.update is not None:
            self.update.message.reply_text(text)
        else:
            log(text)

    def report(self):
        report_list = self.report_predicate() if self.report_predicate else []

        if len(self.duration.durations):
            report_list.append(f"Duration: {self.duration.get_total()}")

        # Old
        # if self.run_counter:
        #     report_list.append(f"Runs counter: {str(self.run_counter)}")

        if len(report_list):
            report_list = [f"***{self.NAME}***"] + report_list

        return '\n'.join(report_list)

    def enter(self):
        close_popup_recursive()
        self.event_dispatcher.publish('enter')

    def finish(self):
        close_popup_recursive()
        self.duration.end()
        message_done = f"Done: {self.NAME} | Duration: {self.duration.get_last()}"

        self.log(message_done)
        self.event_dispatcher.publish('finish')
        self.send_message(message_done)
        # @TODO Test
        # self.results.append([True, False])

    def run(self, upd, ctx, *args):
        if self.completed:
            self.log('is already completed')
            return

        if find_popup_error_detector():
            self.app.relogin()

        self.update = upd
        self.context = ctx
        self.terminate = False
        self.stop = False
        self.run_counter += 1
        self.duration.start()

        self.enter()
        if not self.terminate:
            self.event_dispatcher.publish('run', *args)
        self.finish()
        # @TODO Test
        # self.event_dispatcher.publish('update_results')
