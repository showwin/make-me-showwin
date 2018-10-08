import os
import shutil

import requests
from slackbot.bot import default_reply

from .image import IMAGE_DIR, create_showwin_icon

DEFAULT_REPLY = '@make_me_showwin にメンションを飛ばしながら画像をアップロードしてねー'


def _download_file(message):
    url = message.body['files'][0]['url_private']
    filetype = message.body['files'][0]['filetype']
    filename = message.body['files'][0]['name'].rstrip(f'.{filetype}')

    filepath = filename + '.' + filetype
    tmpfile = IMAGE_DIR + filepath

    token = os.environ.get('SLACK_TOKEN_MAKE_ME_SHOWWIN')
    resp = requests.get(url,
                        headers={'Authorization': 'Bearer ' + token},
                        stream=True)
    f = open(tmpfile, "wb")
    shutil.copyfileobj(resp.raw, f)
    f.close()

    return filename, filetype


@default_reply
def make_me_showwin(message):
    if 'files' not in message.body:
        return message.reply(DEFAULT_REPLY)
    filename, filetype = _download_file(message)
    images = create_showwin_icon(filename, filetype)
    for image in images:
        message.channel.upload_file('showwin-' + image, IMAGE_DIR + image)
        os.remove(IMAGE_DIR + image)
    os.remove(IMAGE_DIR + filename + '.' + filetype)
