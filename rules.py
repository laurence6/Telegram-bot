'''Response rules'''

from base import RULE, rule
import handlers


text_rule = RULE([
    rule('^/hello', handlers.hello),
    rule('^/help', handlers.help),
    rule('^/start', handlers.start),
    rule('^/say$', handlers.sayhello),
    rule('^/say (?P<text>[\s\S]*)$', handlers.say),
    rule('.*', handlers.unknown),
])
audio_rule = RULE([
    rule('[\s\S]*', handlers.sayhello),
])
