# pylint: disable=c0111

from netshowlib.linux._version import get_version
import os
import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

USR_SHARE_PATH = '/usr/share'
if hasattr(sys, 'real_prefix') or os.environ.get('VIRTUAL_ENV'):
    USR_SHARE_PATH = os.path.abspath(os.path.join(sys.prefix, 'share'))

DATA_DIR = os.path.join(USR_SHARE_PATH, 'netshow-lib')

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
    data_files=[((os.path.join(DATA_DIR, 'providers')),
                 ['data/provider/linux'])]
)
