from shared import utils
import logging

doesnt_matter = ['TYPING_START','MESSAGE_CREATE',
    'MESSAGE_UPDATE','MESSAGE_DELETE']

class Interface():
    def __init__(self, main):
        self.guilds = utils.ODST()
        self.main = main
    def process(self, action, data):
        if action == 'READY': #Initial Response
            [*map(self.update_guild, data['guilds'])]
        elif action in ['GUILD_CREATE', 'GUILD_UPDATE']:
            self.update_guild(data)
         #-- User Changes
        elif action == 'GUILD_MEMBERS_CHUNK':
            for member in data['members']:
                self.upsert_member(data['guild_id'],member)
        elif 'GUILD_MEMBER_' in action:
            self.upsert_member(data['guild_id'],data)
        elif 'GUILD_ROLE' in action:
            self.manage_role(data['guild_id'], data)
        elif action not in doesnt_matter and False:
            logging.info(f"Unhandled: {action}")
    def update_guild(self, guild):
        if guild['id'] not in self.guilds:
            self.main.ws.Request_Guild_Members(guild['id'])
            self.guilds[guild['id']] = utils.ODST()
        last_obj = self.guilds[guild['id']]
        #Preprocessing
        guild['members'] = {x['user']['id']: x
            for x in guild.get('members',[])}
        guild['roles'] = {x['id']: x
            for x in guild.get('roles',[])}
        guild['channels'] = {x['id']: x
            for x in guild.get('channels',[])}
        guild['emojis'] = {x['id']: x
            for x in guild.get('emojis',[])}
        add_keys(last_obj, guild)
    def upsert_member(self, guild_id, member):
        user_id = member['user']['id']
        members = self.guilds[guild_id]['members']
        user_obj = members.get(user_id, utils.ODST())
        members[user_id] = {**user_obj, **member}
    def patch_user(self, guild_id, member):
        members = self.guilds[guild_id]['members']
        user_id = member['user']['id']
        add_keys(members[user_id], member)
    def manage_role(self, guild_id, data):
        roles = self.guilds[guild_id]['roles']
        if 'role' in data:
            roles[data['role']['id']] = data['role']
        else:
            del roles[data['role_id']]

def add_keys(obj,data):
    for key in data:
        if not data[key]:
            continue
        if key not in obj or type(data[key]) != dict:
            obj[key] = data[key]
        else:
            obj[key].update(data[key])
