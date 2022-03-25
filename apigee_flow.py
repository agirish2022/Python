from google.cloud import storage
import xml.etree.ElementTree as ET
import itertools
import os
import argparse

DESIREDSCHMA    = {'Proxy': {'PreFlow' : {'Request' : None, 'Response' : None},'PostFlow' : {'Request' : None, 'Response' : None } , 'Flows' : None}, 'Target': {'PreFlow' : {'Request' : None, 'Response' : None},'PostFlow' : {'Request' : None, 'Response' : None } , 'Flows' : None}}

def read_populate(bucketname,path,flowtype):
    client = storage.Client()
    bucket = client.get_bucket(bucketname)
    blob = bucket.get_blob(path)


    data = blob.download_as_string()
    root = ET.fromstring(data)
    reqpreflow = []
    respreflow = []
    reqpostflow = []
    respostflow = []
    reqflowdic = {}
    resflowdic = {}
    condflow = {}
    
    for child in root:
        if child.tag == "PreFlow":
            for subchild in child:
                if subchild.tag == "Request":
                    for subsubchild in subchild:
                        if subsubchild.tag == "Step":
                            requestdict=dict(itertools.zip_longest([i.text for i in subsubchild.findall('Name')], [i.text for i in subsubchild.findall('Condition')]))
                            reqpreflow.append(requestdict)
                if subchild.tag == "Response":
                    for subsubchild in subchild:
                        if subsubchild.tag == "Step":
                            responsedict=dict(itertools.zip_longest([i.text for i in subsubchild.findall('Name')], [i.text for i in subsubchild.findall('Condition')]))
                            respreflow.append(responsedict)
            
        if child.tag == "PostFlow":
            for subchild in child:
                if subchild.tag == "Request":
                    for subsubchild in subchild:
                        if subsubchild.tag == "Step":
                            requestdict=dict(itertools.zip_longest([i.text for i in subsubchild.findall('Name')], [i.text for i in subsubchild.findall('Condition')]))
                            reqpostflow.append(requestdict)
                if subchild.tag == "Response":
                    for subsubchild in subchild:
                        if subsubchild.tag == "Step":
                            responsedict=dict(itertools.zip_longest([i.text for i in subsubchild.findall('Name')], [i.text for i in subsubchild.findall('Condition')]))
                            respostflow.append(responsedict)
        if child.tag == "Flows":
            for subchild in child:
                if subchild.tag == "Flow":
                    flowname = subchild.attrib['name']
                    for flowchild in subchild:
                        if flowchild.tag == "Request":
                            reqflow = []
                            resflow = []
                            for subflowchild in flowchild:
                                if subflowchild.tag == "Step":
                                    requestdict=dict(itertools.zip_longest([i.text for i in subflowchild.findall('Name')], [i.text for i in subflowchild.findall('Condition')]))
                                    reqflow.append(requestdict)
                            reqflowdic[flowname]  = reqflow      
                        if flowchild.tag == "Response":
                            for subflowchild in flowchild:
                                if subflowchild.tag == "Step":
                                    responsedict=dict(itertools.zip_longest([i.text for i in subflowchild.findall('Name')], [i.text for i in subflowchild.findall('Condition')]))
                                    resflow.append(responsedict)
                            resflowdic[flowname]  = resflow        
                        if flowchild.tag == "Condition": 
                            condflow[flowname] =  flowchild.text
              
    proxyflow ={}


    for key in reqflowdic:
        keyname={}
        if key in condflow:
            keyname["Condition"] = condflow[key]
        keyname["Request"] = reqflowdic[key]
        keyname["Response"] = resflowdic[key]
        proxyflow[key] = keyname

        
    #print(flowparser)   

    DESIREDSCHMA[flowtype]['PreFlow']['Request'] = reqpreflow
    DESIREDSCHMA[flowtype]['PreFlow']['Response'] = respreflow
    DESIREDSCHMA[flowtype]['PostFlow']['Request'] = reqpostflow
    DESIREDSCHMA[flowtype]['PostFlow']['Response'] = respostflow
    DESIREDSCHMA[flowtype]['Flows'] = proxyflow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucketname", help="Name of bucket where stored apigee data",
                        type=str,required=True)
    parser.add_argument("--pathtillproxy", help="Path till Proxy Name",
                        type=str,required=True)
    args            =   parser.parse_args()
    bucketname      =   args.bucketname
    pathtillproxy   =   args.pathtillproxy
    path            =   "latest_prod_reports/se-prod/proxies/Quote-V2"
    proxypath       =   os.path.join(pathtillproxy, "apiproxy/proxies", "default.xml") 
    targetpath      =   os.path.join(pathtillproxy, "apiproxy/targets", "default.xml")
    read_populate(bucketname,proxypath,"Proxy")
    read_populate(bucketname,targetpath,"Target")
    print(DESIREDSCHMA)
    
if __name__ == '__main__':
    main()
