# pylint: disable=c0111

from netshowlib.linux._version import get_version
import os
import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass


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
