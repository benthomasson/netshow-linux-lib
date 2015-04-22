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
    def __init__(self, cache=None):
        linux_iface.Iface.__init__(self, cache)

    @property
    def linkstate(self):
        _linkstate_value = super(PrintIface, self).linkstate
        if _linkstate_value == '0':
            return _('admdn')
        elif _linkstate_value == '1':
            return _('dn')
        elif _linkstate_value == '2':
            return _('up')
