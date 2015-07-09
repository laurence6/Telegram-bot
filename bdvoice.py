#! /usr/bin/python3

import logging
import requests


class BDVOICE(object):
    logger = logging.getLogger('bdvoice')
    taurl = 'http://tsn.baidu.com/text2audio'
    aturl = 'http://vop.baidu.com/server_api'
    cuid = 1000
    lan = 'zh'

    ctp = 1 #REST API
    spd = 6
    pit = 4
    vol = 9
    per = 1

    def __init__(self, token):
        self.tok = token
        pass

    def get_audio_from_text(self, tex, cuid=cuid, lan=lan, ctp=ctp, spd=spd, pit=pit, vol=vol, per=per):
        self.logger.debug(locals())
        return requests.post(self.taurl,\
                {'tok':self.tok, 'cuid':cuid, 'lan':lan, 'ctp':ctp, 'spd':spd, 'pit':pit, 'vol':vol, 'per':per, 'tex':tex}).content

    def get_text_from_audio(self, audio):
        pass
