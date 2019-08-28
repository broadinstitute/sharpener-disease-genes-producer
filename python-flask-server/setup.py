# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "sharpener-disease-genes-expander"
VERSION = "1.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="API for an expander based on disease-specific genes",
    author_email="",
    url="",
    keywords=["Swagger", "API for an expander based on disease-specific genes"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Gene-list expander based on disease-specific genes
    """
)

