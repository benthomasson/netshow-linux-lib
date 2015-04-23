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
import netshow.linux.show as show
from nose.tools import set_trace
import mock
from mock import MagicMock


def test_interface_related():
    for _val in ['trunk', 'access', 'l3',
                 'l2', 'bridge', 'bond', 'bondmem',
                 'bridgemem', 'interface']:

        results = {_val: True}
        assert_equals(show._interface_related(results), True)


