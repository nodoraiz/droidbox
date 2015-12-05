#!/usr/bin/python

import xml.etree.ElementTree as ET
import subprocess
import os
import sys
import time

def lookForComponentInManifest(node, attrib):

	result = list()

	command = "cat " + sys.argv[1] + " | grep " + node + " | sed -nE 's/.*" + attrib + "=\"([^\"]+)\".*/\\1/p'"
	elements = subprocess.check_output(command, shell=True)

	for element in elements.split("\n"):
		if element and element.strip():
			if(element.startswith(".")):
				result.append(package + element)
			else:
				result.append(element)

	return result



if len(sys.argv) != 2 or not sys.argv[1].lower().endswith("androidmanifest.xml"):
	print "Expected AndroidManifest, usage:"
	print "python " + sys.argv[0] + " /path/to/AndroidManifest.xml"
	quit()

package = lookForComponentInManifest("manifest", "package")[0]
manifestActivities = lookForComponentInManifest("activity", "name")

for activity in manifestActivities:
	command = "adb shell am start " + package + "/" + activity
	print "\n----\nRunning: " + command
	os.system(command)
	time.sleep(10)
