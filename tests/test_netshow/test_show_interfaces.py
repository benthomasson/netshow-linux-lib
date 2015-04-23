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

from collections import OrderedDict
from asserts import assert_equals, mod_args_generator
import netshow.linux.show_interfaces as showint
import netshow.linux.print_iface as print_iface
from nose.tools import set_trace
import mock
from mock import MagicMock


class TestShowInterfaces(object):

    def setup(self):
        results = {'l2': True}
        self.showint = showint.ShowInterfaces(**results)

    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_single_iface')
    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_many_ifaces')
    def test_run_single_iface(self, mock_many, mock_single):
        # single interface config
        self.showint.single_iface = True
        self.showint.run()
        assert_equals(mock_single.call_count, 1)

    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_single_iface')
    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_many_ifaces')
    def test_run_many_iface(self, mock_many, mock_single):
        # single interface config
        self.showint.single_iface = False
        self.showint.run()
        assert_equals(mock_many.call_count, 1)
        assert_equals(mock_single.call_count, 0)

    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_json_many_ifaces')
    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_cli_many_ifaces')
    def test_many_ifaces_cli_output(self, mock_cli_ifaces, mock_json_ifaces):
        # if json is false get cli output
        self.showint.print_many_ifaces()
        mock_cli_ifaces.assert_called_with('l2')

    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_json_many_ifaces')
    @mock.patch('netshow.linux.show_interfaces.ShowInterfaces.print_cli_many_ifaces')
    def test_many_ifaces_json_output(self, mock_cli_ifaces, mock_json_ifaces):
        # if json is false get cli output
        self.showint.use_json = True
        self.showint.print_many_ifaces()
        mock_json_ifaces.assert_called_with('l2')

    @mock.patch('netshow.linux.show_interfaces.linux_iface.portname_list')
    @mock.patch('netshow.linux.print_iface.PrintIface.is_trunk')
    def test_many_cli_ifaces(self, mock_is_trunk, mock_portlist):
        mock_portlist.return_value = ['eth1', 'eth2']
        mock_is_trunk.return_value = True
        set_trace()
        _table = self.showint.print_cli_many_ifaces('l2')
