#! /usr/bin/python

""" this module contains zeromq utilitiy functions
"""

import zmq


def get_libzmq_version():
    """ zmq library version"""
    return zmq.zmq_version()


def get_pyzmq_version():
    """ python zmq version"""
    return zmq.__version__


def get_zmq_version():
    """ zmq library version and the python zmq version """
    return (get_libzmq_version(), get_pyzmq_version())


def print_zmq_version(logger=None):
    """ prints the zmq library version and the python zmq version """
    output = ('current libzmq version is {0}\n'
              'current pyzmq version is {1}').\
        format(*get_zmq_version())

    if(logger is None):
        print(output)
    else:
        logger.info(output)


if __name__ == '__main__':
    print_zmq_version()
