# Python

**Import and Deploy**
```
python3 apigeeAPIManagement.py --action importanddeploy --organization XXXXXX --environment eval --apiname apifromzip --bundlezipfile apigee-proxies_rev3_2022_03_03.zip
```

**Undeploy and Delete**
```
python3 apigeeAPIManagement.py --action undeployanddelete --organization XXXXXX --environment eval --apiname apifromzip
```
**Apigee Flow**
```
python3 apigee_flow.py --bucketname 'XXXXXX' --pathtillproxy 'XXXXXX'
```

https://github.com/apigee/terraform-modules/tree/main/samples/x-l7xlb


python3 change.py --organization xxxxx --environment test1:test2 --apiname apifrombundle --bundlezipfile apigee-proxies_rev3_2022_03_03.zip --lburl test.ip.nip.io
