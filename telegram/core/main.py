import importlib
import logging
import multiprocessing
import time

from telegram.conf.settings import SETTINGS
from telegram.core.bot import BOT
from telegram.core.message import Request_Message, Response_Message


class Handle_Message(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.load_resolver()
        self.load_middleware()

    def load_resolver(self):
        resolver_mod = importlib.import_module(SETTINGS.RESOLVER)
        self.resolver = getattr(resolver_mod, 'resolve')

    def load_middleware(self):
        self.request_middleware = []
        self.handler_middleware = []
        self.response_middleware = []
        for middleware in SETTINGS.MIDDLEWARES:
            mw_mod, mw_class = middleware.rsplit('.', 1)
            mw_mod = importlib.import_module(mw_mod)
            mw_class = getattr(mw_mod, mw_class)
            mw = mw_class()
            if hasattr(mw, 'process_request'):
                self.request_middleware.append(mw.process_request)
            if hasattr(mw, 'process_handler'):
                self.handler_middleware.append(mw.process_handler)
            if hasattr(mw, 'process_response'):
                self.response_middleware.insert(0, mw.process_response)

    def run(self):
        logger = logging.getLogger('handle_message')
        try:
            while 1:
                request = self.queue.get()

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

                if isinstance(response, Response_Message):
                    getattr(BOT, response.method)(**response)
        except KeyboardInterrupt:
            return
        except Exception as e:
            logger.error(e)


class Get_Updates(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        logger = logging.getLogger('get_updates')
        offset = 0
        limit = 100
        timeout = 15
        try:
            while 1:
                response = BOT.getUpdates(offset, limit, timeout)
                if not response['ok']:
                    logger.warning('getUpdates: %s', response['description'])
                    continue
                result = response['result']
                if result:
                    for r in result:
                        self.queue.put(Request_Message(r['message']))
                    offset = result[-1]['update_id']+1
                    if len(result) < limit:
                        time.sleep(10)
                else:
                    logger.info('No new updates')
                    time.sleep(30)
        except KeyboardInterrupt:
            return
        except Exception as e:
            logger.error(e)


def execute():
    logger = logging.getLogger('execute')
    try:
        queue = multiprocessing.Queue()
        processed = [Get_Updates(queue)]
        for i in range(SETTINGS.WORKER_PROCESSES):
            processed.append(Handle_Message(queue))
        for i in processed:
            i.start()
        for i in processed:
            i.join()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt received')
        exit()
    except Exception as e:
        logger.error(e)
