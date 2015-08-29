#! /usr/bin/env python3
'''Telegram bot'''

import logging


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)-5.5s] %(asctime)s %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    from telegram.core.main import execute

    execute()
