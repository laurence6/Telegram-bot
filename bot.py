#! /usr/bin/env python3
'''Telegram bot'''

import logging
import time

from tgbotapi import BOT
from rules import text_rule, audio_rule


def handle_message(message):
    logger = logging.getLogger('bot.loop.handle_message')
    from_id = message['from']['id']
    chat_id = message['chat']['id']
    message_id = message['message_id']
    sendtime = message['date']
    f = None
    a = {}

    try:
        if sessions[from_id][chat_id] == 'Deny':
            return f, a
    except KeyError:
        sessions[from_id] = {}
        sessions[from_id][chat_id] = 'OK'

    try:
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

        if f:
            a['chat_id'] = chat_id
            a['reply_to_message_id'] = message_id if 'reply_to_message_id' in a else None
            r = getattr(bot, f)(**a)
            if not r['ok']:
                logger.error(f, a)
    except Exception as e:
        logger.error(e)


def loop(offset=0, limit=100, timeout=15):
    logger = logging.getLogger('bot.loop')
    while 1:
        try:
            response = bot.getUpdates(offset, limit, timeout)
            if not response['ok']:
                logger.warning('getUpdates: %s', response['description'])
                continue
            result = response['result']
            if result:
                for r in result:
                    handle_message(r['message'])
                offset = result[-1]['update_id']+1
                if len(result) < limit:
                    time.sleep(10)
            else:
                time.sleep(30)
        except Exception as e:
            logger.error(e)
            time.sleep(1)


def main():
    logger = logging.getLogger('bot')
    try:
        global bot, sessions
        with open('tgtoken') as f:
            token = f.read().rstrip()
            if not token:
                logger.critical('Telegram token is required')
                exit()
        bot = BOT(token)
        sessions = {}
        loop()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt received')
        exit()
    except FileNotFoundError:
        logger.critical('Telegram token file not found')
        exit()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)-5.5s] %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    main()
