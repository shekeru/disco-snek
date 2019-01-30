from core import user
import logging

from bs4 import BeautifulSoup
import requests, io

@user.message_create
@user.prefix('>', ['doujin', 'dump'])
def nhentai(msg, op, link):
    search = BeautifulSoup(requests.get(link).text,
        'html.parser')
    thumbs = search.find('div', id="thumbnail-container")
    images = thumbs.find_all('img', {'class': "lazyload"})
    for image in images:
        url = image.get('data-src').replace('t.',
            'i.', 1).replace('t.', '.', 1)
        user.web.create_message(msg.channel_id, {'content': ''}, {
            url.split('/')[-1]: io.BytesIO(requests.get(url).content)
        })
