#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name = 'donuts_ddns',
      version = '1.0.1',
      author = 'Sergio Tocalini Joerg',
      author_email = 'sergiotocalini@gmail.com',
      url = 'http://developers.corpam.com.ar/donuts/ddns',
      license = 'GNU GPLv3',
      packages = find_packages(),
      classifiers=[
          'Programming Language :: Python',
          ],
      zip_safe=True,
      include_package_data=True,
      entry_points = {
          'console_scripts': [
              'donuts_ddns = donuts_ddns.donuts_ddns:main',
          ]
      }
)
