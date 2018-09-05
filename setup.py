# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fun_mooc',
    version='0.1.0',
    description='Une librairie pour formatter simplement sur la plateforme FUN',
    long_description=readme,
    author='Paul de Fromont',
    author_email='paul.de.fromont@gmail.com',
    url='https://github.com/pdefromont/fun_mooc',
    license=license,
    packages=find_packages()
)
