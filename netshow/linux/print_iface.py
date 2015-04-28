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
    test_iface = PrintIface(name, cache=cache)
    if test_iface.is_bridge():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridge(name, cache=cache)
    elif test_iface.is_bridgemem():
        bridge = nn.import_module('netshow.linux.print_bridge')
        return bridge.PrintBridgeMember(name, cache=cache)
    elif test_iface.is_bond():
        bond = nn.import_module('netshow.linux.print_bond')
        return bond.PrintBond(name, cache=cache)
    elif test_iface.is_bondmem():
        bondmem = nn.import_module('netshow.linux.print_bond')
        return bondmem.PrintBondMember(name, cache=cache)
    return test_iface


class PrintIface(linux_iface.Iface):
    """
    Linux Iface class with print functions
    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)

    @property
    def linkstate(self):
        _linkstate_value = super(PrintIface, self).linkstate
        if _linkstate_value == '0':
            return _('admdn')
        elif _linkstate_value == '1':
            return _('dn')
        elif _linkstate_value == '2':
            return _('up')

    @property
    def mode(self):
        """
        :return: port type. Via interface discovery determine classify port \
        type
        """
        if self.is_l3():
            if self.is_subint():
                return _('subint/l3')
            else:
                return _('access/l3')
        elif self.is_access():
            return _('access/L2')
        elif self.is_trunk():
            return _('trunk/l2')
        else:
            return _('unknown')

    @property
    def speed(self):
        return _('myspeed')

    @property
    def summary(self):
        """
        :return: summary information regarding the interface
        """
        if self.is_l3():
            _str2 = ""
            if self.ip_addr_assign == 'dhcp':
                _str2 = "(%s)" % _('dhcp')

            _str = ', '.join(self.ip_address.allentries) + _str2
            return [_str]

        return ['']
