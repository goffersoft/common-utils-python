#! /usr/bin/python

""" This Module Contains header types specific to
    service tracker messaging protocol
"""

from utils.misc import readonly


class _STMsgHdrType(type):
    """Service Tracker Message Header Names"""
    CONTENT = readonly('Content')
    CONTENT_TYPE = readonly('Content-Type')
    FROM = readonly('From')
    TO = readonly('To')
    REQ_ID = readonly('Req-Id')
    RESP_ID = readonly('Resp-Id')

"""Service Tracker Message Header Type"""
STMsgHdrType = _STMsgHdrType('STMsgHdrType', (object,), {})


if __name__ == '__main__':
    print(STMsgHdrType.CONTENT)
    print(STMsgHdrType.CONTENT_TYPE)
    print(STMsgHdrType.FROM)
    print(STMsgHdrType.TO)
    print(STMsgHdrType.REQ_ID)
    print(STMsgHdrType.RESP_ID)
