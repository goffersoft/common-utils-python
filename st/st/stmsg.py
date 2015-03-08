#! /usr/bin/python

"""This Module Contains Service Tracker Msg Format Classes and functions
     1) get_line_separator - reutrns the configured line separator
     2) get_request_line - reutrns the configured request line
     3) get_response_line - reutrns the configured response line
     4) init - inits the msg module(customizes the
               request_line, response_line, lineseparator).
               install the message validation handler
     5) verify_msg - takes as input a raw byte stream and verifies
                     if the message is a request or a response message of the
                     service tracker message format. the function returns
                     2 values -
                        a STMsgReq or a STMsgResp object on success
                        a reason string on failure.
     6) verify_address - verifies if a string is of the service tracker address
                         format and returns 2 values -
                            a STAddress object on success
                            a reason string on failure.
     7) STMsgReq - service tracker message request class : derived from MsgReq
     8) STMsgResp - service tracker message resonse class : derived
                    from MsgResp
"""

from msg.msgctxt import MsgCtxt
from msg.msg import Msg
from msg.msg import MsgReq
from msg.msg import MsgResp
from msg.msg import splitmsg
from msg.msg import init as initmsg
from msg.msgtype import MsgType
from msg.msgfac import register
from utils.uid import is_valid_uid

try:
    from .stmsghdr import STMsgHdrType
    from .staddr import STAddress
    from .stmsgtype import STMsgType
except:
    from stmsghdr import STMsgHdrType
    from staddr import STAddress
    from stmsgtype import STMsgType


class STMsgReq(MsgReq):
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 hdrs_dict=None,
                 body=None,
                 reqid=None,
                 msgctxt=None):
        """ Initializes an instance of this class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) hdrs_dict -> list of hdrs as a dictionary
                4) body -> message body as a string
                5) reqid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything)
                6) msgctxt -> message context"""
        super(STMsgReq, self).__init__(msg=msg,
                                       msgparts=msgparts,
                                       hdrs_dict=hdrs_dict,
                                       body=body,
                                       reqid=reqid,
                                       msgctxt=msgctxt)

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        mplist = []
        if(self._msgctxt.reqline is not None):
            mplist.append(self._msgctxt.reqline)
        if(self.reqid is not None):
            mplist.append(self.reqid)
        if(self.fromhdr is not None):
            mplist.append(str(self.fromhdr))
        if(self.tohdr is not None):
            mplist.append(str(self.tohdr))
        mplist.append('')
        if(self.body is not None):
            mplist.append(str(self.body))
        return tuple(mplist)

    def update_msgparts(self):
        return self.__update_msgparts()

    @property
    def fromhdr(self):
        """ from addr getter method """
        if(STMsgHdrType.FROM in self.hdrs):
            return self.hdrs[STMsgHdrType.FROM]
        else:
            return None

    @fromhdr.setter
    def fromhdr(self, addr):
        """ from addr setter method """
        if(addr is None):
            self.delhdr(STMsgHdrType.FROM)
        else:
            self.addhdr(STMsgHdrType.FROM, addr)

    @property
    def tohdr(self):
        """ to addr getter method """
        if(STMsgHdrType.TO in self.hdrs):
            return self.hdrs[STMsgHdrType.TO]
        else:
            return None

    @tohdr.setter
    def tohdr(self, addr):
        """ to addr setter method """
        if(addr is None):
            self.delhdr(STMsgHdrType.TO)
        else:
            self.addhdr(STMsgHdrType.TO, addr)

    def is_mgmt(self):
        """ determines if msg if of type MGMT"""
        if(STMsgType.is_mgmt(self.msgparts[5])):
            return True
        else:
            return False

    def is_hello(self):
        """ determines if msg if of type HELLO"""
        if(STMsgType.is_hello(self.msgparts[5])):
            return True
        else:
            return False

    def is_init(self):
        """ determines if msg if of type INIT"""
        if(STMsgType.is_init(self.msgparts[5])):
            return True
        else:
            return False

    def is_bye(self):
        """ determines if msg if of type BYE"""
        if(STMsgType.is_bye(self.msgparts[5])):
            return True
        else:
            return False

    @classmethod
    def verify_msg(cls, msgstr, verify_request_line=True):
        """takes as input a raw byte stream
           and verifies if the message is
           a request message of the service tracker message format
           returns 2 values -
               a STMsgReq object on success
               a reason string on failure."""

        if(msgstr is None):
            return None, 'Invalid Request Message : msgstr == None'

        msgparts = splitmsg(msgstr)

        if(len(msgparts) < 3):
            return None, \
                'Invalid Request Message : too few message parts : expected : \
                 <req-line>:<id>:<from_addr>'

        if(verify_request_line is True):
            if(msgparts[0] != get_request_line()):
                return None, \
                    'Invalid Request Message : Malformed Request Line'

        from_addr, reason = verify_address(msgparts[2])

        hdrs = {}

        if(from_addr is None):
            return None, \
                'Invalid Request Message : Invalid From Address : ' + reason
        else:
            hdrs[STMsgHdrType.FROM] = from_addr

        to_addr = None
        body_index = 4
        if((len(msgparts) >= 4) and
           (msgparts[3] != '')):
            to_addr, reason = verify_address(msgparts[3])
            if(to_addr is None):
                return None, \
                    'Invalid Request Message : Invalid To Address : ' + reason
            else:
                body_index = 5
                hdrs[STMsgHdrType.TO] = to_addr

        if((to_addr is not None) and
           (len(msgparts) >= 5) and
           (msgparts[4] != '')):
                return None, \
                    'Invalid Request Message : Malformed Message'

        body = None
        if(len(msgparts) > body_index):
            body = ''
            for b in msgparts[body_index:]:
                body += str(b) + get_line_separator()

        msg = STMsgReq(msg=msgstr,
                       reqid=msgparts[1],
                       body=body,
                       msgparts=msgparts,
                       hdrs_dict=hdrs)

        return msg, None


class STMsgResp(MsgResp):
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 respcode=None,
                 reason=None,
                 hdrs_dict=None,
                 body=None,
                 respid=None,
                 msgctxt=None):
        """ Initializes an instance of this class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) respcode -> response code as a string (MsgType.RESP only)
                4) reason -> descriptive text indicating reason for
                   success/failure
                5) hdrs_dict -> list of hdrs as a dictionary
                6) body -> message body as a string
                7) respid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything --> MsgType.RESP only)
                8) msgctxt -> Message Context"""
        super(STMsgResp, self).__init__(msg=msg,
                                        msgparts=msgparts,
                                        hdrs_dict=hdrs_dict,
                                        body=body,
                                        respcode=respcode,
                                        reason=reason,
                                        respid=respid,
                                        msgctxt=msgctxt)

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        mplist = []
        if(self._msgctxt.respline is not None):
            mplist.append(self._msgctxt.respline)
        if(self.respid is not None):
            mplist.append(self.respid)
        if(self.fromhdr is not None):
            mplist.append(str(self.fromhdr))
        if(self.tohdr is not None):
            mplist.append(str(self.tohdr))
        mplist.append('')
        if(self.respcode is not None):
            mplist.append(str(self.respcode))
        if(self.reason is not None):
            mplist.append(str(self.reason))
        if(self.body is not None):
            mplist.append(str(self.body))
        return tuple(mplist)

        super(STMsgResp, self).reset(msg=msg,
                                     msgparts=msgparts,
                                     hdrs_dict=hdrs_dict,
                                     body=body,
                                     respcode=respcode,
                                     reason=reason,
                                     respid=respid)

    def update_msgparts(self):
        return self.__update_msgparts()

    @property
    def fromhdr(self):
        """ from addr getter method """
        if(STMsgHdrType.FROM in self.hdrs):
            return self.hdrs[STMsgHdrType.FROM]
        else:
            return None

    @fromhdr.setter
    def fromhdr(self, addr):
        """ from addr setter method """
        if(addr is None):
            self.delhdr(STMsgHdrType.FROM)
        else:
            self.addhdr(STMsgHdrType.FROM, addr)

    @property
    def tohdr(self):
        """ to addr getter method """
        if(STMsgHdrType.TO in self.hdrs):
            return self.hdrs[STMsgHdrType.TO]
        else:
            return None

    @tohdr.setter
    def tohdr(self, addr):
        """ to addr setter method """
        if(addr is None):
            self.delhdr(STMsgHdrType.TO)
        else:
            self.addhdr(STMsgHdrType.TO, addr)

    @classmethod
    def verify_msg(cls, msgstr, verify_response_line=True):
        """takes as input a raw byte stream
           and verifies if the message is
           a response message of the service tracker message format
           returns 2 values -
             a STMsgResp object on success
             a reason string on failure."""
        if(msgstr is None):
            return None, 'Invalid Response Message : msg == None'

        msgparts = splitmsg(msgstr)

        if(len(msgparts) < 3):
            return None, \
                'Invalid Response Message : too few message parts : \
                 expected : <res-line><rep-id><from>>'

        if(verify_response_line is True):
            if(msgparts[0] != get_response_line()):
                return None, \
                    'Invalid Response Message : Malformed Response Line'

        hdrs = {}

        from_addr = None
        from_addr, reason = verify_address(msgparts[2])
        if(from_addr is None):
            return None, \
                'Invalid Response Message : Invalid From Address : ' + reason
        else:
            hdrs[STMsgHdrType.FROM] = from_addr

        to_addr = None
        respcode_index = 4
        reason_index = 5
        body_index = 6
        if((len(msgparts) >= 4) and
           (msgparts[3] != '')):
            to_addr, reason = verify_address(msgparts[3])
            if(to_addr is None):
                return None, \
                    'Invalid Response Message : Invalid To Address : ' + reason
            else:
                respcode_index = 5
                reason_index = 6
                body_index = 7
                hdrs[STMsgHdrType.TO] = to_addr

        if((from_addr is not None) and
           (to_addr is not None) and
           (len(msgparts) >= 5) and
           (msgparts[4] != '')):
                return None, \
                    'Invalid Response Message : Malformed Message'

        respcode = None
        reason = None
        body = None
        if(len(msgparts) > respcode_index):
            respcode = msgparts[respcode_index]
            if(len(msgparts) > reason_index):
                reason = msgparts[reason_index]
                if(len(msgparts) > body_index):
                    body = ''
                    for b in msgparts[body_index:]:
                        body += str(b) + get_line_separator()

        msg = STMsgResp(msg=msgstr,
                        respid=msgparts[1],
                        msgparts=msgparts,
                        hdrs_dict=hdrs,
                        body=body,
                        respcode=respcode,
                        reason=reason)

        return msg, None


def verify_address(addr):
    """ verifies if a string is of the service tracker address format
        and returns 2 values -
           a STAddress object on success
           a reason string on failure."""
    if(addr is None):
        return None, 'Invalid Address : addr == None'

    try:
        address = STAddress(addr=addr)
    except ValueError as reason:
        return None, reason.args[0]

    if(is_valid_uid(address.id) is False):
        return None, 'Invalid Address : Invalid UUID4'

    return address, None


def verify_msg(msgstr, reqtype=None):
    """takes as input a raw byte stream and verifies
      if the message is a request or a response message of the
      service tracker message format. the function returns 2 values -
         a STMsgReq or a STMsgResp object on success
         a reason string on failure."""
    msg = None

    if(msgstr is None):
        return msg, 'Invalid Message : msgstr == None'

    if(msgstr == ''):
        return msg, 'Invalid Message : Empty Message'

    if((reqtype is not None and reqtype == MsgType.REQ) or
       (reqtype is None and msgstr.startswith(get_request_line()) is True)):
        msg, reason = STMsgReq.verify_msg(msgstr, False)
    elif((reqtype is not None and reqtype == MsgType.RESP) or
         (reqtype is None and msgstr.startswith(get_response_line()) is True)):
        msg, reason = StMsgResp.verify_msg(msgstr, False)
    elif (reqtype is not None):
        reason = 'Invalid Message Type : ' + msgtype
    else:
        reason = 'Invalid Message : No Request/Response Line'

    return msg, reason


def get_request_line():
    """request line"""
    return 'Service Tracker Request Message : Version 1.0'


def get_response_line():
    """response line"""
    return 'Service Tracker Response Message : Version 1.0'


def get_line_separator():
    """line separator"""
    return '\r\n'


def init(validate_handler=verify_msg,
         request_line=None,
         response_line=None,
         line_separator=None):
    """inits the service tracker messgage module. customizes the
       1) request line
       2) response line
       3) line separator
       4) registers the message validation
          handler with the msgfac module using the
          register function"""
    if(request_line is None):
        request_line = get_request_line()

    if(response_line is None):
        response_line = get_response_line()

    if(line_separator is None):
        line_separator = get_line_separator()

    initmsg(MsgCtxt(linesep=line_separator,
                    reqline=request_line,
                    respline=response_line))

    register(req_msg_starts_with=request_line,
             resp_msg_starts_with=response_line,
             msg_validation_handler=validate_handler)


if __name__ == '__main__':
    from utils.uid import getuid
    from msg.msgfac import get_req_msg_validation_handler
    from msg.msgfac import print_registry
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    init()
    print_registry(logger)
    print_registry()

    mreq = STMsgReq(body='Hello')
    mreq.fromhdr = STAddress(addrparts=(('a', getuid())))
    print(mreq.debug())

    msgstr = str(mreq)

    msg_handler = get_req_msg_validation_handler(msgstr)

    msg, reason = msg_handler(msgstr, MsgType.REQ)

    if(reason is not None):
        print(reason)

    print(msg.debug())

    msgstr1 = str(msg)

    print('1-->%r' % msgstr)
    print('1a-->%r' % msgstr1)

    if(msgstr == msgstr1):
        print('Message Validation Test passed')
    else:
        print('Message Validation Test failed')

    mresp = STMsgResp(msg='World')
    print('2-->%r' % str(mresp))

    init(request_line='Hello',
         response_line='world')

    mreq = STMsgReq(msg='Hello')
    mresp = STMsgResp(msg='World')

    print('3-->%r' % str(mreq))
    print('4-->%r' % str(mresp))

    init(line_separator='\n')

    mreq = STMsgReq(msg='Hello')
    mresp = STMsgResp(msg='World')

    print('5-->%r' % str(mreq))
    print('6-->%r' % str(mresp))

    print('resetting...')
    mreq.reset()
    mresp.reset()
    print(mreq.debug())
    print(mresp.debug())
