#!/usr/bin/env python
import sys
import subprocess
import time

ccn_dir = '~/Programs/ccnx/ccnx-0.8.2/bin/'
env_debug = 'export CCND_DEBUG=71'
env_repodir = 'export CCNR_DIRECTORY=/home/htor/Programs/ccnx/ccn_shared'
env_logdir = 'export CCND_LOG=/tmp/ccnd.log'

source = 'ccnx:/ udp 172.16.10.53'
rsu = 'ccnx:/ udp 172.16.10.54'
veh1 = 'ccnx:/ udp 172.16.10.55'
veh2 = 'ccnx:/ udp 172.16.10.56'
veh3 = 'ccnx:/ udp 172.16.10.60'
veh4 = 'ccnx:/ udp 172.16.10.61'
veh5 = 'ccnx:/ udp 172.16.10.62'
veh6 = 'ccnx:/ udp 172.16.10.63'
veh7 = 'ccnx:/ udp 172.16.10.64'
veh8 = 'ccnx:/ udp 172.16.10.65'
veh9 = 'ccnx:/ udp 172.16.10.66'
veh10 = 'ccnx:/ udp 172.16.10.67'

IPs = {'source':'172.16.10.53', 'rsu':'172.16.10.54', \
				'veh1':'172.16.10.55', 'veh2':'172.16.10.56', \
				'veh3':'172.16.10.60', 'veh4':'172.16.10.61', \
				'veh5':'172.16.10.62', 'veh6':'172.16.10.63', \
				'veh7':'172.16.10.64', 'veh8':'172.16.10.65', \
				'veh9':'172.16.10.66', 'veh10':'172.16.10.67'}

# Assume a 1600+1600m = 3200m highway
# The LTE BS is in the middle
# Total 8 rates, mapped to 8 sections with 200m for each on one side
# Assume the speed is 40 mph (17.78m/s), so every 11.25s change a rate
txrate = [5.89,8.80,11.74,17.60,17.60,23.47,26.41,29.34,\
					29.34,26.41,23.47,17.60,17.60,11.74,8.80,5.89]

#======================
# Stop all ccnd daemon
#======================
def Clean():
	print 'Cleaning ccn daemon and log...'
	subprocess.call("~/Documents/ccn1/clean_all.py", shell=True)

#=================
# Rate limit clean
#=================
def RateLimitClean():
	print 'Cleaning rate limit rules on rsu...'
	subprocess.call("ssh -t htor@rsu 'echo ctopassword | \
									sudo -S tc qdisc del dev eth0 root'",shell=True)

#======================================
# Install initial rate limit on the rsu
#======================================
def RateLimitInstall(numVeh):
	print 'Install initial rate limit rules on rsu...'
	subprocess.call("ssh -t htor@rsu 'echo ctopassword | \
									sudo -S tc qdisc add dev eth0 root handle 1: \
									cbq avpkt 1000 bandwidth 1024mbit'",shell=True)
	for i in range(1,numVeh+1):
		vehID = 'veh'+str(i)
		subprocess.call("ssh -t htor@rsu 'echo ctopassword | \
										sudo -S tc class add dev eth0 parent 1: classid 1:" + str(i) + \
										" cbq rate 100mbit allot 1500 prio 5 bounded isolated'",shell=True)
		subprocess.call("ssh -t htor@rsu 'echo ctopassword | \
										sudo -S tc filter add dev eth0 parent 1: protocol ip \
										prio 16 u32 match ip dst " + IPs[vehID] + \
										" flowid 1:" + str(i) +"'",shell=True)

#==================
# Change rate limit
#==================
def RateLimitChange(vehID,rate):
	print 'Switch tx rate for veh ' + str(vehID) + '...'
	subprocess.call("ssh -t htor@rsu 'echo ctopassword | \
									sudo -S tc class change dev eth0 parent 1: classid 1:" + str(vehID) + \
									" cbq rate " + str(rate) + "mbit allot 1500 prio 5 bounded isolated'",\
									shell=True)

#============================
# Create Full-connected Topo
#============================
def TopoFullConnected():
	print 'Creating a full-connected topo...'
	print 'Configure source...'
	subprocess.call("ssh -n -f htor@source '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ~/Documents/ccn1/source_start &'", shell=True)
	subprocess.call("ssh -t htor@source 'ccndc add " + rsu +"'",shell=True)

	print 'Configure rsu...'
	subprocess.call("ssh -n -f htor@rsu '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ccndstart &'", shell=True)
	subprocess.call("ssh -t htor@rsu 'ccndc add " + source +"'",shell=True)
	subprocess.call("ssh -t htor@rsu 'ccndc add " + veh1 +"'",shell=True)

	print 'Configuring veh1...'
	subprocess.call("ssh -n -f htor@veh1 '" + env_debug + ";" + env_repodir + ";" + env_logdir + "; nohup ccndstart &'", shell=True)
	subprocess.call("ssh -t htor@veh1 'ccndc add " + rsu +"'",shell=True)
	
#==================
# Get a File
#==================
def GetFile(filename):
	subprocess.call("ssh -n -f htor@veh1 'nohup ccngetfile -v ccnx:/ccn_shared/" + filename + " /tmp/retrieved_" + filename + " > /tmp/ccngetfile.log &'",shell=True)

#==================
# Main procedure
#=================
Clean()
RateLimitClean()
RateLimitInstall(1)
TopoFullConnected()

print txrate
vehID = 1
vehRateIndex = [0]
print txrate[vehRateIndex[vehID-1]]

GetFile('100m.txt')

while 1:
	time.sleep(11.25)
	vehID = 1
	if vehRateIndex[vehID-1] < len(txrate)-1:
		vehRateIndex[vehID-1] += 1
		print txrate[vehRateIndex[vehID-1]]
	else:
		vehRateIndex[vehID-1] = 0
		print txrate[vehRateIndex[vehID-1]]
	RateLimitChange(vehID,txrate[vehRateIndex[vehID-1]])


'''
for t in range(0,300):
	time.sleep(1)
	if (t+1) % 3 == 1:
		print 'handoff from 1 to 2'
		subprocess.call("ccndc add " + rsu3,shell=True)
		subprocess.call("ccndc del " + rsu1,shell=True)
	elif (t+1) % 3 == 2:
		print 'handoff from 2 to 3'
		subprocess.call("ccndc add " + rsu1,shell=True)
		subprocess.call("ccndc del " + rsu2,shell=True)
	else:
		print 'handoff from 3 to 1'
		subprocess.call("ccndc add " + rsu2,shell=True)
		subprocess.call("ccndc del " + rsu3,shell=True)
'''
'''
time.sleep(300)
subprocess.call("killall ccngetfile",shell=True)
'''
