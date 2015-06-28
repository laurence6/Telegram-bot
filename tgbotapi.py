'''The telegram bot API'''

import requests


class BOT(object):
    def __init__(self, token):
        self.baseurl = 'https://api.telegram.org/bot%s/' % token

    def getUpdates(self, offset=0, limit=100):
        '''https://core.telegram.org/bots/api#getupdates'''
        return requests.get(self.baseurl+'getUpdates', {'offset': offset, 'limit': limit,}).json()

    def sendMessage(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendmessage'''
        return requests.get(self.baseurl+'sendMessage', {'chat_id': chat_id, 'text': text, 'disable_web_page_preview': disable_web_page_preview, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()

    def sendPhoto(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendphoto'''
        return requests.get(self.baseurl+'sendPhoto', {'chat_id': chat_id, 'photo': photo, 'caption': caption, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()

    def sendAudio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendaudio'''
        return requests.get(self.baseurl+'sendAudio', {'chat_id': chat_id, 'audio': audio, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()

    def sendVideo(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendvideo'''
        return requests.get(self.baseurl+'sendVideo', {'chat_id': chat_id, 'video': video, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()

    def sendDocument(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#senddocument'''
        return requests.get(self.baseurl+'sendDocument', {'chat_id': chat_id, 'document': document, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()

    def sendLocation(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendlocation'''
        return requests.get(self.baseurl+'sendLocation', {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup,}).json()
