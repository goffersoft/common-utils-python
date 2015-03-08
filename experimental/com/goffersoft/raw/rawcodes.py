#! /usr/bin/python

""" This Module Contains Types for Raw Response Codes
    and the corerespnding helper functions
"""

from com.goffersoft.utils.utils import readonly


class _RawRCType(type):
    """Raw Status Codes"""
    RC_200 = readonly('200')
    RC_OK = readonly('200')
    RC_500 = readonly('500')
    RC_INTERNAL_ERROR = readonly('500')
    RC_403 = readonly('403')
    RC_FORBIDDEN = readonly('403')
    RC_503 = readonly('503')
    RC_SERVICE_UNAVAILABLE = readonly('503')


class _RawRCDescrType(type):
    """Raw Status Codes - Descriptive Text"""
    RC_200 = readonly('Success')
    RC_500 = readonly('Failure : Internal Server Error')
    RC_403 = readonly('Forbidden')
    RC_503 = readonly('Service Unavailable')


RawRCType = _RawRCType('RawRCType', (object,), {})
RawRCDescrType = _RawRCDescrType('RawRCDescrType',
                                 (object,), {})


if __name__ == '__main__':
    print(RawRCType.RC_200)
    print(RawRCType.RC_500)
    print(RawRCType.RC_503)
    print(RawRCType.RC_403)
    print(RawRCType.RC_OK)
