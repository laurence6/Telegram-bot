'''Response rules'''

import re

import handlers


class RULE(list):
    def get(self, string):
        for r in self:
            search = r[0].search(string)
            if search:
                return r[1](**search.groupdict())


def rule(pattern, function, **args):
    return [re.compile(pattern), function, args]


text_rule = RULE([
    rule('^/hello', handlers.hello),
    rule('^/help', handlers.help),
    rule('^/start', handlers.start),
    rule('^/say$', handlers.sayhello),
    rule('^/say (?P<text>.*)$', handlers.say),
    rule('.*', handlers.unknown),
])
audio_rule = RULE([
    rule('.*', handlers.sayhello),
])
