# pylint: disable=E0611
from netshow.netshow import i18n_app
from tabulate import tabulate

_ = i18n_app('netshow-linux-lib')


def bondmem_key_simple():
    """
    explains what the P and N stand for next to bond members
    """
    bond_key = _('bondmember key') + ':'
    in_bond = "(%s)-%s" % (_('P'), _('in bond'))
    not_in_bond = "(%s)-%s" % (_('N'), _('not in bond'))
    _table = [in_bond, not_in_bond]
    _table_entry = ','.join(_table)
    return '\n' + tabulate([[bond_key, _table_entry]], tablefmt='plain') + '\n\n'


def bondmem_key_with_carrier():
    """
    explains what the UP and UN and DN stand for next to bond members
    """
    bond_key = _('bondmember key') + ':'
    in_bond = "(%s)-%s" % (_('UP'), _('carrier up, in bond'))
    not_in_bond = "(%s)-%s" % (_('UN'), _('carrier up, not in bond'))
    down_not_in_bond = "(%s)-%s" % (_('DN'), _('carrier down, not in bond'))
    _table = [in_bond, not_in_bond, down_not_in_bond]
    _table_entry = ','.join(_table)
    return '\n' + tabulate([[bond_key, _table_entry]], tablefmt='plain') + '\n\n'
