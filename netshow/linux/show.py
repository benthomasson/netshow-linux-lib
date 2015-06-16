# print() is required for py3 not py2. so need to disable C0325
# pylint: disable=C0325

"""
Usage:
    netshow neighbors [--json | -j ]
    netshow system [--json | -j ]
    netshow [interface] [ access | bridges | bonds | bondmems | mgmt | l2 | l3 | trunks | <iface> ] [all] [--mac | -m ] [--oneline | -1  | --json | -j]
    netshow (--version | -v)

Help:
    * default is to show intefaces only in the UP state.
    interface                 summary info of all interfaces
    interface access          summary of physical ports with l2 or l3 config
    interface bonds           summary of bonds
    interface bondmems        summary of bond members
    interface bridges         summary of ports with bridge members
    interface trunks          summary of trunk interfaces
    interface mgmt            summary of mgmt ports
    interface l3              summary of ports with an IP.
    interface l2              summary of access, trunk and bridge interfaces
    interface <interface>     list summary of a single interface
    system                    system information
    neighbors                 physical device neighbor information

Options:
    all        show all ports include those are down or admin down
    --mac      show inteface MAC in output
    --version  netshow software version
    --oneline  output each entry on one line
    -1         alias for --oneline
    --json     print output in json
"""

import sys
from network_docopt import NetworkDocopt
from netshowlib._version import get_version
from netshow.linux.show_interfaces import ShowInterfaces
from netshow.linux.show_neighbors import ShowNeighbors
from netshow.linux.show_system import ShowSystem


def _interface_related(results):
    """ give user ability to issue `show bridge` and other
    interface related commands without the interface keyword
    """

    for _result in ('access', 'bondmems', 'bonds',
                    'bridges', 'interface', 'l2',
                    'l3', 'mgmt', 'phy', 'trunks',
                    '<iface>'):
        if results.get(_result):
            return True
    return False


def run():
    """ run linux netshow version """
    if sys.argv[-1] == 'options':
        print_options = True
        sys.argv = sys.argv[0:-1]
    else:
        print_options = False

    cl = NetworkDocopt(__doc__)
    if print_options:
        cl.print_options()
    else:

        if _interface_related(cl):
            _showint = ShowInterfaces(cl)
            print(_showint.run())
        elif cl.get('system'):
            _showsys = ShowSystem(cl)
            print(_showsys.run())
        elif cl.get('neighbors'):
            _shownei = ShowNeighbors(cl)
            print(_shownei.run())
        elif cl.get('--version') or cl.get('-v'):
            print(get_version())
        else:
            print(__doc__)
