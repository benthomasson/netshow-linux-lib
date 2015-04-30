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




