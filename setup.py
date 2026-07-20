#!/usr/bin/env python3
"""
Setup script for SBARDS Project
"""

import os
import json
from setuptools import setup, find_packages

# Read version from config.json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    version = config.get('scanner', {}).get('version', '1.0.0')
except (FileNotFoundError, json.JSONDecodeError):
    version = '1.0.0'

# Read long description from README.md
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'SBARDS Project - Comprehensive Security Scanning System'

# Define required packages
requirements = [
    'yara-python>=4.2.0',
    'python-magic>=0.4.24',
    'requests>=2.28.1',
    'colorama>=0.4.4',
]

# Define entry points
entry_points = {
    'console_scripts': [
        'sbards-scanner=run_scanner:main',
        'sbards-tests=run_tests:main',
    ],
}

setup(
    name='sbards-scanner',
    version=version,
    description='Comprehensive Security Scanning System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SBARDS Project Team',
    author_email='info@sbards-project.example.com',
    url='https://github.com/sbards-project/sbards-scanner',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
    ],
    python_requires='>=3.7',
)
