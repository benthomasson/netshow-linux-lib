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


class TestSystemSummary(object):

    def setup(self):
        self.systemsummary = system_summary.SystemSummary()

    @mock.patch('netshowlib.linux.system_summary.common.read_file_oneline')
    def test_uptime(self, mock_read_file):
        mock_read_file.return_value = '100'
        assert_equals(self.systemsummary.uptime, '100')
        mock_read_file.assert_called_with('/proc/uptime')
