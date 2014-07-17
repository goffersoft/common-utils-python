#! /usr/bin/python

""" This module contains helpers functions (wrappers)
    related to the uuid module. Currently only
    supported uuid version is 4
        is_valid_uid - determines if the input string is
                       a valid uid or not
        getuid - returns a randomly generated UUID4 object
"""


from uuid import uuid4
from uuid import UUID


def getuid(uuid_version=4):
    """returns a randomly generated UUID4 object"""
    return uuid4()


def is_valid_uid(uuid_string, uuid_version=4):
    """
    Validate that a UUID string is in
    fact a valid uuid4.

    Happily, the uuid module does the actual
    checking for us.

    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=uuid_version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    # If the uuidst is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return str(val) == uuid_string


if __name__ == '__main__':
    id = getuid()

    if(is_valid_uid(str(id)) is True):
        print((str(id) + ' is a valid uid'))
    else:
        print((str(id) + ' is not a valid uid'))

    id = 'Hello'

    if(is_valid_uid(str(id)) is True):
        print((str(id) + ' is a valid uid'))
    else:
        print((str(id) + ' is not a valid uid'))
