# pylint: disable=c0111

from netshowlib.linux._version import get_version
import os
import sys
import shutil
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
from distutils.command.install_data import install_data
from distutils import log
from distutils.util import change_root, convert_path
import re


class PostInstall(install_data):
    def run(self):
        # run through the regular install data
        # now install the translation stuff
        # run "setup.py build_i18n -m" first first before executing

        install_data.run(self)
        # for some reason self.root sometimes returns None in a tox env
        # not sure why..this takes care of it.
        if isinstance(self.root, str):
            _install_dir = change_root(self.root, sys.prefix)
            _dest = os.path.join(_install_dir, 'mo')
            _src = 'build/mo'
            try:
                log.info("copying files from %s to %s" % (_src, _dest))
                shutil.copytree(_src, _dest)
            except shutil.Error as _exception:
                log.info("Directory failed to copy. Error: %s" % _exception)
            except OSError as _exception:
                log.info("Directory failed to copy. Error: %s" % _exception)



def data_dir():
    _usr_share_path = os.path.abspath(os.path.join(sys.prefix, 'share'))
    _data_dir = os.path.join(_usr_share_path, 'netshow-lib')
    return _data_dir

from setuptools import setup, find_packages
setup(
    name='netshow-linux-lib',
    version=get_version(),
    url="http://github.com/CumulusNetworks/netshow-lib",
    description="Python Library to Abstract Linux Networking Data",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    zip_safe=False,
    license='GPLv2',
    cmdclass={"install_data": PostInstall},
    namespace_packages=['netshowlib', 'netshowlib.linux'],
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
    data_files=[((os.path.join(data_dir(), 'providers')),
                 ['data/provider/linux'])]
)
