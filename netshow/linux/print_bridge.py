"""
Print and Analysis Module for Linux bridge interfaces
"""
from netshow.linux.print_iface import PrintIface
from netshowlib.linux import common

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

    def untagged_ifaces(self):
        """
        :return: list of untagged interfaces of the bridge
        """
        _untagmems = self.iface.untagged_members.keys()
        if _untagmems:
            _str = "%s:" % (_('untagged'))
            _str += ' ' + ','.join(common.group_ports(_untagmems))
            return _str
        return ''

    def tagged_ifaces(self):
        """
        :return: list of tagged interfaces of the bridge
        """
        _tagmems = self.iface.tagged_members.keys()
        if _tagmems:
            _str = "%s:" % (_('tagged'))
            _str += ' ' + ','.join(common.group_ports(_tagmems))
            return _str
        return ''

    def vlan_id(self):
        """
        :return: vlan id
        :return: 'untagged' if non is available
        """
        _str = self.iface.vlan_tag
        if not _str:
            _str = _('untagged')
        return _str

    def stp_summary(self):
        """
        :return: root switch priority if switch is root of bridge
        :return: root port if switch is not root of bridge
        :return: stp disabled if stp is disabled
        """
        _str = ["%s:" % (_('stp'))]
        if self.iface.stp:
            if self.iface.stp.is_root():
                _str.append("%s(%s)" % (_('rootswitch'),
                                        self.iface.stp.root_priority))
            else:
                _root_ports = self.iface.stp.member_state.get('root')
                # should be only one..but just in case something is messed up
                # print all root ports found
                _rootportnames = []
                for _port in _root_ports:
                    _rootportnames.append(_port.name)
                _str.append("%s(%s)" % (','.join(_rootportnames),
                                        _('root')))
                _str.append("%s(%s)" % (self.iface.stp.root_priority,
                                        _('root_priority')))
        else:
            _str.append(_('disabled'))
        return ' '.join(_str)

    @property
    def summary(self):
        """
        :return: summary information regarding the bridge
        """
        _info = []
        _info.append(self.untagged_ifaces())
        _info.append(self.tagged_ifaces())
        _info.append(self.vlan_id())
        _info.append(self.stp_summary())
        return _info
