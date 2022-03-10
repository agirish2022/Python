import google.auth
import google.auth.transport.requests
import os
import requests
import argparse


def get_token():
    # getting the credentials and project details for gcp project
    credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    #getting request object
    auth_req = google.auth.transport.requests.Request()
    #refresh token
    credentials.refresh(auth_req) 
    return credentials.token # Return token

#Import bundle
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/apis?name=fromzipapi&action=import&validate=true" \
# -X POST \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" \
#  --form 'data=@"api.zip"'
def import_bundle(formedHeaders,organizations,bundlezipfile,apiname):
    try:
        paramstemp = eval(f"(('name', '{apiname}'),('action', 'import'),('validate', 'true'))")
        URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/apis"
        response = requests.post( URL , headers=formedHeaders, params=paramstemp, files={'data': ( bundlezipfile, open(bundlezipfile,'rb'))})
        response.raise_for_status()
    except Exception as e:
        print(e)
    return response.json()['revision']
    
#Deploy bundle as revision    
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/environments/eval/apis/fromzipapi/revisions/1/deployments" \
#  -X POST \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def deploy_as_revision(formedHeaders,organizations,environments,apiname,revisionNum):
    try:
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/environments/{environments}/apis/{apiname}/revisions/{revisionNum}/deployments"
        response = requests.post(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 

#Get deployed revision number
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/apis/testapi/deployments" \
#  -X GET \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def get_rev_num(formedHeaders,organizations,apiname): 
    try:
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/apis/{apiname}/deployments"
        response = requests.get(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 
    return response.json()['deployments'][0]['revision']

#Undeploy revision
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/environments/eval/apis/apifromzip/revisions/1/deployments" \
#  -X DELETE \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def undeploy_revision(formedHeaders,organizations,environments,apiname,revisionNum): 
    try:
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/environments/{environments}/apis/{apiname}/revisions/{revisionNum}/deployments"
        response = requests.delete(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 

#Delete revision        
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/apis/apifromzip/revisions/1" \
#  -X DELETE \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def delete_revision(formedHeaders,organizations,apiname,revisionNum): 
    try:
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/apis/{apiname}/revisions/{revisionNum}"
        response = requests.delete(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 

#Delete proxy        
#curl "https://apigee.googleapis.com/v1/organizations/xxxxx/apis/apifromzip" \
#  -X DELETE \
#  -H 'Content-Type: multipart/form-data' \
#  -H "Authorization: Bearer $TOKEN" 
def delete_proxy(formedHeaders,organizations,apiname): 
    try:
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/apis/{apiname}"
        response = requests.delete(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 
        
       
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", help="give amoung these importanddeploy/undeployanddelete",
                        type=str,required=True)
    parser.add_argument("--organization", help="Organization name",
                        type=str,required=True)
    parser.add_argument("--apiname", help="Name of APIProxy",
                        type=str,required=True)
    parser.add_argument("--environment", help="Give environment name where you wise to deploy",
                        type=str,required=True)
    parser.add_argument("--bundlezipfile", help="Bundle file",
                        type=str)                    
    args            =   parser.parse_args()
    action          =   args.action
    organizations   =   args.organization
    environments    =   args.environment
    apiname         =   args.apiname
    bundlezipfile   =   args.bundlezipfile
    
    TOKEN = get_token()
    formedHeaders = {
    'Authorization': f"Bearer {TOKEN}"
    }
    if action == "importanddeploy" :
        if bundlezipfile == None:
            print("--bundlezipfile argument is expected")
        revisionNum=import_bundle(formedHeaders,organizations,bundlezipfile,apiname)
        deploy_as_revision(formedHeaders,organizations,environments,apiname,revisionNum)
    elif action == "undeployanddelete" :
        revisionNum=get_rev_num(formedHeaders,organizations,apiname)
        undeploy_revision(formedHeaders,organizations,environments,apiname,revisionNum)
        delete_proxy(formedHeaders,organizations,apiname)
    
if __name__ == '__main__':
    main()
       
