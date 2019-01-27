
def echo(user, message, code):
    if message['author']['id'] != user.profile['id']:
        user.web.simple_message(message['channel_id'], message['content'])
