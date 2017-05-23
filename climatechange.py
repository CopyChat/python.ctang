#!/usr/bin/env python

########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import numpy as np
import pylab as pl
import Scientific.IO.NetCDF as IO
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.lines as lines
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
import textwrap

pl.close('all')

########################## for CMIP5 charactors
DIR='/Users/tang/climate/CMIP5/'
VARIABLE='tas'
PRODUCT='Amon'
ENSEMBLE='r1i1p1'

AbsTemp=273.15
RefTemp=5
CRUmean=8.148 #1900-2100 land

TargetModel=[\
        #'CanESM2',\
        #'BCC-CSM1.1',\
        #'CCSM4',\
        #'CNRM-CM5',\
        #'CSIRO-Mk3.6.0',\
        #'EC-EARTH',\
        #'GFDL-ESM2G',\
        'GFDL-ESM2M',\
        #'GISS-E2-H',\
        #'GISS-E2-R',\
        #'HadGEM2-CC',\
        'HadGEM2-ES',\
        #'INM-CM4',\
        'IPSL-CM5A-LR',\
        #'IPSL-CM5A-MR',\
        #'MIROC-ESM-CHEM',\
        #'MIROC-ESM',\
        #'MIROC5',\
        #'MPI-ESM-LR',\
        #'MRI-CGCM3',\
        #'NorESM1-M',\
        #'MPI-ESM-LR',\
        ]

COLORtar=['darkred','black','deeppink','orange',\
        'orangered','yellow','gold','brown','chocolate',\
        'green','yellowgreen','aqua','olive','teal',\
        'blue','purple','darkmagenta','fuchsia','indigo',\
        'dimgray','black','navy']

COLORall=['darkred','darkblue','darkgreen','deeppink',\
        'red','blue','green','pink','gold',\
        'lime','lightcyan','orchid','yellow','lightsalmon',\
        'brown','khaki','aquamarine','yellowgreen','blueviolet',\
        'snow','skyblue','slateblue','orangered','dimgray',\
        'chocolate','teal','mediumvioletred','gray','cadetblue',\
        'mediumorchid','bisque','tomato','hotpink','firebrick',\
        'Chartreuse','purple','goldenrod',\
        'black','orangered','cyan','magenta']
linestyles=['_', '_', '_', '-', '-',\
    '-', '--','--','--', '--',\
    '_', '_','_','_',\
    '_', '_','_','_',\
    '_', '-', '--', ':','_', '-', '--', ':','_', '-', '--', ':','_', '-', '--', ':']
#================================================ CMIP5 models
# for historical
modelist1=['ACCESS1-0','ACCESS1-3',\
        'bcc-csm1-1','bcc-csm1-1-m',\
        'BNU-ESM',\
        'CCSM4','CESM1-BGC','CESM1-CAM5',\
        'CESM1-FASTCHEM','CESM1-WACCM',\
        'CMCC-CESM',\
        'CMCC-CM',\
        #'CMCC-CMS',\  # no data now
        'CNRM-CM5',\
        'CSIRO-Mk3-6-0',\
        #'CSIRO-Mk3L-1-2',\
        'CanESM2',\
        'EC-EARTH',\
        'FGOALS-g2',\
        'FIO-ESM',\
        'GFDL-CM3',\
        'GFDL-ESM2G',\
        'HadGEM2-AO',\
        'GFDL-ESM2M',\
        'GISS-E2-H',\
        'GISS-E2-H-CC',\
        'GISS-E2-R',\
        #'GISS-E2-R-CC',\
        'HadGEM2-CC',\
        'HadGEM2-ES',\
        'IPSL-CM5A-LR','IPSL-CM5A-MR','IPSL-CM5B-LR',\
        'MIROC-ESM','MIROC-ESM-CHEM',\
        #'MIROC4h',\# no data now
        'MIROC5',\
        'MPI-ESM-LR','MPI-ESM-MR','MPI-ESM-P',\
        'MRI-CGCM3','MRI-ESM1',\
        'INMCM4',\
        'NorESM1-M','NorESM1-ME']

# for rcp8.5 
modelist2=['bcc-csm1-1','bcc-csm1-1-m',\
        #'BNU-ESM',\#no data
        #'ACCESS1-0','ACCESS1-3',\#no data
        #'CESM1-CAM5-1-FV2',\# no data
        'CCSM4','CESM1-BGC','CESM1-CAM5',\
        'CMCC-CESM',\
        'CMCC-CM',\
        #'CMCC-CMS',\
        'CSIRO-Mk3-6-0',\
        'CNRM-CM5','CanESM2','FGOALS-g2',\
        'EC-EARTH',\
        #'FIO-ESM',\#no data now
        'GFDL-CM3','GFDL-ESM2G','GFDL-ESM2M',\
        'GISS-E2-H','GISS-E2-H-CC','GISS-E2-R',\
        #'GISS-E2-R-CC',\# no hist data
        'HadGEM2-AO','HadGEM2-CC','HadGEM2-ES',\
        'INMCM4',\
        'IPSL-CM5A-LR','IPSL-CM5A-MR','IPSL-CM5B-LR',\
        'MRI-CGCM3',\
        'MIROC5',\
        'MIROC-ESM-CHEM', 'MIROC-ESM',
        'MPI-ESM-LR','MPI-ESM-MR','NorESM1-M','NorESM1-ME']
print "==============================================="


#=================================================== define the Plot:

fig1=plt.figure(figsize=(16,9))
ax = fig1.add_subplot(111)
plt.xlabel('Year',fontsize=16)  
plt.ylabel('Global Surface Temperature Change ($^\circ$C)',fontsize=16)
plt.title("Global Surface Tempereture Changes simulated by CMIP5 models",fontsize=18)
plt.ylim(-2,6)
plt.xlim(1950,2100)
plt.grid()

plt.xticks(np.arange(1960, 2100+10, 20))
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)

# vertical at 2005
plt.axvline(x=2005.5,linewidth=2, color='gray')
plt.axhline(y=0,linewidth=2, color='gray')

#plt.plot(x,y,color="blue",linewidth=4)
########################## for historical
########################## for historical

print "========== for hist ==============="

EXPERIMENT='hist'
TIME='194001-200512'
YEAR=range(1940,2006)
Nmonth=792
SumTemp=np.zeros(Nmonth/12)
K=0

for Model in modelist1:
#define the K-th model input file:
    K=K+1 # for average 
    if Model =='CNRM-CM5':
        infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'orical_'+'r3i1p1'+'_'+TIME+'.nc'
    else: 
        if Model =='CSIRO-Mk3L-1-2':
            infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                    +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'orical_'+'r1i2p1'+'_'+TIME+'.nc'
        else:
            if Model =='HadGEM2-ES':
                infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                        +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'orical_'+'r5i1p1'+'_'+TIME+'.nc'
            else:
                infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                        +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'orical_'+ENSEMBLE+'_'+TIME+'.nc'
                #an example: tas_Amon_CanESM2_rcp85_r1i1p1_200601-210012.nc & \
                    #this file was copied locally for tests in this book
    print('the file is == ' +infile1)

    #open input files
    infile=IO.NetCDFFile(infile1,'r')

    # read the variable tas
    TAS=infile.variables[VARIABLE][:,:,:].copy()
    print 'the variable tas ===============: ' 
    print TAS

    # calculate the annual mean temp:
    TEMP=range(0,Nmonth,12) 
    for j in range(0,Nmonth,12):
        TEMP[j/12]=np.mean(TAS[j:j+11][:][:])-AbsTemp

    print " temp ======================== absolut"
    print TEMP

    # reference temp: mean of 1996-2005
    RefTemp=np.mean(TEMP[len(TEMP)-10+1:len(TEMP)])

    if K==1:
        ArrRefTemp=[RefTemp]
    else:
        ArrRefTemp=ArrRefTemp+[RefTemp]
        print 'ArrRefTemp ========== ',ArrRefTemp

    TEMP=[t-RefTemp for t in TEMP]
    print " temp ======================== relative to mean of 1986-2005"
    print TEMP

    # get array of temp K*TimeStep
    if K==1:
        ArrTemp=[TEMP]
    else:
        ArrTemp=ArrTemp+[TEMP]


    SumTemp=SumTemp+TEMP
    #print SumTemp

#=================================================== to plot
    print "======== to plot =========="
    print len(TEMP)

    print 'NO. of year:',len(YEAR)

    #plot only target models
    if  Model in TargetModel:
        plt.plot(YEAR,TEMP,\
                #linestyles[TargetModel.index(Model)],\
                color=COLORtar[TargetModel.index(Model)],linewidth=2)




    #if Model=='CanESM2':
        #plt.plot(YEAR,TEMP,color="red",linewidth=1)
    #if Model=='MPI-ESM-LR':
        #plt.plot(YEAR,TEMP,color="blue",linewidth=1)
    #if Model=='MPI-ESM-MR':
        #plt.plot(YEAR,TEMP,color="green",linewidth=1)

#=================================================== for ensemble mean
AveTemp=[e/K for e in SumTemp]
ArrTemp=list(np.array(ArrTemp))
print 'shape of ArrTemp:',np.shape(ArrTemp)
StdTemp=np.std(np.array(ArrTemp),axis=0)
print 'shape of StdTemp:',np.shape(StdTemp)

print "ArrTemp ========================:"
print ArrTemp

print "StdTemp ========================:"
print StdTemp

# 5-95% range ( +-1.64 STD)
StdTemp1=[AveTemp[i]+StdTemp[i]*1.64 for i in range(0,len(StdTemp))]
StdTemp2=[AveTemp[i]-StdTemp[i]*1.64 for i in range(0,len(StdTemp))]

print "Model number for historical is :",K

print "models for historical:";print  modelist2


plt.plot(YEAR,AveTemp,label='HIST mean',color="black",linewidth=4)
plt.plot(YEAR,StdTemp1,color="black",linewidth=0.1)
plt.plot(YEAR,StdTemp2,color="black",linewidth=0.1)
plt.fill_between(YEAR,StdTemp1,StdTemp2,color='black',alpha=0.3)

#plt.show()


# draw NO. of model used:
plt.text(1990,3.2,str(K)+' models',size=16,rotation=0.,
        ha="center",va="center",
        #bbox = dict(boxstyle="round",
            #ec=(1., 0.5, 0.5),
            #fc=(1., 0.8, 0.8),
            )


########################## for rcp8.5:
########################## for rcp8.5:
EXPERIMENT='rcp85'
TIME='200601-210012'
YEAR=range(2006,2101)
Nmonth=1140
SumTemp=np.zeros(Nmonth/12)
K=0


for Model in modelist2:
#define the K-th model input file:
    K=K+1 # for average 
    infile1=DIR+EXPERIMENT+'/'+Model+'/'\
            +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'_'+ENSEMBLE+'_'+TIME+'.nc'
            #an example: tas_Amon_CanESM2_rcp85_r1i1p1_200601-210012.nc & \
                    #this file was copied locally for tests in this book
    print('the file is == ' +infile1)

    #open input files
    infile=IO.NetCDFFile(infile1,'r')

    # read the variable tas
    TAS=infile.variables[VARIABLE][:,:,:].copy()
    print 'the variable tas ===============: ' 
    print TAS

    # calculate the annual mean temp:
    TEMP=range(0,Nmonth,12) 
    for j in range(0,Nmonth,12):
        TEMP[j/12]=np.mean(TAS[j:j+11][:][:])-AbsTemp

    print " temp ======================== absolut"
    print TEMP

    # get the reftemp if the model has historical data here
    print 'ArrRefTemp in HIST ensembles:',np.shape(ArrRefTemp)
    print ArrRefTemp
    if Model in modelist1:
        print 'model index in HIST: ',modelist1.index(Model)
        RefTemp=ArrRefTemp[modelist1.index(Model)]
        print 'RefTemp from HIST: ',RefTemp
    else:
        RefTemp=np.mean(TEMP[0:9])
        print 'RefTemp from RCP8.5: ',RefTemp

        
    #RefTemp=np.mean(TEMP[0:4])

    # temperature change
    TEMP=[t-RefTemp for t in TEMP]
    print " temp ======================== relative to mean of 1986-2005"
    print TEMP

    # get array of temp K*TimeStep
    if K==1:
        ArrTemp=[TEMP]
    else:
        ArrTemp=ArrTemp+[TEMP]


    SumTemp=SumTemp+TEMP
    print 'shape of SumTemp:', np.shape(SumTemp)
    #print SumTemp

#=================================================== to plot
    print "======== to plot =========="

    print 'NO. of year of RCP85 model:',len(YEAR)


    #plot only target models
    if Model in TargetModel:
        plt.plot(YEAR,TEMP,\
                #linestyles[TargetModel.index(Model)],\
                label=Model,\
                color=COLORtar[TargetModel.index(Model)],linewidth=2)

    #RefTemp=ArrRefTemp[modelist1.index(Model)]

    #if Model=='CanESM2':
        #plt.plot(YEAR,TEMP,label=Model,color="red",linewidth=1)
    #if Model=='MPI-ESM-LR':
        #plt.plot(YEAR,TEMP,label=Model,color="blue",linewidth=1)
    #if Model=='MPI-ESM-MR':
        #plt.plot(YEAR,TEMP,label=Model,color="green",linewidth=1)


#=================================================== for ensemble mean
AveTemp=[e/K for e in SumTemp]
ArrTemp=list(np.array(ArrTemp))
print 'shape of ArrTemp:',np.shape(ArrTemp)
StdTemp=np.std(np.array(ArrTemp),axis=0)
print 'shape of StdTemp:',np.shape(StdTemp)

print "ArrTemp ========================:"
print ArrTemp

print "StdTemp ========================:"
print StdTemp

# 5-95% range ( +-1.64 STD)
StdTemp1=[AveTemp[i]+StdTemp[i]*1.64 for i in range(0,len(StdTemp))]
StdTemp2=[AveTemp[i]-StdTemp[i]*1.64 for i in range(0,len(StdTemp))]

print "Model number for historical is :",K

print "models for RCP8.5:";print  modelist2


plt.plot(YEAR,AveTemp,label='RCP8.5 mean',color="red",linewidth=4)
plt.plot(YEAR,StdTemp1,color="red",linewidth=0.1)
plt.plot(YEAR,StdTemp2,color="red",linewidth=0.1)
plt.fill_between(YEAR,StdTemp1,StdTemp2,color='r',alpha=0.3)


# draw NO. of model used:
plt.text(2020,3.2,str(K)+' models',size=16,rotation=0.,
        ha="center",va="center",
        #bbox = dict(boxstyle="round",
            #ec=(1., 0.5, 0.5),
            #fc=(1., 0.8, 0.8),
            )
print "==============================================="

plt.legend(loc=2)

plt.show()
quit()
