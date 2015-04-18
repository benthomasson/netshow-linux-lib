""" Linux System Summary Info
"""
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
from netshowlib.linux import system_summary
import mock
from asserts import assert_equals
from nose.tools import set_trace


class TestSystemSummary(object):

    @mock.patch('netshowlib.linux.system_summary.common.distro_info')
    def setup(self, mock_distro_info):
        mock_distro_info.return_value = {'RELEASE': '14.04',
                                         'ID': 'Ubuntu',
                                         'DESCRIPTION': 'Ubuntu 14.04.1 LTS'}
        self.systemsummary = system_summary.SystemSummary()

    def test_init(self):
        assert_equals(self.systemsummary.os_name, 'Ubuntu')
        assert_equals(self.systemsummary.os_build, 'Ubuntu 14.04.1 LTS')
        assert_equals(self.systemsummary.version, '14.04')

    @mock.patch('netshowlib.linux.system_summary.common.read_file_oneline')
    def test_uptime(self, mock_read_file):
        mock_read_file.return_value = '100'
        assert_equals(self.systemsummary.uptime, '100')
        mock_read_file.assert_called_with('/proc/uptime')
