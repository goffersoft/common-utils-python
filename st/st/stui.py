#! /usr/bin/python

"""This Module Contains  a simple UI
   for testing purposes. A web based
   interface would be more beneficial
"""

import zmq
import threading
import logging

from utils.uid import getuid
from utils.log import init as initlog
from utils.misc import get_raw_input_nonblocking_select
from utils.misc import print_usage
from utils.zmqutils import print_zmq_version

try:
    from .stmsgtype import STMsgType
    from .staddr import STAddress
    from .stmsg import STMsgReq
    from .stmsg import STMsgResp
    from .stmsg import init as initstmsg
    from .stmsgcodes import STRCType
    from .stmsgcodes import STRCDescrType
    from .stsvc import init_stsvc
    from .stdb import stdb_registry_to_str
except:
    from stmsgtype import STMsgType
    from staddr import STAddress
    from stmsg import STMsgReq
    from stmsg import STMsgResp
    from stmsg import init as initstmsg
    from stmsgcodes import STRCType
    from stmsgcodes import STRCDescrType
    from stsvc import init_stsvc
    from stdb import stdb_registry_to_str


def stui_process_mgmt_msg(addr,
                          msg):
    func_name = stui_process_mgmt_msg.__name__
    logger = logging.getLogger()

    if(msg.msgparts[6] == 'e'):
        return False, None
    elif(msg.msgparts[6] == 'l'):
        out_msg = STMsgResp(respid=msg.reqid,
                            respcode=STRCType.RC_200,
                            reason=STRCDescrType.RC_200,
                            body=stdb_registry_to_str())
        out_msg.fromhdr = addr
        out_msg.tohdr = msg.fromhdr
        return True, out_msg

    return True, None


def stui_loop(shutdown_event,
              ctxt=None,
              name='cmd proc',
              id=None,
              discovery_addr='localhost:5555',
              mgmt_addr='localhost:6666',
              poll_timeout=5000):
    func_name = stui_loop.__name__
    try:
        usage = """
           l : List Available Servers
           s <uuid> : Stop a Server
           e : Exit
        """
        logger = logging.getLogger()

        print_zmq_version(logger)

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        stui_addr = STAddress(addrparts=(name, str(id)))

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting Cmd Proc Loop...'
                    '(discover_addr=%s, mgmt_addr=%s'
                    'poll_timeout=%d)',
                    func_name,
                    th.getName(),
                    th.ident, id,
                    discovery_addr,
                    mgmt_addr,
                    poll_timeout)

        cmd_socket = ctxt.socket(zmq.PAIR)
        cmd_socket.bind('inproc://' + str(stui_addr))

        inproc_addr_list = (stui_addr,)
        inproc_event_list = (threading.Event(),)

        svc_shutdown_event = None

        svc_thread, svc_shutdown_event = \
            init_stsvc(ctxt,
                       'stuisvc',
                       id,
                       discovery_addr,
                       mgmt_addr,
                       inproc_addr_list,
                       inproc_event_list,
                       poll_timeout,
                       '../conf/logconf_stuisvc.json')

        print_menu = True
        valid_cmds = ('l', 's', 'e')
        while shutdown_event.is_set() is False:
            try:
                if(print_menu is True):
                    print_usage(usage)

                cmd = get_raw_input_nonblocking_select()
                if(cmd == ''):
                    print_menu = False
                    continue
                elif(cmd not in valid_cmds):
                    print_menu = True
                    logger.info('%s : <%s> not a valid cmd...try again',
                                func_name, cmd)
                    continue
                elif(cmd == 'e'):
                    inproc_event_list[0].set()
                    break
                else:
                    print_menu = True

                msg = STMsgReq(body=STMsgType.MGMT+'\r\n'+cmd)
                msg.fromhdr = stui_addr
                msg.tohdr = stui_addr
                cmd_socket.send(msg.tobytes())
                if(cmd == 'l'):
                    rcvd_msg = cmd_socket.recv()
                    rcvd_msg = rcvd_msg.decode()
                    msg, reason =\
                        STMsgResp.verify_msg(rcvd_msg)
                    if(reason is not None):
                        logger.info('%s : Invalid Msg=%s',
                                    func_name, reason)
                        logger.debug('%s : Msg=%r', func_name, rcvd_msg)
                    elif(msg.tohdr == stui_addr):
                        print('List of services : ')
                        print('respcode=%s, reason=%s' %
                              (msg.respcode, msg.reason))
                        print('%s' % msg.body)
                    else:
                        logger.info('%s : Cmd Loop : Message Not Authentic,'
                                    'Msg=%s', func_name, msg.debug())
            except KeyboardInterrupt:
                break

        logger.info('%s : Shutting Down Cmd Processor...', func_name)
        svc_shutdown_event.set()
        svc_thread.join()
    except:
        logger.exception('%s : Shutting Down Cmd Processor...', func_name)
        if (svc_shutdown_event is not None):
            svc_shutdown_event.set()
            svc_thread.join()


def init_stui(ctxt=None,
              stui_name='stui',
              stui_id=None,
              discovery_addr='localhost:5555',
              mgmt_addr='localhost:6666',
              poll_timeout=5000,
              log_cfg='../conf/logconf_stui.json'):
    func_name = init_stui.__name__
    try:
        initstmsg()

        if(ctxt is None):
            ctxt = zmq.Context()

        if(stui_name is None):
            stui_name = 'stui'

        if(discovery_addr is None):
            discovery_addr = '*:5555'

        if(mgmt_addr is None):
            mgmt_addr = '*:6666'

        if(poll_timeout is None):
            poll_timeout = 5000

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stui.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        shutdown_event = threading.Event()

        args = (shutdown_event, ctxt, stui_name,
                stui_id, discovery_addr,
                mgmt_addr, poll_timeout)

        stui_thread = threading.Thread(target=stui_loop, args=args)

        stui_thread.start()

        return stui_thread, shutdown_event

    except:
        logger.exception('%s : stui initialization failed...',
                         func_name)


if __name__ == '__main__':
    try:
        from .stmain import stui_main
    except:
        from stmain import stui_main

    stui_main()
