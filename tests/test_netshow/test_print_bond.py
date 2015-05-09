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

import netshow.linux.print_bond as print_bond
import netshowlib.linux.bond as linux_bond
import mock
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace


class TestPrintBond(object):
    def setup(self):
        iface = linux_bond.Bond('eth22')
        self.piface = print_bond.PrintBond(iface)

    @mock.patch('netshowlib.linux.iface.Iface.read_from_sys')
    def test_hash_policy(self, mock_read_from_sys):
        mock_read_from_sys.return_value = 'layer3+4 1'
        assert_equals(self.piface.hash_policy, 'layer3+4')


    @mock.patch('netshowlib.linux.iface.Iface.read_from_sys')
    def test_bond_mode(self, mock_read_from_sys):
        mock_read_from_sys.return_value = '802.3ad 4'
        assert_equals(self.piface.mode, 'lacp')

    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_access')
    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_trunk')
    @mock.patch('netshow.linux.print_iface.linux_iface.Iface.is_l3')
    def test_port_category(self, mock_is_l3, mock_is_trunk, mock_is_access):
        # if l3
        mock_is_trunk.return_value = False
        mock_is_l3.return_value = True
        mock_is_access.return_value = False
        assert_equals(self.piface.port_category, 'bond/l3')
        # if trunk
        mock_is_l3.return_value = False
        mock_is_trunk.return_value = True
        mock_is_access.return_value = False
        assert_equals(self.piface.port_category, 'bond/trunk')
        # if access
        mock_is_l3.return_value = False
        mock_is_trunk.return_value = False
        mock_is_access.return_value = True
        assert_equals(self.piface.port_category, 'bond/access')

    @mock.patch('netshowlib.linux.iface.Iface.read_from_sys')
    @mock.patch('netshowlib.linux.bond.BondMember._parse_proc_net_bonding')
    def test_abbver_bondstate(self, mock_parse_proc, mock_read_from_sys):
        values = {'bonding/mode': '802.3ad 4'}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        bondmem = linux_bond.BondMember('eth22')
        bondmem._bondstate = 1
        assert_equals(self.piface.abbrev_bondstate(bondmem), 'P')
        bondmem._bondstate = 0
        assert_equals(self.piface.abbrev_bondstate(bondmem), 'D')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.Iface.read_from_sys')
    def test_print_bondmems(self, mock_read_from_sys,
                            mock_file_oneline):
        # ports up and in bond
        values = {'bonding/slaves': 'eth22 eth24',
                  'carrier': '1',
                  'bonding/mode': 'active-backup 2'}
        values2 = {}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        mock_file_oneline.side_effect = mod_args_generator(values2)
        _output = self.piface.print_bondmems()
        assert_equals(_output.split(), ['bondmems:', 'eth22(UP),', 'eth24(UP)'])
        # ports up but not in bond
        values = {'bonding/slaves': 'eth22 eth24',
                  'carrier': '1',
                  'bonding/mode': '802.3ad 4'}
        values2 = {}
        mock_read_from_sys.side_effect = mod_args_generator(values)
        mock_file_oneline.side_effect = mod_args_generator(values2)
        for _bondmem in self.piface.iface.members.values():
            _bondmem._bondstate = 0
        _output = self.piface.print_bondmems()
        assert_equals(_output.split(), ['bondmems:', 'eth22(UD),', 'eth24(UD)'])


    @mock.patch('netshow.linux.print_bond.PrintBond.access_summary')
    @mock.patch('netshow.linux.print_bond.PrintBond.trunk_summary')
    @mock.patch('netshow.linux.print_bond.PrintBond.print_bondmems')
    def test_summary(self, mock_bondmems, mock_trunk_summary, mock_access_summary):
        mock_trunk_summary.return_value = ['trunk summary']
        mock_access_summary.return_value = ['access summary']
        mock_bondmems.return_value = 'list of bondmembers'
        mock_is_l3 = mock.MagicMock(return_value=True)
        mock_is_trunk = mock.MagicMock(return_value=False)
        mock_is_access = mock.MagicMock(return_value=False)
        self.piface.iface.is_l3 = mock_is_l3
        self.piface.iface.is_trunk = mock_is_trunk
        self.piface.iface.is_access = mock_is_access
        self.piface.iface.ip_address.ipv4 = ['10.1.1.1/24']
        _output = self.piface.summary
        assert_equals(_output, ['list of bondmembers', '10.1.1.1/24'])
        # is not l3 but is a trunk
        mock_is_l3.return_value = False
        mock_is_trunk.return_value = True
        _output = self.piface.summary
        assert_equals(_output, ['list of bondmembers', 'trunk summary'])
        # is not trunk or l3
        mock_is_trunk.return_value = False
        mock_is_access.return_value = True
        _output = self.piface.summary
        assert_equals(_output, ['list of bondmembers', 'access summary'])
        # not l3 or l2
        mock_is_access.return_value = False
        _output = self.piface.summary
        assert_equals(_output, ['list of bondmembers'])

