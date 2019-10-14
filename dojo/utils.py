import sys
import logging

from dojo.constants import (
    QUEUE_PATH
)

def socket_log(logger, socket_name, kind):
    # ideally we should use logging module
    msgs = {
        'new': '∆ New connection',
        'recv': '< Data receieved',
        'sent': '> Sending data',
        'close': 'x Closed',
        'empty': 'ø Empty queue'
    }
    logger.info('{} {}:{}'.format(msgs[kind], *socket_name))


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()