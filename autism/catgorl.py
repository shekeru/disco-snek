from core import user
import logging

from random import randint

@user.message_create
def fuck_robon(msg, op):
    if msg.mention_everyone:
        reply = 'Fuck you, %s. :ok_hand::skin-tone-%s:' % (msg.author.username, randint(1,5))
        user.web.simple_message(msg.channel_id, reply)
        logging.info(f'[TG-Robon-2.0] {reply}')

@user.message_create
def catgorl(msg, op):
    content = msg.content.lower()
    found = any(x for x in ['catgorl', ':gay:', 'catgoy'] if x in content)
    alt = 'catgorl' in [x['username'] for x in msg.mentions]
    if found or alt:
        user.web.simple_message(msg.channel_id, 'nyaa~')
        logging.info('[Auto-Catgoy] nyaa~')

import string
def weeb_test(s):
    count = 0
    for x in s.lower().split(' '):
        try:
            count += 1; dash= x[1] == '-'
            letter = x[0]==x[2] and x[0] in string.ascii_letters
            letter = letter and x[-1] != x[-3]
            if letter and dash and (len(x)>3 or count<2):
                return True
        except:
            pass
    return False

@user.message_create
def weeb(msg, op):
    if weeb_test(msg.content):
        reply = '<@'+msg.author.id+'> Stop stuttering you weeaboo faggot.'
        user.web.simple_message(msg.channel_id, reply)
        logging.info('[Weebaboo-ERP] %s' % reply)

@user.message_create
@user.prefix('>', ['owo', 'uwu'], checks = False)
def gay_flag(msg, op):
    user.web.simple_message(msg.channel_id, ':gay_pride_flag:')
