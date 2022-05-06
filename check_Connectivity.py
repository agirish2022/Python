#python3 check_Connectivity.py --subnetname XXXXXXX --destinationip XXXX --projectid XXXXXXX
import google.auth
import google.auth.transport.requests
import os
import requests
import argparse
import sys
import ipaddress

def get_token():
    # getting the credentials and project details for gcp project
    credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    #getting request object
    auth_req = google.auth.transport.requests.Request()
    #refresh token
    credentials.refresh(auth_req) 
    return credentials.token # Return token

#get VPC ,REGION & CIDR for subnet shared
#https://cloud.google.com/compute/docs/reference/rest/v1/subnetworks/listUsable?apix_params=%7B%22project%22%3A%22ashwinknaik-314910%22%7D
#curl "https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/subnetworks/listUsable" \
#  -X GET \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def get_vpc_region_cidr(formedHeaders,project,subnetname): 
    try:
        DEPLOY_URL = f"https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/subnetworks/listUsable"
        response = requests.get(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e)
    details                     =       {}    
    for item in response.json()['items']:
        if item['subnetwork'].split('/')[-1] == subnetname :
            details['region']           =       item['subnetwork'].split('/')[-3]
            details['vpcname']          =       item['network'].split('/')[-1]
            details['ipCidrRange']      =       item['ipCidrRange']
            return details
            
#https://cloud.google.com/compute/docs/reference/rest/v1/routes/list
#curl "https://compute.googleapis.com/compute/v1/projects/{project}/global/routes" \
#  -X GET \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def get_route_details(formedHeaders,project,vpcname): 
    try:
        DEPLOY_URL = f"https://compute.googleapis.com/compute/v1/projects/{project}/global/routes"
        response = requests.get(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e)
    vpc_route_details   = [] 
    for item in response.json()['items']:
        if item['network'].split('/')[-1] == vpcname :
            vpc_route_details.append(item)
    return vpc_route_details


#https://cloud.google.com/compute/docs/reference/rest/v1/firewalls/list
#curl "https://compute.googleapis.com/compute/v1/projects/{project}/global/firewalls" \
#  -X GET \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def get_fw_details(formedHeaders,project,vpcname): 
    try:
        DEPLOY_URL = f"https://compute.googleapis.com/compute/v1/projects/{project}/global/firewalls"
        response = requests.get(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e)
    vpc_fw_details   = []    
    for item in response.json()['items']:
        if item['network'].split('/')[-1] == vpcname :
            vpc_fw_details.append(item)
    return vpc_fw_details
	
	
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subnetname", help="Subnet details from where connectivity need to check",
                        type=str,required=True)
    parser.add_argument("--destinationip", help="Destination IP to check connectivity from subnet",
                        type=str,required=True)
    parser.add_argument("--projectid", help="Project ID",
                        type=str,required=True)

    args                =   parser.parse_args()
    subnetname          =   args.subnetname
    destinationip       =   args.destinationip
    project             =   args.projectid
   
    TOKEN = get_token()
    formedHeaders = {
    'Authorization': f"Bearer {TOKEN}"
    }
    
    
    
    infodetails         =       get_vpc_region_cidr(formedHeaders,project,subnetname)
    #get_route_details(formedHeaders,project,infodetails['vpcname'])
    #get_fw_details(formedHeaders,project,infodetails['vpcname'])
    if (ipaddress.ip_address(destinationip).is_private):
        vpcroutedetails         =       get_route_details(formedHeaders,project,infodetails['vpcname']) 
        destipsrange_route      =       []
        is_route_exist          =       False
        #import pdb;pdb.set_trace()
        for vpcitem in vpcroutedetails:
            if not ("nextHopGateway" in vpcitem.keys()):
                destipsrange_route.append(vpcitem["destRange"])
        #Check for route presence
        for destiprange_route in destipsrange_route:
            if ipaddress.ip_address(destinationip) in ipaddress.ip_network(destiprange_route):
                is_route_exist = True
        #Check for fw presence        
        if  is_route_exist :
            fwdetails   =   get_fw_details(formedHeaders,project,infodetails['vpcname'])
            allowpriority   = 65536 #65535 Highest priority + 1
            denypriority    = 65536 #65535 Highest priority + 1
            for fwdetail in fwdetails:
                if ((fwdetail["direction"]  == "INGRESS") and ( not ( "targetTags" in fwdetail.keys())) and ("sourceRanges" in fwdetail.keys())) :
                    sourcerangelist   = fwdetail["sourceRanges"]
                    if ("allowed" in fwdetail.keys()):
                        for rangeitem in sourcerangelist: 
                            if(ipaddress.ip_network(infodetails['ipCidrRange'],False).subnet_of(ipaddress.ip_network(rangeitem,False))):
                                allowpriority = int(fwdetail["priority"]) 
                    if ("denied" in fwdetail.keys()): 
                        for rangeitem in sourcerangelist: 
                            if(ipaddress.ip_network(infodetails['ipCidrRange'],False).subnet_of(ipaddress.ip_network(rangeitem,False))):
                                denypriority = int(fwdetail["priority"]) 
                if allowpriority < denypriority :
                    print("Connection Allowed")
                elif allowpriority > denypriority :
                    print("Connection Denied")                       
          
    else:
        #import pdb;pdb.set_trace()
        vpcroutedetails =       get_route_details(formedHeaders,project,infodetails['vpcname'])      
        for vpcitem in vpcroutedetails:
            if "nextHopGateway" in vpcitem.keys():
                if vpcitem["nextHopGateway"].split('/')[-1]   ==   "default-internet-gateway" :           
                    #Checking if Routing is availiable 
                    destiprange     =   vpcitem["destRange"]                 
                    if ipaddress.ip_address(destinationip) in ipaddress.ip_network(destiprange):
                        #Checking if FW is availiable
                        fwdetails   =   get_fw_details(formedHeaders,project,infodetails['vpcname'])
                        allowpriority   = 65536 #65535 Highest priority + 1
                        denypriority    = 65536 #65535 Highest priority + 1
                        for fwdetail in fwdetails:
                            if (fwdetail["direction"]  == "EGRESS") :
                                destrangelist   = fwdetail["destinationRanges"]
                                if ("allowed" in fwdetail.keys()):
                                    for rangeitem in destrangelist: 
                                        if ipaddress.ip_address(destinationip) in ipaddress.ip_network(rangeitem):
                                            allowpriority = int(fwdetail["priority"]) 
                                if ("denied" in fwdetail.keys()): 
                                    for rangeitem in destrangelist: 
                                        if ipaddress.ip_address(destinationip) in ipaddress.ip_network(rangeitem):
                                            denypriority = int(fwdetail["priority"]) 
                            if allowpriority < denypriority :
                                print("Connection Allowed")
                            elif allowpriority > denypriority :
                                print("Connection Denied")    
                        
    
        
        
    
if __name__ == '__main__':
    main()	
	
