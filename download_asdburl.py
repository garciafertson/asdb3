#!/usr/local/bin/python3
# this script input a file with a list of url adresses and send a wget request to dowanload the page,
# if correctly downloaded saves the output in asdb_gbk folder
# rename, append assembly accession to the begining of the name
#if not downloaded saves error message, adress and builds assembly_accession/index.html# adress for next trial

import pandas as pd
import requests
import sys, time
import re

with open(sys.argv[1], "r") as f:
    for line in f:
        line=line.rstrip()
        if "https" in line:
            remote_url=line
            filename="-".join(line.split("/")[-2:])
            data=requests.get(remote_url)
            time.sleep(2)
            if data.ok:
                with open(filename,"wb") as o:
                    o.write(data.content)
            else:
                print(line)
                assembly_acc=line.split("/")[-2]
                root_url="/".join(line.split("/")[0:-1])
                remote_url=root_url+"/index.html#"
                data=requests.get(remote_url)
                time.sleep(1)
                if data.ok:
                    gbk_list=re.findall(r'[\w\.]+\.gbk', data.text)
                    gbk_list=gbk_list[1:]
                    location_list=re.findall(r'Location:.+nt\.', data.text)
                    with open(filename+".tsv", "w") as o:
                        for i,gbk in enumerate(gbk_list):
                            new_url="/".join([root_url,gbk])
                            o.write("%s\t%s\t%s\n" %(line,location_list[i],new_url))

print("ok")
