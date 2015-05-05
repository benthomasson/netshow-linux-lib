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
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace
import re


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

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_tagged_ifaces(self, mock_listdirs):
        # if list of tagged ports exists
        bridgemems = ['bond0.100', 'bond1.100', 'eth9.100', 'eth10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.piface.tagged_ifaces().split(),
                      ['tagged:', 'bond0-1,eth9-10'])
        # if list of tagged ports does not exist
        bridgemems = ['bond0', 'bond1', 'eth9', 'eth10']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.piface.tagged_ifaces(), '')

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_untagged_ifaces(self, mock_listdirs):
        # list of untagged ports exists
        bridgemems = ['bond0', 'bond1', 'eth9', 'eth10']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.piface.untagged_ifaces().split(),
                      ['untagged:', 'bond0-1,eth9-10'])
        # list has no untagged ports
        bridgemems = ['bond0.100', 'bond1.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.piface.untagged_ifaces(), '')

    @mock.patch('netshow.linux.print_bridge.PrintBridge.stp_summary')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.untagged_ifaces')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.tagged_ifaces')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.vlan_id')
    def test_summary(self, mock_vlan_id, mock_tagged, mock_untagged,
                     mock_stp_summary):
        manager = mock.MagicMock()
        manager.attach_mock(mock_stp_summary, 'stp_summary')
        manager.attach_mock(mock_vlan_id, 'vlan_id')
        manager.attach_mock(mock_tagged, 'tagged_ifaces')
        manager.attach_mock(mock_untagged, 'untagged_ifaces')
        self.piface.summary
        expected_calls = [mock.call.untagged_ifaces(),
                          mock.call.tagged_ifaces(),
                          mock.call.vlan_id(),
                          mock.call.stp_summary()]
        assert_equals(manager.method_calls, expected_calls)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.bridge.os.listdir')
    @mock.patch('netshowlib.linux.bridge.Bridge.read_from_sys')
    @mock.patch('netshowlib.linux.bridge.KernelStpBridge.is_root')
    def test_stp_summary(self, mock_is_root, mock_read_from_sys,
                         mock_listdir, mock_oneline):
        # if stp is disabled
        mock_read_from_sys.return_value = '0'
        assert_equals(self.piface.stp_summary().split(), ['stp:', 'disabled'])
        # if stp is root
        values = {
            'bridge/stp_state': '1',
            'bridge/root_id': '4000.fe54007e7eeb',
            'bridge/bridge_id': '4000.fe54007e7eeb'}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        mock_is_root.return_value = True
        assert_equals(self.piface.stp_summary().split(), ['stp:', 'rootswitch(16384)'])
        # if stp is not root
        values = {
            'bridge/stp_state': '1',
            'bridge/root_id': '4000.fe54007e7eeb',
            'bridge/bridge_id': '8000.fe54007e7111'}
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth1/brport/port_id': '1',
            '/sys/class/net/eth2/brport/state': '0',
            '/sys/class/net/eth2/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2/brport/port_id': '2',
        }
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_read_from_sys.side_effect = mod_args_generator(values)
        mock_is_root.return_value = False
        mock_listdir.return_value = ['eth1', 'eth2']
        assert_equals(self.piface.stp_summary().split(),
                      ['stp:', 'eth1(root)', '16384(root_priority)'])

    @mock.patch('netshowlib.linux.bridge.KernelStpBridge.is_root')
    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.bridge.os.listdir')
    @mock.patch('netshowlib.linux.bridge.Bridge.read_from_sys')
    def test_stp_details(self, mock_read_sys, mock_listdir,
                         mock_file_oneline, mock_is_root):
        mock_is_root.return_value = False
        mock_listdir.return_value = ['eth1', 'eth2']
        values1 = {
            'bridge/stp_state': '1',
            'bridge/root_id': '4000.fe54007e7eeb',
            'bridge/bridge_id': '8000.fe54007e7111'}
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth1/brport/port_id': '1',
            '/sys/class/net/eth2/brport/state': '0',
            '/sys/class/net/eth2/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2/brport/port_id': '2',
        }
        mock_read_sys.side_effect = mod_args_generator(values1)
        mock_file_oneline.side_effect = mod_args_generator(values2)
        _output = self.piface.stp_details()
        _outputtable = _output.split('\n')
        assert_equals(re.split(r'\s{2,}', _outputtable[2]),
                      ['stp_mode:', '802.1d / per bridge instance'])
        assert_equals(_outputtable[3].split(),
                      ['root_port:', 'eth1'])
        assert_equals(_outputtable[4].split(),
                      ['root_priority:', '16384'])
        assert_equals(_outputtable[5].split(), ['bridge_priority:', '32768'])
        assert_equals(_outputtable[6].split(), ['vlan_id:', 'untagged'])

    @mock.patch('netshowlib.linux.bridge.Bridge.read_from_sys')
    def test_no_stp_details(self, mock_read_from_sys):
        mock_read_from_sys.return_value = '0'
        _output = self.piface.no_stp_details()
        _outputtable = _output.split('\n')
        assert_equals(_outputtable[2].split(),
                      ['stp_mode:', 'disabled'])
        assert_equals(_outputtable[3].split(),
                      ['vlan_id:', 'untagged'])

    @mock.patch('netshowlib.linux.bridge.Bridge.read_from_sys')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.cli_header')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.ip_details')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.stp_details')
    @mock.patch('netshow.linux.print_bridge.PrintBridge.no_stp_details')
    def test_cli_output(self, mock_no_stp_details, mock_stp_details, mock_ip_details,
                        mock_cli_header, mock_read_from_sys):
        manager = mock.MagicMock()
        manager.attach_mock(mock_no_stp_details, 'no_stp_details')
        manager.attach_mock(mock_stp_details, 'stp_details')
        manager.attach_mock(mock_ip_details, 'ip_details')
        manager.attach_mock(mock_cli_header, 'cli_header')
        self.piface.cli_output()
        # stp enabled
        expected_calls = [mock.call.cli_header(),
                          mock.call.ip_details(),
                          mock.call.stp_details()]
        assert_equals(manager.method_calls, expected_calls)
        # stp disabled
        manager.reset_mock()
        mock_read_from_sys.return_value = '0'
        self.piface.cli_output()
        expected_calls = [mock.call.cli_header(),
                          mock.call.ip_details(),
                          mock.call.no_stp_details()]
        assert_equals(manager.method_calls, expected_calls)

    @mock.patch('netshowlib.linux.bridge.KernelStpBridge.is_root')
    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.bridge.os.listdir')
    @mock.patch('netshowlib.linux.bridge.Bridge.read_from_sys')
    def test_ports_in_fwd_state(self, mock_read_sys, mock_listdir,
                                mock_oneline,
                                mock_is_root):
        values1 = {
            'bridge/stp_state': '1',
            'bridge/root_id': '4000.fe54007e7eeb',
            'bridge/bridge_id': '8000.fe54007e7111'}
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth1/brport/port_id': '1',
            '/sys/class/net/eth2/brport/state': '3',
            '/sys/class/net/eth2/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth2/brport/bridge/bridge/root_port': '1',
            '/sys/class/net/eth2/brport/port_id': '2',
        }
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_read_sys.side_effect = mod_args_generator(values1)
        mock_is_root.return_value = True
        mock_listdir.return_value = ['eth1', 'eth2']
        _output = self.piface.ports_in_fwd_state()
        _outputtable = _output.split('\n')
        assert_equals(_outputtable[0], 'ports_in_fwding_state')
        assert_equals(_outputtable[2], 'eth1-2')


