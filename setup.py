from copy import deepcopy
from optparse import OptionParser
from os import path
import re
import sys

from tools import install_venv

ROOT = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.abspath('/etc/quantum')
BASE_PACKAGES = ['common', 'server', 'client',]
PLUGINS = ['plugins/sample-plugin']

HAS_ALIEN = bool(install_venv.run_command(['which', 'alien']))
HAS_FAKEROOT = bool(install_venv.run_command(['which', 'fakeroot']))


def clean_path(dirty):
    """Makes sure path delimiters are OS compliant"""
    return path.join(*dirty.split('/'))

def create_parser():
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

def source_venv(venv):
    print ['source', path.join(venv,'bin','activate')] 
    return install_venv.run_command(['source',
        path.join(venv, 'bin', 'activate')])

def uninstall_packages(options, args):
    cmd = ['pip', 'uninstall', '-y']

    for p in ['quantum-'+x.split('/')[-1] for x in BASE_PACKAGES+PLUGINS]:
        print "Uninstalling %s" % p
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip uninstall"
        pcmd = deepcopy(cmd)
        pcmd.insert(2, p)
        print pcmd
        install_venv.run_command(pcmd)
        print "done."

def install_packages(options, args):
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
    for p in BASE_PACKAGES+PLUGINS:
        print "Installing %s" % p
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip install")
        pcmd = deepcopy(cmd)
        pcmd.insert(2, path.join(ROOT, clean_path(p)))
        print pcmd
        install_venv.run_command(pcmd)
        print "done."

def build_packages(options, args):
    if not args:
        args = 'rpm'
    if args not in ['rpm', 'deb', 'all']:
        print "arg must be rpm, deb, or all"

    cmd = ['tools/build_rpms.sh']
    for p in BASE_PACKAGES+PLUGINS:
        print "Building %s rpm" % p
        pcmd = deepcopy(cmd)
        pcmd.append(p)
        #install_venv.run_command(pcmd)
        print "done."

    if args is 'rpm':
        return

    cmd = ['tools/build_debs.sh']
    if HAS_FAKEROOT:
        cmd.insert(0, 'fakeroot')
    try:
        for p in BASE_PACKAGES+PLUGINS:
            print "Building %s deb" % p
            pcmd = deepcopy(cmd)
            pcmd.append(p)
            #install_venv.run_command(pcmd)
            print "done."
    except:
        print "You must be root or install fakeroot"
    #cmd = ['cp', './server/*.deb', ROOT+'/']
    #install_venv.run_command(cmd)

def main():
    print "Checking for virtual-env and easy_install"
    install_venv.check_dependencies()

    options, cmd, args = create_parser()
    
    # Execute command
    globals()["%s_packages" % cmd](options, args)

if __name__ == "__main__":
    main()
