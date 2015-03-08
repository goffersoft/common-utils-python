#! /usr/bin/python

"""This Module Contains Msg Base Class
   This is an abstract class whose
   methods will be overridden by
   derived classes customized to
   different msg formats
   This module contains the following functions and classes
     1) _get_default_msgctxt - default message context
     2) get_msgctxt - reutrns the configured message context
     3) init - inits the msg module(customizes the
               message context).
     4) splitmsg - splits the message into parts (tuple) using
                   the linseparator as the delimiter
     5) Msg - Base class of all message formats
     6) MsgReq - Base class of all message request formats
     7) MsgResp - Base class of all message response formats
"""

from copy import copy

try:
    from .msgctxt import MsgCtxt
    from .msgtype import MsgType
    from .msgfac import register
except:
    from msgctxt import MsgCtxt
    from msgtype import MsgType
    from msgfac import register

from utils.uid import getuid
from utils.misc import wrap_func


_def_msgctxt = MsgCtxt(reqline='Generic Request Message : Version 1.0',
                       respline='Generic Response Message : Version 1.0',
                       linesep='\r\n')


def _get_default_msgctxt():
    """default msgctxt"""
    return _def_msgctxt


def get_msgctxt():
    """msgctxt"""
    return _get_default_msgctxt()


def init(msgctxt=None):
    """inits the msg module. customizes the
       1) customizes the MsgCtxt for all messages
       2) registers the message validation
          handler with the msgfac module using the
          register function"""
    global get_msgctxt

    if(msgctxt is None):
        get_msgctxt = _get_default_msgctxt
    else:
        get_msgctxt = wrap_func(msgctxt)

    get_msgctxt.__name__ = 'get_msgctxt'


def splitmsg(msg,
             linesep=None):
    """helper function to split a message to parts
       (tuple) using the line separator as the
       delimiter"""
    if msg is None:
        return ''

    if linesep is None:
        linesep = get_msgctxt().linesep

    return msg.split(linesep)


class Msg(object):
    """ The Base Class For all Message Formats
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
                 hdrs_dict=None,
                 body=None,
                 reqid=None,
                 respcode=None,
                 reason=None,
                 respid=None,
                 msgctxt=None):
        """ Initializes an instance of the base class
            arguments -:
                1) msg -> message as a string
                2) msgparts -> msgparts as a tuple
                   (parts separated by lineseparator)
                3) type -> msgtype.MsgType (REQ or RESP)
                4) hdrs_dict -> list of hdrs as a dictionary
                5) body -> message body as a string
                6) reqid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything)
                7) respcode -> response code as a string (MsgType.RESP only)
                8) reason -> descriptive text indicating reason
                   for success/failure
                9) respid -> as a uuid (typically as a uuid.uuid4()
                            but can be anything --> MsgType.RESP only)
                10) msgctxt -> message ctxt (MsgCtxt)
        """
        if(msgctxt is None):
            self.__msgctxt = get_msgctxt()
        else:
            self.__msgctxt = msgctxt

        self.__reset(msg=msg,
                     msgparts=msgparts,
                     type=type,
                     respcode=respcode,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqid=reqid,
                     respid=respid,
                     reason=reason)

    def __update_msg(self):
        """ internal funtion to update 'msg' """
        if(self.__msg is None and
           self.__msgparts is not None):
            self.__msg = ''
            for m in self.__msgparts:
                self.__msg += str(m) + self.__msgctxt.linesep
        return self.__msg

    def __update_msgparts(self):
        """ internal funtion to update 'msgparts' """
        if(self.__msgparts is None and
           self.__msg is not None):
            self.__msgparts = self.__msg.split(self.__msgctxt.linesep)
        return self.__msgparts

    def __reset(self,
                msg=None,
                msgparts=None,
                type=None,
                hdrs_dict=None,
                body=None,
                reqid=None,
                respcode=None,
                reason=None,
                respid=None):
        """ internal funtion to reset the object to its initial state """
        self.__msg = msg
        self.__msgparts = msgparts
        self.__type = type
        self.__respcode = respcode
        self.__hdrs = hdrs_dict
        self.__body = body
        self.__reqid = reqid
        self.__respid = respid
        self.__reason = reason

        if(hdrs_dict is None):
            self.__hdrs = {}

        self.update_msg()
        self.update_msgparts()

    def reset(self,
              msg=None,
              msgparts=None,
              type=None,
              hdrs_dict=None,
              body=None,
              reqid=None,
              respcode=None,
              reason=None,
              respid=None):
        """ resets the object to its initial state """
        self.__reset(msg=msg,
                     msgparts=msgparts,
                     type=type,
                     respcode=respcode,
                     hdrs_dict=hdrs_dict,
                     body=body,
                     reqid=reqid,
                     respid=respid)

    def update_msg(self):
        """---> Maybe override in derived class <---"""
        return self.__update_msg()

    def update_msgparts(self):
        """ ---> Must override in derived class <---"""
        return self.__update_msgparts()

    @property
    def _msgctxt(self):
        """ msgctxt getter method - returns a reference """
        return self.__msgctxt

    @property
    def msgctxt(self):
        """ msgctxt getter method """
        return copy(self.__msgctxt)

    @msgctxt.setter
    def msgctxt(self, ctxt):
        """ msgctxt setter method """
        if(isinstance(type, MsgCtxt) is False):
            raise(TypeError,
                  'Expected argument to be of type MsgCtxt')

        if(ctxt is not None and
           self.__msgctxt != ctxt):
            self.__msg = None
            if(self.__msgparts is not None and
                (self.__msgctxt.reqline != ctxt.reqline or
                 self.__msgctxt.respline != ctxt.respline)):
                if(self.__type is MsgType.REQ):
                    self.__msgparts[0] = ctxt.reqline
                elif(self.__type is MsgType.RESP):
                    self.__msgparts[0] = ctxt.respline
                else:
                    self.__msgparts = None
            self.__msgctxt = ctxt

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
        return ('type=%s\n'
                'msg=%r\n'
                'msgparts=%s\n'
                'hdrs=%s\n'
                'body=%r\n'
                'reqid=%s\n'
                'respcode=%s\n'
                'reason=%s\n'
                'respid=%s\n'
                'msgctxt=(%s)'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.reqid,
                   self.respcode,
                   self.reason,
                   self.respid,
                   self._msgctxt))


class MsgReq(Msg):
    """ The Base Class For all
        Message Request Formats
    """
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 hdrs_dict=None,
                 body=None,
                 reqid=None,
                 msgctxt=None):
        """ inits the object - see base class for more comments"""
        reqid =\
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         reqid=reqid)

        super(MsgReq, self).__init__(type=MsgType.REQ,
                                     msg=msg,
                                     msgparts=msgparts,
                                     hdrs_dict=hdrs_dict,
                                     body=body,
                                     reqid=reqid,
                                     msgctxt=msgctxt)

    def __reset(self,
                msg=None,
                msgparts=None,
                hdrs_dict=None,
                body=None,
                reqid=None):
        """ internal function to reset the object to its initial state"""
        if(reqid is None):
            reqid = str(getuid())

        return reqid

    def reset(self,
              msg=None,
              msgparts=None,
              hdrs_dict=None,
              body=None,
              reqid=None):
        """ resets the object to its initial state"""
        reqid =\
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         reqid=reqid)

        super(MsgReq, self).reset(type=MsgType.REQ,
                                  msg=msg,
                                  msgparts=msgparts,
                                  hdrs_dict=hdrs_dict,
                                  body=body,
                                  reqid=reqid)

    def debug(self):
        """ return instance data as a string """
        return ('type=%s\n'
                'msg=%r\n'
                'msgparts=%s\n'
                'hdrs=%s\n'
                'body=%r\n'
                'reqid=%s\n'
                'msgctxt=(%s)'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.reqid,
                   self._msgctxt))


class MsgResp(Msg):
    """ The Base Class For all
        Message Response Formats
    """
    def __init__(self,
                 msg=None,
                 msgparts=None,
                 respcode=None,
                 reason=None,
                 hdrs_dict=None,
                 body=None,
                 respid=None,
                 msgctxt=None):
        """ inits the object - see base class for more comments"""
        respid = \
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         respcode=respcode,
                         reason=reason,
                         respid=respid)

        super(MsgResp, self).__init__(type=MsgType.RESP,
                                      msg=msg,
                                      msgparts=msgparts,
                                      hdrs_dict=hdrs_dict,
                                      body=body,
                                      respcode=respcode,
                                      reason=reason,
                                      respid=respid,
                                      msgctxt=msgctxt)

    def __reset(self,
                msg=None,
                msgparts=None,
                respcode=None,
                reason=None,
                hdrs_dict=None,
                body=None,
                respid=None):
        """ internal function to reset the object to its initial state"""
        if(respid is None):
            respid = str(getuid())

        return respid

    def reset(self,
              msg=None,
              msgparts=None,
              respcode=None,
              reason=None,
              hdrs_dict=None,
              body=None,
              respid=None):
        """ resets the object to its initial state"""
        respid = \
            self.__reset(msg=msg,
                         msgparts=msgparts,
                         hdrs_dict=hdrs_dict,
                         body=body,
                         respcode=respcode,
                         reason=reason,
                         respid=respid)

        super(MsgResp, self).reset(type=MsgType.RESP,
                                   msg=msg,
                                   msgparts=msgparts,
                                   hdrs_dict=hdrs_dict,
                                   body=body,
                                   respcode=respcode,
                                   reason=reason,
                                   respid=respid)

    def debug(self):
        """ return instance data as a string """
        return ('type=%s\n'
                'msg=%r\n'
                'msgparts=%s\n'
                'hdrs=%s\n'
                'body=%r\n'
                'respcode=%s\n'
                'reason=%s\n'
                'respid=%s\n'
                'msgctxt=(%s)'
                % (self.type,
                   self.msg,
                   self.msgparts,
                   self.hdrs,
                   self.body,
                   self.respcode,
                   self.reason,
                   self.respid,
                   self._msgctxt))


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
    print(msg.msgctxt)

    mreq.reset()
    mresp.reset()
    msg.reset()
