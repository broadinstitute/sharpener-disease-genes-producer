# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "disease-genes-producer"
VERSION = "1.3.0"

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
    description="MONDO disease association",
    author_email="",
    url="",
    keywords=["Swagger", "MONDO disease association"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Gene-list producer based on disease-specific genes annotated in  Monarch Disease Ontology (https://www.ebi.ac.uk/ols/ontologies/mondo).
    """
)

