class EventDispatcher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, *args):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(*args)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)

    def unsubscribe_all(self):
        self.subscribers.clear()
