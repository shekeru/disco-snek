try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__
#--Imports
from threading import Thread
from queue import Queue
#--Global State
print_queue = Queue()
#--Printing Functions
def output_sync():
    while True:
        args, kwargs = print_queue.get()
        __builtin__.print(*args, **kwargs)
def print(*arg, **kwargs):
    print_queue.put((arg, kwargs))
#--Start The Autism
Thread(target = output_sync).start()
