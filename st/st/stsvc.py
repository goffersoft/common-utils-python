#! /usr/bin/python

"""This Module Contains Service Tracker Service code
"""

import zmq
import threading
import random
import logging

from utils.uid import getuid
from utils.log import init as initlog
from utils.zmqutils import print_zmq_version

try:
    from .stmsgtype import STMsgType
    from .staddr import STAddress
    from .stmsg import STMsgReq
    from .stmsg import STMsgResp
    from .stmsg import init as initstmsg
    from .stmsgcodes import STRCType
    from .stmsgcodes import STRCDescrType
except:
    from stmsgtype import STMsgType
    from staddr import STAddress
    from stmsg import STMsgReq
    from stmsg import STMsgResp
    from stmsg import init as initstmsg
    from stmsgcodes import STRCType
    from stmsgcodes import STRCDescrType


def stsvc_loop(shutdown_event,
               ctxt=None,
               name=None,
               id=None,
               discovery_addr='localhost:5555',
               mgmt_addr='localhost:6666',
               inproc_addr_list=None,
               inproc_shutdown_event_list=None,
               poll_timeout=5000):
    func_name = stsvc_loop.__name__
    try:
        logger = logging.getLogger()

        print_zmq_version(logger)

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        if(name is None):
            name = 'Service ' + str(random.randint(1, 1000000))

        stsvc_addr = STAddress(addrparts=(name, str(id)))
        filter = u''

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting Service Loop...'
                    '(discover_addr=%s, mgmt_addr=%s, '
                    'poll_timeout=%d)',
                    func_name,
                    th.getName(),
                    th.ident, id,
                    discovery_addr,
                    mgmt_addr,
                    poll_timeout)

        discovery_socket = ctxt.socket(zmq.SUB)
        discovery_socket.connect('tcp://' + str(discovery_addr))
        discovery_socket.setsockopt_string(zmq.SUBSCRIBE, filter)
        stsvc_socket = ctxt.socket(zmq.DEALER)
        stsvc_socket.setsockopt(zmq.IDENTITY, str(id).encode())
        stsvc_socket.connect('tcp://' + str(mgmt_addr))
        id = getuid()

        poller = zmq.Poller()
        poller.register(stsvc_socket, zmq.POLLIN)
        poller.register(discovery_socket, zmq.POLLIN)

        inproc_socket_list = []
        inproc_req_dict = None
        num_inproc_socks = None
        if(inproc_addr_list is not None):
            num_inproc_socks = len(inproc_addr_list)
            inproc_req_dict = {}
            inproc_socket_list = []
            for addr in inproc_addr_list:
                inproc_socket = ctxt.socket(zmq.PAIR)
                inproc_socket.connect('inproc://' + str(addr))
                inproc_socket_list.append(inproc_socket)
                poller.register(inproc_socket, zmq.POLLIN)

        init = False
        hello = False
        num_polls = 0
        reqid = None
        stmgr_addr = None

        while shutdown_event.is_set() is False:
            try:
                i = 0
                if(inproc_addr_list is not None and
                   inproc_shutdown_event_list is not None):
                    for event in inproc_shutdown_event_list:
                        if(event.is_set() is True):
                            poller.unregister(inproc_socket_list[i])
                            inproc_socket_list[i] = None
                            num_inproc_socks -= 1
                        i += 1
                    if(num_inproc_socks <= 0):
                        break
                socks = dict(poller.poll(poll_timeout))
            except KeyboardInterrupt:
                break

            if(discovery_socket in socks):
                rcvd_msg = discovery_socket.recv()
                rcvd_msg = rcvd_msg.decode()
                msg, reason = STMsgReq.verify_msg(rcvd_msg)
                if(reason is not None):
                    logger.info('%s : discovery socket : Invalid Msg=%r',
                                func_name, reason)
                    logger.info('%s : Msg=%r', func_name, rcvd_msg)
                else:
                    if(stmgr_addr is None):
                        init = True
                    stmgr_addr = msg.fromhdr

            if(stsvc_socket in socks):
                rcvd_msg = stsvc_socket.recv()
                rcvd_msg = rcvd_msg.decode()
                msg, reason = STMsgResp.verify_msg(rcvd_msg)
                if(reason is not None):
                    logger.info('%s : stsvc_socket : Invalid Msg=%r',
                                func_name, reason)
                    logger.info('%s : Msg=%r', func_name, rcvd_msg)
                else:
                    if((msg.fromhdr.id == stmgr_addr.id) and
                       (msg.tohdr.id == stsvc_addr.id)):
                        if(reqid == msg.respid):
                            reqid = None
                            init = False
                            hello = False
                        elif(msg.respid in inproc_req_dict):
                            i = inproc_req_dict[msg.respid]
                            del inproc_req_dict[msg.respid]
                            if(inproc_socket_list[i] is not None):
                                msg = STMsgResp(respid=msg.respid,
                                                respcode=msg.respcode,
                                                reason=msg.reason,
                                                body=msg.body)
                                msg.fromhdr = stsvc_addr
                                msg.tohdr = inproc_addr_list[i]
                                inproc_socket_list[i].send(msg.tobytes())
                        else:
                            logger.info('%s : stsvc socket : '
                                        'no matching request '
                                        'for this response, Msg=%r',
                                        func_name, rcvd_msg)
                    else:
                        if(msg.fromhdr.id != (stmgr_addr.id)):
                            stmgr_addr = None
                        logger.info('%s : stsvc socket : '
                                    'Message Not Authentic, Msg=%s',
                                    func_name, msg.debug())
                        reqid = None
                        init = False
                        hello = False

            i = 0
            for inproc_sock in inproc_socket_list:
                if(inproc_sock in socks):
                    rcvd_msg = inproc_sock.recv()
                    rcvd_msg = rcvd_msg.decode()
                    msg, reason = STMsgReq.verify_msg(rcvd_msg)
                    if(reason is not None):
                        logger.info('%s : inproc socket(%s) :  '
                                    'Invalid Msg : %r',
                                    func_name,
                                    inproc_addr_list[i],
                                    reason)
                        logger.info('%s : Msg=%r', func_name, rcvd_msg)
                    elif(stmgr_addr is None):
                        if(inproc_socket_list[i] is not None):
                            msg = STMsgResp(respid=msg.reqid,
                                            respcode=STRCType.RC_503,
                                            reason=STRCDescrType.RC_503 +
                                            ' : Service Mgr Not Initialized')
                            msg.fromhdr = stsvc_addr
                            msg.tohdr = inproc_addr_list[i]
                            inproc_socket.send(msg.tobytes())
                    else:
                        msg = STMsgReq(body=msg.body)
                        msg.fromhdr = stsvc_addr
                        msg.tohdr = stmgr_addr
                        inproc_req_dict[msg.reqid] = i
                        stsvc_socket.send(msg.tobytes())
                i += 1

            if(stmgr_addr is not None):
                num_polls += 1
                if(num_polls % 10 == 0):
                    hello = True

            if(init is True):
                if(reqid is None):
                    msg = STMsgReq(body=STMsgType.INIT)
                    msg.fromhdr = stsvc_addr
                    msg.tohdr = stmgr_addr
                    reqid = msg.reqid
                    stsvc_socket.send(msg.tobytes())
            elif(hello is True):
                if(reqid is None):
                    msg = STMsgReq(body=STMsgType.HELLO)
                    msg.fromhdr = stsvc_addr
                    msg.tohdr = stmgr_addr
                    reqid = msg.reqid
                    stsvc_socket.send(msg.tobytes())

            i = 0

        logger.info('%s : Shutting Down Service Loop...', func_name)
    except:
        logger.exception('%s : Shutting Down Service Loop...', func_name)


def init_stsvc(ctxt=None,
               stsvc_name=None,
               stsvc_id=None,
               discovery_addr='localhost:5555',
               mgmt_addr='localhost:6666',
               inproc_addr_list=None,
               inproc_shutdown_event_list=None,
               poll_timeout=5000,
               log_cfg='../conf/logconf_stsvc.json'):
    func_name = init_stsvc.__name__
    try:
        initstmsg()

        if(ctxt is None):
            ctxt = zmq.Context()

        if(stsvc_name is None):
            stmgr_name = 'stmgr'

        if(discovery_addr is None):
            discovery_addr = '*:5555'

        if(mgmt_addr is None):
            mgmt_addr = '*:6666'

        if(poll_timeout is None):
            poll_timeout = 5000

        if(log_cfg is None):
            log_cfg = '../conf/logconf_stsvc.json'

        initlog(log_cfg)

        logger = logging.getLogger()

        shutdown_event = threading.Event()

        args = (shutdown_event, ctxt, stsvc_name,
                stsvc_id, discovery_addr,
                mgmt_addr, inproc_addr_list,
                inproc_shutdown_event_list,
                poll_timeout)

        stsvc_thread = threading.Thread(target=stsvc_loop, args=args)

        stsvc_thread.start()

        return stsvc_thread, shutdown_event
    except:
        logger.exception('%s : stsvc initialization failed...', func_name)


if __name__ == '__main__':
    try:
        from .stmain import stsvc_main
    except:
        from stmain import stsvc_main

    stsvc_main()
