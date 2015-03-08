#! /usr/bin/python

""" this module contains utilitiy functions
    used by ither modules
      print_usage
      print_usage_and_exit
      get_raw_input_nonblocking_select - reads input from sys.stdin
      get_raw_input_nonblocking_signal - reads input from sys.stdin
"""

import sys
import select


def readonly(value):
    """support readonly enum like types"""
    return property(lambda self: value)


def wrap_func(data, func_name=None):
    """wraps 'data' and returns new function"""
    def func():
        return data

    if(func_name is not None):
        func.__name__ = func_name

    return func


def print_usage_and_exit(reason=None, usage=None, logger=None):
    """ prints usage string and exits the program"""
    print_usage(usage, reason, logger, True)


def print_usage(usage=None, reason=None, logger=None, exit=False):
    """ prints usage string and conditionally exits the program"""
    if((usage is None) and (reason is None)):
        return

    if(usage is None):
        output = reason
    elif(reason is None):
        output = usage
    else:
        output = reason + '\n' + usage

    if(logger is None):
        print(output)
    else:
        logger.info(output)

    if(exit is True):
        sys.exit()


class AlarmException(Exception):
    """ Alarm Excpetion class """
    pass


def alarmHandler(signum, frame):
    """ signal handler for SIGALRM """
    raise AlarmException


def get_raw_input_nonblocking_select(prompt='', timeout=5):
    """If there's input ready, do something, else do something
    else. Note timeout is zero so select won't block at all.
           return user input text on success
           return '' on failure """
    if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
        if(sys.version_info >= (3, 0)):
            text = input()
        else:
            text = raw_input()
        if text:
            return text
        else:  # an empty line means stdin has been closed
            return ''
    else:
        return ''


def get_raw_input_nonblocking_signal(prompt='', timeout=20):
    """If there's input ready, do something, else block
       until timeout.
           return user input text on success
           return '' on failure """
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        if(sys.version_info >= (3, 0)):
            text = input()
        else:
            text = raw_input()
        signal.alarm(0)
        return text
    except AlarmException:
        print('\nPrompt timeout. Continuing...')
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


if __name__ == '__main__':
    print_usage('No reason whatsoever')

    usage = """
            Usage Example : {0}  arg[ arg]
            """.format(sys.argv[0])

    print_usage_and_exit('No reason whatsoever', usage)
