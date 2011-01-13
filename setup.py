from copy import deepcopy
from optparse import OptionParser
from os import path

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

def main():
    print "Checking for virtual-env and easy_install"
    install_venv.check_dependencies()
    options, args = create_parser()

    install = ['pip', 'install']

    # Check to see if we need to install locally\
    if options.venv:
        venv = path.abspath(path.expanduser(options.venv))
        install.extend(['-E', venv])
        if not path.exists(venv):
            print "Creating virtual-env at %s" % venv
            install_venv.create_virtualenv(venv, site_packages=True)
        else:
            print "Virtual-env at %s exists" % venv
        print "Activating virtual-env"
        #source_venv(venv)
    elif options.user:
        install = "%s %s" % (install, '--user')

    for p in BASE_PACKAGES:
        print "Installing %s" % p
        #print install % path.join(ROOT, clean_path(p))
        pinstall = deepcopy(install)
        pinstall.insert(2, path.join(ROOT, clean_path(p)))
        print pinstall
        install_venv.run_command(pinstall)
        print "done."

if __name__ == "__main__":
    main()
