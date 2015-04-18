"""
This modules run a OS discovery check for Linux
"""

try:
    import netshowlib.linux.common as common

    def check():
        """
        Linux OS check.
        :return: name of OS found if check is true
        """
        uname_output = common.exec_command('/bin/uname')
        os_name = uname_output.decode('utf-8').strip()
        if os_name == 'Linux':
            return os_name
        return None

    def name_and_priority():
        """
        name and priority for Linux OS
        name = Linux
        priority = 0. Lower priority means less likely candidate
        """
        os_name = check()
        if os_name:
            return {os_name: '0'}
        return None

except ImportError:
    def check():
        """ returns false if this checker is run """
        return False
