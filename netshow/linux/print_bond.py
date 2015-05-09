"""
Print and Analysis Module for Linux bond interfaces
"""

from netshow.linux.print_iface import PrintIface

from flufl.i18n import initialize
from tabulate import tabulate
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


    @property
    def hash_policy(self):
        """
        :return: hash policy for bond
        """
        _hash_policy = self.iface.hash_policy
        if _hash_policy == '1':
            return _('layer3+4')
        elif _hash_policy == '2':
            return _('layer2+3')
        elif _hash_policy == '0':
            return _('layer2')
        else:
            return _('unknown')



    @property
    def mode(self):
        """
        :return: name of the bond mode
        """
        _mode = self.iface.mode
        if _mode == '4':
            return _('lacp')
        elif _mode == '3':
            return _('broadcast')
        elif _mode == '2':
            return _('balance-xor')
        elif _mode == '1':
            return _('active-backup')
        elif _mode == '0':
            return _('balance-rr')
        else:
            return _('unknown')


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

    def bond_details(self):
        """
        print out table with bond details for netshow interface [ifacename]
        """
        _header = [_('bond_details'), '']
        _table = []
        _table.append([_('bond_mode') + ':', self.bond_mode])
        _table.append([_('load_balancing') + ':',  self.hash_policy])
        return tabulate(_table, _header)

    def bondmem_details(self):
        """
        print out table with bond member summary info for netshow interface [ifacename]
        for bond interface
        """
        pass

    def cli_output(self):
        """
        cli output of the linux bond interface
        :return: output for 'netshow interface <ifacename>'
        """
        _str = self.cli_header() + self.new_line()
        _str += self.bond_details() + self.new_line()
        _str += self.ip_details() + self.new_line()
        _str += self.bondmem_details() + self.new_line()
        _str += self.lldp_details() + self.new_line()
        return _str


