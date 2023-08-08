"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
#from pprint import pprint

class c5line:

    def __init__(self,line):
#        self._line=line
        self.SubentP=strExtractStr(line,123,131,"").strip().replace(' ','0')
        self.zaProj=strExtractInt(line,1,5,-1)
        self.zaTarg=strExtractInt(line,6,11,-1)
        self.Meta=strExtractStr(line,12,12," ").strip()
        self.MF=strExtractInt(line,13,15,-1)
        self.MT=strExtractInt(line,16,19,-1)
        self.ProdMeta=strExtractStr(line,20,20," ").strip()
        str1=strExtractStr(line,98,122,"")
        str1=str1.replace(',',' ')
        ind=str1.rfind('(')
        if (ind>0): str1=str1[0:ind]
        self.Refer=str1.strip()
        if (strExtractStr(line,23,31,"").strip()==""): self.noEnergyGiven=True
        else: self.noEnergyGiven=False
        dd=[];i0=23
        for i in range(8):
            dd.append(strExtractFloat(line,i0+i*9,i0+i*9+8,None))
        self.Energy  =dd2val(dd[0],0.)
        self.dEnergy =dd2val(dd[1],0.)
        self.Data    =dd2val(dd[2],0.)
        self.dData   =dd2val(dd[3],0.)
        self.Cos     =dd2val(dd[4],0.)
        self.dCos    =dd2val(dd[5],None)
        self.flagI87 =strExtractStr(line,95,97,"").strip()
        if self.flagI87=="E2":
            self.E2  =dd2val(dd[6],None)
            self.dE2 =dd2val(dd[7],None)
        elif self.flagI87=="QVL":
            self.QValue=dd2val(dd[6],None)
        elif self.flagI87=="LVL":
            LVL      =dd2val(dd[6],0)
            dLVL     =dd2val(dd[7],0)
            if dLVL>LVL:
                self.LVLMin=dd2val(dd[6],None)
                self.LVLMax=dd2val(dd[7],None)
            else:
                self.LVL =dd2val(dd[6],None)
                self.dLVL=dd2val(dd[7],None)
        self.dSys    =strExtractFloat(line,132,140,0.)
        self.dStat   =strExtractFloat(line,141,149,0.)
        self.dOther  =strExtractFloat(line,150,158,0.)
        self.dTot    =strExtractFloat(line,159,167,0.)
        self.Fc      =strExtractFloat(line,249,257,0.)
        self.FcErr   =strExtractFloat(line,258,266,0.)

def strExtractStr(str0,n0,n1,default):
    try:
        str1=str0[n0-1:n1]
        return str1
    except ValueError:
        return default

def strExtractInt(str0,n0,n1,default):
    str1=strExtractStr(str0,n0,n1,'')
    nn=str2int(str1,default)
    return nn

def strExtractFloat(str0,n0,n1,default):
    str1=strExtractStr(str0,n0,n1,'')
    nn=str2float(str1,default)
    return nn

def str2int(str0,default):
    try: nn=int(str0.strip())
    except ValueError: nn=default
    return nn

def str2float(str0,default):
    str1=str0.strip().upper()
    if str1.find('E')<0:
        ind=str1[1:].find('+')
        if ind<0: ind=str1[1:].find('-')
        if ind>0:
            #print('ind='+str(ind)+'['+str1[ind+1:]+']')
            #if str1[ind]!='E': str1=str1[0:ind+1]+'E'+str1[ind+1:]
            str1=str1[0:ind+1]+'E'+str1[ind+1:]
    try: nn=float(str1)
    except ValueError: nn=default
    return nn

def dd2val(dd,default):
    if dd is None: return default
    else: return dd
