#!/usr/bin/env python

########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import datetime 
import pandas as pd
import numpy as np
import pylab as pl
import Scientific.IO.NetCDF as IO
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.lines as lines
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.dates import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
import textwrap

pl.close('all')

#=========================================
SUBPLOT=4
########################## for RegCM output:
NumExp=20

# Define units of time
Abstime = pd.date_range('1997-01-01', '1998-12-31', freq='M')
stick= pd.date_range('1997-01-01', '1998-12-31', freq='3M')
Abstimestamp=[t.strftime("%d %B %Y") for t in stick]
Nmonth=len(Abstime)

RegCM_DIR='/Users/tang/climate/Modeling/Ensemble'
RegCM_tag=[ 'SRF','SRF','SRF','RAD']

VARIABLE=[ 'tas','pr','rsds','clt' ]
UNIT= [ 'degreeC','mm/day','W/m2','%' ]
CROSS_FACTOR=(1,86400,1,100)
PLUS_FACTOR=(-273.15,0,0,0)

OBS_DIR='/Users/tang/climate/GLOBALDATA/OBSDATA'

OBS_PROJ=[ \
        'ERA_Interim',\
        #'CRU',\
        'GPCP',\
        #'TRMM',\
        'CERES',\
        #'CM_SAF',\
        'MODIS',\
        ]
# NOTE: do NOT change the order: tas,pr,rsds,clt


COLORtar=['darkred','blue','deeppink','orange',\
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
print "==============================================="

#=================================================== define the Plot:
fig, ax = plt.subplots(2,2, figsize=(15, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.1, wspace=.2)
ax = ax.ravel()
fig.autofmt_xdate()
plt.setp(ax, xticks=stick[:], xticklabels=Abstimestamp[:])

for J in range(SUBPLOT):

    ax[J].xaxis.set_major_formatter( DateFormatter('%Y-%m') )
    ax[J].set_title(VARIABLE[J] +' ('+UNIT[J] +')')
    ax[J].tick_params(axis='both', which='major', labelsize=14)
    ax[J].grid()

    SumTemp=np.zeros(Nmonth)  # initialize
    for K in range(1,NumExp+1):

        print "========== for Ensemble: ==============="
#=================================================== read RegCM data
        infile1=RegCM_DIR+'/output_'+str(K)+'/pprcmdata/monthly/'+\
                str(K)+'_EIN15.'+RegCM_tag[J]+'.mon.mean.1997-1998.swio.fldmean.nc'
        # .../Ensemble/output_1/pprcmdata/monthly/1_EIN15.RAD.mon.mean.1997-1998.nc

        #open input files
        infile=IO.NetCDFFile(infile1,'r')

        # read the variable tas
        TAS=infile.variables[VARIABLE[J]][:,:,:].squeeze()

        # convert to units
        TEMP = [t*CROSS_FACTOR[J]+PLUS_FACTOR[J] for t in TAS[:]]

        # for std # get array of temp K*TimeStep
        if K==1:
            ArrTemp=[TEMP]
        else:
            ArrTemp=ArrTemp+[TEMP]

        SumTemp=SumTemp+TEMP
        print SumTemp

    # the END of reading Ensemble.

#=================================================== for ensemble mean
    print 'j='+str(J)
    print SumTemp
    print np.shape(SumTemp)

    AveTemp=[e/K for e in SumTemp]
    ArrTemp=list(np.array(ArrTemp))
    print 'shape of ArrTemp:',np.shape(ArrTemp)
    StdTemp=np.std(np.array(ArrTemp),axis=0)
    print 'shape of StdTemp:',np.shape(StdTemp)

    print "ArrTemp ========================:"
    print ArrTemp
    print "StdTemp ========================:"
    print StdTemp

    print len(StdTemp)
    print np.shape(StdTemp)
    print range(0,24)

    # 5-95% range ( +-1.64 STD)
    StdTemp1=[AveTemp[i]+StdTemp[i]*1. for i in range(0,len(StdTemp))]
    StdTemp2=[AveTemp[i]-StdTemp[i]*1. for i in range(0,len(StdTemp))]

    print "Model number for historical is :",K

    ax[J].plot(Abstime[:],AveTemp,label='ensemble mean',color="red",linewidth=2)
    ax[J].plot(Abstime[:],StdTemp1,color="black",linewidth=0.1)
    ax[J].plot(Abstime[:],StdTemp2,color="black",linewidth=0.1)
    ax[J].fill_between(Abstime[:],StdTemp1,StdTemp2,color='black',alpha=0.3)

#=================================================== 
# add forcing data: EIN15

    #forcefile=ERA.clt.mon.mean.1997-1998.swio.fldmean.nc
    #ERA.t2m.mon.mean.1997-1998.swio.fldmean.nc
#=================================================== 
plt.show()
quit()
