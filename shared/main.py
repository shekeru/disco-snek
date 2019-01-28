#--Imports
from functools import wraps
from threading import Timer, Thread
from shared import sockets, rest
from queue import Queue
import traceback
import logging
class Interface:
    def __init__(self, token, bot = True):
        self.token, self.bot = token, bot
        self.web = rest.Interface(self)
        self.ws = sockets.Interface(self)
        self.t = Thread(target = self.loop_run)
        self.events, self.actions = Queue(), {
            'MESSAGE_CREATE': [],
            'MESSAGE_UPDATE': [],
            'MESSAGE_DELETE': []
        }; self.t.start()
    def show_actions(self):
        return self.actions
    def loop_run(self):
        while True:
            event = self.events.get()
            self.publish(event)
    def publish_async(self, event):
        pass
    def publish(self, event):
        if event['t'] in self.actions:
            for action in self.actions[event['t']]:
                action(event['d'], event['t'])
    def quick_append(self, key, function):
        self.actions[key].append(function)
        return function
    # generic event hook
    def add_events(self, *keys):
        def partial(function):
            for key in keys:
                self.quick_append(key, function)
            return function
        return partial
    # prefix filtering logic
    def prefix(self, char, cmds):
        def partial(function):
            def execute(message, op):
                for cmd in cmds:
                    if message.content.startswith(char+cmd):
                        try:
                            self.web.create_reaction(message, '✅')
                            return function(message, op)
                        except Exception as err:
                            self.web.delete_reaction(message, '✅')
                            self.web.create_reaction(message, '❌')
                            logging.error(traceback.format_exc())
                return lambda : None
            return execute
        return partial
    #specialized hooks
    def message_create(self, function):
        return self.quick_append('MESSAGE_CREATE', function)
    def message_update(self, function):
        return self.quick_append('MESSAGE_UPDATE', function)
    def message_delete(self, function):
        return self.quick_append('MESSAGE_DELETE', function)
