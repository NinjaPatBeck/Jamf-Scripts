#!/usr/bin/python3

import requests
import getpass
import base64
import json
import csv

#prompt user for JSS creds, encoode, and build the header
url = 'https://jss.corp.thumbtack.com'
print("Please enter your username:")
username = input()
password = getpass.getpass()
encoded = base64.b64encode(bytes("{u}:{p}".format(u=username,p=password), "utf-8"))
encodedString = str(encoded)
encodedString = encodedString[2:-1]
json_headers = {'authorization':"Basic {e}".format(e=encodedString), 'Accept':'application/json'}
xml_headers = {'authorization':"Basic {e}".format(e=encodedString), 'content-type':'application/xml'}

def getSearchIDs():
    idList = []
    response = requests.get((url + "/JSSResource/advancedcomputersearches"), headers=json_headers)
    responseDict = json.loads(response.text)
    for search in responseDict['advanced_computer_searches']:
        idList.append(search['id'])
    return idList

def getSearchesToUpdate():
	idList = getSearchIDs()
	idsToUpdateList = []
	for id in idList:
		response = requests.get((url + "/JSSResource/advancedcomputersearches/id/{id}".format(id=id)), headers=json_headers)
		responseDict = json.loads(response.text)
		search = responseDict['advanced_computer_search']
		display_fields_list = search['display_fields']
		display_fields_items = []
		for item in display_fields_list:
			display_fields_items.append(item['name'])
		if 'Operating System Version' in display_fields_items:
			print('Search #{id} is all good, man'.format(id=id))
		elif 'Operating System' in display_fields_items:
			print('Search #{id} needs to be fixed, bro'.format(id=id))
			idsToUpdateList.append(id)
		else:
			print('Search #{id} is not even displaying OS info, dude'.format(id=id))
	return idsToUpdateList

def updateSearches():
	idsToUpdateList = getSearchesToUpdate()
	#GET the XML for each search that needs to be updated
	if len(idsToUpdateList) > 0:
		for id in idsToUpdateList:
			response = requests.get((url + "/JSSResource/advancedcomputersearches/id/{id}".format(id=id)), headers=xml_headers)
			responseString = response.text
			#Then replace 'Operating System' with 'Operating System Version' in the XML
			start = responseString.find("<display_fields>")
			end = responseString.find("</display_fields>") + len("</display_fields>")
			displayFieldsString = responseString[start:end]
			sizeStart = displayFieldsString.find("<size>")
			sizeEnd = displayFieldsString.find("</size>") + len("</size>")
			cleanDisplayFieldsString = displayFieldsString[:sizeStart]
			cleanDisplayFieldsString += displayFieldsString[sizeEnd:]
			payload = "<advanced_computer_search>"
			payload += cleanDisplayFieldsString.replace("Operating System", "Operating System Version")
			payload += "</advanced_computer_search>"
			#Then POST that updated XML back into Jamf
			putResponse = requests.put((url + "/JSSResource/advancedcomputersearches/id/{id}".format(id=id)), data=payload, headers=xml_headers)
			print(putResponse)

updateSearches()
