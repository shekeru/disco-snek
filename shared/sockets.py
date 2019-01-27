from shared.out import print
#--Imports
DiscordAPI = "wss://gateway.discord.gg/?encoding=json&v=6"
import json, websocket, sys, traceback
from threading import Thread, Timer
#websocket.enableTrace(True)
class Interface():
    # Socket shit
    def __init__(self, main):
        self.seq, self.session, self.interval = 0, "", None
        self.main, self.trigger = main, Timer(0, lambda: 0)
        self.spawn_ws()
    def spawn_ws(self):
        self.ws = websocket.WebSocketApp(DiscordAPI,
            on_message = self.on_message, on_open = self.on_open,
            on_error = self.on_error, on_close = self.on_close
        ); self.ws.t = Thread(target = lambda: self.ws.run_forever())
        self.trigger.cancel(), self.ws.t.start()
    def send(self, event):
        self.ws.send(json.dumps(event))
    def on_message(self, message):
        event = json.loads(message)
        if event['s']:
            self.seq = event['s']
        print(event), self.dispatch(event)
    def on_open(self):
        pass
    def on_error(self, error):
        print("[Gateway-WS]", error)
        self.spawn_ws()
    def on_close(self):
        self.spawn_ws()
    # initial dispatch
    def dispatch(self, event):
        if event['op'] is 11: # Event: Heartbeat ACK
            return self.resync()
        if event['op'] is 10: # Event: Hello
            self.interval = event['d']['heartbeat_interval'] / 1000
            print('[Gateway-10] Interval set at',
                self.interval, 'seconds'), self.resync()
            if not self.session:
                return self.Identify()
            return self.Resume()
        if event['op'] is 9: # Event: Invalid Session
            print('[Gateway-09] Invalidated', self.session)
            self.session = ""; return self.Identify()
        if event['op'] is 7: # Event: Reconnect
            return self.ws.close()
        if event['t'] == 'READY':
            print('[Connection] Session', event['d']['session_id'])
            self.session = event['d']['session_id']
        if event['t']:
            try:
                pass#self.mainystem.process(event['t'], event['d'])
            except:
                print('<%s>' % event['t'], traceback.format_exc())
        if event['op'] is 0:
            self.main.publish(event)
    # heartbeat
    def resync(self):
        self.trigger.cancel()
        self.trigger = Timer(self.interval, self.Heartbeat)
        self.trigger.start()
    # payloads
    def Heartbeat(self):
        self.send({"op": 1,
            "d": str(self.seq)
        })
    def Identify(self):
        self.send({"op": 2,
            "d": {
                "token": self.main.token,
                "properties" : {
                    "$os": sys.platform,
                    "$browser": "botthingy",
                    "$device": "libqt",
                },
                "large_threshold": 125,
                "compress": False
            }
        })
    def Resume(self):
        self.send({"op": 6,
            "d": {
                "token": self.token,
                "session_id": self.session,
                "seq": self.seq
            }
        })
