from core import user
import logging, time

@user.add_events('MESSAGE_CREATE')
@user.prefix('?', ['ping', 'delay'])
def check_ping(msg, op):
    0/0
    stamp = time.monotonic()
    response = user.web.create_message(msg.channel_id, {'content': 'Pong!'})[1]
    delay = int(round((time.monotonic() - stamp) * 1000))
    embed = {
        'title': 'Ping Info',
        'color': 0xff00ff,
        'fields': [
            { 'name': 'Current Ping', 'value': ''.join(['**', str(delay), 'ms**']) }
        ],
        'footer': { 'text': 'Ping is measured by bot' },
        'thumbnail': { 'url': 'http://cdn.onlinewebfonts.com/svg/img_426066.png' }
    }
    user.web.edit_message(response, {'content': 'Pong!', 'embed': embed})
