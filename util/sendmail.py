#!/bin/env python

import os, sys, smtplib

if __name__ == '__main__':

	if (len(sys.argv) < 6):
		print "usage: %s ip port msgfile from to" % (sys.argv[0])
		sys.exit(1)

	smtphost = sys.argv[1]
	smtpport = sys.argv[2]
	msgfile = sys.argv[3]
	from_addr = sys.argv[4]
	to_addr = sys.argv[5]

	f = open(msgfile)
	msg = f.read()
	f.close()

	smtp = smtplib.SMTP(smtphost, int(smtpport))
	#smtp.set_debuglevel(1)
	smtp.sendmail(from_addr, to_addr, msg)
	smtp.close()
