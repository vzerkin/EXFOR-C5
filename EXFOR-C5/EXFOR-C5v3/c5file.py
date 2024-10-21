"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import math #round
from c5line import *

def readC5fileDataset(fileName,DatasetID):
#    print('---readC5fileDataset---'+fileName+':'+DatasetID)
    ff=open(fileName,"r")
    ii=0
    nowDataset=None
    nowDatasetID='x'
    for line1 in ff:
        line1=line1.rstrip('\n')
        if line1.startswith("#DATASET "):
            ss=line1.strip().split()
            nowDatasetID=ss[1]
            if (nowDatasetID!=DatasetID): continue
            nowDataset={}
            nowDataset['lines']=[]
            ii+=1
        if (nowDataset is not None):
            nowDataset['lines'].append(line1)
            #print('append[[',line1,']]')
        if line1.startswith("#/DATASET "):
            if (nowDataset is not None):
                exctractC5DatasetLines(nowDataset,delLines=True,flagDataLines=True)
                break
    ff.close()
    return nowDataset

def exctractC5Data(ds,fx=1,fy=1,recalc2orig=False):
    lines=ds.get('dataLines')
    if (lines==None): return
    ds['data']=[]
    for i in range(8): ds['data'].append([])
    ii=0
    FcMax=0;FcMin=0
    prec=12
    for line1 in lines:
        ii+=1
#        print(str(ii)+'\t['+line1+']')
        c5=c5line(line1)
        #ds['data'][0].append(c5.Energy*fx)
        #ds['data'][1].append(c5.dEnergy*fx)
        ds['data'][0].append(round(c5.Energy*fx,prec))
        ds['data'][1].append(round(c5.dEnergy*fx,prec))
        Data=c5.Data
        dData=c5.dData
        if recalc2orig:
            #renormalized data: recalculate back to original
            if c5.Fc>0: Data/=c5.Fc
            if c5.FcErr>0: dData/=c5.FcErr
        #ds['data'][2].append(Data*fy)
        #ds['data'][3].append(dData*fy)
        ds['data'][2].append(round(Data*fy,prec))
        ds['data'][3].append(round(dData*fy,prec))

        #renormalized data: collect MinMax Factor for display
        if c5.Fc>0 :
            if FcMax>0 :
                if c5.Fc>FcMax : FcMax=c5.Fc
                if c5.Fc<FcMin : FcMin=c5.Fc
            else :
                FcMax=c5.Fc
                FcMin=c5.Fc
    ds['FcMax']=FcMax
    ds['FcMin']=FcMin
    maxDiff=FcMax
    if maxDiff>0:
        if 1/FcMax>maxDiff: maxDiff=1/FcMax
        if 1/FcMin>maxDiff: maxDiff=1/FcMin
    ds['maxDiff']=maxDiff
    ds['txtDiff']=Fc2Diff(FcMin,FcMax)

def Fc2Diff(FcMin,FcMax):
    if FcMax==0: return ''
    if FcMin<FcMax:
#        ss=f'[{addedFcPercent(FcMin)}..{addedFcPercent(FcMax)}]%'
        ss='['+addedFcPercent(FcMin)+'..'+addedFcPercent(FcMax)+']%'
    else:
#        ss=f'{addedFcPercent(FcMin)}%'
        ss=addedFcPercent(FcMin)+'%'
    return ss

def addedFcPercent(RRR):
#    if RRR<1: ss=f'{(RRR-1)*100:.2f}'
#    else:     ss=f'+{(RRR-1)*100:.2f}'
    if RRR<1: ss= "%.2f" % ((RRR-1)*100)
    else:     ss="-%.2f" % ((RRR-1)*100)
    return ss

def exctractC5DatasetLines(ds,delLines=True,flagDataLines=False):
    lines=ds.get('lines')
    if (lines==None): return

#    for ii,line1 in enumerate(lines): print(ii,line1)

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
#        print(ii,line1)
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
 #                   print('C5DATA_started:'+str(C5DATA_started)+' ii='+str(ii)+' C5DATA_iiline='+str(C5DATA_iiline)+'\t['+line1+']')
                    ds['dataLines'].append(line1)
    if delLines: del ds['lines']
    if corrected is not None:
        if ds['author1'] is not None: ds['author1']+=corrected
        else: ds['author1']=corrected
