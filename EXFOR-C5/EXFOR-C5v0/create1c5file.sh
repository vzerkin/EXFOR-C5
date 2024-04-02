#!/bin/bash
cat EXFOR-C5.txt
echo "        +------------------------------------------+"
echo "        |     EXFOR-C5: full EXFOR in C5 format.   |"
echo "        |  v.zerkin@iaea.org, IAEA-NDS 2010-2023   |"
echo "        |  v.zerkin@gmail.com, version 2024-04-02  |"
echo "        +------------------------------------------+"
echo ""
echo "Create single C5 file from C5 files stored in sub-directories"
echo "Script:$0 `date +%F`,`date +%T` on `uname -n`/`uname -s`"
t00=`date +%s`

FMT="C5.2.3"
if [ "$1" != "" ] ; then
    FMT=$1
fi

#cat */*/*.c5 |grep -v "^#C5.2.3" |grep -v "^#\_\_" |grep -v "^#/C5.2.3" >all.c5

rm -f all.c5
ii=0
nEntry=0; nDatasets=0; nXDatasets=0; nPoints=0
filenames="*/*/*.c5"
for name in $filenames; do
    if [ -f $name ]; then
	ii=$(($ii+1))
#	if [[ "${name:0:1}" != "3" ]]; then continue; fi	#only Area:3
#	if [[ "${name:0:5}" != "1/135" ]]; then continue; fi	#only files from 1/135
#	printf "%5d) %-18s %s \r" $ii ${name} `date +%F,%T`
	if [ $ii -eq 1 ]; then
	    cat ${name}|grep -v "^#/${FMT}">>all.c5
	else
	    cat ${name}|grep -v "^#\_\_\_"|grep -v "^#/${FMT}">>all.c5
	fi
#	nEn=`cat ${name}|grep "^#ENTRY"|sort -u|wc -l`
	nEn=1	#one ENTRY in one C5 file
	nDs=`cat ${name}|grep "^#DATASET"|wc -l`
	nXD=`cat ${name}|grep "^#/${FMT}"|awk '{print $4}'`
	str=`cat ${name}|grep "#C5DATA"|awk '{print $2}'`
	nDa=0
	for nn in $str; do
	    nDa=$(($nDa+$nn))
	done
	nEntry=$(($nEntry+$nEn))          #total Entries
	nDatasets=$(($nDatasets+$nDs))    #converted Datasets
	nXDatasets=$(($nXDatasets+$nXD))  #all Datasets in input EXFOR file
	nPoints=$(($nPoints+$nDa))        #converted data points
	printf "%5d) %-18s %s Datasets:%d Pt:%d \r" $ii ${name} `date +%F,%T` $nDatasets $nPoints
#tst	if [ $ii -ge 10 ]; then break; fi  #tst
    fi
done
printf "%2s%-14s%-16d%-16d%-16d%-16d%-16d\n" '#/' $FMT $nEntry $nDatasets $nXDatasets 0 $nPoints >>all.c5
echo ""
#exit

echo ""
echo "Now your directory:"
echo "`pwd`"
du -hc --time --max-depth=1

echo ""
echo "File all.c5:"
ls -lah all.c5
ls -la  all.c5

echo ""
echo "File all.c5 info:"
head --lines=17 all.c5 
tail --lines=1  all.c5

echo ""
echo "Statistics"

nLines=`cat all.c5|wc -l`
echo "	#Lines:              $nLines"

nEntry=`cat all.c5|grep "^#ENTRY"|sort -u|wc -l`
echo "	#Entries:            $nEntry"

nDatasets=`cat all.c5|grep "^#DATASET"|wc -l`
echo "	#Datasets:           $nDatasets"

nCorr=`cat all.c5|grep "^#C5CORR"|wc -l`
echo "	#Corrected Datasets: $nCorr"

nCovar=`cat all.c5|grep "^#COVARIANCE"|wc -l`
echo "	#Covariance Data:    $nCovar"

str=`cat all.c5|grep "#C5DATA"|awk '{printf $2"+"}'`
nDataPoints=`echo "${str}0"|bc`
echo "	#Data points:        $nDataPoints"

echo "	#Datasets by MF:"
cat all.c5|grep "^#MF"|awk '{print $1":"$2}'|sort|uniq -c |sort -g

#All corrections
echo "#Flag           DatasetID   Fc:Ave      MONIT:Ave   DECAY-DATA  DECAY-MON" >c5corr.lst
cat all.c5|grep "^#/C5CORR" >>c5corr.lst

echo ""
echo "Script:$0 `date +%F,%T` finished."
t11=`date +%s`; dt0=$(($t11-t00))
echo "Elapsed time: ${dt0}sec"
