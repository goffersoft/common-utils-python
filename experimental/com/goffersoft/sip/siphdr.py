#! /usr/bin/python

from com.goffersoft.utils.utils import readonly


""" This Module Contains header types specific to sip
    messaging protocol
"""


class _SipMsgHdrType(type):
    """Sip Message Header Names """
    CONTENT = readonly('Content')
    CONTENT_TYPE = readonly('Content-Type')
    FROM = readonly('From')
    TO = readonly('To')
    REQ_ID = readonly('Req-Id')
    RESP_ID = readonly('Resp-Id')


"""Sip Message Header Type """
SipMsgHdrType = _SipMsgHdrType('MsgHdrType', (object,), {})


if __name__ == '__main__':
    pass
