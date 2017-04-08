#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='opv_api_client',
    packages=find_packages(),
    author="",
    author_email="",
    description="The OPV api client",
    long_description=open('README.md').read(),
    install_requires=["requests"],
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=False,
    url='https://github.com/OpenPathView/OPV_DBRest-client',
    entry_points={}
)
