#! /usr/bin/python

"""This Module Contains Service Tracker MsgType enums
     1) STMsgType Extends the Enum base class STBaseMsgType
     2) STMsgType provides useful static helper methods to check
        validity of the message type
     3) Service Tracker Message Types
        1) STMsgType.INIT --> initial msg sent by agent to manager
        2) STMsgType.HELLO -->
            1) Broadcast(PUB/SUB) Message sent by Manager to all agents
            2) Subsequent keepalive messages from agent to manager
        3) STMsgType.MGMT --> mgr(UI) to mgr
        4) STMsgType.BYE --> sent from agent to mgr when agent goes away.
"""

from utils.misc import readonly


class _STMsgType(type):
    INIT = readonly('init')
    HELLO = readonly('hello')
    MGMT = readonly('mgmt')
    BYE = readonly('bye')


STBaseMsgType = _STMsgType('STMsgType', (object,), {})


class STMsgType(STBaseMsgType):
    @classmethod
    def is_valid(cls, msg_type, ignore_case=True):
        if(cls.is_init(msg_type, ignore_case) is True or
           cls.is_hello(msg_type, ignore_case) is True or
           cls.is_mgmt(msg_type, ignore_case) is True or
           cls.is_bye(msg_type, ignore_case) is True):
            return True
        return False

    @classmethod
    def is_init(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.INIT):
            return True

        return False

    @classmethod
    def is_hello(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.HELLO):
            return True

        return False

    @classmethod
    def is_bye(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.BYE):
            return True

        return False

    @classmethod
    def is_mgmt(cls, msg_type, ignore_case=True):
        if(ignore_case is True):
            type = msg_type.lower()
        else:
            type = msg_type

        if(type == STMsgType.MGMT):
            return True

        return False


if __name__ == '__main__':
    print(STMsgType.MGMT)
    print(STMsgType.HELLO)
    print(STMsgType.INIT)
    print(STMsgType.BYE)
