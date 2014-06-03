from unittest import TestCase

from testfixtures import LogCapture

import logging


class TestLogInit(TestCase):
    def test_log_message(self):
        with LogCapture() as l:
            logger = logging.getLogger()
            logger.info('a info message')
            logger.error('a error message')
            logger.debug('a debug message')
            logger.critical('a critical message')
            logger.warn('a warning message')
            logger.exception('a exception message')
            l.check(
                ('root', 'INFO', 'a info message'),
                ('root', 'ERROR', 'a error message'),
                ('root', 'DEBUG', 'a debug message'),
                ('root', 'CRITICAL', 'a critical message'),
                ('root', 'WARNING', 'a warning message'),
                ('root', 'ERROR', 'a exception message'),
                )
