#! /usr/bin/python

"""This Module Contains log helper functionss
     1) init - initializes the python logging
               module.
"""

import os
import json
import logging
import logging.config


def init(
        default_path='../conf/logconf_template.json',
        default_level=logging.DEBUG,
        env_key='LOG_CFG'
        ):
    """Setup logging configuration
       1) initializes the default log level.
       2) reads the log conf file the name
          and location of which is passed in
          by the LOG_CFG env key or from the
          default_path argument
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
        print('**** Log Init Error : Cannot Find \
              Json Log Cfg File : ' + default_path)
        logging.basicConfig(level=default_level)

if __name__ == "__main__":
    import logging
    import logging.config

    print('python log version --> ' + logging.__version__)

    init()

    logger = logging.getLogger(__name__)

    logger.info('hello world')

    logger.debug('hello world')

    logger.error('hello world')

    logger.warning('hello world')

    logger.critical('hello world')

    try:
        if('Hello' > 3):
            logger.exception('the if statement throws an exception '
                             'in the python3 world(as it should) '
                             'but gets executed in the python2 world')
    except:
        logger.exception('hello world')
