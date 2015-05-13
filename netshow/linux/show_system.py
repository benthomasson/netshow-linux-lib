""" Module for printing out basic linux system information
"""

from netshowlib.linux.system_summary import SystemSummary
from flufl.i18n import initialize
from datetime import timedelta
import json
from netshow.linux.netjson_encoder import NetEncoder

_ = initialize('netshow-linux-lib')


class ShowSystem(object):
    """
    Class responsible for printing out basic linux system summary info
    """
    def __init__(self, **kwargs):
        self.use_json = kwargs.get('--json') or kwargs.get('-j')
        self.system = SystemSummary()

    def run(self):
        """
        :return: output regarding system like OS type, etc
        """
        if self.use_json:
            return json.dumps(self,
                              cls=NetEncoder, indent=4)
        else:
            return self.cli_output()

    def cli_output(self):
        """
        print linux basic system output on a terminal
        """
        _str = ''
        _str += "%s %s\n" % (self.system.os_name,
                             self.system.version)
        _str += "%s: %s\n" % (_('build'), self.system.os_build)
        _str += "%s: %s\n" % (_('uptime'), self.uptime)
        return _str

    @property
    def uptime(self):
        """
        :return: system uptime in humanly readable form
        """
        return str(timedelta(
            seconds=int(float(self.system.uptime))))
