'''Handlers'''

import logging
import io

from base import bot, voice


logger = logging.getLogger('bot.handlers')


def unknown(**args):
    return bot.sendPhoto(chat_id=args['chat_id'], photo='AgADBQADrKcxGzZ5NgZi9Dn3WRmEFnPksTIABNjitpp_sm1i9vsAAgI', caption='Speak English please. 喵?', reply_to_message_id=args['message_id'])


def hello(**args):
    return bot.sendMessage(chat_id=args['chat_id'], text='''Hello, I'm Jarvis.''', reply_to_message_id=args['message_id'])


def help(**args):
    return bot.sendMessage(chat_id=args['chat_id'], text='''I don't want to help you because I am busy.''', reply_to_message_id=args['message_id'])


def start(**args):
    return bot.sendMessage(chat_id=args['chat_id'], text='''Hello, I'm Jarvis.\nWhat can I do for you?''')


def sayhello(**args):
    return bot.sendAudio(chat_id=args['chat_id'], audio='AwADBQADUQADSt0PB2rFIs3sIl4VAg', reply_to_message_id=args['message_id'])


def say(**args):
    return bot.sendAudio(chat_id=args['chat_id'], audio=('mp3', io.BytesIO(voice.get_audio_from_text(args['text']))), reply_to_message_id=args['message_id'])
