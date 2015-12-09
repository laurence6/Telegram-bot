class RequestMessage(dict):
    name = 'request'
    def __init__(self, message):
        self.update(message)

class ResponseMessage(dict):
    name = 'response'
    def __init__(self, method, args):
        self.method = method
        self.update(args)
