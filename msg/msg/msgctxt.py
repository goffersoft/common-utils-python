#! /usr/bin/python

"""This Module Contains MsgCtxt Class
   This class provides a context for the
   message class to use. This module contains
   the following functions and classes
     1) MsgCtxt - Message Context class
"""


class MsgCtxt(object):
    """ The MsgCtxt Class
    """
    def __init__(self,
                 linesep,
                 reqline,
                 respline):
        """ Initializes an MsgCtxt class
            arguments -:
                1) linesep -> string to break message into lines
                2) reqline -> requent line (MsgType.REQ only) as a sring
                3) respline -> response line (MsgType.RESP only) as a sring
        """
        self.__linesep = linesep
        self.__reqline = reqline
        self.__respline = respline

    @property
    def linesep(self):
        """ linesep getter method """
        return self.__linesep

    @linesep.setter
    def linesep(self, linesep):
        """ linesep setter method """
        if(self.__linesep != linesep):
            self.__linesep = linesep

    @property
    def reqline(self):
        """ reqline getter method """
        return self.__reqline

    @reqline.setter
    def reqline(self, reqline):
        """ reqline setter method """
        if((reqline is not None) and
           (self.__reqline != reqline)):
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
            self.__respline = respline

    def tostr(self):
        """ return msgctxt as a string """
        return self.debug()

    def __repr__(self):
        """ overload python built-in function - repr or str """
        return self.tostr()

    def __eq__(self, obj):
        """ overload == operator """
        return (isinstance(obj, MsgCtxt) and
                self.linesep == obj.linesep and
                self.reqline == obj.reqline and
                self.respline == obj.respline)

    def __ne__(self, obj):
        """ overload != operator """
        return not self == obj

    def debug(self):
        """ return instance data as a string """
        return ('linesep=%r, '
                'reqline=%s, '
                'respline=%s\n'
                % (self.linesep,
                   self.reqline,
                   self.respline,
                   ))


if __name__ == '__main__':
    msgctxt = MsgCtxt(reqline='Generic Request Message : Version 1.0',
                      respline='Generic Response Message : Version 1.0',
                      linesep='\r\n')

    print(msgctxt.debug())
