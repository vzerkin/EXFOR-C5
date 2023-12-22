"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
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
 *   Viktor Zerkin, PhD                                                            *
 *   e-mail: V.Zerkin@iaea.org                                                     *
 *   International Atomic Energy Agency                                            *
 *   Nuclear Data Section, P.O.Box 100                                             *
 *   Wagramerstrasse 5, Vienna A-1400, AUSTRIA                                     *
 *   Phone: +43 1 2600 21714; Fax: +43 1 26007                                     *
 *                                                                                 *
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

print("Program: c5data1.py, ver. 2023-12-22")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023")
print("Purpose: find datasets by reaction, load C5-file, extract data, plot by Plotly\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

base='./'

def sort_ya1(ds):
    rr=str(ds['year1'])+','+ds['author1']
    return rr

datasets=read_csv_file('Datasets.csv')
nDatasets=len(datasets)
print('-0-Datasets:'+str(nDatasets))

#reacode='13-AL-27(N,TOT),,SIG'
#reacode='13-AL-27(N,G)13-AL-28,,SIG'
reacode='13-AL-27(N,A)11-NA-24,,SIG'
#reacode='93-NP-237(A,2N)95-AM-239,,SIG'
#reacode='25-MN-55(N,A)23-V-52,,SIG'

datasets=filter_datasets(datasets,'ReactionCode',reacode)
nDatasets=len(datasets)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)

xtitle='Incident energy (eV)'
ytitle='Cross section (b)'
dss=[];ii=0
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

#_________________Preparing EXFOR data for plot_________________
data1=[]; ii=0; iorig=0; irenorm=0
for ds in dss:
    tr=Scatter(x=ds['x'],y=ds['y']
	,text=ds['x4lbl']
	,name=str(ii+1)+') '+ds['x4lbl']+' pt:'+str(len(ds['x']))+' #'+ds['DatasetID']
	,marker_symbol=str(ii%33)
	,marker_size=8
	,mode="markers"
	)
    if (ds['dy'] is not None): tr.error_y=dict(type='data',array=ds['dy'],visible=True,thickness=0.9)
    if (ds['dy'] is not None): tr.error_x=dict(type='data',array=ds['dx'],visible=True,thickness=0.9)
    if (ds['x4lbl'].find('*')>0):
        tr.marker.line=dict(color='Black',width=0.8)
        irenorm+=1
    else: iorig+=1
    data1.append(tr)
    ii+=1
#    break

xtype='linear';ytype='linear'
xtype='log'#;ytype='log'
plotTitle=reacode;

#_________________Plot data from EXFOR_________________
plot1={}
plot1['data']=data1
xaxis=dict(title=xtitle,showline=True,linecolor='black',ticks='outside'
,showgrid=True,gridcolor='#aaaaaa',type=xtype)
yaxis={'title':ytitle,'showline':True,'linecolor':'black'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
}
plot1['layout']=Layout(title='EXFOR cross sections \u03c3(E): '+plotTitle
	+'  Datasets:'+' original: '+str(iorig)+' renormalized: '+str(irenorm)
	+'<br><i>EXFOR-C5, by V.Zerkin, IAEA-NDS, 2010-2023, ver.2023-12-22 //running:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='c5data1'
plotly.offline.plot(plot1,filename=outhtml+'.html')
