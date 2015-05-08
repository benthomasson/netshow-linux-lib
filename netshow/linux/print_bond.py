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
        else:
            return _('bond/l2')
