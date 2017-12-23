#!/usr/bin/python3
from setuptools import setup

setup(
   name='package-installer-ubuntu',
   version='1.0',
   description='Installs packages and changes configuration files on Ubuntu OS',
   author='Valentin Kormanov',
   author_email='guve4e@gmail.com',
   packages=['package-installer-ubuntu'],
   install_requires=['tqdm', 'jsonschema'], #external packages as dependencies
)
