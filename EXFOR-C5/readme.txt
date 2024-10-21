                            Nuclear Data Section (NDS)
                 Department of Nuclear Sciences and Applications
                    International Atomic Energy Agency (IAEA)
                       Wagramer Strasse 5, P.O.Box 100
                            A-1400 Vienna, Austria
                  Tel:(+43 1) 2600-21714; Fax:(+43 1) 26007

                            Full EXFOR in C5 format
           Created 3-August-2023 by Viktor Zerkin, V.Zerkin@iaea.org
               Last updated: 17-October-2024, V.Zerkin@gmail.com
_______________________________________________________________________________

Contents:
1. EXFOR-C5v[N]-YYYYMMDD.zip (size:~250Mb) contains:
   1) C5 files (total size:~2.6Gb):
      in a directory structure - one ENTRY in one file;
      full EXFOR translated into C5* format, data version [N]:0|1|2|3|4|5|6
   2) EXFOR-C5v[N]-YYYYMMDD.tto: terminal output of x4toc5
   3) EXFOR-C5v[N]-YYYYMMDD.readme: rules of citation of this distribution
   4) Datasets.json, Datasets.csv:
      datasets index - summary table of the contents of C5 files
   5) create1c5file.sh: bash script to produce single C5 file
   6) index1data.py: Python-3 code to reproduce datasets 
      index files (JSON and CSV)
   7) c5data1.py: Python-3 code to retrieve and plot c5data
   8) c5data2.py: Python-3 code: retrieve and compare renormalized data
2. Official files: LICENSE.TXT, COPYRIGHT.TXT 
3. readme.txt: this file
4. history.txt: distribution of full EXFOR in C4/C5, IAEA-NDS, 2007-2023
5. x4toc4usr.txt: Users' guide for program X4TOC4 (includes description of C4)
6. EXFOR14A.DAT: X4TOC4 EXFOR Reaction - MF/MT Equivalence Table
_______________________________________________________________________________

Data Versions:
   EXFOR-C5v0 - converted incident energy from C.M. to Lab.
	      - converted Rutherford-Ratio to B/SR (MF4)
   EXFOR-C5v1 - options from EXFOR-C5v2 +
	      - datasets with unknown MT are included (MF>0, MT=0)
   EXFOR-C5v2 - options from EXFOR-C5v0 +
	      - angle and data: C.M. to Lab. (for MF4)
	      - replaced Q-Value by E-Level
	      - reset MT:51,601,651,701,751,801 by MT+iLevel (for partial reactions)
	      - sort data: CS(EN), DA(EN:AN), DE(EN,E2), DAE(EN:AN:E2)
   EXFOR-C5v3 - options from EXFOR-C5v2 +
	      - auto-renormalized using modern monitor CS data
   EXFOR-C5v4 - options from EXFOR-C5v3 +
	      - auto-renormalized using modern Decay-data
   EXFOR-C5v5 - options from EXFOR-C5v4 +
	      - generated correlation matrix (DOI:10.1051/epjconf/20122700009)
   EXFOR-C5v6 - options from EXFOR-C5v4 +
	      - convert CS-ratio:MF203 to CS:MT3 (if "recommended" data of 
                reaction-denominator exist)
_______________________________________________________________________________

Examples.

Required: Python3: $ python --version
	  Plotly:  $ pip install plotly
Programs:
 1) index1data.py*    find all c5 files recursively, read, produce Datasets-index in JSON, CSV
 2) c5data1.py        find datasets in CSV by reaction, extract data, plot by Plotly -> html
 3) c5data2.py        find renormalized data, recalculate original values, plot by Plotly
*Note. This version of index1data.py exclude "derived" data from the Dataset index, 
       i.e. EXFOR data having SF9 are not considered:
       CALC   Calculated data
       DERIV  Derived data
       EVAL   Evaluated data
       RECOM  Recommended data
Run:
 $ python -B index1data.py
 $ python -B c5data1.py
 $ python -B c5data2.py
_______________________________________________________________________________

Questions and Answers.

1.Q: What is C4 format?
  A: C4 is a computation format presenting experimental data from EXFOR
     database. Data in C4 format are much easier to process by application
     programs than EXFOR format*. C4 was designed for comparison of experi-
     mental data with evaluations and therefore uses ENDF coding (MF-MT-ZA).
     Program converting data from EXFOR to C4 (X4TOC4) was written by
     D.E.Cullen (when working in the IAEA) and developed by A.Trkov.
  "Users' guide for program X4TOC4" says:
     "The computation format uses a classification system and units
     which are compatible with ENDF. Data is classified by (1) ZA
     of projectile, (2) ZA of target, (3) metastable state of target,
     (4) MF - type of data, (5) MT - reaction, (6) metastable state
     of residual nucleus. To identify the source of the data the first
     author and year and the EXFOR accession and sub-accession number
     are included in the format. In addition, fields are assigned to
     define the status of the EXFOR data (e.g., S = superceded),
     whether data is in the laboratory or center-of-mass frame of
     reference and the physical significance of the last 2 output
     fields (LVL = level energy, HL = half-life). Finally the format
     includes 8 fields in which the output data are contained (e.g.,
     incident energy, data, cosine, uncertainties, etc.)"
     See full description in the file "x4toc4usr.txt".
   * EXFOR originaly stands for "EXchange FORmat" - format for exchange
     experimental data between national/international nuclear data centres.

2.Q: What is C5 format? 
  A: It is C4 format extended with:
     a)	Identification information is given as comment starting with #.
     b)	Information is presented as sequence of Datasets; Dataset presents
	data of single Reaction corresponding to EXFOR <SUBENT-Pointer>.
	Content of C5 file:
	#C5.2.3  <Date:C5-Created> <Time:C5-Created> <Date:EXFOR-Master>
 __	#DATASET <SUBENT+Pointer> #1
|	#ENTRY
|		...ENTRY Information: reference, title, full list of authors,...
|		...DATASET Information: EXFOR-Reaction, MF, MT,...
|	#C5CORR         #Corrections description
|	#/C5CORR
|	#C5DATA         <nDataPoints>
|		...DATA as in C4 format with additional columns
|	#/C5DATA
|__	#/DATASET
	#DATASET #2
	#DATASET #3
	...
	#DATASET #n
	#/C5.2.3

3.Q: What are the options to translate EXFOR to C5 data by "x4toc5"?
  A: Program x4toc5 can generate C5 file recalculating data:
     - by default, all data translated to "basic units", e.g. "MeV" to "eV"
     - convert Rutherford ratios to B/SR
     - convert C.M. data to Lab (for angular distributions)
     - recalculate data to inverse reactions
     - renormalize data using monitors (old and new cross section data)
     - renormalize data using intensities of gamma-lines in DECAY-DATA and DECAY-MON
     - set MT+iLevel for excited states: MT50+, MT600+, MT650+, searching iLevel in RIPL
     - replace Q-Value by E-Level (for partial reactions)
     - sort data: CS(EN), DA(EN:AN), DE(EN,E2), DAE(EN:AN:E2)
     - include old and new monitor data without data renormalization

4.Q: What is the differences between versions of C5 files?
  A: Versions of C5 data:
	   EXFOR-C5v0 - default optons of C4
	   EXFOR-C5v2 - converted C.M. to Lab. (for MT4)
		      - replaced Q-Value by E-Level
		      - reset MT51, MT601, by MT+iLevel (for partial reactions)
		      - sort data: CS(EN), DA(EN:AN), DE(EN,E2), DAE(EN:AN:E2)
	   EXFOR-C5v3 - options from EXFOR-C5v2 +
		      - auto-renormalized using modern monitor CS data
	   EXFOR-C5v4 - options from EXFOR-C5v3 +
		      - auto-renormalized using modern Decay-data
	   EXFOR-C5v5 - options from EXFOR-C5v4 +
		      - auto-generated correlation matrix

5.Q: What is the contents of C5 columns additional to C4?
  A: Columns 132:167:
	(4F9.0) dSys, dStat, dOther, dTot - generalized absolute: fully correlated, 
		uncorrelated, partially correlated and total uncertainties
  A: Columns 168:212
	(5F9.0) dSys%, dStat%, dOther%, dTot%, dData%
		generalized relative uncertainties (dData/Data) in per-cents
  A: Columns 213:235
	(5F9.0) M0,dM0,M1,dM1,Fc
		M0:old montor (cross sections in barn);  dM0:uncertanty of M0 (barn)
		M1:new montor (cross sections in barn);  dM1:uncertanty of M1 (barn)
		Fc: final factor (including renormalization by monitor and decay-data)

6.Q: What is the meaning of the fields in the lines #C5.2.2 and #/C5.2.2?
  A: These lines mark begin/end of an C5 file:
	a) #C5.2.2 N1 N2 N3
	   N1 - date of request (date when this C4-file was created)
	   N2 - time, when request started
	   N3 - date of last update of EXFOR database,
		from which data were retrieved (source database)
	b) #/C5.2.2 N1 N2 N3 N4 N5
	   N1 - number of Entries in this file (start with #ENTRY)
	   N2 - number of Datasets in this file (start with #DATASET)
	   N3 - total number of datasets in the source EXFOR database
	   N5 - total number of data points

7.Q: Is there any alternative way to get EXFOR data in computational form?
  A: There are several ways/methods to get EXFOR data in computational form:
	a) Web EXFOR retrieval system:
	   http://nds.iaea.org/exfor/
	b) X4Pro - universal, fully relational EXFOR database (SQLite)
	   http://nds.iaea.org/cdroms/#x4pro1
	c) EXFOR-X5json - comprehensive presentation of full EXFOR library 
	   with supplementary data in X5-json format
	   http://nds.iaea.org/cdroms/#x5json
	   https://github.com/vzerkin/EXFOR-X5json
	d) EXFOR-C5 - full EXFOR library translated to computational format C5
	   https://nds.iaea.org/cdroms/#c5
	   https://github.com/vzerkin/EXFOR-C5

-End-
