"""
Linux Iface module with print functions
"""

from netshowlib.linux import iface as linux_iface
from flufl.i18n import initialize

_ = initialize('netshow')


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
