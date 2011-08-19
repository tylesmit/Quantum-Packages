try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os


Name='quantum-server'
ProjecUrl=""
Version='0.1'
License='Apache License 2.0'
Author='Tyler Smith'
AuthorEmail='tylesmit@cisco.com'
Maintainer=''
Summary='Common functionalities for Quantum'
ShortDescription=Summary
Description=Summary

requires = [
    'quantum-common'
]

EagerResources = [
    'quantum',
]

ProjectScripts = [
]

PackageData = {
}

DataFiles = [
        ('/etc/quantum/',
	['etc/quantum.conf','etc/quantum.conf.sample',
	'etc/quantum.conf.test', 'etc/plugins.ini'])
]


setup(
    name=Name,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    license=License,
    scripts=ProjectScripts,
    install_requires=requires,
    include_package_data=True,
    packages=find_packages('lib'),
    package_data=PackageData,
    data_files=DataFiles,
    package_dir = {'': 'lib'},
    eager_resources = EagerResources,
    namespace_packages = ['quantum'],
    entry_points={
        'console_scripts' : [
            'quantum = quantum.server:main'
        ]
    },
)
