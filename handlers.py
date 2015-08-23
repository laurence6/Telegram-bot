'''Handlers'''

import logging
import io

from base import voice


logger = logging.getLogger('bot.handlers')


def unknown(**args):
    return 'sendPhoto', {'photo':'AgADBQADrKcxGzZ5NgZi9Dn3WRmEFnPksTIABNjitpp_sm1i9vsAAgI', 'caption':'Speak English please. 喵?', 'reply_to_message_id':True}


def hello(**args):
    return 'sendMessage', {'text':'''Hello, I'm Jarvis.''', 'reply_to_message_id':True}


def help(**args):
    return 'sendMessage', {'text':'''I don't want to help you because I am busy.''', 'reply_to_message_id':True}


def start(**args):
    return 'sendMessage', {'text':'''Hello, I'm Jarvis.\nWhat can I do for you?'''}


def sayhello(**args):
    return 'sendAudio', {'audio':'AwADBQADUQADSt0PB2rFIs3sIl4VAg', 'reply_to_message_id':True}


def say(**args):
    return 'sendAudio', {'audio':('mp3', io.BytesIO(voice.get_audio_from_text(args['text']))), 'reply_to_message_id':True}
