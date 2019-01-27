import logging, requests
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
        user = self.get('/users/@me')
        if user.status_code < 400:
            self.main.profile = user.json()
            logging.debug(f"Hello {self.main.profile['username']}")
        else:
            logging.error("Token is invalid...")
    # Autism Calls
    def call(s,callType,call,*args,**kwargs):
        method = getattr(super(), callType)
        return method(DiscordAPI+call,*args,**kwargs)
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
