# pylint: disable=E0611
"""
Linux Iface module with print functions
"""

import netshowlib.netshowlib as nn
from netshowlib.linux import iface as linux_iface
from netshowlib.linux import common
from tabulate import tabulate
from netshow.linux.common import _
import inflection

def iface(name, cache=None):
    """
    :return: ``:class:PrintIface`` instance that matches \
        correct iface type of the named interface
    :return: None if interface does not exist
    """
    # create test iface.
    test_iface = linux_iface.iface(name, cache=cache)
    if not test_iface.exists():
        return None
    if test_iface.is_bridge():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridge(test_iface)
    elif test_iface.is_bond():
        bond = nn.import_module('netshow.linux.print_bond')
        return bond.PrintBond(test_iface)
    elif test_iface.is_bondmem():
        bondmem = nn.import_module('netshow.linux.print_bond')
        return bondmem.PrintBondMember(test_iface)
    elif test_iface.is_bridgemem():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridgeMember(test_iface)
    return PrintIface(test_iface)


class PrintIface(object):
    """
    Printer for Linux Iface class
    """
    def __init__(self, _iface):
        self.iface = _iface

    @property
    def name(self):
        """
        :return: name of the interface
        """
        return self.iface.name

    @classmethod
    def new_line(cls):
        """
        :return: print newline in cli output. its just two "\n"
        """
        return "\n\n"

    @property
    def linkstate(self):
        """
        :return string that prints out link state. admin down or down or up
        """
        _linkstate_value = self.iface.linkstate
        if _linkstate_value == 0:
            return _('admdn')
        elif _linkstate_value == 1:
            return _('dn')
        elif _linkstate_value == 2:
            return _('up')

    @property
    def port_category(self):
        """
        :return: port type. Via interface discovery determine classify port \
        type
        """
        if self.iface.is_loopback():
            return _('loopback')
        elif self.iface.is_l3():
            if self.iface.is_subint():
                return _('subint/l3')
            else:
                return _('access/l3')

        return _('access')

    @property
    def speed(self):
        """
        :return: print out current speed
        """
        _str = _('n/a')
        _speed_value = self.iface.speed
        if _speed_value is None or int(_speed_value) > 4294967200:
            return _str
        elif int(_speed_value) < 1000:
            _str = _speed_value + 'M'
        else:
            # Python3 supports this true division thing so 40/10 gives you 4.0
            # To not have the .0, have to do double _'/'_
            _str = str(int(_speed_value) // 1000) + 'G'
        return _str

    @property
    def summary(self):
        """
        :return: summary information regarding the interface
        """
        if self.iface.is_l3():
            _str2 = ""
            if self.iface.ip_addr_assign == 1:
                _str2 = "(%s)" % _('dhcp')

            _str = ', '.join(self.iface.ip_address.allentries) + _str2
            return [_str]

        return ['']

    def cli_header(self):
        """
        :return common cli header when printing single iface info
        """
        _header = [
            '',
            _('name'), _('mac'),
            _('speed'), _('mtu'), _('mode')]
        _table = [[
            self.linkstate,
            self.name,
            self.iface.mac,
            self.speed,
            self.iface.mtu,
            self.port_category]]
        return tabulate(_table, _header) + self.new_line()

    def cli_output(self):
        """
        Each PrintIface child should define their own  of this function
        :return: output for 'netshow interface <ifacename>'
        """
        _str = self.cli_header()
        _str += self.ip_details()
        _str += self.lldp_details()
        return _str

    def ip_details(self):
        """
        :return: basic IP info about the interface for single iface info
        """
        _header = [_('ip_details'), '']
        _table = []
        if not self.iface.is_l3():
            return ''
        else:
            _table.append(["%s:" % (_('ip')),
                           ', '.join(self.iface.ip_address.allentries)])
            _table.append(["%s:" % (_('arp_entries')),
                           len(self.iface.ip_neighbor.allentries)])

        return tabulate(_table, _header) + self.new_line()

    def lldp_details(self):
        """
        :return: lldp details about this specific interface
        """
        lldp_output = self.iface.lldp
        if not lldp_output:
            return ''
        _header = [_('lldp'), '', '']
        _table = []
        _table.append([self.iface.name, '====',
                       "%s(%s)" % (lldp_output[0].get('adj_port'),
                                   lldp_output[0].get('adj_hostname'))])
        del lldp_output[0]
        for _entry in lldp_output:
            _table.append(['', '====',
                           "%s(%s)" % (_entry.get('adj_port'),
                                       _entry.get('adj_hostname'))])

        return tabulate(_table, _header) + self.new_line()

    def trunk_summary(self):
        """
        :return: summary info for a trunk port
        """
        _vlanlist = self.iface.vlan_list
        native_vlans = []
        tagged_vlans = []
        for _str in _vlanlist:
            if _str.isdigit():
                tagged_vlans.append(_str)
            else:
                native_vlans.append(_str)
        _strlist = []
        if tagged_vlans:
            _strlist.append(_('tagged') + ': ' +
                            ','.join(common.create_range('', tagged_vlans)))

        if native_vlans:
            _strlist.append(_('untagged') + ': ' +
                            ','.join(common.group_ports(native_vlans)))

        return _strlist

    def access_summary(self):
        """
        :return: summary info for an access port
        """
        _bridgename = ','.join(self.iface.bridge_masters.keys())
        return [_('untagged') + ': ' + _bridgename]

    @classmethod
    def abbrev_linksummary(cls, linuxiface):
        """
        :return: 'U' if port is up
        :return: 'D' if port is down or admdn
        """
        if linuxiface.linkstate == 2:
            return _('U')
        else:
            return _('D')

    @classmethod
    def _pretty_vlanlist(cls, bridgelist):
        """
        :return: list of vlans that match category. First list of \
            native ports, then vlan ids of tagged bridgers
        """
        _native_vlans = []
        _tagged_vlans = []
        for _bridge in bridgelist:
            _vlantag = _bridge.vlan_tag
            if _vlantag:
                _tagged_vlans += _vlantag
            else:
                _native_vlans.append(_bridge.name)
        _vlanlist = common.group_ports(_native_vlans) +  \
            common.create_range('', _tagged_vlans)
        return [', '.join(_vlanlist)]

    def bridgemem_details(self):
        """
        :return: list vlans or bridge names of various stp states
        """
        if not self.iface.is_bridgemem():
            return None

        _str = ''
        _stpstate = self.iface.stp.state
        for _category, _bridgelist in _stpstate.items():
            if _stpstate.get(_category):
                _header = [_("vlans in %s state") %
                           (inflection.titleize(_category))]
                _table = [self._pretty_vlanlist(_bridgelist)]
                _str += tabulate(_table, _header, numalign="left") + \
                    self.new_line()
        return _str
