#This simple script inputs the dowloads files from the asdb v3 database
#and modifies the adress for downloading the gbk files (there are ~169K gbk files)
#Then I will write a bash script for sendind download requests, in a nextfow script
#in bathces of five files sleeping 5 seconds between file requests and using 3 cores (3 processes in parallel)
#retry each process 3 times at most and apply error strategy of waiting exponential time up to 10 min

import pandas as pd
import numpy as np
import re 

df=pd.read_csv("asdb_3_ud.tsv", sep="\t") 

i=0
reacc=re.compile(r'/(?P<ac>\w+)\.\d+(?P<reg>\.region\d\d\d\.gbk)$')
for row in df["updated_url"].values:
    m=reacc.search(row)
    i=int(m.start())
    root_url= row[0:i+1]
    if re.match(r'\w{2,3}_\D{6,}', m.group(1)):
        name=m.group(1)
        prefix=name[-5:]
        sufix=name[0:7]
        n=root_url+"c"+prefix+"_"+sufix+".."+m.group(2)
        #print(n)
    elif re.match(r'\w\w_\D{4,}',m.group(1) ):
        n=root_url+"".join(m.group(1,2))
    else:
        n=row
    df.iat[i,14]=n
    #print(n)
    i+=1

df.to_csv("asdb_3_updated.2.tsv", sep="\t", index=False)

#org1=""
#org2=""
#start_arr=[]
#temp_lines={}
#prev_line=False
#
#out= open("asdb_3_download.tsv") 
#with open("tmp.tsv", "r") as f:
#    colnames=next(f)
#    for line in f:
#        org1=dd
#        if(prev_line and org1 != org2):
#
#        line=line.rstrip()
#       line_arr=line.split("\t")
#       ncbi_id=line_arr[3]
#       start=int(line_arr[4])
#       download=line_arr[12]



