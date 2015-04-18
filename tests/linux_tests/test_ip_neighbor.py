# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
# pylint: disable=E0611
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace
import mock
from netshowlib.linux import ip_neighbor


@mock.patch('netshowlib.linux.ip_neighbor.common.exec_command')
def test_cacheinfo(mock_arp_exec):
    values = {
        '/sbin/ip -4 neighbor show':
        str.encode(open('tests/linux_tests/arp_ipv4.txt').read()),
        '/sbin/ip -6 neighbor show':
        str.encode(open('tests/linux_tests/arp_ipv6.txt').read())
    }

    mock_arp_exec.side_effect = mod_args_generator(values)
    result = ip_neighbor.cacheinfo()
    assert_equals(len(result.get('eth0').get('ipv4')), 1)
    assert_equals(len(result.get('eth0').get('ipv6')), 0)
    assert_equals(len(result.get('vlan1').get('ipv4')), 7)
    assert_equals(len(result.get('vlan1').get('ipv6')), 4)


class TestIpNeighbor(object):
    def setup(self):
        self.ipneigh = ip_neighbor.IpNeighbor('eth1')

    @mock.patch('netshowlib.linux.ip_neighbor.cacheinfo')
    def test_run(self, mock_cacheinfo):
        mock_cacheinfo.return_value = {'eth1':
                                       {'ipv4':
                                        {'10.1.1.1': '11:22:33:44:55:66'},
                                        'ipv6': {}}}
        self.ipneigh.run()
        assert_equals(self.ipneigh.ipv4, {'10.1.1.1': '11:22:33:44:55:66'})

    @mock.patch('netshowlib.linux.ip_neighbor.cacheinfo')
    def test_all_neighbors(self, mock_cacheinfo):
        mock_cacheinfo.return_value = {'eth1':
                                       {'ipv4': {'10.1.1.1':
                                                 '11:22:33:44:55:66'},
                                        'ipv6': {'10:1:1::1':
                                                 '11:22:33:44:55:66'}}}
        assert_equals(self.ipneigh.allentries,
                      {'10.1.1.1': '11:22:33:44:55:66',
                       '10:1:1::1': '11:22:33:44:55:66'})
