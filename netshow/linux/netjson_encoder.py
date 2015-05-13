# pylint: disable=E0202
"""
Module for Converting python class attributes into JSON
"""
from json import JSONEncoder


class NetEncoder(JSONEncoder):
    """
    NetEncoder is my custom JSONEncoder class that prints out
    the json output of any PrintIface Class or subclass.
    """
    def default(self, obj):
        # print out properties
        property_names = [_p for _p in dir(obj.__class__) if isinstance(
            getattr(obj.__class__, _p), property)]
        _hash = {}
        for _property in property_names:
            _hash[_property] = getattr(obj, _property)
        if hasattr(obj, 'iface'):
            _hash['iface_obj'] = obj.iface
        elif hasattr(obj, 'system'):
            _hash['system_obj'] = obj.system.__dict__
        return _hash
