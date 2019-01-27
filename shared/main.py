from shared.out import print
#--Imports
from shared import sockets, rest

class Interface:
    def __init__(self, token, bot = True):
        self.token, self.bot = token, bot
        self.web = rest.Interface(self)
        self.ws = sockets.Interface(self)
        self.actions = {
            'MESSAGE_CREATE': [],
            'MESSAGE_UPDATE': []
        }
    def publish(self, event):
        if event['t'] in self.actions:
            for action in self.actions[event['t']]:
                action(self, event['d'], event['t'])
    def quick_append(self, key, function):
        self.actions[key].append(function)
        return function
    def message_create(self, function):
        return self.quick_append('MESSAGE_CREATE',
            function)
    def message_update(self, function):
        return self.quick_append('MESSAGE_UPDATE',
            function)
