"""
Print and Analysis Module for Linux bond interfaces
"""

from netshow.linux.print_iface import PrintIface

from flufl.i18n import initialize

_ = initialize('netshow-linux-lib')


class PrintBondMember(PrintIface):
    """
    Print and Analysis Class for Linux bond member interfaces
    """
    def mode(self):
        pass


class PrintBond(PrintIface):
    """
    Print and Analysis Class for Linux bond interfaces
    """

    @property
    def port_category(self):
        """
        :return: port category for a bond
        """
        if self.iface.is_l3():
            return _('bond/l3')
        elif self.iface.is_trunk():
            return _('bond/trunk')
        elif self.iface.is_access():
            return _('bond/access')
        else:
            return _('bond')

    @property
    def summary(self):
        """
        :return: summary info for bonds for 'netshow interfaces'
        """
        _arr = []
        _arr.append(self.print_bondmems())
        if self.iface.is_l3():
            _arr.append(', '.join(self.iface.ip_address.allentries))
        elif self.iface.is_trunk():
            _arr += self.trunk_summary()
        elif self.iface.is_access():
            _arr += self.access_summary()
        return _arr



    @classmethod
    def abbrev_bondstate(cls, bondmem):
        """
        :param bondmem: :class:`netshowlib.linux.BondMember` instance
        :return: 'P' if bondmem in bond
        :return: 'D' if bondmem is not in bond
        """
        if bondmem.bondstate == 1:
            return _('P')
        else:
            return _('D')

    def print_bondmems(self):
        """
        :return: bondmember list when showing summary in netshow interfaces \
            for the bond interface
        """
        _arr = []
        for _bondmem in self.iface.members.values():
            _arr.append("%s(%s%s)" % (_bondmem.name,
                        self.abbrev_linksummary(_bondmem),
                        self.abbrev_bondstate(_bondmem)))
        return ': '.join([_('bondmems'), ', '.join(sorted(_arr))])
