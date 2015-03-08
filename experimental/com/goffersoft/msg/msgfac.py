#! /usr/bin/python

from msgtype import MsgType

""" Dictonaries to store message validation handlers
    assumption is that the first few bytes of the incmining
    message determines the handler to be used to validate
    the incoming message
    The handler is a function that takes 2 arguments.
      1) MsgType,
      2) message as a string.
    The handler returns a class derived from the Msg base class.
    <Msg> handler(MsgType, msg_as_String)
    This module contains the following function
    1) register - regosters a handler
    2) print_registry - utility to print registered handlers
    3) get_req_msg_validation_handler - get handler for a message request
    4) get_resp_msg_validation_handler - get handler for a message response
    5) get_resp_msg_validation_handler - get handler for a message response
    6) get_msg_validation_handler - gets a request / response msg handler based
                                    on message pattern
"""


req_msg_proto_registry = {}
resp_msg_proto_registry = {}


def register(req_msg_starts_with,
             resp_msg_starts_with,
             msg_validation_handler
             ):
    """ Registers a handler """
    req_msg_proto_registry[req_msg_starts_with] = msg_validation_handler
    resp_msg_proto_registry[resp_msg_starts_with] = msg_validation_handler


def print_registry(logger=None):
    """ prints the list of message patterns
        and their associated handlers"""
    if(logger is None):
        print(str(req_msg_proto_registry))
        print(str(resp_msg_proto_registry))
    else:
        logger.info(str(req_msg_proto_registry))
        logger.info(str(resp_msg_proto_registry))


def get_req_msg_validation_handler(msg_starts_with):
    """ Returns a handler for message requests
        otherwise returns None"""
    for k in req_msg_proto_registry:
        if (msg_starts_with.startswith(k) is True):
            return req_msg_proto_registry[k]
    return None


def get_resp_msg_validation_handler(msg_starts_with):
    """ Returns a handler for message response
        otherwise returns None"""
    for k in resp_msg_proto_registry:
        if (msg_starts_with.startswith(k) is True):
            return resp_msg_proto_registry[k]
    return None


def get_msg_validation_handler(msg_starts_with):
    """ Returns a handler for a meesage request
        if not found returns a handler for a
        message response. otherwise returns None"""
    handler = get_req_msg_validation_handler(msg_starts_with)
    if(handler is None):
        handler = get_resp_msg_validation_handler(msg_starts_with)
    return handler


if __name__ == '__main__':
    def validate_hello_msg(type):
        print ('validate_hello_msg called, type=' + type)

    def validate_sip_msg(type):
        print ('validate_sip_msg called, type= ' + type)

    def validate_http_msg(type):
        print ('validate_http_msg called, type= ' + type)

    def validate_myproto_msg(type):
        print ('validate_myproto_msg called, type= ' + type)

    register('Hello-Req',
             'Hello-Resp',
             validate_hello_msg)
    register('Http-Req',
             'Http-Resp',
             validate_http_msg)
    register('Sip-Req',
             'Sip-Resp',
             validate_sip_msg)
    register('MyProto-Req',
             'MyProto-Resp',
             validate_myproto_msg)

    msg_handler = get_req_msg_validation_handler('Hello-Req')
    assert(msg_handler is validate_hello_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_resp_msg_validation_handler('Hello-Resp')
    assert(msg_handler is validate_hello_msg)
    msg_handler(MsgType.RESP)
    msg_handler = get_msg_validation_handler('Hello-Req')
    assert(msg_handler is validate_hello_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_msg_validation_handler('Hello-Resp')
    assert(msg_handler is validate_hello_msg)
    msg_handler(MsgType.RESP)

    msg_handler = get_req_msg_validation_handler('Sip-Req')
    assert(msg_handler is validate_sip_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_resp_msg_validation_handler('Sip-Resp')
    assert(msg_handler is validate_sip_msg)
    msg_handler(MsgType.RESP)
    msg_handler = get_msg_validation_handler('Sip-Req')
    assert(msg_handler is validate_sip_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_msg_validation_handler('Sip-Resp')
    assert(msg_handler is validate_sip_msg)
    msg_handler(MsgType.RESP)

    msg_handler = get_req_msg_validation_handler('Http-Req')
    assert(msg_handler is validate_http_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_resp_msg_validation_handler('Http-Resp')
    assert(msg_handler is validate_http_msg)
    msg_handler(MsgType.RESP)
    msg_handler = get_msg_validation_handler('Http-Req')
    assert(msg_handler is validate_http_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_msg_validation_handler('Http-Resp')
    assert(msg_handler is validate_http_msg)
    msg_handler(MsgType.RESP)

    msg_handler = get_req_msg_validation_handler('MyProto-Req')
    assert(msg_handler is validate_myproto_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_resp_msg_validation_handler('MyProto-Resp')
    assert(msg_handler is validate_myproto_msg)
    msg_handler(MsgType.RESP)
    msg_handler = get_msg_validation_handler('MyProto-Req')
    assert(msg_handler is validate_myproto_msg)
    msg_handler(MsgType.REQ)
    msg_handler = get_msg_validation_handler('MyProto-Resp')
    assert(msg_handler is validate_myproto_msg)
    msg_handler(MsgType.RESP)
