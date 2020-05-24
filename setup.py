#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is at http://randsik.rtfd.org."""

setup(
    name='randsik',
    version='0.1.0',
    description='Randsik (random + musik) is a library for generating generative music in Python ',
    long_description=readme + '\n\n' + doclink + '\n\n',
    author='Travis Hathaway',
    author_email='travis.j.hathaway@gmail.com',
    url='https://github.com/travishathaway/randsik',
    packages=[
        'randsik',
    ],
    package_dir={'randsik': 'randsik'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='randsik',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
