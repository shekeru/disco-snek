from shared.out import print
#--Imports
from shared import sockets, rest

class Interface:
    def __init__(self, token, bot = True):
        self.token, self.bot = token, bot
        self.web = rest.Interface(self)
        self.ws = sockets.Interface(self)
