import urllib
import httplib
import json
import time
import requests
import re

def makeHTTPRequest(url, method, params, headers):
    r = None

    if( method == "GET"):
        r = requests.get(url, headers = headers)
    if( method == "PUT"):
        r = requests.put(url, data = json.dumps(params), headers = headers)

    return r
def GetDetails(url1,url2,header):
	r = makeHTTPRequest(url1+url2,"GET","NaN",header)
	jsonresp =  r.json()
	#print type(jsonresp)
	content = jsonresp["content"]
	payload = content["value"]
	#print payload
	return payload

def getendpoints(header):
	endpoints =[]
	r = makeHTTPRequest("http://localhost:8080/api/clients","GET","NaN",header)
	a = r.json()
	#print a[0]
	l= len(a)
	#print l
	while l>0:
		try:
			found = re.search('u\'endpoint\': u\'(.+?)\',', str(a[l-1])).group(1)
		except AttributeError:
			found = "UNKNOWN" # apply your error handling
			#print str(a[l-1])
		#print found
		l -= 1
		endpoints.append(found)
	
	return endpoints

def main():
	SERVER_URL = "http://localhost:8080"
	endpoints=[]
	header={"Accept": "application/json, text/plain, */*", "Content-type": "application/json; charset=UTF-8"};
	endpoints = getendpoints(header)
	resourceId = ["/32700/0/32800","/32700/0/32801","/32700/0/32802"] # resource ID represents the Parking spot ID, Parking spot status and vehicle ID
	count=len(endpoints)
	#print count
	k=0
	for k in range (0,count):                                         # the for loop is to provide the overview of the whole parking system. 
		url1 = SERVER_URL + "/api/clients/" + endpoints[k]
		psID= resourceId[0]
		PSID = GetDetails(url1,psID,header)
		psStatus = resourceId[1]
		PSStatus = GetDetails(url1,psStatus,header)
		try:
			found = re.search('value=(.+?),', PSStatus).group(1)
		except AttributeError:
			found = PSStatus # apply your error handling
		PSStatus = found
		vId = resourceId[2]
		VId = GetDetails(url1,vId,header)
		try:
			found = re.search('value=(.+?),', VId).group(1)
		except AttributeError:
			found = VId # apply your error handling
		VId = found
		print PSID,"|",PSStatus,"|",VId
		

if __name__ == '__main__':
    main()