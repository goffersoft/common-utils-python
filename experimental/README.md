collection of python code - experimental


RPC Services - Using Rabbit - MQ
--------------------------------

This is a modified version of Tutorial6 - RPC
https://www.rabbitmq.com/tutorials/tutorial-six-python.html

docs : ./docs/rpcarch.pdf

packages : com.goffersoft.rabbitmq.rpc 

modules :

    1) rpc_find.py - finds the server that can execute the rpc method

    2) rpc_client.py - executes a rpc method and returns the result

    3) rpc_nameservice.py - the rpc nameservice (must be running before
                            rpc_find is executed) - locates where a particular
                                rpc service can be executed

    4) rpc_service.py - the rpc_service (must be running before rpc_client can 
                        be executed). - executes the rpc method and returns the
                        result back to the client.


ServiceTracker - Using Zero - MQ
--------------------------------

docs : ./docs/servicetrackerarch.pdf

packages : com.goffersoft.zeromq.servicetracker

modules : 

    1)servicetracker.py - 
      A protocol to discover and manager services. Consists of 3 modules

      service-manager - keeps track of a manages existing or new services
                  as they come and go 

      cmd-proc - a commond line tool to interact with the service manager
           (currenty only lists services)

      service - talks to the service manager(via ROUTER, DEALER, 
          PUB-SUB sockets) and optionally talks to thother
          inproc services (the cmd-proc uses the service module
          to recive and send messages to the service manager.)
          PAIR sockets are uses for communication.


Utility Packagaes
------------------

package : com.goffersoft.logging

modules :

    1) logconf.py - utility function to complement the logging module

package : com.goffersoft.zeromq.zmqutils

modules :

    1) zmqutils.py - zero mq utilities

package : com.goffersoft.sip

modules :

    1) sipcodes.py - sip codes

    2) siphdr.py - sip headers

package : com.goffersoft.http

modules :

    1) httpcodes.py - http codes

    2) httphdr.py - http headers

package : com.goffersoft.msg

modules :

    1) msg.py - base classes for all protocol message classes

    2) msgtype.py - generic message types

    3) msgfac.py - implementation of a generic message factory 

package : com.goffersoft.raw

modules :

    1) raw.py - raw protocol implementations

    2) rawcodes.py - raw response codes and desriptions

    3) rawhdr.py - raw header types

package : com.goffersoft.utils

modules :

    1) uid.py - useful functions that complements the UUID module

    2) utils.py - general utilities

    3) address.py - Address class 
