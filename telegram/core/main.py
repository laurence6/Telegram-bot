import importlib
import logging
import threading

from telegram.conf.settings import SETTINGS
from telegram.core.bot import BOT
from telegram.core.message import RequestMessage, ResponseMessage


class RequestQueue(object):
    def __init__(self):
        self.requests_list = []
        self.requests_list_condition = threading.Condition(threading.Lock())
        self.processing = []
        self.processing_lock = threading.Lock()

    def get(self):
        while 1:
            if self.requests_list == []:
                with self.requests_list_condition:
                    self.requests_list_condition.wait()
            with self.requests_list_condition:
                for n, i in enumerate(self.requests_list):
                    message_id = '%s%s' % (i['chat']['id'], i['from']['id'])
                    with self.processing_lock:
                        if not message_id in self.processing:
                            self.processing.append(message_id)
                            ret = self.requests_list.pop(n)
                            return ret
                self.requests_list_condition.wait()

    def done(self, message_id):
        with self.processing_lock:
            self.processing.remove(message_id)
        with self.requests_list_condition:
            self.requests_list_condition.notify_all()

    def put(self, request):
        self.requests_list.append(request)
        with self.requests_list_condition:
            self.requests_list_condition.notify_all()


def load_resolver():
    resolver_mod = importlib.import_module(SETTINGS.RESOLVER)
    global resolver
    resolver = getattr(resolver_mod, 'resolve')


def load_middleware():
    global request_middleware
    global handler_middleware
    global response_middleware
    request_middleware = []
    handler_middleware = []
    response_middleware = []
    for middleware in SETTINGS.MIDDLEWARES:
        mw_mod, mw_class = middleware.rsplit('.', 1)
        mw_mod = importlib.import_module(mw_mod)
        mw_class = getattr(mw_mod, mw_class)
        mw = mw_class()
        if hasattr(mw, 'process_request'):
            request_middleware.append(mw.process_request)
        if hasattr(mw, 'process_handler'):
            handler_middleware.append(mw.process_handler)
        if hasattr(mw, 'process_response'):
            response_middleware.insert(0, mw.process_response)


class HandleMessage(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        load_resolver()
        self.resolver = globals()['resolver']
        load_middleware()
        self.request_middleware = globals()['request_middleware']
        self.handler_middleware = globals()['handler_middleware']
        self.response_middleware = globals()['response_middleware']

    def run(self):
        logger = logging.getLogger('handle_message')
        while 1:
            try:
                request = self.queue.get()
                chat_and_from_id = '%s%s' % (request['chat']['id'], request['from']['id'])

                response = None

                for middleware in self.request_middleware:
                    response = middleware(request)
                    if not response is None:
                        break
                if response is None:
                    handler, handler_args = self.resolver(request)
                    for middleware in self.handler_middleware:
                        response = middleware(request, handler, handler_args)
                        if not response is None:
                            break

                if response is None:
                    response = handler(request, **handler_args)

                for middleware in self.response_middleware:
                    response = middleware(request, response)

                if isinstance(response, ResponseMessage):
                    getattr(BOT, response.method)(**response)

                self.queue.done(chat_and_from_id)
            except KeyboardInterrupt:
                return
            except Exception as e:
                logger.error(e)


class GetUpdates(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        logger = logging.getLogger('get_updates')
        offset = 0
        limit = 100
        timeout = 60
        while 1:
            try:
                response = BOT.getUpdates(offset, limit, timeout)
                if not response['ok']:
                    logger.warning('getUpdates: %s', response['description'])
                    continue
                result = response['result']
                if result:
                    for r in result:
                        self.queue.put(RequestMessage(r['message']))
                    offset = result[-1]['update_id']+1
                else:
                    logger.info('No new updates')
            except KeyboardInterrupt:
                return
            except Exception as e:
                logger.error(e)


def execute():
    logger = logging.getLogger('execute')
    try:
        request_queue = RequestQueue()
        processed = [GetUpdates(request_queue)]
        for i in range(SETTINGS.WORKER_PROCESSES):
            processed.append(HandleMessage(request_queue))
        for i in processed:
            i.start()
        for i in processed:
            i.join()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt received')
        exit()
    except Exception as e:
        logger.error(e)
