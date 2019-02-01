import urllib
import httplib
import json
import time
import requests
import re
import time

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
	l= len(a)
	while l>0:
		try:
			found = re.search('u\'endpoint\': u\'(.+?)\',', str(a[l-1])).group(1)
		except AttributeError:
			found = "UNKNOWN" # apply your error handling
			print str(a[l-1])
		#print found
		l -= 1
		endpoints.append(found)
	
	return endpoints

def main():
	SERVER_URL = "http://localhost:8080"
	endpoints=[]
	header={"Accept": "application/json, text/plain, */*", "Content-type": "application/json; charset=UTF-8"};
	endpoints = getendpoints(header)
	PSlist=[]
	PSstatlist=[]
	print("Sl.No:PARKING SPOTS:STATUS")
	for k in range(0,len(endpoints)):
		endpoint = endpoints[k]
	#r = makeHTTPRequest(SERVER_URL + "/api/clients/" + endpoint + "/32700/0/32801","PUT",{"id": 32801, "value": "reserved"}, header)
		#Get Parkspot ID
		url1 = SERVER_URL + "/api/clients/" + endpoint
		psID= "/32700/0/32800"
		PSID = GetDetails(url1,psID,header)
		psStatus = "/32700/0/32801"
		PSSTATUS = GetDetails(url1,psStatus,header)
		try:
			found = re.search('value=(.+?),', PSSTATUS).group(1)
		except AttributeError:
			found = PSSTATUS # apply your error handling
		PSSTATUS = found
		print k+1,":",PSID,":",PSSTATUS#'\x1b[6;30;42m' + PSSTATUS + '\x1b[0m')
		PSlist.append(PSID)
		PSstatlist.append(PSSTATUS)
	FLAG = 0
	for k in range(0,len(endpoints)):
		if PSstatlist[k]=="free":
			FLAG = 1
	if FLAG!=0:
		choice = raw_input("Choose a free parking spot by its Serial Number: ")
		int_choice = int(choice)
		if 0 < int_choice <= len(endpoints):
			print "Enter from and to what time you wish to reserve a spot (HH:mm:ss):"
			try:
				fromm = int(time.mktime(time.strptime(raw_input("From: "), "%H:%M:%S")))
				too = int(time.mktime(time.strptime(raw_input("To:   "), "%H:%M:%S")))
			except:
				print "ERROR: Date was of the wrong format"

			r = makeHTTPRequest(SERVER_URL + "/api/clients/" + endpoints[int_choice-1] + "/32700/0/32801","PUT",{"id": 32801, "value": "reserved"}, header)
			print "Parking spot",PSlist[int_choice-1],"reserved"
			##WAIT TILL END
			end = raw_input("\nEnter END, when you wish to stop using parking spot:\n")
			if end == "END":
				Billrate=GetDetails(url1,"/32700/0/32803",header)
				r = makeHTTPRequest(SERVER_URL + "/api/clients/" + endpoints[int_choice-1] + "/32700/0/32801","PUT",{"id": 32801, "value": "free"}, header)
				r = makeHTTPRequest(SERVER_URL + "/api/clients/" + endpoints[int_choice-1] + "/32700/0/32802","PUT",{"id": 32802, "value": "UNKNOWN"}, header)
				PS_t = (too-fromm)/60
				total = float(Billrate)*PS_t
				print "\nTotal time(minutes): ",PS_t
				print "Billing rate per minute: ",Billrate
				print "Total (Euros): ",total
				print "\n THANKS FOR USING TUE PARKING SYSTEM"
				print "SEE YOU SOON | TOT GAUW!"
			else:
				print "ERROR"				
		else:
			print "Not a valid input"
	else:
		print "No free Parking spot! Come back later."

if __name__ == '__main__':
    main()
