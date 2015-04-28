"""
Print and Analysis Module for Linux bridge interfaces
"""

import netshowlib.linux.bridge as linux_bridge
from flufl.i18n import initialize

_ = initialize('netshow-linux-lib')


class PrintBridgeMember(linux_bridge.BridgeMember):
    """
    Print and Analysis Class for Linux bridge member interfaces
    """
    pass


class PrintBridge(linux_bridge.Bridge):
    """
    Print and Analysis Class for Linux bridge interfaces
    """
    pass
