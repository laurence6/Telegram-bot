import logging
import re

from bdvoice import BDVOICE
from tgbotapi import BOT


logger = logging.getLogger('base')


sessions = {}

try:
    with open('bdvoicetoken') as f:
        token = f.read().rstrip()
        if not token:
            logger.critical('Bdvoice token is required')
            exit()
        voice = BDVOICE(token)

    with open('tgtoken') as f:
        token = f.read().rstrip()
        if not token:
            logger.critical('Telegram bot token is required')
            exit()
        bot = BOT(token)
except FileNotFoundError as e:
    logger.critical('Token file not found %s' % e)
    exit()


class RULE(list):
    def handle(self, string, message):
        for r in self:
            search = r[0].search(string)
            if search:
                message.update(search.groupdict())
                message.update(r[2])
                return r[1](**message)


def rule(pattern, function, **args):
    return [re.compile(pattern), function, args]
