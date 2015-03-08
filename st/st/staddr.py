#! /usr/bin/python

"""This Module Contains Address Base Class
   This is a base class whose
   methods maybe overridden by
   derived classes customized to
   different address formats
   This module contains the following functions and classes
       1) Address - base class to create a logical address.
"""

from utils.address import Address
from utils.uid import getuid


class STAddress(Address):
    """ The Base Class For all
        Address Formats
    """

    def __init__(self,
                 addr=None,
                 addrparts=None,
                 fieldseparator=':'):
        """ Initializes an instance of the Address class
            arguments -:
                1) addr -> address as a string
                2) addrparts -> addrparts as a tuple
                   (parts separated by fieldseparator)
                3) fieldseparator -> delimiter to break address into fields
        """

        if(fieldseparator is None):
            fieldseparator = ':'

        super(STAddress, self).__init__(addr=addr,
                                        addrparts=addrparts,
                                        fieldseparator=fieldseparator)

        if(self.addrparts is not None and
           len(self.addrparts) != 2):
                raise ValueError('Invalid Address : expected <name>:<id>')

    @property
    def name(self):
        """name getter method """
        return self.addrparts[0]

    @name.setter
    def name(self, name):
        """ name setter method """
        if(name is not None and
           self.addrparts[0] != name):
                self.addrparts = (name, self.addrparts[1])

    @property
    def id(self):
        """ id getter method """
        return self.addrparts[1]

    @id.setter
    def id(self, id):
        """ id ddr setter method """
        if(id is not None and
           id != self.addrparts[1]):
            self.addrparts = (self.addrparts[0], id)


if __name__ == '__main__':
    addr = STAddress(addrparts=('staddr', getuid()))

    print('%r' % addr.name)
    print('%r' % addr.id)
    print(addr.debug())

    addr.id = getuid()
    addr.name = 'staddr-1'
    print(addr.debug())

    addr = STAddress(addr=('staddr-3:' + str(getuid())))
    print(addr.debug())

    try:
        addr = STAddress(addr=('staddr-3:' + str(getuid()) +
                         ':' + str(getuid())))
    except ValueError as v:
        print('staddr-4 ' + v.args[0])
