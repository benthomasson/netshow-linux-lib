# pylint: disable=E0611
from netshow.netshow import i18n_app
from tabulate import tabulate

_ = i18n_app('netshow-linux-lib')


def legend(show_legend=True):
    if not show_legend:
        return ''
    _table = []
    _table.append([_('legend') + ':', ''])
    _table.append([_('UP') + ':',
                   _('carrier up')])
    _table.append([_('UN') + ':',
                   _('carrier up, bond member not in bond')])
    _table.append([_('DN') + ':',
                   _('carrier down')])
    _table.append([_('ADMDN') + ':',
                   _('admin down use "ip link set <iface> up" to initialize')])
    _table.append([_('DRMNT') + ':',
                   _('carrier up, link dormant')])
    return '\n' + tabulate(_table) + '\n'
