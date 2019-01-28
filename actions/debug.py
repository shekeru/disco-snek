from core import user
import logging

@user.message_create
@user.message_update
def local_print(message, code):
    logging.info(f"{code} >>> {message.content}")
