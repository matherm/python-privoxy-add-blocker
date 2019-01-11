# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 11:25:05 2014

@author: Matthias
"""

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import string
import datetime
import os
import sys


#Date
date = datetime.datetime.now()
print(date)


URL = "http://winhelp2002.mvps.org/hosts.txt"
PRIVOXY_PATH = "C:\\Program Files (x86)\\Privoxy\\user.action"
BLOCK_START_PATTERN = '{ +block }' +'\n'
BLOCK_END_PATTERN = '#{MVPS_END}' + ' ' + str(date) + '\n'

FOLDER_PATH ='temp/'
F_HOSTS = FOLDER_PATH + 'hosts'
F_CLEANED = FOLDER_PATH + 'cleanedHosts'
F_PRIVOXY_HEADER = FOLDER_PATH + 'privoxy_header'


#Change working directory
os.chdir(sys.path[0])

if not os.path.exists(FOLDER_PATH):
	os.mkdir(FOLDER_PATH)

count_old_hosts = 0
#check old cleaned
if os.path.exists(F_CLEANED):
	cleand_hosts_old = open(F_CLEANED,'r')
	count_old_hosts = 0
	for l in cleand_hosts_old:
		count_old_hosts = count_old_hosts + 1
	cleand_hosts_old.close()


#Download file
tmp = urllib2.urlopen(URL)
myFile = open(F_HOSTS,'wb')
myFile.write(tmp.read())
myFile.close()

#Clean file
hosts = open(F_HOSTS,'r')
cleaned = open(F_CLEANED,'w')
count_new_hosts = 0
for v in hosts:
    if not v.startswith('\n'):
        if not v.startswith('#'):
            if not v.startswith('127'):
                if not v.startswith('::'):
                    s = v.replace('0.0.0.0 ','')
                    posOfHash = s.find('#')
                    if posOfHash != -1:
                       s = s[:posOfHash] + '\n'
                    cleaned.write(s)
                    count_new_hosts = count_new_hosts + 1
    if v.find('Updated') != -1:
    	print(v)
cleaned.close()

#Read Privoxy Header
privoxy = open(PRIVOXY_PATH, 'r')
privoxy_header = open(F_PRIVOXY_HEADER, 'w')
for v in privoxy:
    if v.startswith(BLOCK_START_PATTERN):
        break;
    privoxy_header.write(v)    
privoxy.close()
privoxy_header.close()

#Write privoxy file
privoxy = open(PRIVOXY_PATH, 'w')
privoxy_header = open(F_PRIVOXY_HEADER, 'r')
cleanedHosts = open(F_CLEANED,'r') 

privoxy.write(privoxy_header.read())

privoxy.write(BLOCK_START_PATTERN)
privoxy.write(cleanedHosts.read())
privoxy.write(BLOCK_END_PATTERN)

privoxy_header.close()
cleanedHosts.close()
privoxy.close()

print('DONE ')
print( str(count_new_hosts) + ' hosts.')
print(str(count_new_hosts - count_old_hosts) + ' hosts added ')

