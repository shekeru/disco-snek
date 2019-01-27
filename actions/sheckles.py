from core import user
import logging

from random import randint

@user.add_events('MESSAGE_CREATE')
def robon(msg, op):
    if msg.mention_everyone:
        reply = 'Fuck you, %s. :ok_hand::skin-tone-%s:' % (msg.author.username, randint(1,5))
        user.web.simple_message(msg.channel_id, reply)
        logging.info(f'[TG-Robon-2.0] {reply}')

@user.message_create
@user.message_update
def local_print(message, code):
    logging.info(f"{code} >>> {message['content']}")
