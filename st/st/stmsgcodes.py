#! /usr/bin/python

""" This Module Contains Types for Service Tracker Response Codes
    and the corerespnding helper functions
"""

from utils.misc import readonly


class _STRCType(type):
    """Service Tracker Status Codes"""
    RC_200 = readonly('200')
    RC_OK = readonly('200')
    RC_500 = readonly('500')
    RC_INTERNAL_ERROR = readonly('500')
    RC_403 = readonly('403')
    RC_FORBIDDEN = readonly('403')
    RC_503 = readonly('503')
    RC_SERVICE_UNAVAILABLE = readonly('503')


class _STRCDescrType(type):
    """Service Tracker Status Codes - Descriptive Text"""
    RC_200 = readonly('Success')
    RC_500 = readonly('Failure : Internal Server Error')
    RC_403 = readonly('Forbidden')
    RC_503 = readonly('Service Unavailable')


STRCType = _STRCType('STRCType', (object,), {})
STRCDescrType = _STRCDescrType('STRCDescrType',
                               (object,), {})


if __name__ == '__main__':
    print(STRCType.RC_200)
    print(STRCType.RC_500)
    print(STRCType.RC_503)
    print(STRCType.RC_403)
    print(STRCType.RC_OK)

    print(STRCDescrType.RC_200)
    print(STRCDescrType.RC_500)
    print(STRCDescrType.RC_503)
    print(STRCDescrType.RC_403)
    print(STRCType.RC_OK)
