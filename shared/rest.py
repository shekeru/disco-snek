import logging, requests, time
#Constants
DiscordAPI = "https://discordapp.com/api/v6"
#--Rest API
class Interface(requests.Session):
    def __init__(self, main):
        self.main = main; super().__init__()
        self.headers['Authorization'] = ("Bot %s" if
            self.main.bot else "%s") % self.main.token
        self.load_profile()
    def load_profile(self):
        code, user = self.get('/users/@me')
        if code < 400:
            self.main.profile = user
            logging.debug(f"Hello {self.main.profile['username']}")
        else:
            logging.error("Token is invalid...")
    # message creation
    def create_message(self, channel_id, payload):
        return self.post(f"/channels/{channel_id}/messages",
            json = payload)
    def simple_message(self, channel_id, text):
        return self.create_message(channel_id, {'content': text})
    # Autism Calls
    def call(s,callType,call,*args,**kwargs):
        method = getattr(super(), callType)
        response = method(DiscordAPI+call,*args,**kwargs)
        code, payload = response.status_code, response.json()
        if code is 429:
            time.sleep(payload['retry_after'] / 995)
            return s.call(callType,call,*args,**kwargs)
        return (code, payload)
    def get(s,call,*args,**kwargs):
        return s.call('get',call,*args,**kwargs)
    def post(s,call,*args,**kwargs):
        return s.call('post',call,*args,**kwargs)
    def put(s,call,*args,**kwargs):
        return s.call('put',call,*args,**kwargs)
    def delete(s,call,*args,**kwargs):
        return s.call('delete',call,*args,**kwargs)
    def patch(s,call,*args,**kwargs):
        return s.call('patch',call,*args,**kwargs)
