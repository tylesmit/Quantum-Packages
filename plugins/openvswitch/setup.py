try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

Name='quantum-openvswitch-plugin'
ProjecUrl=""
Version='0.1'
License='Apache License 2.0'
Author=''
AuthorEmail=''
Maintainer=''
Summary='OpenVSwitch plugin for Quantum'
ShortDescription=Summary
Description=Summary

requires = [
    'quantum-common',
    'quantum-server',
]

EagerResources = [
    'quantum',
]

ProjectScripts = [
]

PackageData = {
}

DataFiles = [
        ('/etc/quantum/plugins/openvswitch',
	['etc/ovs_quantum_plugin.ini'])
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
)
