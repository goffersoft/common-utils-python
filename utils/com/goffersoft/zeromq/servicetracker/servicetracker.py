#! /usr/bin/python

import zmq
import threading
import sys
import random
import logging
import time

from com.goffersoft.utils.uid import getuid
from com.goffersoft.utils.utils import readonly
from com.goffersoft.utils.utils import print_usage
from com.goffersoft.utils.utils import print_usage_and_exit
from com.goffersoft.utils.utils import nonBlockingRawInputUsingSelect
from com.goffersoft.utils.address import Address
from com.goffersoft.raw.raw import MsgReqRaw
from com.goffersoft.raw.raw import MsgRespRaw
from com.goffersoft.raw.raw import verify_reqmsg
from com.goffersoft.raw.raw import verify_respmsg
from com.goffersoft.raw.raw import init as initraw
from com.goffersoft.raw.rawcodes import RawRCType
from com.goffersoft.raw.rawcodes import RawRCDescrType
from com.goffersoft.logging import logconf


class _STMsgType(type):
    INIT = readonly('init')
    HELLO = readonly('hello')
    MGMT = readonly('mgmt')
    BYE = readonly('bye')


STBaseMsgType = _STMsgType('STMsgType', (object,), {})


class STMsgType(STBaseMsgType):
    @classmethod
    def is_valid(cls, msg_type, ignore_case=True):
        if(cls.is_init(msg_type, ignore_case) is True or
           cls.is_hello(msg_type, ignore_case) is True or
           cls.is_mgmt(msg_type, ignore_case) is True or
           cls.is_bye(msg_type, ignore_case) is True):
            return True
        return False

    @classmethod
    def is_init(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.INIT):
            return True

        return False

    @classmethod
    def is_hello(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.HELLO):
            return True

        return False

    @classmethod
    def is_bye(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.BYE):
            return True

        return False

    @classmethod
    def is_mgmt(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.MGMT):
            return True

        return False


class ServiceInfo:
    def __init__(self,
                 service_name,
                 service_id,
                 last_msg_type):
        self.__service_name = service_name
        self.__service_id = service_id
        self.__last_update = time.time()
        self.__last_msg_type = last_msg_type

    def get_last_msg_type(self):
        return self.__last_msg_type

    def set_last_msg_type(self, msg_type):
        self.__last_msg_type = msg_type

    def get_service_name(self):
        return self.__service_name

    def set_service_name(self, service_name):
        self.__service_name = service_name

    def get_service_id(self):
        return self.__service_id

    def set_service_id(self, service_id):
        self.__service_id = service_id

    def get_last_update_time(self):
        return self.__last_update

    def refresh_update_time(self):
        self.__last_update = time.time()

    def time_since_last_update(self):
        return (time.time() - self.__last_update)

    def __str__(self):
        return ('service_name = {0} : service_id = {1} :'
                'time_since_lastUpdate = {2} : last_msg_type = {3}'.
                format(self.__service_name,
                       self.__service_id,
                       str(time.time() - self.__last_update),
                       self.__last_msg_type))


def cmd_proc_loop(shutdown_event,
                  ctxt=None,
                  name='cmd proc',
                  id=None,
                  discovery_addr='localhost:5555',
                  mgmt_addr='localhost:6666',
                  discovery_interval=5,
                  poll_timeout=5000):
    func_name = cmd_proc_loop.__name__
    try:
        usage = """
           l : List Available Servers
           s <uuid> : Stop a Server
           e : Exit
        """
        logger = logging.getLogger()

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        cmd_proc_addr = Address(addrparts=(name, str(id)))

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting Cmd Proc Loop...'
                    '(discover_addr=%s, mgmt_addr=%s'
                    'discover_interval=%d, poll_timeout=%d)',
                    func_name,
                    th.getName(),
                    th.ident, id,
                    discovery_addr,
                    mgmt_addr,
                    discovery_interval,
                    poll_timeout)

        cmd_socket = ctxt.socket(zmq.PAIR)
        cmd_socket.bind('inproc://' + str(cmd_proc_addr))

        inproc_addr_list = (cmd_proc_addr,)
        inproc_event_list = (threading.Event(),)

        service_thread, service_shutdown_event = \
            init_service(ctxt,
                         'cmd proc service',
                         id,
                         discovery_addr,
                         mgmt_addr,
                         inproc_addr_list,
                         inproc_event_list,
                         discovery_interval,
                         poll_timeout,
                         '../../../../conf/logconf_servicecmd.json')

        print_menu = True
        valid_cmds = ('l', 's', 'e')
        while shutdown_event.is_set() is False:
            try:
                if(print_menu is True):
                    print_usage(usage)

                cmd = nonBlockingRawInputUsingSelect()
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

                msg = MsgReqRaw(body=STMsgType.MGMT+'\r\n'+cmd)
                msg.fromhdr = cmd_proc_addr
                msg.tohdr = cmd_proc_addr
                cmd_socket.send(msg.tobytes())
                if(cmd == 'l'):
                    rcvd_msg = cmd_socket.recv()
                    rcvd_msg = rcvd_msg.decode()
                    msg, reason =\
                        verify_respmsg(rcvd_msg)
                    if(reason is not None):
                        logger.info('%s : Invalid Msg=%s',
                                    func_name, reason)
                        logger.debug('%s : Msg=%r', func_name, rcvd_msg)
                    elif(msg.tohdr == cmd_proc_addr):
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
        service_shutdown_event.set()
        service_thread.join()
    except:
        logger.exception('%s : Shutting Down Cmd Processor...', func_name)
        service_shutdown_event.set()
        service_thread.join()


def service_mgr_process_msg(service_mgr_addr,
                            from_id,
                            registry,
                            in_msg):
    func_name = service_mgr_process_msg.__name__
    logger = logging.getLogger()

    msg, reason = verify_reqmsg(in_msg)

    if(reason is not None):
        logger.info('%s : Invalid Msg : %s', func_name, reason)
        logger.info('%s : Msg=%r', func_name, in_msg)
        return True, None

    if((msg.tohdr.addrparts[1] != service_mgr_addr.addrparts[1]) and
       (msg.fromhdr.addrparts[1] != from_id)):
        logger.info('%s : Message Not Authentic, Msg=%r', func_name, in_msg)
        return True, None

    retval = None
    if(STMsgType.is_mgmt(msg.msgparts[5])):
        retval, outmsg = service_mgr_process_mgmt_msg(service_mgr_addr,
                                                      registry,
                                                      msg)
    else:
        retval, outmsg = service_mgr_process_service_msg(service_mgr_addr,
                                                         registry,
                                                         msg)

    return retval, outmsg


def service_mgr_process_mgmt_msg(service_mgr_addr,
                                 registry,
                                 msg):
    func_name = service_mgr_process_mgmt_msg.__name__
    logger = logging.getLogger()

    if(msg.msgparts[6] == 'e'):
        return False, None
    elif(msg.msgparts[6] == 'l'):
        out_msg = MsgRespRaw(respid=msg.reqid,
                             respcode=RawRCType.RC_200,
                             reason=RawRCDescrType.RC_200,
                             body=service_mgr_registry_to_str(registry))
        out_msg.fromhdr = service_mgr_addr
        out_msg.tohdr = msg.fromhdr
        return True, out_msg

    return True, None


def service_mgr_process_service_msg(service_mgr_addr,
                                    registry,
                                    msg):

    func_name = service_mgr_process_service_msg.__name__
    logger = logging.getLogger()

    add = False
    purge = False
    st_msg_type = None
    out_msg = MsgRespRaw(respid=msg.reqid,
                         respcode=RawRCType.RC_200,
                         reason=RawRCDescrType.RC_200,
                         body=service_mgr_registry_to_str(registry))
    out_msg.fromhdr = service_mgr_addr
    out_msg.tohdr = msg.fromhdr

    if(STMsgType.is_init(msg.msgparts[5])):
        st_msg_type = STMsgType.INIT
        add = True
    elif(STMsgType.is_hello(msg.msgparts[5])):
        st_msg_type = STMsgType.HELLO
        add = True
    elif(STMsgType.is_bye(msg.msgparts[5])):
        st_msg_type = STMsgType.BYE
        purge = True
        out_msg = None
    else:
        out_msg = None
        logger.info('%s : Message Invalid, Msg=%s', func_name, msg.debug())

    if(purge is True):
        if(msg.fromhdr.addrparts[1] in registry.keys()):
            del registry[msg.fromhdr.addrparts[1]]

    if(add is True):
        if(msg.fromhdr.addrparts[1] in registry.keys()):
            sinfo = registry[msg.fromhdr.addrparts[1]]
            sinfo.set_service_name(msg.fromhdr.addrparts[0])
            sinfo.set_service_id(msg.fromhdr.addrparts[1])
            sinfo.set_last_msg_type(st_msg_type)
            sinfo.refresh_update_time()
        else:
            registry[msg.fromhdr.addrparts[1]] = \
                ServiceInfo(msg.fromhdr.addrparts[0],
                            msg.fromhdr.addrparts[1],
                            st_msg_type)

    return True, out_msg


def service_mgr_registry_to_str(registry):
    func_name = service_mgr_registry_to_str.__name__
    logger = logging.getLogger()
    msg = ''
    i = 1
    for sid, sinfo in registry.items():
        msg += '[' + str(i) + '] : ' + str(sinfo) + '\n'
        i += 1
    return msg


def service_mgr_update_registry(registry, ttl=60):
    func_name = service_mgr_update_registry.__name__
    logger = logging.getLogger()

    for sid, sinfo in registry.items():
        if(sinfo.time_since_last_update() >= ttl):
            del registry[sid]


def service_mgr_housekeeping(service_mgr_addr,
                             discovery_socket,
                             shutdown_event,
                             discovery_interval,
                             init=False):
    func_name = service_mgr_housekeeping.__name__
    logger = logging.getLogger()
    if(shutdown_event.is_set() is True):
        logger.info('%s : %s : %s : '
                    'Shutting Down Periodic Timer...',
                    func_name,
                    threading.current_thread().getName(),
                    threading.current_thread().ident)
        return

    msg = MsgReqRaw(body='hello')
    msg.fromhdr = service_mgr_addr
    discovery_socket.send(msg.tobytes())

    housekeeping_args = (service_mgr_addr,
                         discovery_socket,
                         shutdown_event,
                         discovery_interval)

    t = threading.Timer(discovery_interval,
                        service_mgr_housekeeping,
                        housekeeping_args)

    if(init is True):
        logger.info('%s : %s : %s : '
                    'Starting Periodic Housekeeping Timer...',
                    func_name,
                    threading.current_thread().getName(),
                    threading.current_thread().ident)

    t.start()


def service_mgr_loop(shutdown_event,
                     ctxt=None,
                     name='service mgr',
                     id=None,
                     discovery_addr='*:5555',
                     mgmt_addr='*:6666',
                     discovery_interval=5,
                     poll_timeout=5000):
    func_name = service_mgr_loop.__name__
    try:
        logger = logging.getLogger()
        registry = {}

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        service_mgr_addr = Address(addrparts=(name, str(id)))

        discovery_socket = ctxt.socket(zmq.PUB)
        mgmt_socket = ctxt.socket(zmq.ROUTER)
        discovery_socket.bind('tcp://' + str(discovery_addr))
        mgmt_socket.bind('tcp://' + str(mgmt_addr))

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting Service Manager...'
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

        service_mgr_housekeeping(service_mgr_addr,
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

                    retval, out_msg = service_mgr_process_msg(service_mgr_addr,
                                                              msgparts[0],
                                                              registry,
                                                              msg)

                    if(retval is False):
                        break

                    if(out_msg is not None):
                        out_msgparts = (msgparts[0], out_msg.tobytes())
                        mgmt_socket.send_multipart(out_msgparts)

                service_mgr_update_registry(registry)
            except KeyboardInterrupt:
                logger.exception('%s : Service Manager Exception...',
                                 func_name)
                break

        logger.info('%s : Shutting Down Service Manager...',
                    func_name)
        housekeeping_shutdown_event.set()
    except:
        logger.exception('%s : Shutting Down Service Manager...',
                         func_name)
        housekeeping_shutdown_event.set()


def service_loop(shutdown_event,
                 ctxt=None,
                 name=None,
                 id=None,
                 discovery_addr='localhost:5555',
                 mgmt_addr='localhost:6666',
                 inproc_addr_list=None,
                 inproc_shutdown_event_list=None,
                 update_interval=10,
                 poll_timeout=5000):
    func_name = service_loop.__name__
    try:
        logger = logging.getLogger()

        if(ctxt is None):
            ctxt = zmq.Context()

        if(id is None):
            id = getuid()

        if(name is None):
            name = 'Service ' + str(random.randint(1, 1000000))

        service_addr = Address(addrparts=(name, str(id)))
        filter = u''

        th = threading.current_thread()
        th.setName(name)
        logger.info('%s : %s : %s : %s : Starting Service Loop...'
                    '(discover_addr=%s, mgmt_addr=%s, '
                    'update_interval=%d, poll_timeout=%d)',
                    func_name,
                    th.getName(),
                    th.ident, id,
                    discovery_addr,
                    mgmt_addr,
                    update_interval,
                    poll_timeout)

        discovery_socket = ctxt.socket(zmq.SUB)
        discovery_socket.connect('tcp://' + discovery_addr)
        discovery_socket.setsockopt_string(zmq.SUBSCRIBE, filter)
        service_socket = ctxt.socket(zmq.DEALER)
        service_socket.setsockopt(zmq.IDENTITY, str(id).encode())
        service_socket.connect('tcp://' + mgmt_addr)
        id = getuid()

        poller = zmq.Poller()
        poller.register(service_socket, zmq.POLLIN)
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
        service_mgr_addr = None

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
                msg, reason = verify_reqmsg(rcvd_msg)
                if(reason is not None):
                    logger.info('%s : discovery socket : Invalid Msg=%r',
                                func_name, reason)
                    logger.info('%s : Msg=%r', func_name, rcvd_msg)
                else:
                    if(service_mgr_addr is None):
                        init = True
                    service_mgr_addr = msg.fromhdr

            if(service_socket in socks):
                rcvd_msg = service_socket.recv()
                rcvd_msg = rcvd_msg.decode()
                msg, reason = verify_respmsg(rcvd_msg)
                if(reason is not None):
                    logger.info('%s : service_socket : Invalid Msg=%r',
                                func_name, reason)
                    logger.info('%s : Msg=%r', func_name, rcvd_msg)
                else:
                    if((msg.fromhdr.addrparts[1] ==
                       service_mgr_addr.addrparts[1]) and
                       (msg.tohdr.addrparts[1] ==
                           service_addr.addrparts[1])):
                        if(reqid == msg.respid):
                            reqid = None
                            init = False
                            hello = False
                        elif(msg.respid in inproc_req_dict):
                            i = inproc_req_dict[msg.respid]
                            del inproc_req_dict[msg.respid]
                            if(inproc_socket_list[i] is not None):
                                msg = MsgRespRaw(respid=msg.respid,
                                                 respcode=msg.respcode,
                                                 reason=msg.reason,
                                                 body=msg.body)
                                msg.fromhdr = service_addr
                                msg.tohdr = inproc_addr_list[i]
                                inproc_socket_list[i].send(msg.tobytes())
                        else:
                            logger.info('%s : service socket : '
                                        'no matching request '
                                        'for this response, Msg=%r',
                                        func_name, rcvd_msg)
                    else:
                        if(msg.fromhdr.addrparts[1] !=
                           (service_mgr_addr.addrparts[1])):
                            service_mgr_addr = None
                        logger.info('%s : service socket : '
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
                    msg, reason = verify_reqmsg(rcvd_msg)
                    if(reason is not None):
                        logger.info('%s : inproc socket(%s) :  Invalid Msg : %r',
                                    func_name,
                                    inproc_addr_list[i],
                                    reason)
                        logger.info('%s : Msg=%r', func_name, rcvd_msg)
                    elif(service_mgr_addr is None):
                        if(inproc_socket_list[i] is not None):
                            msg = MsgRespRaw(respid=msg.reqid,
                                             respcode=RawRCType.RC_503,
                                             reason=RawRCDescrType.RC_503 +
                                             ' : Service Mgr Not Initialized')
                            msg.fromhdr = service_addr
                            msg.tohdr = inproc_addr_list[i]
                            inproc_socket.send(msg.tobytes())
                    else:
                        msg = MsgReqRaw(body=msg.body)
                        msg.fromhdr = service_addr
                        msg.tohdr = service_mgr_addr
                        inproc_req_dict[msg.reqid] = i
                        service_socket.send(msg.tobytes())
                i += 1

            if(service_mgr_addr is not None):
                num_polls += 1
                if(num_polls % 10 == 0):
                    hello = True

            if(init is True):
                if(reqid is None):
                    msg = MsgReqRaw(body=STMsgType.INIT)
                    msg.fromhdr = service_addr
                    msg.tohdr = service_mgr_addr
                    reqid = msg.reqid
                    service_socket.send(msg.tobytes())
            elif(hello is True):
                if(reqid is None):
                    msg = MsgReqRaw(body=STMsgType.HELLO)
                    msg.fromhdr = service_addr
                    msg.tohdr = service_mgr_addr
                    reqid = msg.reqid
                    service_socket.send(msg.tobytes())

            i = 0

        logger.info('%s : Shutting Down Service Loop...', func_name)
    except:
        logger.exception('%s : Shutting Down Service Loop...', func_name)


def init_cmd_proc(ctxt=None,
                  cmd_proc_name='Command Processor',
                  cmd_proc_id=None,
                  discovery_addr='localhost:5555',
                  mgmt_addr='localhost:6666',
                  discovery_interval=5,
                  poll_timeout=5000,
                  log_cfg='../../../../conf/logconf_cmdproc.json'):
    func_name = init_cmd_proc.__name__
    try:
        initraw()
        if(log_cfg is not None):
            logconf.init_logging(log_cfg)
        logger = logging.getLogger()
        shutdown_event = threading.Event()
        args = (shutdown_event, ctxt, cmd_proc_name,
                cmd_proc_id, discovery_addr,
                mgmt_addr, discovery_interval, poll_timeout)
        cmd_proc_thread = threading.Thread(target=cmd_proc_loop, args=args)
        cmd_proc_thread.start()
        return cmd_proc_thread, shutdown_event
    except:
        logger.exception('%s : Command Processor Initialization Failed...',
                         func_name)


def init_service_mgr(ctxt=None,
                     service_mgr_name='Service Manager',
                     service_mgr_id=None,
                     discovery_addr='*:5555',
                     mgmt_addr='*:6666',
                     discovery_interval=5,
                     poll_timeout=5000,
                     log_cfg='../../../../conf/logconf_servicemgr.json'):
    func_name = init_service_mgr.__name__
    try:
        initraw()
        if(log_cfg is not None):
            logconf.init_logging(log_cfg)
        logger = logging.getLogger()
        shutdown_event = threading.Event()
        args = (shutdown_event, ctxt, service_mgr_name,
                service_mgr_id, discovery_addr,
                mgmt_addr, discovery_interval, poll_timeout)
        service_mgr_thread = threading.Thread(target=service_mgr_loop,
                                              args=args)
        service_mgr_thread.start()
        return service_mgr_thread, shutdown_event
    except:
        logger.exception('%s : Service Manager Initialization Failed...',
                         func_name)


def init_service(ctxt=None,
                 service_name=None,
                 service_id=None,
                 discovery_addr='localhost:5555',
                 mgmt_addr='localhost:6666',
                 inproc_addr_list=None,
                 inproc_shutdown_event_list=None,
                 update_interval=10,
                 poll_timeout=5000,
                 log_cfg='../../../../conf/logconf_service.json'):
    func_name = init_service.__name__
    try:
        logger = logging.getLogger()
        initraw()
        if(log_cfg is not None):
            logconf.init_logging(log_cfg)
        shutdown_event = threading.Event()
        args = (shutdown_event, ctxt, service_name,
                service_id, discovery_addr,
                mgmt_addr, inproc_addr_list,
                inproc_shutdown_event_list,
                update_interval, poll_timeout)
        service_thread = threading.Thread(target=service_loop, args=args)
        service_thread.start()
        return service_thread, shutdown_event
    except:
        logger.exception('%s : Service Initialization Failed...', func_name)


if __name__ == '__main__':
    usage = """
            {0} <'service' or 'service_mgr' or 'cmd_proc' >
            """.format(sys.argv[0])

    try:
        event = None
        logger = logging.getLogger()
        ctxt = zmq.Context()

        if(len(sys.argv) != 2):
            print_usage_and_exit(usage, '**1 arg required**')

        if(sys.argv[1] == 'service'):
            t, event = init_service(ctxt)
        elif(sys.argv[1] == 'service_mgr'):
            t, event = init_service_mgr(ctxt)
        elif(sys.argv[1] == 'cmd_proc'):
            t, event = init_cmd_proc(ctxt)
        else:
            print_usage_and_exit(usage, '**bad arg**')

        while t.is_alive() is True:
            t.join(timeout=1.0)
    except:
        if(event is not None):
            logger.info('Shutting Down...')
            event.set()
            t.join()
