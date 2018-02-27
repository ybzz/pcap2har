#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='pcap2har',
    version="1.0",
    description="Converts .pcap network capture files to HTTP Archive files",
    author='andrewf',
    packages=find_packages('.'),
    package_dir={'': '.'},

    install_requires=[
        "chardet",
        "beautifulsoup4",
        "dpkt-fix",
    ],

    entry_points={
        'console_scripts': [
            'pcap2har = pcap2har.cli:main',
        ],
    },
)
