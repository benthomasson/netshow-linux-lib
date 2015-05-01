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
    def mode(self):
        pass
