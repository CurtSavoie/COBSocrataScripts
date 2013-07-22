#!/usr/bin/env python
import urllib2
import json
import MultipartPostHandler
import time


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

multiOpener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
urllib2.install_opener(multiOpener)

baseURL = "https://data.cityofboston.gov"
TOKEN = "XXXXXX"
AUTH = "Basic XXXXXX"
dataID = "XXXXXX"  
fileName = "XXXXXX.csv"  
fileID = ""
copyID = ""
method = "POST"

# Make Working Copy
request = urllib2.Request(baseURL + "/api/views/" + dataID + "/publication.json?method=copySchema")
request.add_header("Authorization", AUTH)
request.add_header("X-App-Token", TOKEN)
opener.addheaders = [("Authorization", "X-App-Token")]
request.get_method = lambda: method
data = opener.open(request).read()
final = json.loads(data)
copyID = final["id"]
print copyID

# Scan File For Upload
request = urllib2.Request(baseURL + "/api/imports2?method=scan")
request.add_header("Authorization", AUTH)
request.add_header("X-App-Token", TOKEN)
params = {"file": open("/Users/Admin/Documents/crime.csv", "rb")}
multiOpener.addheaders = [("Authorization", "X-App-Token")]
request.get_method = lambda: method
data = multiOpener.open(request, params).read()
final = json.loads(data)
fileID = final["fileId"]
print final["fileId"]

# Import file
request = urllib2.Request(baseURL + "/api/imports2?method=replace&viewUid=" + copyID + "&fileId=" + fileID + "&name=" + fileName + "&skip=1")
request.add_header("Authorization", AUTH)
request.add_header("X-App-Token", TOKEN)
request.get_method = lambda: method
opener.addheaders = [("Authorization", "X-App-Token")]
data = opener.open(request).read()
final = json.loads(data)
print final.has_key("details")

# for files that are large and get queued

while final.has_key("details") == True:
    method = "GET"
    time.sleep(10)
    request = urllib2.Request(baseURL + "/api/imports2.json?ticket=" + final["ticket"])
    request.add_header("Authorization", AUTH)
    request.add_header("X-App-Token", TOKEN)
    request.get_method = lambda: method
    opener.addheaders = [("Authorization", "X-App-Token")]
    data = opener.open(request).read()
    final = json.loads(data)
    print final


# Publish Dataset
method = "POST"
request = urllib2.Request(baseURL + "/api/views/" + copyID + "/publication.json")
request.add_header("Authorization", AUTH)
request.add_header("X-App-Token", TOKEN)
opener.addheaders = [("Authorization", "X-App-Token")]
request.get_method = lambda: method
data = opener.open(request).read()
print "PUBLISHED"
