#! /usr/bin/python

import os
import json
import logging
import logging.config


def init_logging(
    default_path='./conf/logconf_template.json',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            cfg = json.load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(level=default_level)

if __name__ == "__main__":
    from projtemplate import hello
    from projtemplate import uniqid
    import logging
    import logging.config

    hello.say_hello()
    print uniqid.get_uniqid()

    print logging.__version__

    init_logging()

    logger = logging.getLogger(__name__)

    logger.info('hello world')

    logger.debug('hello world')

    logger.error('hello world')

    logger.warning('hello world')

    logger.critical('hello world')

    logger.exception('hello world')