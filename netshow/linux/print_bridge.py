"""
Print and Analysis Module for Linux bridge interfaces
"""
from netshow.linux.print_iface import PrintIface

from flufl.i18n import initialize

_ = initialize('netshow-linux-lib')


class PrintBridgeMember(PrintIface):
    """
    Print and Analysis Class for Linux bridge member interfaces
    """
    def mode(self):
        pass


class PrintBridge(PrintIface):
    """
    Print and Analysis Class for Linux bridge interfaces
    """
    @property
    def port_category(self):
        """
        :return: port category of bridge. Then return its a L2 or L3 port as wel
        """
        if self.iface.is_l3():
            return _('bridge/l3')
        return _('bridge/l2')
