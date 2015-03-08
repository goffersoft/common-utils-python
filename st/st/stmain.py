#! /usr/bin/python

"""This Module Contains Service Tracker entry point
"""

import zmq
import logging

from utils.log import init as initlog

try:
    from .stmgr import init_stmgr
    from .stui import init_stui
    from .stsvc import init_stsvc
except:
    from stmgr import init_stmgr
    from stui import init_stui
    from stsvc import init_stsvc


def stmgr_main(ctxt=None,
               stmgr_name='stmgr',
               stmgr_id=None,
               discovery_addr='*:5555',
               mgmt_addr='*:6666',
               discovery_interval=5,
               poll_timeout=5000,
               log_cfg='../conf/logconf_stmgr.json'):
    try:
        event = None

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stmgr.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        t, event = init_stmgr(ctxt,
                              stmgr_name,
                              stmgr_id,
                              discovery_addr,
                              mgmt_addr,
                              discovery_interval,
                              poll_timeout,
                              log_cfg)

        while t.is_alive() is True:
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        logger.info('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()
    except:
        logger.exception('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()


def stui_main(ctxt=None,
              stui_name='stui',
              stui_id=None,
              discovery_addr='localhost:5555',
              mgmt_addr='localhost:6666',
              poll_timeout=5000,
              log_cfg='../conf/logconf_stui.json'):
    try:
        event = None

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stui.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        t, event = init_stui(ctxt,
                             stui_name,
                             stui_id,
                             discovery_addr,
                             mgmt_addr,
                             poll_timeout,
                             log_cfg)

        while t.is_alive() is True:
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        logger.info('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()
    except:
        logger.exception('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()


def stsvc_main(ctxt=None,
               stsvc_name='stsvc',
               stsvc_id=None,
               discovery_addr='localhost:5555',
               mgmt_addr='localhost:6666',
               inproc_addr_list=None,
               inproc_shutdown_event_list=None,
               poll_timeout=5000,
               log_cfg='../conf/logconf_stsvc.json'):
    try:
        event = None

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stsvc.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        t, event = init_stsvc(ctxt,
                              stsvc_name,
                              stsvc_id,
                              discovery_addr,
                              mgmt_addr,
                              inproc_addr_list,
                              inproc_shutdown_event_list,
                              poll_timeout,
                              log_cfg)

        while t.is_alive() is True:
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        logger.info('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()
    except:
        logger.exception('Shutting Down...')
        if(event is not None):
            event.set()
            t.join()


if __name__ == '__main__':
    import sys
    from utils.misc import print_usage_and_exit

    usage = """
            {0} <'stsvc' or 'stmgr' or 'stui' >
            """.format(sys.argv[0])

    try:
        event = None
        logger = logging.getLogger()
        ctxt = zmq.Context()

        if(len(sys.argv) != 2):
            print_usage_and_exit(usage, '**1 arg required**')

        if(sys.argv[1] == 'stsvc'):
            stsvc_main(ctxt=ctxt)
        elif(sys.argv[1] == 'stmgr'):
            stmgr_main(ctxt=ctxt)
        elif(sys.argv[1] == 'stui'):
            stui_main(ctxt=ctxt)
        else:
            print_usage_and_exit(usage, '**bad arg**')

    except:
        logger.exception('Shutting Down...')
