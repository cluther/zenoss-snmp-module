##############################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
##############################################################################

import os
from setuptools import setup


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='zenoss-snmp-module',
    py_modules=['zenoss_snmp_module'],

    version='1.0.0rc3',
    description="Net-SNMP pass_persist script for monitoring Zenoss.",
    long_description=read('README.rst'),

    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Monitoring',
    ],

    keywords="zenoss snmp net-snmp",
    author='Chet Luther',
    author_email='chet.luther@gmail.com',
    url='http://github.com/cluther/zenoss-snmp-module',
    license='GPLv2',

    install_requires=[
        'argparse',
        'which',
        'python-rrdtool',
        'snmp-passpersist>=1.2.2',
    ],

    data_files=[
        ('', ['README.rst', 'ZENOSS-PROCESS-MIB.txt']),
    ],

    entry_points={
        'console_scripts': [
            'zenoss-snmp-module = zenoss_snmp_module:main'
        ],
    },
)
