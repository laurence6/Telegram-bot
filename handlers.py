'''Handlers'''

import logging
import io

import bdvoice


logger = logging.getLogger('handlers')
try:
    with open('bdvoicetoken') as f:
        token = f.read().rstrip()
        if not token:
            logger.critical('Bdvoice token is required')
            exit()
        voice = bdvoice.BDVOICE(token)
except FileNotFoundError:
    logger.critical('Bdvoice token file not found')
    exit()

def unknown(**args):
    return 'sendPhoto', {'photo':'AgADBQADrKcxGzZ5NgZi9Dn3WRmEFnPksTIABNjitpp_sm1i9vsAAgI', 'caption':'Speak English please. 喵?', 'reply_to_message_id':True}


def hello(**args):
    return 'sendMessage', {'text':'Hello, I\'m Jarvis.', 'reply_to_message_id':True}


def help(**args):
    return 'sendMessage', {'text':'I don\'t want to help you because i\'m busy.', 'reply_to_message_id':True}


def start(**args):
    return 'sendMessage', {'text':'Hello, I\'m Jarvis.\nWhat can I do for you?'}


def sayhello(**args):
    return 'sendAudio', {'audio':'AwADBQADBAADSt0PB4a5C-Prm7oKAg'}


def say(**args):
    return 'sendAudio', {'audio':('mp3', io.BytesIO(voice.get_audio_from_text(args['text'])))}
