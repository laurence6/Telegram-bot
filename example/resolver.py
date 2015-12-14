'''Response rules'''

import re

import handlers


class Rule(list):
    def get_handler(self, string):
        args = {}
        for i in self:
            search = i[0].search(string)
            if search:
                args.update(search.groupdict())
                args.update(i[2])
                return i[1], args


def rule(pattern, function, **args):
    return [re.compile(pattern), function, args]


TEXT_RULE = Rule([
    rule('^/hello', handlers.hello),
    rule('^/help', handlers.help),
    rule('^/start', handlers.start),
    rule('^/say$', handlers.sayhello),
    rule('^/say (?P<text>[\s\S]*)$', handlers.say),
    rule('[\s\S]*', handlers.unknown),
])
AUDIO_RULE = Rule([
    rule('[\s\S]*', handlers.sayhello),
])


def resolve(request):
    if 'text' in request:
        text = request['text']
        return TEXT_RULE.get_handler(text)
    elif 'photo' in request:
        pass
    elif 'voice' in request:
        return AUDIO_RULE.get_handler('')
    elif 'audio' in request:
        return AUDIO_RULE.get_handler('')
    elif 'video' in request:
        pass
    elif 'document' in request:
        pass
