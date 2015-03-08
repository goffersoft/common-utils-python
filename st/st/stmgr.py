#! /usr/bin/python

"""This Module Contains Service Tracker Manager code
"""

import zmq
import threading
import logging

from utils.uid import getuid
from utils.log import init as initlog
from utils.zmqutils import print_zmq_version

try:
    from .stdb import stdb_registry_to_str
    from .stdb import stdb_delete_from_registry
    from .stdb import stdb_update_registry
    from .stdb import stdb_prune_registry
    from .stmsgtype import STMsgType
    from .staddr import STAddress
    from .stmsg import STMsgReq
    from .stmsg import STMsgResp
    from .stmsg import init as initstmsg
    from .stmsgcodes import STRCType
    from .stmsgcodes import STRCDescrType
    from .stui import stui_process_mgmt_msg
except:
    from stdb import stdb_registry_to_str
    from stdb import stdb_delete_from_registry
    from stdb import stdb_update_registry
    from stdb import stdb_prune_registry
    from stmsgtype import STMsgType
    from staddr import STAddress
    from stmsg import STMsgReq
    from stmsg import STMsgResp
    from stmsg import init as initstmsg
    from stmsgcodes import STRCType
    from stmsgcodes import STRCDescrType
    from stui import stui_process_mgmt_msg


def stmgr_process_msg(stmgr_addr,
                      from_id,
                      in_msg):
    func_name = stmgr_process_msg.__name__
    logger = logging.getLogger()

    msg, reason = STMsgReq.verify_msg(in_msg)

    if(reason is not None):
        logger.info('%s : Invalid Msg : %s', func_name, reason)
        logger.info('%s : Msg=%r', func_name, in_msg)
        return True, None

    if((msg.tohdr.id != stmgr_addr.id) and
       (msg.fromhdr.id != from_id)):
        logger.info('%s : Message Not Authentic, Msg=%r', func_name, in_msg)
        return True, None

    retval = None
    if(msg.is_mgmt()):
        retval, outmsg = stmgr_process_mgmt_msg(stmgr_addr,
                                                msg)
    else:
        retval, outmsg = stmgr_process_svc_msg(stmgr_addr,
                                               msg)

    return retval, outmsg


def stmgr_process_mgmt_msg(stmgr_addr,
                           msg):
    func_name = stmgr_process_mgmt_msg.__name__
    logger = logging.getLogger()

    return stui_process_mgmt_msg(stmgr_addr,
                                 msg)


def stmgr_process_svc_msg(stmgr_addr,
                          msg):

    func_name = stmgr_process_svc_msg.__name__
    logger = logging.getLogger()

    add = False
    purge = False
    st_msg_type = None
    out_msg = STMsgResp(respid=msg.reqid,
                        respcode=STRCType.RC_200,
                        reason=STRCDescrType.RC_200,
                        body=stdb_registry_to_str())
    out_msg.fromhdr = stmgr_addr
    out_msg.tohdr = msg.fromhdr

    if(msg.is_init()):
        st_msg_type = STMsgType.INIT
        add = True
    elif(msg.is_hello()):
        st_msg_type = STMsgType.HELLO
        add = True
    elif(msg.is_bye()):
        st_msg_type = STMsgType.BYE
        purge = True
        out_msg = None
    else:
        out_msg = None
        logger.info('%s : Message Invalid, Msg=%s', func_name, msg.debug())

    if(purge is True):
        stdb_delete_from_registry(msg.fromhdr.id)

    if(add is True):
        stdb_update_registry(msg.fromhdr.id,
                             msg.fromhdr.name,
                             st_msg_type)

    return True, out_msg


def stmgr_housekeeping(stmgr_addr,
                       discovery_socket,
                       shutdown_event,
                       discovery_interval,
                       init=False):
    func_name = stmgr_housekeeping.__name__
    logger = logging.getLogger()
    if(shutdown_event.is_set() is True):
        logger.info('%s : %s : %s : '
                    'Shutting Down Periodic Timer...',
                    func_name,
                    threading.current_thread().getName(),
                    threading.current_thread().ident)
        return

    msg = STMsgReq(body='hello')
    msg.fromhdr = stmgr_addr
    discovery_socket.send(msg.tobytes())

    housekeeping_args = (stmgr_addr,
                         discovery_socket,
                         shutdown_event,
                         discovery_interval)

    t = threading.Timer(discovery_interval,
                        stmgr_housekeeping,
                        housekeeping_args)

    if(init is True):
        logger.info('%s : %s : %s : '
                    'Starting Periodic Housekeeping Timer...',
                    func_name,
                    threading.current_thread().getName(),
                    threading.current_thread().ident)

    t.start()


def stmgr_loop(shutdown_event,
               ctxt=None,
               name='stmgr',
               id=None,
               discovery_addr='*:5555',
               mgmt_addr='*:6666',
               discovery_interval=5,
               poll_timeout=5000):
    func_name = stmgr_loop.__name__
    try:
        logger = logging.getLogger()

        print_zmq_version(logger)

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        stmgr_addr = STAddress(addrparts=(name, str(id)))

        discovery_socket = ctxt.socket(zmq.PUB)
        mgmt_socket = ctxt.socket(zmq.ROUTER)
        discovery_socket.bind('tcp://' + str(discovery_addr))
        mgmt_socket.bind('tcp://' + str(mgmt_addr))

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting stmgr...'
                    '(discover_addr=%s, mgmt_addr=%s'
                    'discover_interval=%d, poll_timeout=%d)',
                    func_name,
                    th.getName(),
                    th.ident, id,
                    discovery_addr,
                    mgmt_addr,
                    discovery_interval,
                    poll_timeout)

        housekeeping_shutdown_event = threading.Event()

        stmgr_housekeeping(stmgr_addr,
                           discovery_socket,
                           housekeeping_shutdown_event,
                           discovery_interval,
                           True)

        poller = zmq.Poller()
        poller.register(mgmt_socket, zmq.POLLIN)

        while shutdown_event.is_set() is False:
            try:
                socks = dict(poller.poll(poll_timeout))

                if(mgmt_socket in socks):
                    msgparts = mgmt_socket.recv_multipart()
                    numparts = len(msgparts)
                    i = 1
                    msg = ''
                    while(i < numparts):
                        msg += msgparts[i].decode()
                        i += 1

                    retval, out_msg = stmgr_process_msg(stmgr_addr,
                                                        msgparts[0],
                                                        msg)

                    if(retval is False):
                        break

                    if(out_msg is not None):
                        out_msgparts = (msgparts[0], out_msg.tobytes())
                        mgmt_socket.send_multipart(out_msgparts)

                stdb_prune_registry()
            except KeyboardInterrupt:
                    logger.exception('%s : stmgr exception...', func_name)
                    break

        logger.info('%s : Shutting Down stmgr...',
                    func_name)
        housekeeping_shutdown_event.set()
    except:
        logger.exception('%s : Shutting Down stmgr...', func_name)
        housekeeping_shutdown_event.set()


def init_stmgr(ctxt=None,
               stmgr_name='stmgr',
               stmgr_id=None,
               discovery_addr='*:5555',
               mgmt_addr='*:6666',
               discovery_interval=5,
               poll_timeout=5000,
               log_cfg='../conf/logconf_stmgr.json'):
    func_name = init_stmgr.__name__
    try:
        initstmsg()

        if(ctxt is None):
            ctxt = zmq.Context()

        if(stmgr_name is None):
            stmgr_name = 'stmgr'

        if(discovery_addr is None):
            discovery_addr = '*:5555'

        if(mgmt_addr is None):
            mgmt_addr = '*:6666'

        if(discovery_interval is None):
            discovery_interval = 5

        if(poll_timeout is None):
            poll_timeout = 5000

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stmgr.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        shutdown_event = threading.Event()

        args = (shutdown_event, ctxt, stmgr_name,
                stmgr_id, discovery_addr,
                mgmt_addr, discovery_interval, poll_timeout)

        stmgr_thread = threading.Thread(target=stmgr_loop,
                                        args=args)

        stmgr_thread.start()

        return stmgr_thread, shutdown_event
    except:
        logger.exception('%s : stmgr initialization failed...',
                         func_name)


if __name__ == '__main__':
    try:
        from .stmain import stmgr_main
    except:
        from stmain import stmgr_main

    stmgr_main()
