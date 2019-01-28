import shared.main as bot
import creds, logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

if __name__ != '__main__':
    user = bot.Interface(creds.token)

import actions.sheckles
import actions.debug
import actions.ping
