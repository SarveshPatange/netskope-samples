#import stuff
import json
import requests
import csv

#Ask for Netskope REST API Token and Tenant name
token = raw_input("Enter Netskope REST API Token: ")
t_name = raw_input("Enter Netskope tenant name: ")
query_type = raw_input("Which API endpoint (report, clients, events)? ")
period = raw_input("Enter Time Period (3600|86400|604800|2592000|5184000|7776000): ")

#construct url
if query_type == 'report':
    eventtype = raw_input("Enter Event Type (connection, application, alert): ")
    groupby = raw_input("Group By (application, user, device, activity): ")
    # hardcoded to groupby = device and subgroupby = none
    url = "https://%s.goskope.com/api/v1/%s?token=%s&type=%s&timeperiod=%s&groupby=%s" % (t_name,query_type,token,eventtype,period,groupby)
elif query_type == 'clients':
    url = "https://%s.goskope.com/api/v1/%s?token=%s" % (t_name,query_type,token)
elif query_type == 'events':
    type_of_event = raw_input("Enter event type (application, connection, audit): ")
    querystring = raw_input("Enter Query String: ")
    url = "https://%s.goskope.com/api/v1/%s?token=%s&type=%s&timeperiod=%s&query=%s" % (t_name,query_type,token,type_of_event,period,querystring)
    print url

#make the request and get the output
r = requests.get(url)
output = r.json()
json_status = output['status']

if json_status == 'success':
    print("API RESPONSE: " +json_status) # show request status

    #print output in a pretty format
    #print("Here's the output: ")
    #print(json.dumps(output, indent=4))

    #save output to file
    with open('NS-API-output.json','wb') as f:
        json.dump(output,f)
    print("Output saved to: NS-API-output.json")
else:
    print("Well. That didn't work.")
