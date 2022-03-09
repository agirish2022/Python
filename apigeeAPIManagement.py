import google.auth
import google.auth.transport.requests
import os
import requests
import argparse
import ast


def get_token():
    # getting the credentials and project details for gcp project
    credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    #getting request object
    auth_req = google.auth.transport.requests.Request()
    #refresh token
    credentials.refresh(auth_req) 
    return credentials.token # Return token
        
#def create_header():
#    TOKEN = get_token()
#    headers = {
#   #'Content-Type': 'multipart/form-data',
#    'Authorization': f"Bearer {TOKEN}"
#    }
#    return headers

#Import bundle

def import_bundle(formedHeaders,organizations,bundlezipfile,apiname):
    try:
        paramstemp = eval(f"(('name', '{apiname}'),('action', 'import'),('validate', 'true'))")
        #filestemp = ast.literal_eval(f"{{'data': ('{bundlezipfile}', open('{bundlezipfile}', 'rb'))}}")
        #{'data': (bundlezipfile, open('{bundlezipfile}', 'rb'))}
        #with open(r'C:\Users\example\Desktop\code\de.txt','rb') as filedata:
        #r = requests.post(url,  auth=(user, password), files={'file': filedata})
        URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/apis"
        #response = requests.post( URL , headers=formedHeaders, params=paramstemp, files=filestemp)
        response = requests.post( URL , headers=formedHeaders, params=paramstemp, files={'data': ( bundlezipfile, open(bundlezipfile,'rb'))})
        response.raise_for_status()

    except Exception as e:
        print(e)
    return response.json()['revision']
    
#Deploy bundle as revision    


def deploy_as_revision(formedHeaders,organizations,environments,apiname,revisionNum):
    try:
        #revisionNum = import_bundle()
        DEPLOY_URL = f"https://apigee.googleapis.com/v1/organizations/{organizations}/environments/{environments}/apis/{apiname}/revisions/{revisionNum}/deployments"
        response = requests.post(DEPLOY_URL, headers=formedHeaders)
        response.raise_for_status()
    except Exception as e:
        print(e) 
       
       
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--organization", help="Organization name",
                        type=str,required=True)
    parser.add_argument("--environment", help="Give environment name where you wise to deploy",
                        type=str,required=True)
    parser.add_argument("--apiname", help="Name of APIProxy",
                        type=str,required=True)
    parser.add_argument("--bundlezipfile", help="Bundle file",
                        type=str,required=True)                    
    args = parser.parse_args()
    organizations=args.organization
    environments=args.environment
    apiname=args.apiname
    bundlezipfile=args.bundlezipfile
    
    TOKEN = get_token()
    formedHeaders = {
    #'Content-Type': 'multipart/form-data',
    'Authorization': f"Bearer {TOKEN}"
    }
    revisionNum=import_bundle(formedHeaders,organizations,bundlezipfile,apiname)
    deploy_as_revision(formedHeaders,organizations,environments,apiname,revisionNum)
      
    
    
if __name__ == '__main__':
    main()
       

