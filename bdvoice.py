#! /usr/bin/python3

import logging
import requests


class BDVOICE(object):
    logger = logging.getLogger('bdvoice')
    taurl = 'http://tsn.baidu.com/text2audio'
    aturl = 'http://vop.baidu.com/server_api'
    tok = ''

    def __init__(self, token):
        self.tok = token

    def get_audio_from_text(self, tex, cuid='1000', lan='zh', ctp=1, spd=6, pit=4, vol=9, per=1):
        self.logger.debug(locals())
        return requests.post(self.taurl,\
                params={'tok':self.tok, 'cuid':cuid, 'lan':lan, 'ctp':ctp, 'spd':spd, 'pit':pit, 'vol':vol, 'per':per, 'tex':tex}).content

    def get_text_from_audio(self, audio, audioformat, audiorate, cuid='1000'):
        self.logger.debug(locals())
        return requests.post(self.aturl,\
                params={'token':self.tok, 'cuid':cuid},\
                data={'data':audio},\
                headers={'content-type': 'audio/%s;rate=%s' % (audioformat, audiorate)})
