#! /usr/bin/python

"""This Module Contains Address Base Class
   This is a base class whose
   methods will be overridden by
   derived classes customized to
   different address formats
   This module contains the following funcstions and classes
       1) _get_field_separator - internal function to return the default
                                 field separator
       2) get_field_separator - returns the field separator
       3) _wrap_func - initernal function for wrapping constants in functions
       4) init - inits the address module (customizes the field separator)
       5) Address - base class to create a logical address.
"""


def _get_field_separator():
    """ default field separator"""
    return ':'


def get_field_separator():
    """ field separator"""
    return _get_field_separator()


def _wrap_func(str):
    """ function to wrap 'str'
        in a function"""
    def func():
        return str
    return func


def init(field_separator=None):
    """ inits the address module.
        customizes the field_separator"""
    global get_field_separator

    if(field_separator is None):
        get_field_separator = _get_field_separator
    else:
        get_field_separator = _wrap_func(field_separator)
    get_field_separator.__name__ = 'get_field_separator'


class Address(object):
    """ The Base Class For all
        Address Formats
    """

    def __init__(self,
                 addr=None,
                 addrparts=None,
                 fieldseparator=None):
        """ Initializes an instance of the Address class
            arguments -:
                1) addr -> address as a string
                2) addrparts -> addrparts as a tuple
                   (parts separated by fieldseparator)
                3) fieldseparator -> delimiter to break address into fields
        """
        self.__reset(addr=addr,
                     addrparts=addrparts,
                     fieldseparator=fieldseparator)

    def __reset(self,
                addr=None,
                addrparts=None,
                fieldseparator=None):
        """ internal function to reset object state"""
        self.__fieldsep = fieldseparator
        self.__addr = addr
        self.__addrparts = addrparts
        if(self.__fieldsep is None):
            self.__fieldsep = get_field_separator()
        self.__update_addr()
        self.__update_addrparts()

    def __update_addr(self):
        """ internal function to update addr parts"""
        if(self.__fieldsep is not None and
           self.__addr is None and
           self.__addrparts is not None):
            self.__addr = ''
            for a in self.__addrparts:
                self.__addr += str(a) + self.__fieldsep
            self.__addr = self.__addr[0:len(self.__addr) -
                                      len(self.__fieldsep)]

    def __update_addrparts(self):
        """ internal function to update addrparts"""
        if(self.__fieldsep is not None and
           self.__addrparts is None and
           self.__addr is not None):
            self.__addrparts = tuple(self.__addr.split(self.__fieldsep))

    def reset(self,
              addr=None,
              addrparts=None,
              fieldseparator=None):
        """ resets object state"""
        self.__reset(addr=addr,
                     addrparts=addrparts,
                     fieldseparator=fieldseparator)

    @property
    def fieldseparator(self):
        """ fieldseparator getter method """
        return self.__fieldsep

    @fieldseparator.setter
    def fieldseparator(self, fieldsep):
        """ fieldseparator setter method """
        if(self.__fieldsep != fieldsep):
            self.__fieldsep = fieldsep
            self.__addr = None

    @property
    def addr(self):
        """ addr getter method """
        self.__update_addr()
        return self.__addr

    @addr.setter
    def addr(self, addr):
        """ addr setter method """
        if(addr != self.__addr):
            self.__addr = addr
            self.__addrparts = None

    @property
    def addrparts(self):
        """ addrparts getter method """
        self.__update_addrparts()
        return self.__addrparts

    @addrparts.setter
    def addrparts(self, addrparts):
        """ addrparts setter method """
        if(addrparts != self.__addrparts):
            self.__addrparts = addrparts
            self.__addr = None

    def tostr(self):
        """ return addr as a string """
        return self.addr

    def tobytes(self):
        """ return addr as bytes """
        if(self.addr is not None):
            return self.addr.encode()
        return None

    def __repr__(self):
        """ overload python built-in function - repr or str """
        return self.tostr()

    def __eq__(self, obj):
        return (isinstance(obj, Address) and
                self.addr == obj.addr and
                self.addrparts == obj.addrparts)

    def __ne__(self, obj):
        return not self == obj

    def debug(self):
        """ return instance data as a string """
        return ('addr=%r\n'
                'addrparts=%s\n'
                'fieldseparator=%r\n'
                % (self.addr,
                   self.addrparts,
                   self.fieldseparator))


if __name__ == '__main__':
    addr = Address(addr='Hello:world')
    addr1 = Address(addrparts=('Hello-1', 'world-1'))

    print(addr.debug())
    print(addr1.debug())

    addr.fieldseparator = ';'
    print(addr.debug())

    addr.addr = 'Hello-2;World-2'
    print(addr.debug())

    init(field_separator='<>')
    addr2 = Address(addrparts=('Hello-10', 'world-10'))

    addr.addrparts = ('Hello-3', 'World-3')
    print(addr.debug())
    print('%r' % addr.tostr())
    print('%r' % addr.tobytes())
    print('%r' % addr)
    print('%r' % addr2)
