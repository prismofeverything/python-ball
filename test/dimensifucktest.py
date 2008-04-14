#!/bin/env python
from dimensifuck import *

a = Dimensifuck()
#a.loadMatrix("0^+=^\n"
#             "1_  _\n"
#             "2v=.v\n")
#
#a.run()
a.loadFile(sys.argv[1])

a.run(verbose = False)
