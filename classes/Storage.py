from helpers.common import folder_ensure
# @TEMP Commented
# from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import os
import json


def format_date(date):
    return date.isoformat()
    # return date.strftime('%Y-%m-%d')


def today():
    return format_date(datetime.now())


def date_past(days=1):
    return format_date(datetime.now() - timedelta(days=days))


def date_future(days=1):
    return format_date(datetime.now() + timedelta(days=days))


class Storage:
    def __init__(self, name, folder=None):
        output = None
        if folder is not None:
            output = os.path.normpath(folder)
            folder_ensure(output)
        self.path = os.path.join(output if output is not None else '', f"{name}.json")
        self.db = None
        # @TEMP Commented
        # self.db = TinyDB(self.path)

    def exists(self, title, date=today()):
        Entity = Query()
        return self.db.contains((Entity.title == title) & (Entity.date == date))

    def update(self, title, data, date=today()):
        Entity = Query()
        self.db.update({'data': data}, (Entity.title == title) & (Entity.date == date))

    def insert(self, title, data, date=today()):
        self.db.insert({'title': title, 'data': data, 'date': date})

    def add(self, title, data, date=today()):
        # @TODO Double check the approach
        if self.exists(title, date):
            self.update(title, data, date)
        else:
            self.insert(title, data, date)

        # @TODO Test
        # Save the database to a readable JSON file with indentation
        # data = self.get_all_entries()
        # with open('readable_db.json', 'w') as f:
        #     json.dump(data, f, indent=4)

    def get_by_title(self, title):
        Entity = Query()
        return self.db.search(Entity.title == title)

    def get_by_date(self, date):
        Entity = Query()
        return self.db.search(Entity.date == date)

    def get_entries(self, days=0, title=None):
        Entity = Query()
        target_date = (datetime.now() + timedelta(days=days)).date()

        def _get_fromisoformat(d):
            fromisoformat = datetime.fromisoformat(d).date()
            return fromisoformat == target_date

        if title:
            return self.db.search((Entity.date.test(_get_fromisoformat)) & (Entity.title == str(title)))
        else:
            return self.db.search(Entity.date.test(_get_fromisoformat))

    def get_all_entries(self):
        return self.db.all()
