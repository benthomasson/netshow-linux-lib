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

from asserts import assert_equals
import netshow.linux.show_system as show_system
import mock
import json
import re


class TestShowSystem(object):

    def setup(self):
        results = {'json': False}
        self.system = show_system.ShowSystem(results)

    @mock.patch('netshowlib.linux.system_summary.common.distro_info')
    @mock.patch('netshowlib.linux.system_summary.common.read_file_oneline')
    def test_run(self, mock_read_file,
                 mock_distro_info):
        mock_distro_info.return_value = {'RELEASE': '14.04',
                                         'ID': 'Ubuntu',
                                         'DESCRIPTION': 'Ubuntu 14.04.1 LTS'}
        # using json
        mock_read_file.return_value = '100'
        results = {'--json': True}
        _systemsum = show_system.ShowSystem(results)
        _output = _systemsum.run()
        assert_equals(json.loads(_output).get('system_dict').get('version'),
                      '14.04')
        # not using json
        results = {'--json': False}
        _systemsum = show_system.ShowSystem(results)
        _output = _systemsum.run()
        assert_equals(_output.split('\n')[0].split(), ['Ubuntu', '14.04'])
        assert_equals(re.split(r':\s+',
                               _output.split('\n')[1]),
                      ['build', 'Ubuntu 14.04.1 LTS'])
        assert_equals(_output.split('\n')[2].split(), ['uptime:', u'0:01:40'])
