from copy import deepcopy
from optparse import OptionParser
from os import path
import re
import sys

from tools import install_venv

ROOT = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.abspath('/etc/quantum')
BASE_PACKAGES = ['common', 'server', 'client']
PLUGINS = ['plugins/sample-plugin']


def check_deb_build_dependencies():
    alien = bool(install_venv.run_command(['which', 'alien'],
                                          check_exit_code=False))
    fakeroot = bool(install_venv.run_command(['which', 'fakeroot'],
                                             check_exit_code=False))
    if not alien:
        raise Exception("You must have alien installed to build debs")

    return (alien, fakeroot)

def clean_path(dirty):
    """Makes sure path delimiters are OS compliant"""
    return path.join(*dirty.split('/'))


def create_parser():
    """Setup the option parser"""
    usagestr = "Usage: %prog [OPTIONS] <command> [args]"
    parser = OptionParser(usage=usagestr)
    parser.add_option("-V", "--virtualenv", "--venv", dest="venv",
        action="store_true", default=False, help="Install to a virtual-env")
    parser.add_option("-U", "--user", dest="user", action="store_true",
        default=False, help="Install to users's home")
    options, args = parser.parse_args()
    cmd = args[0]
    args = args[1:]
    return (options, cmd, args)


def install_packages(options, args=None):
    """Builds and installs packages"""
    # Start building a command list
    cmd = ['pip', 'install']

    # If no options, just a regular install.  If venv, create, prepare and
    # install in venv.  If --user install in user's local dir.  Usually
    # ~/.local/
    if options.venv:
        if install_venv.VENV_EXISTS:
            print "Virtual-env exists"
        else:
            install_venv.create_virtualenv(no_pip=True)
        install_venv.install_dependencies()
        cmd.extend(['-E', install_venv.VENV])
    elif options.user:
        cmd.append('--user')

    # Install packages
    # TODO(Tyler) allow users to pass in packages in cli
    for package in BASE_PACKAGES + PLUGINS:
        print "Installing %s" % package
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip install")
        pcmd = deepcopy(cmd)
        pcmd.insert(2, path.join(ROOT, clean_path(package)))
        print pcmd
        install_venv.run_command(pcmd)
        print "done."


def uninstall_packages(options, args=None):
    """Removes packages"""
    cmd = ['pip', 'uninstall', '-y']

    for package in ['quantum-' + x.split('/')[-1] \
                    for x in BASE_PACKAGES + PLUGINS]:
        print "Uninstalling %s" % package
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip uninstall"
        pcmd = deepcopy(cmd)
        pcmd.insert(2, package)
        print pcmd
        install_venv.run_command(pcmd)
        print "done."


def build_packages(options, args=None):
    """Build RPM and/or deb packages"""
    # If we weren't given a package type, default to rpm
    if not args:
        args = ['rpm']
    if args[0] not in ['rpm', 'deb', 'all']:
        raise Exception("Packge type must be rpm, deb, or all")

    # Since we need to cd to build rpms, we call this sh script
    cmd = ['tools/build_rpms.sh']
    for package in BASE_PACKAGES + PLUGINS:
        print "Building %s rpm" % package
        pcmd = deepcopy(cmd)
        pcmd.append(package)
        install_venv.run_command(pcmd)
        print "done."

    # If we're only building rpms we're done
    if args[0] is 'rpm':
        return

    # Use alient to build debs from the rpms
    alien, fakeroot = check_deb_build_dependencies()
    cmd = ['tools/build_debs.sh']
    if fakeroot:
        cmd.insert(0, 'fakeroot')
    try:
        for p in BASE_PACKAGES + PLUGINS:
            print "Building %s deb" % p
            pcmd = deepcopy(cmd)
            pcmd.append(p)
            install_venv.run_command(pcmd)
            print "done."
    except:
        print "You must be root or install fakeroot"
    #cmd = ['cp', './server/*.deb', ROOT+'/']
    #install_venv.run_command(cmd)


def main():
    """Main Build script for Quantum"""
    print "Checking for virtual-env and easy_install"
    install_venv.check_dependencies()

    options, cmd, args = create_parser()

    # Execute command
    try:
        globals()["%s_packages" % cmd](options, args)
    except KeyError as exc:
        print "Command %s' not found" % exc.__str__().split('_')[0]

if __name__ == "__main__":
    main()
