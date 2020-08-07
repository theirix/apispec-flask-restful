#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for apispec_flask_restful"""

from setuptools import setup, find_packages

setup(
    name="apispec-flask-restful",
    version="0.2",
    author="theirix",
    author_email="theirix@gmail.com",
    description=(
        "Flask-RESTful plugin for apispec"),
    license="MIT",
    keywords='apispec swagger openapi specification documentation spec rest api',
    url="https://github.com/theirix/apispec-flask-restful",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={},
    install_requires=['apispec[yaml]>=1.0.0', 'Flask-RESTful'],
    tests_require=['pytest', 'pytest-cov'],
    test_suite='tests'
)
