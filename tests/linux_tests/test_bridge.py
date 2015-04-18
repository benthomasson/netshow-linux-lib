""" Linux Bridge Module tests
"""
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
import netshowlib.linux.bridge as linux_bridge
import mock
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace
from mock import MagicMock


class TestKernelStpBridgeMem(object):
    """ Kernel stp bridgemember class tests"""
    def setup(self):
        self.iface = linux_bridge.BridgeMember('eth1')
        self.stp = linux_bridge.KernelStpBridgeMember(self.iface)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    @mock.patch('netshowlib.linux.common.read_symlink')
    def test_state_access_port(self, mock_symlink, mock_os_path,
                               mock_oneline):
        mock_subint = MagicMock()
        self.iface.get_sub_interfaces = mock_subint
        # bridgemember is access port
        mock_subint = []
        mock_symlink.return_value = 'br10'
        values = {
            '/sys/class/net/eth1/brport': True
        }
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': 'aaa',
            '/sys/class/net/eth1/brport/port_id': 'aaa'
        }
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_os_path.side_effect = mod_args_generator(values)
        briface = linux_bridge.Bridge('br10')
        linux_bridge.BRIDGE_CACHE['br10'] = briface
        assert_equals(self.stp.state, {
            'disabled': [],
            'blocking': [],
            'forwarding': [briface],
            'root': [briface],
            'intransition': [],
            'stp_disabled': []
        })

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    @mock.patch('netshowlib.linux.common.read_symlink')
    def test_state_trunk_port(self, mock_symlink, mock_os_path,
                              mock_oneline):
        mock_subint = MagicMock()
        mock_subint.return_value = ['eth1.11', 'eth1.20', 'eth1.30']
        self.iface.get_sub_interfaces = mock_subint
        # bridgemember is trunk port
        values = {
            '/sys/class/net/eth1/brport': True,
            '/sys/class/net/eth1.11/brport': True,
            '/sys/class/net/eth1.20/brport': False,
            '/sys/class/net/eth1.30/brport': True,
        }
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': 'aaa',
            '/sys/class/net/eth1/brport/port_id': 'aaa',
            '/sys/class/net/eth1.11/brport/state': '0',
            '/sys/class/net/eth1.11/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth1.11/brport/bridge/bridge/root_port': 'aaa',
            '/sys/class/net/eth1.11/brport/port_id': 'aaa',
            '/sys/class/net/eth1.30/brport/state': '0',
            '/sys/class/net/eth1.30/brport/bridge/bridge/stp_state': '0'

        }
        values3 = {
            '/sys/class/net/eth1/brport/bridge': 'br10',
            '/sys/class/net/eth1.11/brport/bridge': 'br11',
            '/sys/class/net/eth1.20/brport/bridge': None,
            '/sys/class/net/eth1.30/brport/bridge': 'br30'
        }
        mock_symlink.side_effect = mod_args_generator(values3)
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_os_path.side_effect = mod_args_generator(values)
        br10 = linux_bridge.Bridge('br10')
        br11 = linux_bridge.Bridge('br11')
        br30 = linux_bridge.Bridge('br30')
        linux_bridge.BRIDGE_CACHE['br10'] = br10
        linux_bridge.BRIDGE_CACHE['br11'] = br11
        linux_bridge.BRIDGE_CACHE['br30'] = br30
        assert_equals(self.stp.state, {
            'disabled': [br11],
            'blocking': [],
            'forwarding': [br10],
            'root': [br10],
            'stp_disabled': [br30],
            'intransition': []
        })


class TestKernelStpBridge(object):
    def setup(self):
        br0 = linux_bridge.Bridge('br0')
        self.stp = linux_bridge.KernelStpBridge(br0)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_root_priority(self, mock_read_oneline):
        mock_read_oneline.return_value = '8000.112233445566'
        assert_equals(self.stp.root_priority, '32768')
        mock_read_oneline.assert_called_with(
            '/sys/class/net/br0/bridge/root_id')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_bridge_priority(self, mock_read_oneline):
        mock_read_oneline.return_value = '4000.112233445566'
        assert_equals(self.stp.root_priority, '16384')
        mock_read_oneline.assert_called_with(
            '/sys/class/net/br0/bridge/root_id')

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    def test_member_state(self, mock_os_path,
                          mock_oneline, mock_listdir):
        # bridge has only untagged ports
        mock_listdir.return_value = ['eth1', 'eth2']
        values = {
            '/sys/class/net/eth1/brport': True,
            '/sys/class/net/eth2/brport': True,
        }
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth1/brport/port_id': '1',
            '/sys/class/net/eth2/brport/state': '0',
            '/sys/class/net/eth2/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2/brport/port_id': '2',
        }

        mock_os_path.side_effect = mod_args_generator(values)
        mock_oneline.side_effect = mod_args_generator(values2)
        eth1 = self.stp.bridge.members.get('eth1')
        eth2 = self.stp.bridge.members.get('eth2')
        assert_equals(self.stp.member_state, {
            'disabled': [eth2],
            'blocking': [],
            'forwarding': [eth1],
            'root': [eth1],
            'intransition': []
        })

        # bridge has only tagged ports
        mock_listdir.return_value = ['eth1.1', 'eth2.1']
        values = {
            '/sys/class/net/eth1/brport': True,
            '/sys/class/net/eth2/brport': True,
        }
        values2 = {
            '/sys/class/net/eth1.1/brport/state': '3',
            '/sys/class/net/eth1.1/brport/bridge/bridge/root_port': '2',
            '/sys/class/net/eth1.1/brport/port_id': '2',
            '/sys/class/net/eth2.1/brport/state': '0',
            '/sys/class/net/eth2.1/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2.1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2.1/brport/port_id': '10',
        }

        mock_os_path.side_effect = mod_args_generator(values)
        mock_oneline.side_effect = mod_args_generator(values2)
        eth1 = self.stp.bridge.members.get('eth1')
        eth2 = self.stp.bridge.members.get('eth2')
        assert_equals(self.stp.member_state, {
            'disabled': [eth2],
            'blocking': [],
            'forwarding': [eth1],
            'root': [eth1],
            'intransition': []
        })

        # bridge has mix of tagged and untagged ports
        mock_listdir.return_value = ['eth1.1', 'eth2.1', 'eth3']
        values = {
            '/sys/class/net/eth1/brport': True,
            '/sys/class/net/eth2/brport': True,
            '/sys/class/net/eth3/brport': True,
        }
        values2 = {
            '/sys/class/net/eth1.1/brport/state': '3',
            '/sys/class/net/eth1.1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth1.1/brport/port_id': '1',
            '/sys/class/net/eth2.1/brport/state': '0',
            '/sys/class/net/eth2.1/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2.1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2.1/brport/port_id': '3',
            '/sys/class/net/eth3/brport/state': '3',
            '/sys/class/net/eth3/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth3/brport/port_id': '5',
        }

        mock_os_path.side_effect = mod_args_generator(values)
        mock_oneline.side_effect = mod_args_generator(values2)
        eth1 = self.stp.bridge.members.get('eth1')
        eth2 = self.stp.bridge.members.get('eth2')
        eth3 = self.stp.bridge.members.get('eth3')
        assert_equals(self.stp.member_state, {
            'disabled': [eth2],
            'blocking': [],
            'forwarding': [eth1, eth3],
            'root': [eth1],
            'intransition': []
        })

        # bridge does not have any members but STP is enabled
        mock_listdir.return_value = []
        mock_os_path.side_effect = {}
        mock_oneline.side_effect = {}
        assert_equals(self.stp.member_state, {
            'disabled': [],
            'blocking': [],
            'forwarding': [],
            'root': [],
            'intransition': []
        })


class TestLinuxBridgeMember(object):
    """ Linux Bridgemember tests"""

    def setup(self):
        """ setup function """
        self.iface = linux_bridge.BridgeMember('eth2')

    def test_attributes(self):
        assert_equals(isinstance(self.iface.stp,
                                 linux_bridge.KernelStpBridgeMember), True)


class TestLinuxBridge(object):
    """ Linux Bridge tests """

    def setup(self):
        """ setup function """
        self.iface = linux_bridge.Bridge('br0')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_stp(self, mock_read_oneline):
        """ test getting STP """
        # if STP is disabled
        mock_read_oneline.return_value = '0'
        assert_equals(self.iface.stp, None)
        mock_read_oneline.assert_called_with('/sys/class/net/br0/bridge/stp_state')
        # if stp is enabled
        mock_read_oneline.return_value = '1'
        assert_equals(isinstance(self.iface.stp,
                                 linux_bridge.KernelStpBridge), True)

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_list_of_bridge_members(self, mock_listdirs):
        bridgemems = ['eth8', 'eth9']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.members.keys())), sorted(bridgemems))
        assert_equals(isinstance(self.iface.members.get('eth8'),
                                 linux_bridge.BridgeMember), True)
        mock_listdirs.assert_called_with('/sys/class/net/br0/brif')

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_tagged_bridge_members(self, mock_listdirs):
        bridgemems = ['eth7', 'eth8', 'eth9.100', 'eth10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.tagged_members.keys())),
                      sorted(['eth9', 'eth10']))

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_untagged_bridge_members(self, mock_listdirs):
        bridgemems = ['eth7', 'eth8', 'eth9.100', 'eth10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.untagged_members.keys())),
                      sorted(['eth7', 'eth8']))

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_vlan_tag(self, mock_listdirs):
        # single tag
        bridgemems = ['eth7', 'eth8', 'eth9.100', 'eth10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '100')
        # multiple tags
        bridgemems = ['eth7', 'eth8', 'eth9.100', 'eth10.100',
                      'eth11.10', 'eth12.3']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '3, 10, 100')
        # no tag
        bridgemems = ['eth7', 'eth8']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '')
