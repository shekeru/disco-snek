import shared.main as bot
import creds, logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

user = bot.Interface(creds.token)

@user.message_create
@user.message_update
def local_print(user, message, code):
    logging.info(code,'>>>', message['content'])

from actions.debug import echo
user.message_create(echo)
user.message_update(echo)
