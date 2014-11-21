#!/usr/bin/env python
import sys
import subprocess

ccn_dir = '~/Programs/ccnx/ccnx-0.8.2/bin/'
env_debug = 'export CCND_DEBUG=71'
env_repodir = 'export CCNR_DIRECTORY=/home/htor/Programs/ccnx/ccn_shared'
env_logdir = 'export CCND_LOG=/tmp/ccnd.log'

#======================
# Stop all ccnd daemon
#======================
def Clean():
	print 'Cleaning ccn daemon and log...'
	subprocess.call("ssh -t htor@source 'cd " + ccn_dir + "; ./ccnrm ccnx:/; ./ccndstop; rm /tmp/ccnd.log'", shell=True)
	subprocess.call("ssh -t htor@rsu1 'cd " + ccn_dir + "; ./ccnrm ccnx:/; ./ccndstop; rm /tmp/ccnd.log'", shell=True)
	subprocess.call("ssh -t htor@rsu2 'cd " + ccn_dir + "; ./ccnrm ccnx:/; ./ccndstop; rm /tmp/ccnd.log'", shell=True)
	subprocess.call("ssh -t htor@rsu3 'cd " + ccn_dir + "; ./ccnrm ccnx:/; ./ccndstop; rm /tmp/ccnd.log'", shell=True)
	subprocess.call("ssh -t htor@veh1 'cd " + ccn_dir + "; ./ccnrm ccnx:/; ./ccndstop; rm /tmp/ccnd.log'", shell=True)

#============================
# Create Full-connected Topo
#============================
def TopoFullConnected():
	print 'Creating a full-connected topo...'
	print 'Configure source...'
	tmp_config = [];
	tmp_config.append('add ccnx:/ udp 172.16.10.54')
	tmp_config.append('add ccnx:/ udp 172.16.10.55')
	tmp_config.append('add ccnx:/ udp 172.16.10.56')
	tmp_config.append('add ccnx:/ udp 172.16.10.60')
	#print tmp_config
	subprocess.call("ssh -t htor@source 'rm ~/.ccnx/ccnd.conf; echo " + tmp_config[0] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[1] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[2] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[3] + " >> ~/.ccnx/ccnd.conf'",shell=True)
	#subprocess.call("ssh -n -f htor@source '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Programs/ccnx/ccnx-0.8.2/bin/ccndstart &'", shell=True)
	subprocess.call("ssh -n -f htor@source '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Documents/ccn1/source_start &'", shell=True)
	
	print 'Configure rsu1...'
	tmp_config = [];
	tmp_config.append('add ccnx:/ udp 172.16.10.53')
	tmp_config.append('add ccnx:/ udp 172.16.10.55')
	tmp_config.append('add ccnx:/ udp 172.16.10.56')
	tmp_config.append('add ccnx:/ udp 172.16.10.60')
	#print tmp_config
	subprocess.call("ssh -t htor@rsu1 'rm ~/.ccnx/ccnd.conf; echo " + tmp_config[0] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[1] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[2] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[3] + " >> ~/.ccnx/ccnd.conf'",shell=True)
	subprocess.call("ssh -n -f htor@rsu1 '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Programs/ccnx/ccnx-0.8.2/bin/ccndstart &'", shell=True)

	print 'Configure rsu2...'
	tmp_config = [];
	tmp_config.append('add ccnx:/ udp 172.16.10.53')
	tmp_config.append('add ccnx:/ udp 172.16.10.54')
	tmp_config.append('add ccnx:/ udp 172.16.10.56')
	tmp_config.append('add ccnx:/ udp 172.16.10.60')
	#print tmp_config
	subprocess.call("ssh -t htor@rsu2 'rm ~/.ccnx/ccnd.conf; echo " + tmp_config[0] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[1] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[2] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[3] + " >> ~/.ccnx/ccnd.conf'",shell=True)
	subprocess.call("ssh -n -f htor@rsu2 '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Programs/ccnx/ccnx-0.8.2/bin/ccndstart &'", shell=True)

	print 'Configure rsu3...'
	tmp_config = [];
	tmp_config.append('add ccnx:/ udp 172.16.10.53')
	tmp_config.append('add ccnx:/ udp 172.16.10.54')
	tmp_config.append('add ccnx:/ udp 172.16.10.55')
	tmp_config.append('add ccnx:/ udp 172.16.10.60')
	#print tmp_config
	subprocess.call("ssh -t htor@rsu3 'rm ~/.ccnx/ccnd.conf; echo " + tmp_config[0] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[1] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[2] + " >> ~/.ccnx/ccnd.conf; echo " + tmp_config[3] + " >> ~/.ccnx/ccnd.conf'",shell=True)
	subprocess.call("ssh -n -f htor@rsu3 '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Programs/ccnx/ccnx-0.8.2/bin/ccndstart &'", shell=True)
	
	print 'Configuring veh1...'
	subprocess.call("ssh -n -f htor@veh1 '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Programs/ccnx/ccnx-0.8.2/bin/ccndstart &'", shell=True)
	

#==================
# Main procedure
#=================
Clean()
TopoFullConnected()
