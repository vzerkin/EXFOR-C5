"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import csv

def read_csv_file(filename):
    reader=csv.reader(open(filename,'r'))
    array=[]
    ii=0
    for row in reader:
        #print(str(ii),'\t',row)
        if (ii==0): header=row;
        else:
            dict1={}
            for i in range(len(header)):
                key=header[i]
                val=row[i]
                dict1[key]=val
            array.append(dict1)
        ii+=1
    return array

def filter_datasets(datasets,nam,val):
    array=[]
    ii=0
    for dataset in datasets:
        #print(str(ii),'\t',dataset)
        xx=dataset.get(nam)
        #print(str(ii),'\txx:',xx)
        if xx is None: continue;
        if (xx!=val): continue
        array.append(dataset)
        ii+=1
    return array

def not_filter_datasets(datasets,nam,val):
    array=[]
    ii=0
    for dataset in datasets:
        #print(str(ii),'\t',dataset)
        xx=dataset.get(nam)
        #print(str(ii),'\txx:',xx)
        if (xx==val): continue
        array.append(dataset)
        ii+=1
    return array
