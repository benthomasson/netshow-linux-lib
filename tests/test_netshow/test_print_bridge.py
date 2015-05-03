# http://pylint-messages.wikidot.com/all-codes
# attribute defined outside init
# pylint: disable=W0201
# pylint: disable=R0913
# disable unused argument
# pylint: disable=W0613
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# disable invalid name
# pylint: disable=C0103
# pylint: disable=F0401
# pylint: disable=E0611
# pylint: disable=W0611

import netshow.linux.print_bridge as print_bridge
import netshowlib.linux.bridge as linux_bridge
import mock
from asserts import assert_equals
from nose.tools import set_trace


class TestPrintBridge(object):
    def setup(self):
        iface = linux_bridge.Bridge('eth22')
        self.piface = print_bridge.PrintBridge(iface)

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_l3')
    def test_port_category(self, mock_is_l3):
        # if l3 is true and is not loopback
        mock_is_l3.return_value = True
        assert_equals(self.piface.port_category, 'bridge/l3')
        # if l3 is not true
        mock_is_l3.return_value = False
        assert_equals(self.piface.port_category, 'bridge/l2')

    @mock.patch('netshowlib.linux.bridge.Bridge._memberlist_str')
    def test_vlan_id(self, mock_bridgemems):
        # tagged ports
        mock_bridgemems.return_value = ['eth1.100', 'eth2.100', 'eth3', 'eth4']
        assert_equals(self.piface.vlan_id(), '100')
        # untagged ports
        mock_bridgemems.return_value = ['eth1', 'eth12', 'eth13']
        assert_equals(self.piface.vlan_id(), 'untagged')
        # no ports
        mock_bridgemems.return_value = ['']
        assert_equals(self.piface.vlan_id(), 'untagged')
