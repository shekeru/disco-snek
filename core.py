import shared.main as bot
import creds, logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
user = bot.Interface(creds.token)

import actions.sheckles
import actions.debug
