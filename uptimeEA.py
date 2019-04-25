#!/bin/python

'''
This script is designed as a Jamf Extension Attribute
It gathers uptime information from a macOS computer
Then cuts the result down to just the number of days
Written by Patrick Beck for Thumbtack
'''

import subprocess

#get the output from the shell command 'uptime'
raw = subprocess.check_output('uptime')
#the output is a bytes object. we want a string
raw = raw.decode('utf-8')
#replace commas with spaces
raw = raw.replace(',', '')
#split at the spaces into a list
raw = raw.split()
#initialize the result variable
number_of_days = 0

#check to make sure 'days' is in the output list
#if 'days' is not present, then uptime is < 2 days
#initial value of 0 is a acceptable result
if 'days' in raw:
	#get the index location of 'days'
	days_index = raw.index('days')
	#in the output, the number is right before 'days'
	number_of_days = raw[(days_index - 1)]

#give the result back, formatted for JAMF
print("<result>" + number_of_days + "</result>")
