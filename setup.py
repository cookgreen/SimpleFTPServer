import os
from setuptools import setup, find_packages

version='0.2.0'

setup(name='SnowMonkeyFTPServer',
      version=version,
      packages=find_packages(),
      description='Simple, Light FTP Server',
      author='Cook Green',
      url='https://github.com/cookgreen/SnowMonkeyFTPServer',
      license='GPL',
      install_requires=[
            'setuptools',
            'wxpython'
          ])
