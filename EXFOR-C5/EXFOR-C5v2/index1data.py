"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import os
import json
import sys
import csv

print("Program: index1data.py, ver. 2024-10-17")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023-2024")
print("Purpose: scan dir recursively, find files by extension .c5,")
print("         create index of Datasets for data search,")
print("         store index in JSON and CSV files\n")

base='./'

def filesFromDir(dirName,ext,ilevel=0,allFiles=[]):
    listOfFiles=os.listdir(dirName)
    nfiles=0;ndirs=0
    for file1 in listOfFiles:
        fullPath=os.path.join(dirName,file1)
        if os.path.isdir(fullPath):
            ndirs+=1
            filesFromDir(fullPath,ext,ilevel=ilevel+1,allFiles=allFiles)
        else:
            if not fullPath.endswith(ext): continue
            nfiles+=1
            allFiles.append(fullPath)
    return allFiles

def readC5file(fileName,allC5Datasets=None,delLines=True,flagDataLines=False):
    if allC5Datasets==None: allC5Datasets=[]
#    print('---readC5file---'+str(len(allC5Datasets)))
    ff=open(fileName,"r")
    ii=0
    nowDataset=None
    for line1 in ff:
        line1=line1.rstrip('\n')
        if line1.startswith("#DATASET "):
            nowDataset={}
            nowDataset['c5file']=fileName[len(base):].replace('\\','/')
            nowDataset['lines']=[]
            #allC5Datasets.append(nowDataset)
            ii+=1
        if (nowDataset is not None):
            nowDataset['lines'].append(line1)
        if line1.startswith("#/DATASET "):
            exctractC5DatasetLines(nowDataset,delLines=delLines,flagDataLines=flagDataLines)
            needed=True
            if nowDataset.get('derived') is not None: needed=False #exclude derived (not measured data)
            if needed: allC5Datasets.append(nowDataset)
            nowDataset=None
    ff.close()
    return allC5Datasets

def exctractC5DatasetLines(ds,delLines=True,flagDataLines=False):
    lines=ds.get('lines')
    if (lines==None): return

    #initialize only to define order in JSON output
    ds['Entry']=None
    ds['DatasetID']=None
    ds['x4status']=None
    ds['updated']=None
    ds['year1']=None
    ds['author1']=None
#    ds['corrected']=None
    ds['derived']=None
    ds['zaProj1']=None
    ds['zaTarg1']=None
    ds['zTarg1']=None
    ds['Targ1']=None
    ds['Proj1']=None
    ds['Emis1']=None
    ds['ReactionType']=None
    ds['MF']=None
    ds['MT']=None
    ds['nPoints']=None
    ds['ReactionCode']=None
    if flagDataLines: ds['dataLines']=[]

    C5DATA_started=False
    C5DATA_iiline=0
    C5DATA_ndata=0
    corrected=None
    ii=0
    for line1 in lines:
        ii+=1
        #print (ii,line1)
        subs=line1.strip().split()
        if   line1.startswith("#ENTRY "):    ds['Entry']=subs[1]
        elif line1.startswith("#DATASET "):  ds['DatasetID']=subs[1]
        elif line1.startswith("#DATE "):     ds['updated']=int(subs[1])
        elif line1.startswith("#STATUS "):   ds['x4status']=subs[1]
        elif line1.startswith("#YEAR "):     ds['year1']=int(subs[1])
        elif line1.startswith("#AUTHOR1 "):  ds['author1']=line1[16:].strip().rstrip('+')
#        elif line1.startswith("#C5CORR "):   ds['corrected']='CORRECTED'
        elif line1.startswith("#C5CORR "):   corrected='*'
        elif line1.startswith("#Ratio2CS "): corrected='#' #Ratio:MF203-->CS:MF3
        elif line1.startswith("#TARG "):     ds['zaTarg1']=int(subs[1]); ds['zTarg1']=int(subs[1])//1000
        elif line1.startswith("#PROJ "):     ds['zaProj1']=int(subs[1])
        elif line1.startswith("#TARGET "):
            SF1=line1[48:64].strip()
            Targ1='-'.join(SF1.split('-')[1:])
            Targ1=Targ1[:1].upper()+Targ1[1:].lower()
            ds['Targ1']=Targ1
        elif line1.startswith("#REAC1 "):
            SF23=subs[1].split(',')
            ds['Proj1']=SF23[0].lower()
            ds['Emis1']=SF23[1]
        elif line1.startswith("#ReactionType "): ds['ReactionType']=subs[1]
        elif line1.startswith("#MF "):       ds['MF']=int(subs[1])
        elif line1.startswith("#MT "):       ds['MT']=int(subs[1])
        elif line1.startswith("#REACTION "): ds['ReactionCode']=subs[1]
        elif line1.startswith("#DERIVED "):  ds['derived']='DERIVED'
        elif line1.startswith("#C5DATA "):
            ds['nPoints']=int(subs[1])
            C5DATA_ndata=int(subs[1])
            C5DATA_started=True
            C5DATA_iiline=0
        elif line1.startswith("#/C5DATA "): C5DATA_started=False
        if C5DATA_started:
            C5DATA_iiline+=1
            if C5DATA_iiline>6:
                if flagDataLines: 
                    #print('C5DATA_started:'+str(C5DATA_started)+' ii='+str(ii)+' C5DATA_iiline='+str(C5DATA_iiline)+'\t['+line1+']')
                    ds['dataLines'].append(line1)
    if delLines: del ds['lines']
    if corrected is not None:
        if ds['author1'] is not None: ds['author1']+=corrected
        else: ds['author1']=corrected

c5files=filesFromDir(base,'.c5') #recursively finds all files: .c5
nc5files=len(c5files)
print('c5files:'+str(nc5files))

#read c5 files extracting information for indexing data
ii=0
Datasets=None
for c5file in c5files:
    ii+=1
    #if (ii>3): break #uncomment for fast test
#    Datasets=readC5file(c5file) #Datasets from single file
#    Datasets=readC5file(c5file,Datasets,flagDataLines=True) #accumulating Datasets with: exctact data lines
    Datasets=readC5file(c5file,Datasets) #accumulating Datasets
    print(str(ii)+'/'+str(nc5files)+' file:'+c5file+' total_datasets:'+str(len(Datasets)), end='\r')
print('')

#ii=0
#for Datasets1 in Datasets:
#    ii+=1; print(ii,'::::',Datasets1)

Datasets=sorted(Datasets, key=lambda i:i['DatasetID'])

#out index of data to JSON file
with open("C5-Datasets.json",'w') as outfile: json.dump(Datasets,outfile,indent=2)

#out index of data to CSV file: selected columns only
cols=['c5file','Entry','DatasetID'
	,'x4status'
	,'updated','year1','author1'
	,'zaProj1','zaTarg1','zTarg1','Targ1','Proj1','Emis1'
	,'ReactionType','MF','MT','nPoints','ReactionCode']
with open("C5-Datasets.csv", "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
    writer.writeheader()
    writer.writerows(Datasets)
print('\nProgram index1data successfully completed')
