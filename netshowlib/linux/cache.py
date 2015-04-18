"""
This module produces the cache info for Linux
"""

from netshowlib import netshowlib as nnlib


class Cache(object):
    """
    This class produces the cache info for Linux \
        networking such as ip addressing, lldp, QOS
    """
    def __init__(self):
        self.ipaddr = {}
        self.lldp = {}
        self.stp = {}
        self.feature_list = ['ip_neighbor', 'lldp', 'ip_address']
        self.run()

    def run(self, features=None):
        """
        :param features:  List of features to enable. If set to ``None`` \
            cache from all features is obtained

        :return:  returns Cache instance of appropriate OS type
        """
        _featurelist = self.feature_list
        if features:
            _featurelist = features

        for _feature in _featurelist:
            _feature_mod = nnlib.import_module('netshowlib.linux.' + _feature)
            self.__dict__[_feature] = _feature_mod.cacheinfo()
