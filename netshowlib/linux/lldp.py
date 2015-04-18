# http://pylint-messages.wikidot.com/all-codes
"""
This module defines properties and functions for collecting LLDP information
from a linux device using the ``lldpctl`` command
"""
from netshowlib.linux.common import exec_command
import xml.etree.ElementTree as ElementTree


def _exec_lldp(ifacename=None):
    """
     exec lldp and return output from LLDP or None
     """
    lldp_output = None
    exec_str = '/usr/sbin/lldpctl -f xml'
    if ifacename:
        exec_str += ' %s' % (ifacename)
    try:
        lldp_cmd = exec_command(exec_str)
        lldp_output = ElementTree.fromstring(lldp_cmd)
    except:
        pass
    return lldp_output


def cacheinfo():
    """
    Cacheinfo function for LLDP information
    :return: hash of :class:`linux.lldp<Lldp>` objects with interface name as their keys
    """
    lldp_hash = {}
    lldp_element = _exec_lldp()
    if lldp_element is None:
        return lldp_hash
    for interface in lldp_element.iter('interface'):
        local_port = interface.get('name')
        lldpobj = {}
        lldpobj['adj_port'] = interface.findtext('port/descr')
        lldpobj['adj_hostname'] = interface.findtext('chassis/name')
        lldpobj['adj_mgmt_ip'] = interface.findtext('chassis/mgmt-ip')
        if not lldp_hash.get(local_port):
            lldp_hash[local_port] = []
        lldp_hash[local_port].append(lldpobj)
    return lldp_hash

def interface(ifacename, cache):
    """
    Will use the cache provided first to get lldp information. If not found
    will run :meth:`cacheinfo()` and generate new lldp information

    :param ifacename: name of the interface
    :param cache: instance of a :class:`netshowlib.linux.cache.Cache` that may have LLDP information
    :return: array of lldp information regarding a single interface.
    """
    if cache:
        lldp_cache = cache.lldp
    else:
        lldp_cache = cacheinfo()

    ifacelldp = lldp_cache.get(ifacename)
    if ifacelldp:
        return ifacelldp
    else:
        return None
