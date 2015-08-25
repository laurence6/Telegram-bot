#! /usr/bin/env python3
'''Telegram bot'''

import logging
import time


def handle_message(message):
    logger = logging.getLogger('bot.loop.handle_message')
    from_id = message['from']['id']
    chat_id = message['chat']['id']
    message_id = message['message_id']
    sendtime = message['date']
    message_info = {'from_id':from_id, 'chat_id':chat_id,\
            'message_id':message_id, 'sendtime':sendtime}

    try:
        if sessions[from_id][chat_id] == 'Deny':
            return
    except KeyError:
        sessions[from_id] = {}
        sessions[from_id][chat_id] = 'OK'

    try:
        if 'text' in message:
            text = message['text']
            return text_rule.handle(text, message_info)
        elif 'photo' in message:
            pass
        elif 'voice' in message:
            return audio_rule.handle('', message_info)
        elif 'audio' in message:
            return audio_rule.handle('', message_info)
        elif 'video' in message:
            pass
        elif 'document' in message:
            pass
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
        loop()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt received')
        exit()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)-5.5s] %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    from base import bot, sessions
    from rules import text_rule, audio_rule
    main()
