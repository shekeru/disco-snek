from core import user
import logging, time

@user.add_events('MESSAGE_CREATE')
def check_ping(msg, op):

    if not msg.content.startswith('ping'): return

    stamp = time.monotonic()
    response = user.web.create_message(msg.channel_id, {'content': 'Pong!'})
    delay = int(round((time.monotonic() - stamp) * 1000))
    embed = {
        'title': 'Ping Info',
        'color': 0xff00ff,
        'fields': [
            { 'name': 'Current Ping', 'value': ''.join(['**', str(delay), 'ms**']) }
        ],
        'footer': { 'text': 'Ping as measured by bot' }
    }

    user.web.edit_message(response, {'content': 'Pong!', 'embed': embed})