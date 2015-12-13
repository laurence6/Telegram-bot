class DryRun(object):
    def process_response(self, request, response):
        print('Request: %s\nResponse: %s' % (request, response))
        return None
