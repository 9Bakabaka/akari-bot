import os
import urllib.parse

from PIL import Image as PILImage

from core.config import config
from core.builtins import Bot, Image as BImage
from core.component import module
from core.dirty_check import rickroll
from core.constants.exceptions import ConfigValueError
from core.utils.http import download, get_url
from .check import secret_check

appid = config('wolfram_alpha_appid', cfg_type=str, secret=True)

w = module(
    'wolframalpha',
    alias=['wolfram', 'wa'],
    developers=['DoroWolf'],
    desc='{wolframalpha.help.desc}',
    support_languages=['en_us'], doc=True)


@w.handle('<query> {{wolframalpha.help}}')
async def _(msg: Bot.MessageSession, query: str):
    if await secret_check(query):
        await msg.finish(rickroll(msg))
    url_query = urllib.parse.quote(query)
    if not appid:
        raise ConfigValueError(msg.locale.t('error.config.secret.not_found'))
    url = f"http://api.wolframalpha.com/v1/simple?appid={appid}&i={url_query}&units=metric"

    try:
        img_path = await download(url, status_code=200)
        if img_path:
            with PILImage.open(img_path) as img:
                output = os.path.splitext(img_path)[0] + ".png"
                img.save(output, "PNG")
            os.remove(img_path)
            await msg.finish([BImage(output)])
    except ValueError as e:
        if str(e).startswith('501'):
            await msg.finish(msg.locale.t('wolframalpha.message.incomprehensible'))
        else:
            raise e


@w.handle('ask <question> {{wolframalpha.help.ask}}')
async def _(msg: Bot.MessageSession, question: str):
    if await secret_check(question):
        await msg.finish(rickroll(msg))
    url_query = urllib.parse.quote(question)
    if not appid:
        raise ConfigValueError(msg.locale.t('error.config.secret.not_found'))
    url = f"http://api.wolframalpha.com/v1/result?appid={appid}&i={url_query}&units=metric"
    try:
        data = await get_url(url, 200)
        await msg.finish(data)
    except ValueError as e:
        if str(e).startswith('501'):
            await msg.finish(msg.locale.t('wolframalpha.message.incomprehensible'))
        else:
            raise e
