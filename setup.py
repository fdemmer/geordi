#!/usr/bin/env python
"""Installs geordi"""

import os
import sys
from setuptools import setup, find_packages


def long_description():
    """Get the long description from the README"""
    f = open(os.path.join(sys.path[0], 'README.rst'))
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
    dependency_links=[
        'https://bitbucket.org/bitbucket/gprof2dot/get/116454888109e59df656ef456e60bc2df08fd53b.tar.gz#egg=gprof2dot-bitbucket_visjs'
    ],
    download_url='https://bitbucket.org/brodie/geordi/get/0.3.tar.gz',
    install_requires=['gprof2dot==bitbucket_visjs'],
    keywords='django graph profiler',
    license='GNU Lesser GPL',
    long_description=long_description(),
    name='geordi',
    packages=find_packages(),
    include_package_data=True,
    package_data={'geordi': ['static/**/*', 'templates/**/*']},
    scripts=['scripts/geordi'],
    url='https://bitbucket.org/brodie/geordi',
    version='0.4',
)
