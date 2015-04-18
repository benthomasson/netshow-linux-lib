# http://pylint-messages.wikidot.com/all-codes
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

from asserts import assert_equals, mod_args_generator
import netshowlib.linux.cache as linux_cache
from nose.tools import set_trace
import mock
from mock import MagicMock


class TestLinuxCache(object):

    def setup(self):
        self.cache = linux_cache.Cache()

    def test_feature_list(self):
        assert_equals(self.cache.feature_list, ['ip_neighbor', 'lldp', 'ip_address'])

    @mock.patch('netshowlib.netshowlib.import_module')
    def test_cache_feature_runs(self, mock_import):
        # test if features=None
        self.cache.run()
        assert_equals(
            mock_import.call_args_list,
            [mock.call('netshowlib.linux.ip_neighbor'),
             mock.call('netshowlib.linux.lldp'),
             mock.call('netshowlib.linux.ip_address')]
        )
        mock_import.reset_mock()
        # test if features=['ipaddr']
        mock_ipaddr = MagicMock()
        mock_ipaddr.cacheinfo.return_value = 'ip cache info'
        values = {'netshowlib.linux.ipaddr': mock_ipaddr}
        mock_import.side_effect = mod_args_generator(values)
        self.cache.run(features=['ipaddr'])
        assert_equals(
            mock_import.call_args_list,
            [mock.call('netshowlib.linux.ipaddr')])
        assert_equals(self.cache.ipaddr, 'ip cache info')
