#! /usr/bin/python

from com.goffersoft.utils.utils import readonly

""" This Module Contains header types specific to http
"""


class _HttpMsgHdrType(type):
    """Http Message Header Names """
    CONTENT = readonly('Content')
    CONTENT_TYPE = readonly('Content-Type')
    FROM = readonly('From')
    TO = readonly('To')
    REQ_ID = readonly('Req-Id')
    RESP_ID = readonly('Resp-Id')


"""Http Message Header Type """
HttpMsgHdrType = _HttpMsgHdrType('MsgHdrType', (object,), {})


if __name__ == '__main__':
    pass
