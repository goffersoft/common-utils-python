#! /usr/bin/python

"""This Module Contains Msg Base Class
   This is an abstract class whose
   methods will be overridden by
   derived classes customized to
   different msg formats
   This module contains the following functions and classes
     1) _get_line_separator - default line separator
     2) get_line_separator - reutrns the configured line separator
     3) _get_request_line - default request line
     4) get_request_line - reutrns the configured request line
     5) _get_response_line - default response line
     6) get_response_line - reutrns the configured response line
     7) _wrap_func - internal function to customize above functions
     8) init - inits the msg module(customizes the
               request_line, response_line, lineseparator).
               install the message validation handler
     9) splitmsg - splits the message into parts (tuple) using
                   the linseparator as the delimiter
    10) Msg - Base class of all message formats
    11) MsgReq - Base class of all message request formats
    12) MsgResp - Base class of all message response formats
"""

from msgtype import MsgType
from msgfac import register
from com.goffersoft.utils.uid import getuid


def _get_line_separator():
    """ default line separator"""
    return '\r\n'


def _get_request_line():
    """ default request line"""
    return 'Generic Request Message : Version 1.0'


def _get_response_line():
    """ default response line"""
    return 'Generic Response Message : Version 1.0'


def get_line_separator():
    """line separator"""
    return _get_line_separator()


def get_request_line():
    """request line"""
    return _get_request_line()


def get_response_line():
    """response line"""
    return _get_response_line()


def _wrap_func(str):
    """wraps 'str' and returns new fucntion"""
    def func():
        return str
    return func


def init(validate_handler,
         request_line=None,
         response_line=None,
         line_separator=None):
    """inits the msg module. customizes the
       1) request line
       2) response line
       3) line separator
       4) registers the message validation
          handler with the msgfac module using the
          register function"""
    global get_request_line
    global get_response_line
    global get_line_separator

    if(request_line is None):
        get_request_line = _get_request_line
    else:
        get_request_line = _wrap_func(request_line)
    get_request_line.__name__ = 'get_request_line'

    if(response_line is None):
        get_response_line = _get_response_line
    else:
        get_response_line = _wrap_func(response_line)
    get_response_line.__name__ = 'get_response_line'

    if(line_separator is None):
        get_line_separator = _get_line_separator
    else:
        get_line_separator = _wrap_func(line_separator)
    get_line_separator.__name__ = 'get_line_separator'

    register(get_request_line(),
             get_response_line(),
             validate_handler)


def splitmsg(msg,
             lineseparator=None):
    """helper function to split a message to parts
       (tuple) using the line separator as the
       delimiter"""
    if msg is None:
        return ''

    if lineseparator is None:
        lineseparator = get_line_separator()

    return msg.split(lineseparator)


class Msg(object):
    """ The Base Class For all
        Message Formats
        Assummption :
            Messages are broken into lines
            lines are delineated by lineseparator
            First Line is a request or a response line
            the rest of the message is typically group
            into headers and a body but need not be. The
            actual format is determined by the derviced
            classes.
    """
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 type=None,
                 lineseparator=None,
                 hdrs_dict=None,
                 body=None,
                 reqline=None,
                 reqid=None,
                 respcode=None,
                 reason=None,
                 respline=None,
                 respid=None):
        """ Initializes an instance of the base class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) type -> msgtype.MsgType (REQ or RESP)
                4) lineseparator -> string to break message into lines
                5) hdrs_dict -> list of hdrs as a dictionary
                6) body -> message body as a string
                7) reqline -> requent line (MsgType.REQ only) as a sring
                8) reqid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything)
                9) respcode -> response code as a string (MsgType.RESP only)
               10) reason -> descriptive text indicating reason
                   for success/failure
               11) respline -> response line (MsgType.RESP only) as a sring
               12) respid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything --> MsgType.RESP only)
        """
        self.__reset(lineseparator=lineseparator,
                     msg=msg,
                     msgparts=msgparts,
                     type=type,
                     respcode=respcode,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqline=reqline,
                     respline=respline,
                     reqid=reqid,
                     respid=respid,
                     reason=reason)

    def __update_msg(self):
        """ internal funtion to update 'msg' """
        if(self.__linesep is not None and
           self.__msg is None and
           self.__msgparts is not None):
            self.__msg = ''
            for m in self.__msgparts:
                self.__msg += str(m) + self.__linesep
        return self.__msg

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        if(self.__linesep is not None and
           self.__msgparts is None and
           self.__msg is not None):
            self.__msgparts = self.__msg.split(self.__linesep)
        return self.__msgparts

    def __reset(self,
                msg=None,
                msgparts=None,
                type=None,
                lineseparator=None,
                hdrs_dict=None,
                body=None,
                reqline=None,
                reqid=None,
                respcode=None,
                reason=None,
                respline=None,
                respid=None):
        """ internal funtion to reset the object to its initial state """
        self.__linesep = lineseparator
        self.__msg = msg
        self.__msgparts = msgparts
        self.__type = type
        self.__respcode = respcode
        self.__hdrs = hdrs_dict
        self.__body = body
        self.__reqline = reqline
        self.__respline = respline
        self.__reqid = reqid
        self.__respid = respid
        self.__reason = reason

        if(hdrs_dict is None):
            self.__hdrs = {}

        if(lineseparator is None):
            self.__linesep = get_line_separator()

        self.update_msg()
        self.update_msgparts()

    def reset(self,
              msg=None,
              msgparts=None,
              type=None,
              lineseparator=None,
              hdrs_dict=None,
              body=None,
              reqline=None,
              reqid=None,
              respcode=None,
              reason=None,
              respline=None,
              respid=None):
        """ resets the object to its initial state """
        self.__reset(lineseparator=lineseparator,
                     msg=msg,
                     msgparts=msgparts,
                     type=type,
                     respcode=respcode,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqline=reqline,
                     respline=respline,
                     reqid=reqid,
                     respid=respid)

    def update_msg(self):
        """---> Maybe override in derived class <---"""
        return self.__update_msg()

    def update_msgparts(self):
        """ ---> Must override in derived class <---"""
        return self.__update_msgparts()

    @property
    def lineseparator(self):
        """ lineseparator getter method """
        return self.__linesep

    @lineseparator.setter
    def lineseparator(self, linesep):
        """ lineseparator setter method """
        if(self.__linesep != linesep):
            self.__linesep = linesep
            self.__msg = None

    @property
    def msg(self):
        """ msg getter method """
        if(self.__msg is None):
            if(self.__msgparts is None):
                self.__msgparts = self.update_msgparts()
            self.__msg = self.update_msg()
        return self.__msg

    @msg.setter
    def msg(self, msg):
        """ msg setter method """
        if(msg != self.__msg):
            self.__msg = msg
            self.__msgparts = None
            self.update_msgparts()

    @property
    def msgparts(self):
        """ msgparts getter method """
        if(self.__msgparts is None):
            self.__msgparts = self.update_msgparts()
        return self.__msgparts

    @msgparts.setter
    def msgparts(self, msgparts):
        """ msgparts setter method """
        if(msgparts != self.__msgparts):
            self.__msgparts = msgparts
            self.__msg = None
            self.update_msg()

    @property
    def type(self):
        """ msgtype getter method """
        return self.__type

    @type.setter
    def type(self, type):
        """ msgtype setter method """
        if(isinstance(type, MsgType) is False):
            raise(TypeError,
                  'Expected argument to be of type MsgType')

        if(self.__type != type):
            self.msg = None
            self.msgparts = None
            self.__type = type

    @property
    def respcode(self):
        """ response code getter method """
        return self.__respcode

    @respcode.setter
    def respcode(self, respcode):
        """ response code setter method """
        if((respcode is not None) and
           (self.__respcode != respcode)):
            self.msg = None
            self.msgparts = None
            self.__respcode = respcode

    @property
    def reason(self):
        """ reason code getter method """
        return self.__reason

    @reason.setter
    def reason(self, reason):
        """ reason code setter method """
        if((reason is not None) and
           (self.__reason != reason)):
            self.msg = None
            self.msgparts = None
            self.__reason = reason

    @property
    def hdrs(self):
        """ hdrs getter method """
        return self.__hdrs

    def addhdr(self, key, value):
        """ add a hdr (key, value) to hdrs"""
        if(key is not None):
            if(self.__hdrs is None):
                self.__hdrs = {}
            self.__hdrs[key] = value
            self.msg = None
            self.msgparts = None

    def delhdr(self, key):
        """ delete a hdr (key) from hdrs"""
        if((key is not None) and
           (key in self.__hdrs)):
            del self.__hdrs[key]
            self.msg = None
            self.msgparts = None

    @hdrs.setter
    def hdrs(self, hdrs):
        """ hdrs setter method """
        if((hdrs is not None) and
           (self.__hdrs != hdrs)):
            self.msg = None
            self.msgparts = None
            self.__hdrs = hdrs

    @property
    def body(self):
        """ body getter method """
        return self.__body

    @body.setter
    def body(self, body):
        """ body setter method """
        if((body is not None) and
           (self.__body != body)):
            self.msg = None
            self.msgparts = None
            self.__body = body

    @property
    def reqline(self):
        """ reqline getter method """
        return self.__reqline

    @reqline.setter
    def reqline(self, reqline):
        """ reqline setter method """
        if((reqline is not None) and
           (self.__reqline != reqline)):
            self.msg = None
            self.msgparts = None
            self.__reqline = reqline

    @property
    def respline(self):
        """ response line getter method """
        return self.__respline

    @respline.setter
    def respline(self, respline):
        """ response line setter method """
        if((respline is not None) and
           (self.__respline != respline)):
            self.msg = None
            self.msgparts = None
            self.__respline = respline

    @property
    def reqid(self):
        """ request id getter method """
        return self.__reqid

    @reqid.setter
    def reqid(self, id):
        """ request id setter method """
        if(id is None):
            id = str(getuid())

        if(self.__reqid != id):
            self.msg = None
            self.msgparts = None
            self.__reqid = id

    @property
    def respid(self):
        """ response id getter method """
        return self.__respid

    @respid.setter
    def respid(self, id):
        """ response id setter method """
        if(id is None):
            id = str(getuid())

        if(self.__respid != id):
            self.msg = None
            self.msgparts = None
            self.__respid = id

    def tostr(self):
        """ return msg as a string """
        return self.msg

    def tobytes(self):
        """ return msg as bytes """
        if(self.msg is not None):
            return self.msg.encode()
        return None

    def __repr__(self):
        return self.tostr()

    def debug(self):
        """ return instance data as a string """
        return ('type=%s\nmsg=%r\nmsgparts=%s\n'
                'hdrs=%s\nbody=%r\n'
                'lineseparator=%r\n'
                'reqline=%s\n'
                'reqid=%s\n'
                'respcode=%s\n'
                'reason=%s\n'
                'respline=%s\n'
                'respid=%s\n'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.lineseparator,
                   self.reqline,
                   self.reqid,
                   self.respcode,
                   self.reason,
                   self.respline,
                   self.respid))


class MsgReq(Msg):
    """ The Base Class For all
        Message Request Formats
    """
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 lineseparator='\r\n',
                 hdrs_dict=None,
                 body=None,
                 reqline=None,
                 reqid=None):
        """ inits the object - see base class for more comments"""
        reqid, reqline =\
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         lineseparator=lineseparator,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         reqline=reqline,
                         reqid=reqid)

        super(MsgReq, self).__init__(type=MsgType.REQ,
                                     msg=msg,
                                     msgparts=msgparts,
                                     lineseparator=lineseparator,
                                     hdrs_dict=hdrs_dict,
                                     body=body,
                                     reqline=reqline,
                                     reqid=reqid)

    def __reset(self,
                msg=None,
                msgparts=None,
                lineseparator='\r\n',
                hdrs_dict=None,
                body=None,
                reqline=None,
                reqid=None):
        """ internal function to reset the object to its initial state"""
        if(reqid is None):
            reqid = str(getuid())

        if(reqline is None):
            reqline = get_request_line()

        return reqid, reqline

    def reset(self,
              msg=None,
              msgparts=None,
              lineseparator='\r\n',
              hdrs_dict=None,
              body=None,
              reqline=None,
              reqid=None):
        """ resets the object to its initial state"""
        reqid, reqline =\
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         lineseparator=lineseparator,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         reqline=reqline,
                         reqid=reqid)

        super(MsgReq, self).reset(type=MsgType.REQ,
                                  msg=msg,
                                  msgparts=msgparts,
                                  lineseparator=lineseparator,
                                  hdrs_dict=hdrs_dict,
                                  body=body,
                                  reqline=reqline,
                                  reqid=reqid)

    def debug(self):
        """ return instance data as a string """
        return ('type=%s\nmsg=%r\nmsgparts=%s\n'
                'hdrs=%s\nbody=%r\n'
                'lineseparator=%r\n'
                'reqline=%r\n'
                'reqid=%s\n'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.lineseparator,
                   self.reqline,
                   self.reqid))


class MsgResp(Msg):
    """ The Base Class For all
        Message Response Formats
    """
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 lineseparator='\r\n',
                 respcode=None,
                 reason=None,
                 hdrs_dict=None,
                 body=None,
                 respline=None,
                 respid=None):
        """ inits the object - see base class for more comments"""
        respid, respline = \
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         lineseparator=lineseparator,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         respcode=respcode,
                         reason=reason,
                         respline=respline,
                         respid=respid)

        super(MsgResp, self).__init__(type=MsgType.RESP,
                                      msg=msg,
                                      msgparts=msgparts,
                                      lineseparator=lineseparator,
                                      hdrs_dict=hdrs_dict,
                                      body=body,
                                      respcode=respcode,
                                      reason=reason,
                                      respline=respline,
                                      respid=respid)

    def __reset(self,
                msg=None,
                msgparts=None,
                lineseparator=None,
                respcode=None,
                reason=None,
                hdrs_dict=None,
                body=None,
                respline=None,
                respid=None):
        """ internal function to reset the object to its initial state"""
        if(respid is None):
            respid = str(getuid())

        if(respline is None):
            respline = get_response_line()

        return respid, respline

    def reset(self,
              msg=None,
              msgparts=None,
              lineseparator=None,
              respcode=None,
              reason=None,
              hdrs_dict=None,
              body=None,
              respline=None,
              respid=None):
        """ resets the object to its initial state"""
        respid, respline = \
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         lineseparator=lineseparator,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         respcode=respcode,
                         reason=reason,
                         respline=respline,
                         respid=respid)

        super(MsgResp, self).reset(type=MsgType.RESP,
                                   msg=msg,
                                   msgparts=msgparts,
                                   lineseparator=lineseparator,
                                   hdrs_dict=hdrs_dict,
                                   body=body,
                                   respcode=respcode,
                                   reason=reason,
                                   respline=respline,
                                   respid=respid)

    def debug(self):
        """ return instance data as a string """
        return ('type=%s\nmsg=%r\nmsgparts=%s\n'
                'hdrs=%s\nbody=%r\n'
                'lineseparator=%r\n'
                'respcode=%s\n'
                'reason=%s\n'
                'respline=%r\n'
                'respid=%s\n'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.lineseparator,
                   self.respcode,
                   self.reason,
                   self.respline,
                   self.respid))


if __name__ == '__main__':
    mreq = MsgReq(msg='Hello')
    mresp = MsgResp(msg='World')
    msg = Msg(msg='Hello World')

    print(mreq.debug())
    print(mresp.debug())
    print(msg.debug())
    print(mreq.debug())
    print(mresp.debug())
    print(msg.debug())

    mreq.reset()
    mresp.reset()
    msg.reset()
