#!/usr/bin/env python
import os
import sys

wd = os.getcwd()
for project in ['common', 'server', 'client', 'plugins/sample-plugin']:
    sys.path.append(os.path.join(wd, project, 'lib'))

from quantum.run_tests import main as tests
tests()
#print " ".join(sys.argv[1:])
#call(["quantum-tests", " ".join(sys.argv[1:])])
