class JapperEvents:
    def __init__(self):
        self._japper_events = {}

    def on(self, event, callback):
        if event not in self._japper_events:
            self._japper_events[event] = []

        if callback not in self._japper_events[event]:
            self._japper_events[event].append(callback)

    def emit(self, event, *args):
        if event in self._japper_events:
            for callback in self._japper_events[event]:
                callback(*args)

    def off(self, event, callback):
        if event in self._japper_events:
            self._japper_events[event].remove(callback)
            if len(self._japper_events[event]) == 0:
                del self._japper_events[event]
