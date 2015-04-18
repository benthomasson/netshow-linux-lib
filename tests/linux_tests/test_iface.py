# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
import netshowlib.linux.iface as linux_iface
import netshowlib.linux.bridge as linux_bridge
import netshowlib.linux.bond as linux_bond
import netshowlib.linux.cache as linux_cache
import xml.etree.ElementTree as ET
import mock
from asserts import assert_equals, mod_args_generator, \
    mock_open_str, touch
from nose.tools import set_trace


@mock.patch('netshowlib.linux.iface.Iface.is_bond')
@mock.patch('netshowlib.linux.iface.Iface.is_bridge')
@mock.patch('netshowlib.linux.iface.Iface.is_bridgemem')
def test_iface_type(mock_bridgemem,
                    mock_bridge, mock_bond):
    # port is a bridge
    mock_bond.return_value = False
    mock_bridgemem.return_value = False
    mock_bridge.return_value = True
    eth1 = linux_iface.iface_type('eth1')
    assert_equals(isinstance(eth1, linux_bridge.Bridge), True)
    # port is bond
    mock_bridgemem.return_value = False
    mock_bridge.return_value = False
    mock_bond.return_value = True
    bond0 = linux_iface.iface_type('bond0')
    assert_equals(isinstance(bond0, linux_bond.Bond), True)
    # port is bridgemem
    mock_bridgemem.return_value = True
    mock_bridge.return_value = False
    mock_bond.return_value = False
    bridgemem = linux_iface.iface_type('eth2')
    assert_equals(isinstance(bridgemem, linux_bridge.BridgeMember), True)
    # regular port
    mock_bridge.return_value = False
    mock_bond.return_value = False
    eth2 = linux_iface.iface_type('eth2')
    assert_equals(isinstance(eth2, linux_iface.Iface), True)
    assert_equals(isinstance(eth2, linux_bond.Bond), False)
    assert_equals(isinstance(eth2, linux_bridge.Bridge), False)


class TestLinuxIface(object):
    """ Linux Iface tests """

    def setup(self):
        """ setup function """
        self.iface = linux_iface.Iface('eth1')

    @mock.patch('netshowlib.linux.lldp._exec_lldp')
    def test_lldp(self, mock_lldp):
        lldp_out = open('tests/linux_tests/lldp_output.txt').read()
        mock_lldp.return_value = ET.fromstring(lldp_out)
        lldp_output = self.iface.lldp
        # confirm correct number of lldp enabled ports
        assert_equals(len(lldp_output), 2)
        assert_equals(lldp_output[0].get('adj_hostname'), 'right')

    @mock.patch('netshowlib.linux.iface.common.os.readlink')
    def test_read_symlink(self, mock_readlink):
        mock_readlink.return_value = '../../bond25'
        assert_equals(self.iface.read_symlink('master'), 'bond25')
        mock_readlink.assert_called_with('/sys/class/net/eth1/master')

    def test_iface_constant_types(self):
        """ test that linux iface constants are set """
        assert_equals(linux_iface.L2_INT, 1)
        assert_equals(linux_iface.L3_INT, 2)
        assert_equals(linux_iface.BRIDGE_INT, 3)
        assert_equals(linux_iface.BOND_INT, 4)
        assert_equals(linux_iface.BONDMEM_INT, 5)
        assert_equals(linux_iface.TRUNK_INT, 6)
        assert_equals(linux_iface.MGMT_INT, 7)
        assert_equals(linux_iface.LOOPBACK_INT, 8)
        assert_equals(linux_iface.PHY_INT, 9)
        assert_equals(linux_iface.SUB_INT, 10)
        assert_equals(linux_iface.SVI_INT, 11)
        assert_equals(linux_iface.VXLAN_INT, 12)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_read_mac(self, mock_read_oneline):
        """ test reading mac address """
        _testmac = '11:22:33:44:55:66'
        mock_read_oneline.return_value = _testmac
        assert_equals(self.iface.mac, _testmac)
        mock_read_oneline.assert_called_with('/sys/class/net/eth1/address')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_read_mtu(self, mock_read_oneline):
        """ test reading mtu """
        _testmtu = '9000'
        mock_read_oneline.return_value = _testmtu
        assert_equals(self.iface.mtu, _testmtu)
        mock_read_oneline.assert_called_with('/sys/class/net/eth1/mtu')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_read_alias(self, mock_read_oneline):
        """ test reading interface description / alias """
        _alias = 'port description'
        mock_read_oneline.return_value = _alias
        assert_equals(self.iface.description, _alias)
        mock_read_oneline.assert_called_with('/sys/class/net/eth1/ifalias')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_read_speed(self, mock_read_oneline):
        """ test get speed """
        _speed = '1000'
        mock_read_oneline.return_value = _speed
        assert_equals(self.iface.speed, _speed)
        mock_read_oneline.assert_called_with('/sys/class/net/eth1/speed')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_read_link_state(self, mock_read_oneline):
        """ test get link state """
        # port is admin down
        mock_read_oneline.return_value = None
        assert_equals(self.iface.linkstate, 0)
        mock_read_oneline.assert_called_with('/sys/class/net/eth1/carrier')
        # port is down
        mock_read_oneline.return_value = '0'
        assert_equals(self.iface.linkstate, 1)
        # clear link_state
        self.iface._linkstate = None
        # port is up
        mock_read_oneline.return_value = '1'
        assert_equals(self.iface.linkstate, 2)

    @mock.patch('netshowlib.linux.ip_address.cacheinfo')
    def test_read_ipaddr(self, mock_cache_info):
        """ test reading IP address """
        # no cache provided.
        mock_cache_info.return_value = {'eth2': {
            'ipv4': ['192.168.1.1/24'], 'ipv6': ['10:1:1::1/128']}}
        self.iface = linux_iface.Iface('eth2')
        _ipaddr = self.iface.ip_address
        assert_equals(_ipaddr.ipv4, ['192.168.1.1/24'])
        new_cache = linux_cache.Cache()
        new_cache.ip_address = {'eth2': {'ipv4': ['10.1.1.1/24']}}
        self.iface = linux_iface.Iface('eth2', new_cache)
        assert_equals(self.iface.ip_address.ipv4, ['10.1.1.1/24'])

    # tests the _initial_tests functions as well
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    def test_is_bond(self, mock_path_exists):
        self.iface._name = 'bond0'
        values = {'/sys/class/net/bond0/bonding': True}
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.is_bond(), True)

    @mock.patch('netshowlib.linux.iface.os.path.exists')
    def test_is_bridge(self, mock_path_exists):
        self.iface._name = 'br0'
        values = {'/sys/class/net/br0/brif': True}
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.is_bridge(), True)

    @mock.patch('netshowlib.linux.iface.os.path.exists')
    def test_is_bondmem(self, mock_path_exists):
        values = {'/sys/class/net/eth1/master/bonding': True}
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.is_bondmem(), True)

    @mock.patch('netshowlib.linux.iface.glob.glob')
    def test_get_sub_interfaces(self, mock_listdir):
        mock_listdir.return_value = ['/stuff/m/eth1.25', '/stuff/m/eth1.100']
        result = self.iface.get_sub_interfaces()
        assert_equals(result, ['eth1.25', 'eth1.100'])
        mock_listdir.assert_called_with('/sys/class/net/eth1.*')

    @mock.patch('netshowlib.linux.iface.Iface.get_sub_interfaces')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    def test_is_bridgemem_port_type(self, mock_path_exists,
                                    mock_get_subints):
        # port is not a l2 port
        values = {'/sys/class/net/eth1/brport': False}
        mock_path_exists.side_effect = mod_args_generator(values)
        mock_get_subints.return_value = []
        assert_equals(self.iface.get_bridgemem_port_type(), 0)
        # port is not a l2 port but has subints that are l2 ports
        values = {'/sys/class/net/eth1/brport': False,
                  '/sys/class/net/eth1.100/brport': True}
        mock_get_subints.return_value = ['eth1.100']
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.get_bridgemem_port_type(), 2)

        # port is an access
        mock_get_subints.return_value = []
        values = {'/sys/class/net/eth1/brport': True}
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.get_bridgemem_port_type(), 1)
        # if port has native port that is in bridge and subints in bridge
        mock_get_subints.return_value = ['eth1.100']
        values = {'/sys/class/net/eth1/brport': True,
                  '/sys/class/net/eth1.100/brport': True}
        mock_path_exists.side_effect = mod_args_generator(values)
        assert_equals(self.iface.get_bridgemem_port_type(), 2)

    @mock.patch('netshowlib.linux.iface.Iface.get_bridgemem_port_type')
    def test_is_bridgemem_initial_test(self, mock_bridgemem_port):
        mock_bridgemem_port.return_value = 0
        assert_equals(self.iface.is_l2(), False)
        # check if access port
        mock_bridgemem_port.return_value = 1
        assert_equals(self.iface.is_l2(), True)
        assert_equals(self.iface.is_trunk(), False)
        assert_equals(self.iface.is_access(), True)
        assert_equals(self.iface.is_bridgemem(), True)
        # check if trunk port
        mock_bridgemem_port.return_value = 2
        assert_equals(self.iface.is_trunk(), True)
        assert_equals(self.iface.is_bridgemem(), True)

    def test_is_subint_initial_test(self):
        # port is not a subint int
        self.iface._name = 'eth1'
        assert_equals(self.iface.is_subint(), False)
        self.iface._name = 'eth1.100'
        assert_equals(self.iface.is_subint(), True)

    def test_is_loopback(self):
        assert_equals(self.iface.is_loopback(), False)
        self.iface._name = 'lo'
        assert_equals(self.iface.is_loopback(), True)

    def test_if_dhcp_file_is_empty(self):
        touch('/tmp/empty_file')
        dhcpfile = open('/tmp/empty_file')
        with mock.patch(mock_open_str()) as mock_open:
            mock_open.return_value = dhcpfile
            assert_equals(self.iface.ip_addr_assign, None)

    def test_checking_if_dhcp_is_used(self):
        dhcpfile = open('tests/linux_tests/dhclient.eth0.leases')
        # some fancy mocking to bypass ip address checking
        self.iface._ip_address = mock.MagicMock()
        self.iface.ip_address.allentries = ['192.168.122.64/24']
        # -----
        with mock.patch(mock_open_str()) as mock_open:
            mock_open.return_value = dhcpfile
            assert_equals(self.iface.ip_addr_assign, 'dhcp')
