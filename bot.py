#! /usr/bin/env python3
'''A telegram bot'''

import logging
import time

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

import tgbotapi
from rules import text_rule, audio_rule


def handle_message(message):
    logger = logging.getLogger('bot.handle_message')
    from_id = message['from']['id']
    chat_id = message['chat']['id']
    message_id = message['message_id']
    sendtime = message['date']

    if 'text' in message:
        text = message['text']
        f, a = text_rule.get(text)
    elif 'photo' in message:
        pass
    elif 'audio' in message:
        f, a = audio_rule.get('')
    elif 'video' in message:
        pass
    elif 'document' in message:
        pass

    a['chat_id'] = chat_id
    a['reply_to_message_id'] = message_id if 'reply_to_message_id' in a else None
    return f, a


def loop(bot, offset=0, limit=100, timeout=15):
    logger = logging.getLogger('bot')
    while 1:
        response = tgbot.getUpdates(offset, limit, timeout)
        if not response['ok']:
            logger.warning('getUpdates: %s', response['description'])
            continue
        result = response['result']
        for r in result:
            f, a = handle_message(r['message'])
            if f:
                r = getattr(bot, f)(**a)
                if not r['ok']:
                    logger.error(f, a)
        if result:
            offset = result[-1]['update_id']+1
            if len(result) < limit:
                time.sleep(10)
        else:
            time.sleep(30)
            continue


if __name__ == '__main__':
    try:
        with open('tgtoken') as f:
            token = f.read().rstrip()
            if not token:
                logging.critical('Telegram token is required')
                exit()
            tgbot = tgbotapi.BOT(token)
        loop(tgbot)
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt received')
        exit()
    except FileNotFoundError:
        logging.critical('Telegram token file not found')
        exit()
