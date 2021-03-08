# Copyright (c) 2010 Simplistix Ltd
# See license.txt for license details.

import os
from setuptools import setup,find_packages

package_name = 'Products.SimpleUserFolder'
base_dir = os.path.dirname(__file__)

setup(
    name=package_name,
    version='0.0.0',
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="A scriptable, subclassable, fully documented and tested user folder implementation for Zope 2.",
    url='https://github.com/zms-publishing/SimpleUserFolder',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
    )
