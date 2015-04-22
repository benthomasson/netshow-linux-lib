""" Linux LACP module tests
"""
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
import netshowlib.linux.lacp as linux_lacp
import mock
from asserts import assert_equals
from nose.tools import set_trace


class TestLinuxLacp(object):
    """ Linux LACP tests """

    def setup(self):
        """ setup function """
        self.lacp = linux_lacp.Lacp('bond0')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_getting_lacp_rate(self, mock_file_oneline):
        mock_file_oneline.return_value = 'fast 1'
        assert_equals(self.lacp.rate, '1')
        mock_file_oneline.assert_called_with(
            '/sys/class/net/bond0/bonding/lacp_rate')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_getting_sys_priority(self, mock_file_oneline):
        mock_file_oneline.return_value = '65535'
        assert_equals(self.lacp.sys_priority, '65535')
        mock_file_oneline.assert_called_with(
            '/sys/class/net/bond0/bonding/ad_sys_priority')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_partner_mac_address(self, mock_file_oneline):
        result = '00:00:00:11:11:11'
        mock_file_oneline.return_value = result
        assert_equals(self.lacp.partner_mac, result)
        mock_file_oneline.assert_called_with(
            '/sys/class/net/bond0/bonding/ad_partner_mac')
