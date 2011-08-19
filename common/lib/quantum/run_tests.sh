#!/bin/bash

function usage {
  echo "Usage: $0 [OPTION]..."
  echo "Run Quantum's test suite(s)"
  echo ""
  echo "  -V, --virtual-env        Always use virtualenv.  Install automatically if not present"
  echo "  -N, --no-virtual-env     Don't use virtualenv.  Run tests in local environment"
  echo "  -f, --force              Force a clean re-build of the virtual environment. Useful when dependencies have been added."
  echo "  -h, --help               Print this usage message"
  echo ""
  echo "Note: with no options specified, the script will try to run the tests in a virtual environment,"
  echo "      If no virtualenv is found, the script will ask if you would like to create one.  If you "
  echo "      prefer to run tests NOT in a virtual environment, simply pass the -N option."
  exit
}

function process_option {
  case "$1" in
    -h|--help) usage;;
    -V|--virtual-env) let always_venv=1; let never_venv=0;;
    -N|--no-virtual-env) let always_venv=0; let never_venv=1;;
    -f|--force) let force=1;;
    *) noseargs="$noseargs $1"
  esac
}

venv=.quantum-venv
with_venv=tools/with_venv.sh
always_venv=0
never_venv=0
force=0
noseargs=
wrapper=""

for arg in "$@"; do
  process_option $arg
done

function run_tests {
  # Just run the test suites in current environment
  ${wrapper} rm -f tests.sqlite
  ${wrapper} $NOSETESTS 2> run_tests.err.log
}

NOSETESTS="python run_tests.py $noseargs"

if [ $never_venv -eq 0 ]
then
  # Remove the virtual environment if --force used
  if [ $force -eq 1 ]; then
    echo "Cleaning virtualenv..."
    rm -rf ${venv}
  fi
  if [ -e ${venv} ]; then
    wrapper="${with_venv}"
  else
    if [ $always_venv -eq 1 ]; then
      # Automatically install the virtualenv
      python tools/install_venv.py
      wrapper="${with_venv}"
    else
      echo -e "No virtual environment found...create one? (Y/n) \c"
      read use_ve
      if [ "x$use_ve" = "xY" -o "x$use_ve" = "x" -o "x$use_ve" = "xy" ]; then
        # Install the virtualenv and run the test suite in it
        python tools/install_venv.py
		    wrapper=${with_venv}
      fi
    fi
  fi
fi

# FIXME(sirp): bzr version-info is not currently pep-8. This was fixed with
# lp701898 [1], however, until that version of bzr becomes standard, I'm just
# excluding the vcsversion.py file
#
# [1] https://bugs.launchpad.net/bzr/+bug/701898
#
PEP8_EXCLUDE=vcsversion.py
PEP8_OPTIONS="--exclude=$PEP8_EXCLUDE --repeat --show-source"
PEP8_INCLUDE="bin/* quantum tests tools run_tests.py"
run_tests && pep8 $PEP8_OPTIONS $PEP8_INCLUDE || exit 1
