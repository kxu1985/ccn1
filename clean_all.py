#!/usr/bin/env python
import sys
import subprocess

#======================
# Stop all ccnd daemon
#======================
def Clean():
	print 'Cleaning ccn daemon, log and config...'
	subprocess.call("ssh -t htor@source 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@rsu 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh1 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh2 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh3 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh4 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh5 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh6 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh7 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh8 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh9 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)
	subprocess.call("ssh -t htor@veh10 'ccnrm ccnx:/; ccndstop; rm /tmp/ccnd.log; rm ~/.ccnx/ccnd.conf'", shell=True)

Clean()
print "Finish."
