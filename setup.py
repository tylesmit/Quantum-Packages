from copy import deepcopy
from optparse import OptionParser
from os import path
import re
import sys

from tools import install_venv

ROOT = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.abspath('/etc/quantum')
BASE_PACKAGES = ['common', 'server', 'client', 'plugins/sample-plugin']


def clean_path(dirty):
    """Makes sure path delimiters are OS compliant"""
    return path.join(*dirty.split('/'))

def create_parser():
    usagestr = "Usage: %prog [OPTIONS] <command> [args]"
    parser = OptionParser(usage=usagestr)
    parser.add_option("-V", "--virtualenv", "--virtual-env", "--venv",
        dest="venv", type="string", default="",
        help="Install to the given virtual env")
    parser.add_option("-U", "--user", dest="user", action="store_true",
        default=False, help="Install to users's home")
    return parser.parse_args()

def source_venv(venv):
    print ['source', path.join(venv,'bin','activate')] 
    return install_venv.run_command(['source',
        path.join(venv, 'bin', 'activate')])

def uninstall_packages(options):
    cmd = ['pip', 'uninstall', '-y']

    for p in ['quantum-'+x.split('/')[-1] for x in BASE_PACKAGES]:
        print "Uninstalling %s" % p
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip uninstall"
        pcmd = deepcopy(cmd)
        pcmd.insert(2, p)
        print pcmd
        install_venv.run_command(pcmd)
        print "done."

def install_packages(options):
    cmd = ['pip', 'install']

    # Get Python lib
    lib_re = re.compile('^/usr/lib/python[0-9]\.[0-9]$')
    if options.user:
        lib_re = re.compile('^/usr/local/lib/python[0-9]\.[0-9]/dist-packages$')

    lib_path = [x for x in sys.path if lib_re.match(x)][0]
    if options.user:
        cmd.append('--user')
        #cmd.append("--install-option=--install-scripts=/usr/local/bin")
        #cmd.append("--install-option=--install-lib='%s" % lib_path)

    for p in BASE_PACKAGES:
        print "Installing %s" % p
        # Each package needs its own command list, and it needs the path
        # in the correct place (after "pip install"
        pcmd = deepcopy(cmd)
        pcmd.insert(2, path.join(ROOT, clean_path(p)))
        print pcmd
        install_venv.run_command(pcmd)
        print "done."

def main():
    print "Checking for virtual-env and easy_install"
    install_venv.check_dependencies()
    options, args = create_parser()

    if 'install' in args:
        install_packages(options)

    if 'uninstall' in args:
        uninstall_packages(options)

if __name__ == "__main__":
    main()
