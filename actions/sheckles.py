from core import user
import logging

from random import randint

#@user.add_events('MESSAGE_CREATE')
@user.message_create
def fuck_robon(msg, op):
    if msg.mention_everyone:
        reply = 'Fuck you, %s. :ok_hand::skin-tone-%s:' % (msg.author.username, randint(1,5))
        user.web.simple_message(msg.channel_id, reply)
        logging.info(f'[TG-Robon-2.0] {reply}')

@user.message_create
@user.prefix('>', ['fuck', 'frick'])
def alt_robon(msg, op, *args):
    reply = args[0]+' you, %s <3' % msg.author.username
    user.web.simple_message(msg.channel_id, reply)
    logging.info(f'[TG-Robon-3.0] {reply}')
#
# test = user.prefix('>', ['fuck', 'frick'])(alt_robon)
# user.message_create(test)
