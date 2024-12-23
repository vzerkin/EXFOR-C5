"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
 * Copyright (C) 2023-2024 Viktor Zerkin (NRDC), v.zerkin@gmail.com                *
 *-----------------------------------------------------------------------------    *
 * Permission is hereby granted, free of charge, to any person obtaining a copy    *
 * of this software and associated documentation files (the "Software"), to deal   *
 * in the Software without restriction, including without limitation the rights    *
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
 * copies of the Software, and to permit persons to whom the Software is furnished *
 * to do so, subject to the following conditions:                                  *
 *                                                                                 *
 * The above copyright notice and this permission notice shall be included in all  *
 * copies or substantial portions of the Software.                                 *
 *                                                                                 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
 * THE SOFTWARE.                                                                   *
 *                                                                                 *
 *-----------------------------------------------------------------------------    *
 *   AUTHOR:                                                                       *
 *   Viktor Zerkin, PhD, IAEA(1999-2023), NRDC(1996-2024)                          *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""

import datetime
import json
import sys
sys.path.append('./')
from c5subr import *
from c5file import *
import plotly
from plotly.graph_objs import Scatter, Layout 
from pprint import pprint

print("Program: c5data3.py, ver.2024-12-02")
print("Author:  V.Zerkin, IAEA, Vienna, 2024")
print("Purpose: find datasets by reaction, load C5-file, extract data, plot by Plotly\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

base='./'

def sort_ya1(ds):
    a1=ds['author1'].replace('*','').replace('#','')
    rr=str(ds['year1'])+','+a1+','+ds['DatasetID']
    return rr

datasetBlackList={
     "231620022":"92-U-235(N,G)92-U-236,,SIG 2014 C.Guerrero. Many points with negative CS"
    ,"33075002" :"25-MN-55(N,A)23-V-52,,SIG  1962,O.N.Kaul"
    ,"31316015" :"25-MN-55(N,A)23-V-52,,SIG  1965,C.S.Khurana"
    ,"11274030" :"25-MN-55(N,A)23-V-52,,SIG  1953,E.B.Paul"
    ,"11274037" :"30-ZN-64(N,P)29-CU-64,,SIG 1953,E.B.Paul"
}

#reacode='13-AL-27(N,TOT),,SIG'
#reacode='13-AL-27(N,G)13-AL-28,,SIG'
#reacode='93-NP-237(A,2N)95-AM-239,,SIG'
#reacode='25-MN-55(N,A)23-V-52,,SIG'

reacode='92-U-235(N,G)92-U-236,,SIG'
reacode2='92-U-235(N,G),,SIG'

#reacode='13-AL-27(N,A)11-NA-24,,SIG'
#reacode2='13-AL-27(N,A),,SIG'


print('\n#_________________Read full list of Datasets_________________')
datasets=read_csv_file("C5-Datasets.csv")
nDatasets=len(datasets)
print('-0-Datasets:'+str(nDatasets))

print('\n#_________________Filter Datasets: select needed and valid_________________')
datasets1=filter_datasets(datasets,'ReactionCode',reacode)
datasets2=filter_datasets(datasets,'ReactionCode',reacode2)
print('-1-Datasets1:'+str(len(datasets1)))
print('-1-Datasets2:'+str(len(datasets2)))
datasets=datasets1+datasets2
n1=nDatasets=len(datasets)
print('-1-Datasets:'+str(nDatasets))
datasets=not_filter_datasets(datasets,'x4status','SPSDD')
datasets=not_filter_datasets(datasets,'x4status','PRELIM')
for DatasetID in datasetBlackList.keys():
    datasets=not_filter_datasets(datasets,'DatasetID',DatasetID)
n2=nDatasets=len(datasets)
print('-2-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)
with open('data3lst.json','w') as outfile: json.dump(datasets,outfile,indent=2)

xtitle='Incident energy (eV)'
ytitle='Cross section (b)'

print('\n#_________________Extract data from C5 files_________________')
dss=[];ii=0
printData=False
for dataset in datasets:
    c5file=base+dataset['c5file']
    DatasetID=dataset['DatasetID']
#tst    if DatasetID!='31842017': continue  #test
#    print(str(ii+1)+')\tFile:'+c5file+' Dataset:'+DatasetID)
    ds=readC5fileDataset(c5file,DatasetID)
    if ds is None: continue
    print(str(ii+1)+') File:'+c5file+' Dataset:'+DatasetID
	+' '+str(ds['year1'])+' '+ds['author1'].title()
	+' #dataPoints:'+str(len(ds['dataLines'])))
    exctractC5Data(ds)
    if printData:
        print('	Energy:	',ds['data'][0])
        print('	dEnergy:',ds['data'][1])
        print('	Data:   ',ds['data'][2])
        print('	dData:  ',ds['data'][3])
    ds['y']=ds['data'][2]
    ds['dy']=ds['data'][3]
    ds['x']=ds['data'][0]
    ds['dx']=ds['data'][1]
    ds['x4lbl']=str(ds['year1'])+' '+ds['author1'].title()
    dss.append(ds)
    ii+=1
dss=sorted(dss,key=sort_ya1,reverse=True)

print('\n#_________________Preparing EXFOR data for plot_________________')
data1=[]; ii=0; iorig=0; irenorm=0; iratio=0
for ds in dss:
    flagModif0=''
    flagModif1=''
    msize=msize1=9
    iSymPlus=0
    symColor='Black'
    symWidth=1
    flagModif0='X ' #Original EXFOR data
    symBorder=True
    lblPrefix=' '
    if (ds['x4lbl'].find('*')>0):
        flagModif0='C ' #Renormalized: CS=CS/m0*m1 (auto-corrected)
        flagModif1=':cs/m0*m1' #Renormalized: CS=CS/m0*m1
        symBorder=True
        symColor='Red'
        msize1=msize+2
        #iSymPlus=200	#-dot
        iSymPlus=300	#-open-dot
        symWidth=1.8
        lblPrefix='*'
        irenorm+=1
    elif (ds['x4lbl'].find('#')>0):
        flagModif0='R '   #Multiplied:   CS=Ratio*m1
        flagModif1=':ratio*m1'   #Multiplied:   CS=Ratio*m1
        symBorder=False
        msize1=msize+2
        iSymPlus=100  #-open
        lblPrefix='#'
        iratio+=1
    else:
        iorig+=1
    lbl=lblPrefix+str(ii+1)+') '+flagModif0+ds['x4lbl']+' pt:'+str(len(ds['x']))\
	+' x4:'+ds['DatasetID']+flagModif1
    tr=Scatter(x=ds['x'],y=ds['y']
	,text=ds['x4lbl']
	,name=lbl
	,marker_symbol=str(ii%25+iSymPlus)
	,marker_size=msize1
	,mode="markers"
	)
    if (symBorder): tr.marker.line=dict(color=symColor,width=symWidth)
    if (ds['dy'] is not None): tr.error_y=dict(type='data',array=ds['dy'],visible=True,thickness=0.9)
    if (ds['dy'] is not None): tr.error_x=dict(type='data',array=ds['dx'],visible=True,thickness=0.9)
    data1.append(tr)
    ii+=1
#    break

xtype='linear';ytype='linear'
xtype='log'
ytype='log'
plotTitle=reacode;

print('\n#_________________Plot data from EXFOR_________________')
plot1={}
plot1['data']=data1
xaxis=dict(title=xtitle,showline=True,linecolor='black',ticks='outside'
,showgrid=True,gridcolor='#aaaaaa',type=xtype)
yaxis={'title':ytitle,'showline':True,'linecolor':'black'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
}
xaxis['mirror']='ticks'; yaxis['mirror']='ticks' 

plot1['layout']=Layout(title='EXFOR cross sections \u03c3(E): '+plotTitle
#	+' #Total datasets:'+str(n2)
	+'  Datasets:'+str(n2)
	+' excluded:'+str(n1-n2) #superseded or withdrawn, and preliminary
	+'  Original data:'+str(iorig)
	+' renormalized:'+str(irenorm)+'*C'
	+' ratio2cs:'+str(iratio)+'#R'
	+'<br><i>EXFOR-C5, by V.Zerkin, IAEA-NDS, 2010-2024, ver.2024-12-02 //running:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='c5data3'
plotly.offline.plot(plot1,filename=outhtml+'.html')

#needs: $ pip3 install -U kaleido
plotly.io.write_image(plot1,outhtml+'.png',width=1200,height=790)

print('\nProgram successfully completed')
