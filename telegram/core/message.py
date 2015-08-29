class Request_Message(dict):
    name = 'request'
    def __init__(self, message):
        self.update(message)

class Response_Message(dict):
    name = 'response'
    def __init__(self, method, args):
        self.method = method
        self.update(args)
