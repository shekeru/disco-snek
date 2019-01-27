from shared.out import print
import shared.main as bot
import creds

user = bot.Interface(creds.token)

@user.message_create
@user.message_update
def local_print(user, message, code):
    print(code,'>>>', message['content'])

from actions.debug import echo
user.message_create(echo)
user.message_update(echo)
