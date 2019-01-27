
def echo(user, message, code):
    if message['author']['id'] != user.profile['id']:
        user.web.post(f"/channels/{message['channel_id']}/messages",
            json = {'content': message['content']})
