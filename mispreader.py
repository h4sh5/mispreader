#!/usr/bin/env python

import requests
import json
import sys

if len(sys.argv) < 2:
	print "%s <feed-url>" % sys.argv[0]
	exit(1)

url = sys.argv[1]

usage = \
'''
?: usage
n: next
l: last
v: view details
s: save
ls: list all
#: view #th item (# is a number)
'''


print "getting manifest data..."


# get the manifest
r = ""
# try:
# 	with open("manifest.json", "r") as f:
# 		r += f.read()
# except IOError:
# 	print "manifest file not found, downloading it to manifest.json ..."
req = requests.get(url + "/manifest.json")
# with open("manifest.json", "w") as f:
r += req.text
	# f.write(req.text)


def dump_data(viewIndex):
	global infoIDs
	if not infoIDs[viewIndex].get("data"):
		r = requests.get(url + infoIDs[viewIndex].keys()[0] + ".json")
		infoIDs[viewIndex]["data"] = json.loads(r.text)

	print json.dumps(infoIDs[viewIndex]["data"], indent=4, sort_keys=True)


data = json.loads(r)

infoIDs = []

counter = 0
for key in data:
	print counter, key, data[key]['info'].encode("ascii","ignore")
	counter += 1
	infoIDs.append({key:data[key]['info']})

viewIndex = 0
while 1:
	try:
		print viewIndex, infoIDs[viewIndex].values()[0].encode("ascii","ignore")
	except:
		print viewIndex, infoIDs[viewIndex].values()[-1].encode("ascii","ignore")
	cmd = raw_input("(misp-view) ")

	if cmd == 'q':
		exit(0)

	elif cmd == "?":
		print usage
	elif cmd == "n":
		viewIndex += 1;
		continue

	elif cmd == "l": # go back one
		viewIndex -= 1;
		continue

	elif cmd == 'v':
		dump_data(viewIndex)

	elif cmd == 's':
		if not infoIDs[viewIndex].get("data"):
			r = requests.get(url + infoIDs[viewIndex].keys()[0] + ".json")
			infoIDs[viewIndex]["data"] = json.loads(r.text)
		with open("saved/" + str(infoIDs[viewIndex]["data"]['Event']['info']).replace("/", "|"), "a") as f:
			f.write(json.dumps(infoIDs[viewIndex]["data"], indent=4, sort_keys=True))
		print "saved."

	elif cmd == 'ls':
		counter = 0
		for key in data:
			print counter, key, data[key]['info']
			counter += 1


	elif cmd.encode("utf-8").decode().isnumeric():
		viewIndex = int(cmd)


	else:
		continue




