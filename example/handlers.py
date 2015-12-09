'''Handlers'''

import logging
import io

from telegram.core.message import ResponseMessage
from telegram.utils.bdvoice import BDVOICE


logger = logging.getLogger('bot.handlers')


def unknown(request, **args):
    return ResponseMessage('sendPhoto', {'chat_id':request['chat']['id'], 'photo':'AgADBQADrKcxGzZ5NgZi9Dn3WRmEFnPksTIABNjitpp_sm1i9vsAAgI', 'caption':'Speak English please. 喵?', 'reply_to_message_id':request['message_id']})


def hello(request, **args):
    return ResponseMessage('sendMessage', {'chat_id':request['chat']['id'], 'text':'''Hello, I'm Jarvis.''', 'reply_to_message_id':request['message_id']})


def help(request, **args):
    return ResponseMessage('sendMessage', {'chat_id':request['chat']['id'], 'text':'''I don't want to help you because I am busy.''', 'reply_to_message_id':request['message_id']})


def start(request, **args):
    return ResponseMessage('sendMessage', {'chat_id':request['chat']['id'], 'text':'''Hello, I'm Jarvis.\nWhat can I do for you?'''})


def sayhello(request, **args):
    return ResponseMessage('sendAudio', {'chat_id':request['chat']['id'], 'audio':'AwADBQADUQADSt0PB2rFIs3sIl4VAg', 'reply_to_message_id':request['message_id']})


def say(request, **args):
    return ResponseMessage('sendAudio', {'chat_id':request['chat']['id'], 'audio':('mp3', io.BytesIO(BDVOICE.get_audio_from_text(args['text']))), 'reply_to_message_id':request['message_id']})
