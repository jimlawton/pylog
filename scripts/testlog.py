#!/usr/bin/env python

from pylog import *

startLogging(verbose=True, debug=True)
debug("debug: debug")
info("debug: info")
warn("debug: warning")
error("debug: error")
critical("debug: critical")
stopLogging()

