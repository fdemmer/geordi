#!/usr/bin/env python
"""Installs geordi"""

import os
import sys
from setuptools import setup, find_packages


def readfile(fn):
    f = open(os.path.join(sys.path[0], fn))
    try:
        return f.read()
    finally:
        f.close()

setup(
    author='Brodie Rao',
    author_email='brodie@sf.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v2 (LGPLv2)'),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    description='A Django middleware for interactive profiling',
    download_url='https://bitbucket.org/bitbucket/geordi/get/0.4.tar.gz',
    keywords='django graph profiler',
    license='GNU Lesser GPL',
    long_description=readfile('README.rst'),
    name='geordi',
    packages=find_packages(),
    include_package_data=True,
    package_data={'geordi': ['static/**/*', 'templates/**/*']},
    scripts=['scripts/geordi', 'scripts/gprof2dot'],
    url='https://bitbucket.org/bitbucket/geordi',
    version=readfile('version.txt').strip(),
)
