import secrets

from core.builtins import Bot
from core.utils.i18n import get_target_locale
from core.component import module


r = module('random', alias={'rand': 'random', 'rng': 'random'}, developers=['Dianliang233'], desc='{random.desc}', )


@r.handle('number <min> <max> {{random.number.help}}', )
async def _(msg: Bot.MessageSession):
    _min = msg.parsed_msg['<min>']
    _max = msg.parsed_msg['<max>']
    random = secrets.randbelow(int(_max) - int(_min) + 1) + int(_min)
    await msg.finish('' + str(random))


@r.handle('choice ... {{random.choice.help}}', )
async def _(msg: Bot.MessageSession):
    choices = msg.parsed_msg['...']
    await msg.finish(secrets.choice(choices))
