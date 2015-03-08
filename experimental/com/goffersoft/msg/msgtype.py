#! /usr/bin/python

from com.goffersoft.utils.utils import readonly

"""This Module Contains MsgType enums
     MsgType.REQ --> Message is a Request
     MsgType.RESP --> Message is a Response
"""


class _MsgType(type):
    """Msg Types"""
    REQ = readonly('REQ')
    RESP = readonly('RESP')


"""Msg Types"""
MsgType = _MsgType('MsgType', (object,), {})


if __name__ == '__main__':
    print(MsgType.REQ)
    print(MsgType.RESP)
