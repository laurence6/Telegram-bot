import logging

from bdvoice import BDVOICE


logger = logging.getLogger('base')


try:
    with open('bdvoicetoken') as f:
        token = f.read().rstrip()
        if not token:
            logger.critical('Bdvoice token is required')
            exit()
        voice = BDVOICE(token)
except FileNotFoundError:
    logger.critical('Bdvoice token file not found')
    exit()
