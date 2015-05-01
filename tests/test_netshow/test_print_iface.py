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

import netshow.linux.print_iface as print_iface
import netshowlib.linux.iface as linux_iface
import mock
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace


class TestPrintIface(object):
    def setup(self):
        iface = linux_iface.Iface('eth22')
        self.piface = print_iface.PrintIface(iface)

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.read_from_sys')
    def test_linkstate(self, mock_read_from_sys):
        # admin down
        values = {'carrier': None}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        assert_equals(self.piface.linkstate, 'admdn')
        # down
        values = {'carrier': '0'}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        assert_equals(self.piface.linkstate, 'dn')
        # up
        self.piface.iface._linkstate = None # reset linkstate setting
        values = {'carrier': '1'}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        assert_equals(self.piface.linkstate, 'up')


    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_loopback')
    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_l3')
    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_subint')
    def test_port_category(self, mock_is_subint, mock_is_l3,
                           mock_is_loopback):
        # if l3 is true and is not loopback
        mock_is_loopback.return_value = False
        mock_is_l3.return_value = True
        mock_is_subint.return_value = False
        assert_equals(self.piface.port_category, 'access/l3')
        # if l3/subint is true
        mock_is_l3.return_value = True
        mock_is_subint.return_value = True
        assert_equals(self.piface.port_category, 'subint/l3')
        # if l3 is not true
        mock_is_l3.return_value = False
        assert_equals(self.piface.port_category, 'access')
        # is loopback and of cause l3
        mock_is_l3.return_value = True
        mock_is_loopback.return_value = True
        mock_is_subint.return_value = False
        assert_equals(self.piface.port_category, 'loopback')


    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.read_from_sys')
    def test_speed(self, mock_read_from_sys):
        # 100M
        mock_read_from_sys.return_value = '100'
        assert_equals(self.piface.speed, '100M')

        # 1G
        self.piface.iface._speed = None
        mock_read_from_sys.return_value = '1000'
        assert_equals(self.piface.speed, '1G')

        # 40G
        self.piface.iface._speed = None
        mock_read_from_sys.return_value = '40000'
        assert_equals(self.piface.speed, '40G')

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.read_from_sys')
    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.check_port_dhcp_assignment')
    def test_summary(self, mock_is_l3, mock_dhcp):
        # if not l3. summary is blank
        mock_is_l3.return_value = False
        assert_equals(self.piface.summary, [''])
        # is l3 but not dhcp
        mock_is_l3.return_value = True
        self.piface.iface.ip_address.ipv4 = ['10.1.1.1/24']
        assert_equals(self.piface.summary, ['10.1.1.1/24'])
        # is l3 and is dhcp
        self.piface.iface._ip_addr_assign = 1
        assert_equals(self.piface.summary, ['10.1.1.1/24(dhcp)'])

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.read_from_sys')
    def test_single_iface_cli_header(self, mock_read_from_sys):
        values = {'carrier': '1',
                  'address': '11:22:33:44:55:66',
                  'speed': '1000',
                  'mtu': '9000'}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        _output = self.piface.cli_header()
        assert_equals(_output.split('\n')[0].split(),
                      ['name', 'mac', 'speed', 'mtu', 'mode'])
        assert_equals(_output.split('\n')[2].split(),
                      ['up', 'eth22', '11:22:33:44:55:66', '1G',
                       '9000', 'access'])

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_l3')
    def test_ip_details(self, mock_is_l3):
        # if not l3.. print empty string
        mock_is_l3.return_value = False
        assert_equals(self.piface.ip_details(), '')
        # if l3, print ip details
        mock_is_l3.return_value = True
        self.piface.iface.ip_address.ipv4 = ['10.1.1.1/24']
        self.piface.iface.ip_neighbor._all_neighbors = {
            '10.1.1.2': '222',
            '10.1.1.3': '333'}
        _output = self.piface.ip_details()
        _outputtable = _output.split('\n')
        assert_equals(_outputtable[0], 'ip_details')
        assert_equals(_outputtable[2].split(), ['ip:', '10.1.1.1/24'])
        assert_equals(_outputtable[3].split(), ['arp_entries:', '2'])
