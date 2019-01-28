#--Imports
from shared import sockets, rest

class Interface:
    def __init__(self, token, bot = True):
        self.token, self.bot = token, bot
        self.web = rest.Interface(self)
        self.ws = sockets.Interface(self)
        self.actions = {
            'MESSAGE_CREATE': [],
            'MESSAGE_UPDATE': [],
            'MESSAGE_DELETE': []
        }
    def publish(self, event):
        if event['t'] in self.actions:
            for action in self.actions[event['t']]:
                action(event['d'], event['t'])
    def quick_append(self, key, function):
        self.actions[key].append(function)
        return function
    def add_events(self, *keys):
        def partial(function):
            for key in keys:
                self.quick_append(key, function)
            return function
        return partial
    # event functions (for convenience)
    def message_create(self, function):
        return self.quick_append('MESSAGE_CREATE', function)
    def message_update(self, function):
        return self.quick_append('MESSAGE_UPDATE', function)
    def message_delete(self, function):
        return self.quick_append('MESSAGE_DELETE', function)
