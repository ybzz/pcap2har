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
        "chardet>=3.0.4",
        "beautifulsoup4>=4.6.0",
        "dpkt>=1.9.1",
    ],

    entry_points={
        'console_scripts': [
            'pcap2har = pcap2har.cli:main',
        ],
    },
)
