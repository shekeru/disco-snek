#--Imports
import traceback, logging
import functools, decorator, inspect
from threading import Timer, Thread
from shared import sockets, rest
from queue import Queue
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
        self.identities = {}
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
                try:
                    action(event['d'], event['t'])
                except:
                    logging.error(traceback.format_exc())
    def quick_append(self, key, function):
        new_function = self.comp_format(function)
        self.actions[key].append(new_function)
        return new_function
    def comp_format(self, function):
        function_id = inspect.getmodule(function).__name__
        function_id += '-' + function.__name__
        @functools.wraps(function)
        def formatted(message, op, *args, **kwargs):
            args, spec = [*args], inspect.getargspec(function)
            words = (message.content or "").split()[1:]
            logging.debug(f"{function_id} - {spec}")
            for arg in spec.args[2:]:
                args.append(words.pop(0))
            if spec.varargs:
                args += words
            #logging.info(f"{function.__name__} - {args}")
            return function(message, op, *args, **kwargs)
        if function_id not in self.identities:
            self.identities[function_id] = formatted
        return self.identities[function_id]
    # generic event hook
    def add_events(self, *keys):
        def partial(function):
            for key in keys:
                self.quick_append(key, function)
            return function
        return partial
    # prefix filtering logic
    def prefix(self, char, cmds, checks = True):
        def wrapper(function):
            @functools.wraps(function)
            def executed(message, op, *args):
                spec = inspect.getargspec(function)
                if not spec.varargs:
                    args = [*args][:len(spec.args) - 2]
                for cmd in cmds:
                    if message.content.startswith(char+cmd):
                        try:
                            if checks:
                                self.web.create_reaction(message, '✅')
                            return function(message, op, *args)
                        except Exception as err:
                            if checks:
                                self.web.delete_reaction(message, '✅')
                                self.web.create_reaction(message, '❌')
                return lambda : None
            return executed
        return wrapper
    #specialized hooks
    def message_create(self, function):
        return self.quick_append('MESSAGE_CREATE', function)
    def message_update(self, function):
        return self.quick_append('MESSAGE_UPDATE', function)
    def message_delete(self, function):
        return self.quick_append('MESSAGE_DELETE', function)
