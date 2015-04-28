"""
Print and Analysis Module for Linux bond interfaces
"""

import netshowlib.linux.bond as linux_bond
from flufl.i18n import initialize

_ = initialize('netshow-linux-lib')


class PrintBondMember(linux_bond.BondMember):
    """
    Print and Analysis Class for Linux bond member interfaces
    """
    pass


class PrintBond(linux_bond.Bond):
    """
    Print and Analysis Class for Linux bond interfaces
    """
    pass
