'''The telegram bot API'''

import requests


class BOT(object):
    '''
    File: tuple(str(filetype), file_like_object(content)) or list(str(filetype), file_like_object(content))
    '''
    def __init__(self, token):
        self.baseurl = 'https://api.telegram.org/bot%s/' % token

    def getUpdates(self, offset=0, limit=100):
        '''https://core.telegram.org/bots/api#getupdates'''
        return requests.get(self.baseurl+'getUpdates', {'offset': offset, 'limit': limit}).json()

    def sendMessage(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendmessage'''
        return requests.post(self.baseurl+'sendMessage', {'chat_id': chat_id, 'text': text, 'disable_web_page_preview': disable_web_page_preview, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()

    def sendPhoto(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendphoto'''
        if isinstance(photo, str):
            return requests.post(self.baseurl+'sendPhoto', {'chat_id': chat_id, 'photo': photo, 'caption': caption, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()
        elif isinstance(photo, (list, tuple)):
            return requests.post(self.baseurl+'sendPhoto', {'chat_id': chat_id,                 'caption': caption, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}, files={'photo', photo}).json()

    def sendAudio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendaudio'''
        if isinstance(audio, str):
            return requests.post(self.baseurl+'sendAudio', {'chat_id': chat_id, 'audio': audio, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()
        elif isinstance(audio, (list, tuple)):
            return requests.post(self.baseurl+'sendAudio', {'chat_id': chat_id,                 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}, files={'audio': audio}).json()

    def sendVideo(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendvideo'''
        if isinstance(video, str):
            return requests.post(self.baseurl+'sendVideo', {'chat_id': chat_id, 'video': video, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()
        elif isinstance(video, (list, tuple)):
            return requests.post(self.baseurl+'sendVideo', {'chat_id': chat_id,                 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}, files={'video': video}).json()

    def sendDocument(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#senddocument'''
        if isinstance(document, str):
            return requests.post(self.baseurl+'sendDocument', {'chat_id': chat_id, 'document': document, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()
        elif isinstance(document, (list, tuple)):
            return requests.post(self.baseurl+'sendDocument', {'chat_id': chat_id,                       'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}, files={'document': document}).json()

    def sendLocation(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        '''https://core.telegram.org/bots/api#sendlocation'''
        return requests.post(self.baseurl+'sendLocation', {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'reply_to_message_id': reply_to_message_id, 'reply_markup': reply_markup}).json()
