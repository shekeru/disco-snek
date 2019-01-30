import shared.main as bot
import creds, logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level = logging.INFO)

if __name__ != '__main__':
    user = bot.Interface(creds.token)
from core import user

import actions
if not creds.partner:
    import autism
# for guild in user.state.guilds.values():
#     print(guild['name'],'has %s members' % len(guild['members']))
