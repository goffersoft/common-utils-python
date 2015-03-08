ServiceTracker - Using Zero - MQ
--------------------------------

docs : ./docs/servicetrackerarch.pdf

packages : servicetracker

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


    2) stmsg.py - service tracker protocol implementations

    3) stcodes.py - service tracker response codes and desriptions

    4) sthdr.py - service tracker header types

insatll and run :

install :

1) cd python_utils

2) install utils module

    a) pushd utils
    
    b) sudo python setup.py install

    c) popd

3) install the msg module

    a) pushd msg

    b) sudo python setup.py install

    c) popd


run :

1) cd python_utils/st/st

2) execute the following commands each cammnd
   should be executed in separate terminal windows

    a) python stmain.py stmgr

    b) python stmain.py stsvc

    c) python stmain.py stui

3) log files by default are located in /tmp
