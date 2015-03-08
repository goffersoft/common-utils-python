#! /usr/bin/python

"""This Module Contains Service Tracker DB Utilities
   (A Hash map for now).
   Rudimentary hash map for testing.
   Evetually a distributed cache would be more
   beneficial
   This Module contains the following functions
   1) stdb_registry_to_str - converts the registry
                             hashmap into a string
   2) stdb_prune_registry - deletes stale entries
                            from the registry
   3) stdb_delete_from_registry - deletes an entry
                                  from the registry
   4) stdb_get_from_registry - gets an entry
                               from the registry
   5) stdb_update_registry - updates an entry
                             in the registry.
                             If the entry is not found
                             a new entry is added. Otherwise
                             the existing entry is modified.
"""

import logging

try:
    from .sinfo import ServiceInfo
except:
    from sinfo import ServiceInfo


stdb = {}


def stdb_registry_to_str(registry=stdb):
    """ Converts the registry hashmap into a string"""
    func_name = stdb_registry_to_str.__name__
    logger = logging.getLogger()
    msg = ''
    i = 1
    for sid, sinfo in registry.items():
        msg += '[' + str(i) + '] : ' + str(sinfo) + '\n'
        i += 1
    return msg


def stdb_prune_registry(ttl=60, registry=stdb):
    """ deletes stale entries from the registry """
    func_name = stdb_update_registry.__name__
    logger = logging.getLogger()

    for sid, sinfo in registry.items():
        if(sinfo.time_since_last_update() >= ttl):
            del registry[sid]


def stdb_delete_from_registry(sid, registry=stdb):
    """ deletes an entry from the registry """
    del registry[sid]


def stdb_get_from_registry(sid, registry=stdb):
    """ gets an entry from the registry """
    return registry[sid]


def stdb_update_registry(sid, sname, msg_type, registry=stdb):
    """ updates an entry in the registry.
        if the entry is not found a new entry is
        added. Otherwise the existing entry is
        modified."""
    if(sid in registry.keys()):
        sinfo = registry[sid]
        sinfo.svc_name = sname
        sinfo.svc_id = sid
        sinfo.last_msg_type = msg_type
        sinfo.refresh_update_time()
    else:
        registry[sid] = \
            ServiceInfo(svc_name=sname,
                        svc_id=sid,
                        last_msg_type=msg_type)


if __name__ == '__main__':
    pass
