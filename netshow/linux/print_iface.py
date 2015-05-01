"""
Linux Iface module with print functions
"""

import netshowlib.netshowlib as nn
from netshowlib.linux import iface as linux_iface
from flufl.i18n import initialize

_ = initialize('netshow-linux-lib')


def iface(name, cache=None):
    """
    :return: print class object that matches correct iface type of the named interface
    """
    # create test iface.
    test_iface = linux_iface.iface(name, cache=cache)
    if test_iface.is_bridge():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridge(test_iface)
    elif test_iface.is_bridgemem():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridgeMember(test_iface)
    elif test_iface.is_bond():
        bond = nn.import_module('netshow.linux.print_bond')
        return bond.PrintBond(test_iface)
    elif test_iface.is_bondmem():
        bondmem = nn.import_module('netshow.linux.print_bond')
        return bondmem.PrintBondMember(test_iface)
    return PrintIface(test_iface)


class PrintIface(object):
    """
    Printer for Linux Iface class
    """
    def __init__(self, _iface):
        self.iface = _iface
        self.name = self.iface.name
        self.mtu = self.iface.mtu

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
        if self.iface.is_l3():
            if self.iface.is_subint():
                return _('subint/l3')
            else:
                return _('access/l3')
        else:
            return _('unknown')

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
            if self.iface.ip_addr_assign == 'dhcp':
                _str2 = "(%s)" % _('dhcp')

            _str = ', '.join(self.iface.ip_address.allentries) + _str2
            return [_str]

        return ['']
