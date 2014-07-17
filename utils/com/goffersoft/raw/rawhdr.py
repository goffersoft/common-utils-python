#! /usr/bin/python

from com.goffersoft.utils.utils import readonly

""" This Module Contains header types specific to raw
    messaging protocol
"""


class _RawMsgHdrType(type):
    """Raw Message Header Names"""
    CONTENT = readonly('Content')
    CONTENT_TYPE = readonly('Content-Type')
    FROM = readonly('From')
    TO = readonly('To')
    REQ_ID = readonly('Req-Id')
    RESP_ID = readonly('Resp-Id')

"""Raw Message Header Type"""
RawMsgHdrType = _RawMsgHdrType('RawMsgHdrType', (object,), {})


if __name__ == '__main__':
    pass
