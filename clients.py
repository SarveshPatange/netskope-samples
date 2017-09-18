#import stuff
import json
import requests
import csv

#Ask for Netskope REST API Token and Tenant name
token = raw_input("Enter Netskope REST API Token: ")
t_name = raw_input("Enter Netskope tenant name: ")
period = raw_input("Enter Time Period (3600|86400|604800|2592000|5184000|7776000): ")

#construct url
url = "https://%s.goskope.com/api/v1/clients?token=%s" % (t_name,token)
#print(url)

#make the request and get the output
response = requests.get(url)
clients = response.json()
csvfile = open("exported-clients.csv", "w")
writer = csv.writer(csvfile, delimiter = ",")
writer.writerow(["Username","OS","OS Version","Classification Status", "Last Event"])

for i in clients["data"]:
	row = i["attributes"]["users"][0]["username"],i["attributes"]["host_info"]["os"],i["attributes"]["host_info"]["os_version"],i["attributes"]["users"][0]["device_classification_status"],i["attributes"]["last_event"]["status"]
	writer.writerow(row)
csvfile.close()

for i in clients["data"]:
	print i["attributes"]["users"][0]["username"],i["attributes"]["host_info"]["os"],i["attributes"]["host_info"]["os_version"],i["attributes"]["last_event"]["status"]
