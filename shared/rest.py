from shared.utils import Map, struct
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
    # gen 1 calls
    def create_message(self, channel_id, payload, files = {}):
        return self.post(f"/channels/{channel_id}/messages",
            json = payload, files = files)
    def simple_message(self, channel_id, text):
        return self.create_message(channel_id, {'content': text})
    # message editing
    def modify_message(self, channel_id, id, payload, files = {}):
        return self.patch(f"/channels/{channel_id}/messages/{id}",
            json = payload, files = files)
    def edit_message(self, message, new_message):
        return self.modify_message(message['channel_id'],
            message['id'], new_message)
    # message deletion
    def delete_message(self, channel_id, id):
        return self.delete(f"/channels/{channel_id}/messages/{id}")
    # reactions
    def react_create(self, channel_id, id, emoji, who = '@me'):
        return self.put(f"/channels/{channel_id}/messages/{id}/reactions/{emoji}/{who}")
    def react_remove(self, channel_id, id, emoji, who = '@me'):
        return self.delete(f"/channels/{channel_id}/messages/{id}/reactions/{emoji}/{who}")
    def create_reaction(self, message, emoji):
        return self.react_create(message['channel_id'], message['id'], emoji)
    def delete_reaction(self, message, emoji):
        return self.react_remove(message['channel_id'], message['id'], emoji)
    # Autism Calls
    def call(s,callType,call,*args,**kwargs):
        method = getattr(super(), callType)
        for key in kwargs.get('files', []):
            kwargs['files'][key].seek(0,0)
        response = method(DiscordAPI+call,*args, **kwargs)
        code, payload = response.status_code, None
        if code != 204:
            payload = struct(response.json())
        if code == 429:
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
