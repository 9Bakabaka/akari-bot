import ujson as json
import os

from core.builtins import ErrorMessage
from core.utils.http import get_url, post_url
from .maimaidx_music import get_cover_len5_id

assets_path = os.path.abspath('./assets/maimai')

async def update_alias():
    try:
        url = "https://download.fanyu.site/maimai/alias_uc.json"
        data = await get_url(url, 200, fmt='json')
    except:
        return False

    file_path = os.path.join(assets_path, "mai_alias.json")
    with open(file_path, 'w') as file:
        json.dump(data, file)

    return True


async def get_alias(msg, input, get_music=False):
    file_path = os.path.join(assets_path, "mai_alias.json")

    if not os.path.exists(file_path):
        await msg.finish(msg.locale.t("maimai.message.alias.file_not_found", prefix=msg.prefixes[0]))
    with open(file_path, 'r') as file:
        data = json.load(file)

    result = []
    if get_music:
        input = input.replace("_", " ")
        if input in data:
            result = data[input]
    else:
        for alias, ids in data.items():
            if input in ids:
                result.append(alias)

    return result


async def get_record(msg, payload):
    url = f"https://www.diving-fish.com/api/maimaidxprober/query/player"
    try:
        data = await post_url(url,
                              data=json.dumps(payload),
                              status_code=200,
                              headers={'Content-Type': 'application/json', 'accept': '*/*'}, fmt='json')
    except ValueError as e:
        if str(e).startswith('400'):
            await msg.finish(msg.locale.t("maimai.message.user_not_found"))
        if str(e).startswith('403'):
            await msg.finish(msg.locale.t("maimai.message.forbidden"))

    return data


async def get_plate(msg, payload):
    url = f"https://www.diving-fish.com/api/maimaidxprober/query/plate"
    try:
        data = await post_url(url,
                              data=json.dumps(payload),
                              status_code=200,
                              headers={'Content-Type': 'application/json', 'accept': '*/*'}, fmt='json')
    except ValueError as e:
        if str(e).startswith('400'):
            await msg.finish(msg.locale.t("maimai.message.user_not_found"))
        if str(e).startswith('403'):
            await msg.finish(msg.locale.t("maimai.message.forbidden"))

    return data

def get_cover(sid):
    cover_url = f"https://www.diving-fish.com/covers/{get_cover_len5_id(sid)}.png"
    cover_dir = f"./assets/maimai/static/mai/cover/"
    cover_path = cover_dir + f'{get_cover_len5_id(sid)}.png'
    if sid == '11364': #8-EM 的封面需要改动
        return os.path.abspath(cover_path)
    else:
        return cover_url
