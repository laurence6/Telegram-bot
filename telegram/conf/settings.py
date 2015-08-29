import importlib


class Settings(object):
    def __init__(self, setting_module):
        mod = importlib.import_module(setting_module)
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))


SETTINGS = Settings('settings')
