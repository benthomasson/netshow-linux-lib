# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
# pylint: disable=W0613
import netshowlib.linux.ip_address as ip_address_mod
import netshowlib.linux.cache as feature_cache
from asserts import assert_equals
from nose.tools import set_trace
import mock

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestLinuxIpAddress(object):

    def test_ips(self):
        self.ip_address = ip_address_mod.IpAddress('eth1')
        self.ip_address.ipv4 = ['10.1.1.1/24']
        self.ip_address.ipv6 = ['10:1:1::1/64']
        assert_equals(self.ip_address.allentries, ['10.1.1.1/24', '10:1:1::1/64'])

    @mock.patch('netshowlib.linux.ip_address.parse_ip_cache')
    def test_cacheinfo(self, mock_parse):
        mock_parse.return_value = "hash of ips"
        result = ip_address_mod.cacheinfo()
        assert_equals(result, "hash of ips")

    @mock.patch('netshowlib.linux.ip_address.cacheinfo')
    def test_run_ip_address(self, mock_ip_cache):
        """ get ipv6 and ipv4 info """
        # using feature cache
        _output = open('tests/linux_tests/ip_addr_show.txt').read()
        output = StringIO(_output)
        mock_ip_cache.return_value = ip_address_mod.parse_ip_cache(output)
        _feature_cache = feature_cache.Cache()
        ip_address = ip_address_mod.IpAddress('eth0', _feature_cache)
        ip_address.run()
        assert_equals(ip_address.ipv4, ['192.168.0.33/24'])
        assert_equals(ip_address.ipv6, [])
        # without feature cache
        ip_address = ip_address_mod.IpAddress('eth0')
        ip_address.run()
        assert_equals(ip_address.ipv4, ['192.168.0.33/24'])
        assert_equals(ip_address.ipv6, [])

    def test_parse_ip_cache(self):
        """ testing parsing ip cache info """
        _output = open('tests/linux_tests/ip_addr_show.txt').read()
        output = StringIO(_output)
        result = ip_address_mod.parse_ip_cache(output)
        assert_equals(
            result,
            {
                'lo': {
                    'ipv4': [],
                    'ipv6': []
                },
                'net2compute': {
                    'ipv4': ['192.168.50.1/24'],
                    'ipv6': []
                },
                'virbr0': {
                    'ipv4': ['192.168.122.1/24'],
                    'ipv6': []
                },
                'vnet0': {
                    'ipv4': [],
                    'ipv6': []
                },
                'eth0': {
                    'ipv4': ['192.168.0.33/24'],
                    'ipv6': []
                }
            })
