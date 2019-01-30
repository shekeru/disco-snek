from core import user
import logging

@user.message_create
@user.prefix('>', ['doujin', 'dump'])
def nhentai(msg, op, link):
    user.web.simple_message(msg.channel_id, link)
