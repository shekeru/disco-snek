from core import user
import logging

@user.message_create
@user.message_update
#@user.add_events('MESSAGE_CREATE', 'MESSAGE_UPDATE')
def local_print(message, code):
    logging.info(f"{code} >>> {message.content}")
