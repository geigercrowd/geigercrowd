#!/usr/bin/python2.6
import os
import sys

if not os.getenv("DEBUG"):
    import cgitb
    cgitb.enable()

import gheat

if os.getenv("DEBUG"):
    os.remove("/var/cache/"+os.getenv("REQUEST_URI"))

fn = gheat.get_tile("/"+"/".join(os.getenv("REQUEST_URI").split("/")[-4:]))

if not os.path.exists(fn):
    print "Status: 404 Not Found"
    print "Content-type: text/plain"
    print ""
    print fn
    sys.exit(1)

if os.getenv("DEBUG"):
    print "Content-type: text/plain"
    print ""
    print fn
    sys.exit(0)

print "Location: http://%s%s" % (os.getenv("HTTP_HOST"),os.getenv("REQUEST_URI"))
print ""
