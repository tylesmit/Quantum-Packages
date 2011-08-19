try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

Name='quantum-common'
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
    'eventlet>=0.9.12',
    'Routes>=1.12.3',
    'nose',
    'Paste',
    'PasteDeploy',
    'pep8>=0.5.0',
    'python-gflags',
    'simplejson',
    'sqlalchemy',
    'webob',
    'webtest'
]

EagerResources = [
    'quantum',
]

ProjectScripts = [
]

PackageData = {
}


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
    package_dir = {'': 'lib'},
    eager_resources = EagerResources,
    namespace_packages = ['quantum'],
    entry_points={
        'console_scripts' : [
            'quantum_tests = quantum.run_tests:main'
        ]
    },
)
