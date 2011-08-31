from subprocess import call
import sys
print " ".join(sys.argv[1:])
call(["quantum-tests", " ".join(sys.argv[1:])])
