import pandas as pd
import numpy as np
import re

df = pd.read_csv("asdb_3.tsv", sep='\t')
ndf=pd.DataFrame()

#print(df.groupby("NCBI accession").count().head())
ncbi_acc_set = set(df["NCBI accession"])

for acc in ncbi_acc_set:
    df_acc=df[df["NCBI accession"] == acc]
    df_acc=df_acc.sort_values(by="From")
    #add rownumber column
    df_acc["N"]=np.arange(df_acc.shape[0])+1
    #modifiy download string replace
    df_acc["updated_url"]=df_acc["Download URL"].str.replace("api/v1.0/download/genbank","output")
    df_acc["updated_url"]=df_acc["updated_url"].str.replace("\w+/\d+/\d+/\d+$", "", regex=True)
    df_acc["updated_url"]=df_acc["updated_url"]+df_acc["NCBI accession"]+".region"+df_acc["N"].astype(str).str.zfill(3)+".gbk"
    ndf=ndf.append(df_acc)
    #df_acc.to_csv("tmpout1.tsv", sep="\t", index=False)

ndf.to_csv("asdb_3_ud.tsv", sep="\t", index=False)



