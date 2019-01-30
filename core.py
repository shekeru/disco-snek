import shared.main as bot
import creds, logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level = logging.INFO)

if __name__ != '__main__':
    user = bot.Interface(creds.token)

import actions
if not creds.partner:
    import autism
