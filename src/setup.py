#!/usr/bin/env python3.2

from setuptools import setup
import sys

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    extra['convert_2to3_doctests'] = ['src/your/module/README.txt']
    extra['use_2to3_fixers'] = ['your.fixers']

setup(
    name='your.module',
    version = '1.0',
    description='This is your awesome module',
    author='You',
    author_email='your@email',
    package_dir = {'': 'src'},
    packages = ['your', 'you.module'],
    test_suite = 'your.module.tests',
    install_requires=['setuptools',
                      'cherrypy>=3.2.2',
                      'pymongo3>=1.9b1',
                      'jinja2>=2.6',
                      'jsmin>=2.0.2',
                      'csstyle>=0.1',
                      ],
    **extra
)
