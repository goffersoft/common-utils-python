#! /usr/bin/python

"""This Module Contains Raw Msg Format Classes and functions
     1) get_line_separator - reutrns the configured line separator
     2) get_request_line - reutrns the configured request line
     3) get_response_line - reutrns the configured response line
     4) init - inits the msg module(customizes the
               request_line, response_line, lineseparator).
               install the message validation handler
     5) verify_reqmsg - takes as input a raw byte stream
                        and verifies if the message is
                        a request message of the raw format
                        returns 2 values -
                            a MsgReqRaw object on success
                            a reason string on failure.
     6) verify_respmsg - takes as input a raw byte stream
                         and verifies if the message is
                         a response message of the raw format
                         returns 2 values -
                            a MsgRespRaw object on success
                            a reason string on failure.
     7) verify_msg - takes as input a raw byte stream and verifies
                     if the message is a request or a response message of the
                     raw format. the function returns 2 values -
                        a MsgReqRaw or a MsgRespRaw object on success
                        a reason string on failure.
     8) verify_address - verifies if a string is of the raw address
                         format and returns 2 values -
                            a Address object on success
                            a reason string on failure.
     9) MsgReqRaw - raw message request class : derived from MsgReq
    10) MsgRespRaw - raw message resonse class : derived from MsgResp
"""

from com.goffersoft.msg.msg import Msg
from com.goffersoft.msg.msg import MsgReq
from com.goffersoft.msg.msg import MsgResp
from com.goffersoft.msg.msg import splitmsg
from com.goffersoft.msg.msg import init as initmsg
from com.goffersoft.msg.msgtype import MsgType
from rawhdr import RawMsgHdrType
from com.goffersoft.utils.address import Address
from com.goffersoft.utils.uid import is_valid_uid


class MsgReqRaw(MsgReq):
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 lineseparator=None,
                 hdrs_dict=None,
                 body=None,
                 reqline=None,
                 reqid=None):
        """ Initializes an instance of this class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) lineseparator -> string to break message into lines
                4) hdrs_dict -> list of hdrs as a dictionary
                5) body -> message body as a string
                6) reqline -> request line as a sring
                7) reqid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything)"""
        self.__reset(msg=msg,
                     msgparts=msgparts,
                     lineseparator=lineseparator,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqline=reqline,
                     reqid=reqid)

        super(MsgReqRaw, self).__init__(msg=msg,
                                        msgparts=msgparts,
                                        lineseparator=lineseparator,
                                        hdrs_dict=hdrs_dict,
                                        body=body,
                                        reqline=reqline,
                                        reqid=reqid)

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        mplist = []
        if(self.reqline is not None):
            mplist.append(self.reqline)
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

    def __reset(self,
                msg=None,
                msgparts=None,
                lineseparator='\r\n',
                hdrs_dict=None,
                body=None,
                reqline=None,
                reqid=None):
        """ internal funtion to reset the object to its initial state """
        pass

    def reset(self,
              msg=None,
              msgparts=None,
              lineseparator='\r\n',
              hdrs_dict=None,
              body=None,
              reqline=None,
              reqid=None):
        """ resets the object to its initial state """
        self.__reset(msg=msg,
                     msgparts=msgparts,
                     lineseparator=lineseparator,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqline=reqline,
                     reqid=reqid)

        super(MsgReqRaw, self).reset(msg=msg,
                                     msgparts=msgparts,
                                     lineseparator=lineseparator,
                                     hdrs_dict=hdrs_dict,
                                     body=body,
                                     reqline=reqline,
                                     reqid=reqid)

    def update_msgparts(self):
        return self.__update_msgparts()

    @property
    def fromhdr(self):
        """ from addr getter method """
        if(RawMsgHdrType.FROM in self.hdrs):
            return self.hdrs[RawMsgHdrType.FROM]
        else:
            return None

    @fromhdr.setter
    def fromhdr(self, addr):
        """ from addr setter method """
        if(addr is None):
            self.delhdr(RawMsgHdrType.FROM)
        else:
            self.addhdr(RawMsgHdrType.FROM, addr)

    @property
    def tohdr(self):
        """ to addr getter method """
        if(RawMsgHdrType.TO in self.hdrs):
            return self.hdrs[RawMsgHdrType.TO]
        else:
            return None

    @tohdr.setter
    def tohdr(self, addr):
        """ to addr setter method """
        if(addr is None):
            self.delhdr(RawMsgHdrType.TO)
        else:
            self.addhdr(RawMsgHdrType.TO, addr)


class MsgRespRaw(MsgResp):
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 lineseparator=None,
                 respcode=None,
                 reason=None,
                 hdrs_dict=None,
                 body=None,
                 respline=None,
                 respid=None):
        """ Initializes an instance of this class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) lineseparator -> string to break message into lines
                4) respcode -> response code as a string (MsgType.RESP only)
                5) reason -> descriptive text indicating reason for
                   success/failure
                6) hdrs_dict -> list of hdrs as a dictionary
                7) body -> message body as a string
                8) respline -> response line (MsgType.RESP only) as a sring
                9) respid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything --> MsgType.RESP only)"""
        self.__reset(msg=msg,
                     msgparts=msgparts,
                     lineseparator=lineseparator,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     respcode=respcode,
                     reason=reason,
                     respline=respline,
                     respid=respid)

        super(MsgRespRaw, self).__init__(msg=msg,
                                         msgparts=msgparts,
                                         lineseparator=lineseparator,
                                         hdrs_dict=hdrs_dict,
                                         body=body,
                                         respcode=respcode,
                                         reason=reason,
                                         respline=respline,
                                         respid=respid)

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        mplist = []
        if(self.respline is not None):
            mplist.append(self.respline)
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

    def __reset(self,
                msg=None,
                msgparts=None,
                lineseparator='\r\n',
                respcode=None,
                reason=None,
                hdrs_dict=None,
                body=None,
                respline=None,
                respid=None):
        """ internal funtion to reset the object to its initial state """
        pass

    def reset(self,
              msg=None,
              msgparts=None,
              lineseparator='\r\n',
              respcode=None,
              reason=None,
              hdrs_dict=None,
              body=None,
              respline=None,
              respid=None):
        """ resets the object to its initial state """
        self.__reset(msg=msg,
                     msgparts=msgparts,
                     lineseparator=lineseparator,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     respcode=respcode,
                     reason=reason,
                     respline=respline,
                     respid=respid)

        super(MsgRespRaw, self).reset(msg=msg,
                                      msgparts=msgparts,
                                      lineseparator=lineseparator,
                                      hdrs_dict=hdrs_dict,
                                      body=body,
                                      respcode=respcode,
                                      reason=reason,
                                      respline=respline,
                                      respid=respid)

    def update_msgparts(self):
        return self.__update_msgparts()

    @property
    def fromhdr(self):
        """ from addr getter method """
        if(RawMsgHdrType.FROM in self.hdrs):
            return self.hdrs[RawMsgHdrType.FROM]
        else:
            return None

    @fromhdr.setter
    def fromhdr(self, addr):
        """ from addr setter method """
        if(addr is None):
            self.delhdr(RawMsgHdrType.FROM)
        else:
            self.addhdr(RawMsgHdrType.FROM, addr)

    @property
    def tohdr(self):
        """ to addr getter method """
        if(RawMsgHdrType.TO in self.hdrs):
            return self.hdrs[RawMsgHdrType.TO]
        else:
            return None

    @tohdr.setter
    def tohdr(self, addr):
        """ to addr setter method """
        if(addr is None):
            self.delhdr(RawMsgHdrType.TO)
        else:
            self.addhdr(RawMsgHdrType.TO, addr)


def verify_address(addr):
    """ verifies if a string is of the raw address format
        and returns 2 values -
           a Address object on success
           a reason string on failure."""
    if(addr is None):
        return None, 'Invalid Address : addr == None'

    address = Address(addr=addr, fieldseparator=':')

    addrparts = address.addrparts

    if(len(addrparts) != 2):
        return None, 'Invalid Address : expected <name>:<uuid4>'

    if(is_valid_uid(addrparts[1]) is False):
        return None, 'Invalid Address : Invalid UUID4'

    return address, None


def verify_msg(msgstr, reqtype=None):
    """takes as input a raw byte stream and verifies
      if the message is a request or a response message of the
      raw format. the function returns 2 values -
         a MsgReqRaw or a MsgRespRaw object on success
         a reason string on failure."""
    msg = None

    if(msgstr is None):
        return msg, 'Invalid Message : msgstr == None'

    if(msgstr == ''):
        return msg, 'Invalid Message : Empty Message'

    if((reqtype is not None and reqtype == MsgType.REQ) or
       (reqtype is None and msgstr.startswith(get_request_line()) is True)):
        msg, reason = verify_reqmsg(msgstr, False)
    elif((reqtype is not None and reqtype == MsgType.RESP) or
         (reqtype is None and msgstr.startswith(get_response_line()) is True)):
        msg, reason = verify_respmsg(msgstr, False)
    elif (reqtype is not None):
        reason = 'Invalid Message Type : ' + msgtype
    else:
        reason = 'Invalid Message : No Request/Response Line'

    return msg, reason


def verify_respmsg(msgstr, verify_response_line=True):
    """takes as input a raw byte stream
       and verifies if the message is
       a response message of the raw format
       returns 2 values -
         a MsgRespRaw object on success
         a reason string on failure."""
    if(msgstr is None):
        return None, 'Invalid Response Message : msg == None'

    msgparts = splitmsg(msgstr)

    if(len(msgparts) < 3):
        return None, \
            'Invalid Response Message : too few message parts : expected : \
             <res-line><rep-id><from>>'

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
        hdrs[RawMsgHdrType.FROM] = from_addr

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
            hdrs[RawMsgHdrType.TO] = to_addr

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

    msg = MsgRespRaw(msg=msgstr,
                     respline=msgparts[0],
                     respid=msgparts[1],
                     msgparts=msgparts,
                     hdrs_dict=hdrs,
                     body=body,
                     respcode=respcode,
                     reason=reason)

    return msg, None


def verify_reqmsg(msgstr, verify_request_line=True):
    """takes as input a raw byte stream
       and verifies if the message is
       a request message of the raw format
       returns 2 values -
           a MsgReqRaw object on success
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
        hdrs[RawMsgHdrType.FROM] = from_addr

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
            hdrs[RawMsgHdrType.TO] = to_addr

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

    msg = MsgReqRaw(msg=msgstr,
                    reqline=msgparts[0],
                    reqid=msgparts[1],
                    body=body,
                    msgparts=msgparts,
                    hdrs_dict=hdrs)

    return msg, None


def get_request_line():
    """request line"""
    return 'Raw Request Message : Version 1.0'


def get_response_line():
    """response line"""
    return 'Raw Response Message : Version 1.0'


def get_line_separator():
    """line separator"""
    return '\r\n'


def init(validate_handler=verify_msg,
         request_line=None,
         response_line=None,
         line_separator=None):
    """inits the raw module. customizes the
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

    initmsg(validate_handler,
            request_line,
            response_line,
            line_separator)


if __name__ == '__main__':
    from com.goffersoft.utils.uid import getuid
    from com.goffersoft.msg.msgfac import get_req_msg_validation_handler
    from com.goffersoft.msg.msgfac import print_registry
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    init()
    print_registry(logger)
    print_registry()

    mreq = MsgReqRaw(body='Hello')
    mreq.fromhdr = Address(addrparts=(('a', getuid())))

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

    mresp = MsgRespRaw(msg='World')
    print('2-->%r' % str(mresp))

    init(request_line='Hello',
         response_line='world')

    mreq = MsgReqRaw(msg='Hello')
    mresp = MsgRespRaw(msg='World')

    print('3-->%r' % str(mreq))
    print('4-->%r' % str(mresp))

    init(line_separator='\n')

    mreq = MsgReqRaw(msg='Hello')
    mresp = MsgRespRaw(msg='World')

    print('5-->%r' % str(mreq))
    print('6-->%r' % str(mresp))

    print('resetting...')
    mreq.reset()
    mresp.reset()
    print(mreq.debug())
    print(mresp.debug())
