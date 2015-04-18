# http://pylint-messages.wikidot.com/all-codes
# disable too few public methods message
# pylint: disable=R0903
"""
System Overview:  Uptime, OS Distribution and CPU Architecture
"""
from netshowlib.linux import common
import platform


class SystemSummary(object):
    """
    Class provides some details regarding the system OS

    * **uptime**: uptime of the linux device
    * **arch**: CPU architecture
    * **version**: OS Distribution Version
    * **os_name**: OS Distribution Name
    * **os_build**: OS Build number if available.
    """

    def __init__(self):
        self.distro_info = common.distro_info()
        self.arch = platform.machine()
        self.version = self.distro_info.get('RELEASE')
        self.os_name = self.distro_info.get('ID')
        self.os_build = self.distro_info.get('DESCRIPTION')
        self._uptime = None

    @property
    def uptime(self):
        """
        :return: uptime of the linux device in seconds
        """
        filepath = '/proc/uptime'
        uptime = common.read_file_oneline(filepath)
        self._uptime = uptime.split()[0]
        return self._uptime
