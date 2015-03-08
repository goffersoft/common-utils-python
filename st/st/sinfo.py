#! /usr/bin/python

"""This Module Contains Service Tracker Code
   1) The ServiceInfo Class. Contains information
      about a particular service.
"""

import time


class ServiceInfo(object):
    def __init__(self,
                 svc_name,
                 svc_id,
                 last_msg_type):
        self.__svc_name = svc_name
        self.__svc_id = svc_id
        self.__last_update = time.time()
        self.__last_msg_type = last_msg_type

    @property
    def last_msg_type(self):
        return self.__last_msg_type

    @last_msg_type.setter
    def last_msg_type(self, msg_type):
        self.__last_msg_type = msg_type

    @property
    def svc_name(self):
        return self.__svc_name

    @svc_name.setter
    def svc_name(self, sname):
        self.__svc_name = sname

    @property
    def svc_id(self):
        return self.__svc_id

    @svc_id.setter
    def svc_id(self, sid):
        self.__svc_id = sid

    def get_last_update_time(self):
        return self.__last_update

    def refresh_update_time(self):
        self.__last_update = time.time()

    def time_since_last_update(self):
        return int(time.time() - self.__last_update)

    def __str__(self):
        return ('svc_name = {0} : svc_id = {1} :'
                'time_since_last_update = {2} : last_msg_type = {3}'.
                format(self.svc_name,
                       self.svc_id,
                       self.time_since_last_update(),
                       self.last_msg_type))

    def debug(self):
        return str(self)


if __name__ == '__main__':
    sinfo = ServiceInfo(svc_name='svc-1',
                        svc_id='1',
                        last_msg_type='init')
    time.sleep(1)
    print(sinfo.debug())
    sinfo.last_msg_type = 'hello'
    sinfo.svc_name = 'svc-2'
    sinfo.svc_id = '2'
    time.sleep(1)
    print(sinfo.debug())
    sinfo.refresh_update_time()
    print(sinfo.debug())
