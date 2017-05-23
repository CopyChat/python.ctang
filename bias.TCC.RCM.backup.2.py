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
DIR='/Users/tang/climate/CORDEX/'
VARIABLE='clt'
PRODUCT='Amon'
ENSEMBLE='r1i1p1'
EXPERIMENT='hist'
TIME='195001-200512'

OBS='CRU'

K=0

DriModels=['CCCma-CanESM2',\
        'CNRM-CERFACS-CNRM-CM5',\
        'CNRM-CERFACS-CNRM-CM5',\
        'CSIRO-QCCCE-CSIRO-Mk3-6-0',\
        'ICHEC-EC-EARTH',\
        'ICHEC-EC-EARTH',\
        'ICHEC-EC-EARTH',\
        'ICHEC-EC-EARTH',\
        'IPSL-IPSL-CM5A-MR',\
        'MIROC-MIROC5',\
        'MOHC-HadGEM2-ES',\
        'MOHC-HadGEM2-ES',\
        'MPI-M-MPI-ESM-LR',\
        'MPI-M-MPI-ESM-LR',\
        'NCC-NorESM1-M',\
        'NOAA-GFDL-GFDL-ESM2M']

nameGCMs=['CanESM2',\
        'CNRM-CM5',\
        'CNRM-CM5',\
        'CSIRO-Mk3-6-0',\
        'EC-EARTH',\
        'EC-EARTH',\
        'EC-EARTH',\
        'EC-EARTH',\
        'IPSL-CM5A-MR',\
        'MIROC5',\
        'HadGEM2-ES',\
        'HadGEM2-ES',\
        'MPI-ESM-LR',\
        'MPI-ESM-LR',\
        'NorESM1-M',\
        'GFDL-ESM2M']
RCMs=['SMHI-RCA4_v1',\
        'CLMcom-CCLM4-8-17_v1',\
        'SMHI-RCA4_v1',\
        'SMHI-RCA4_v1',\
        'CLMcom-CCLM4-8-17_v1',\
        'KNMI-RACMO22T_v1',\
        'DMI-HIRHAM5_v2',\
        'SMHI-RCA4_v1',\
        'SMHI-RCA4_v1',\
        'SMHI-RCA4_v1',\
        'CLMcom-CCLM4-8-17_v1',\
        'SMHI-RCA4_v1',\
        'CLMcom-CCLM4-8-17_v1',\
        'SMHI-RCA4_v1',\
        'SMHI-RCA4_v1',\
        'SMHI-RCA4_v1']

nameRCMs=['RCA4_v1',\
        'CCLM4-8-17_v1',\
        'RCA4_v1',\
        'RCA4_v1',\
        'CCLM4-8-17_v1',\
        'RACMO22T_v1',\
        'HIRHAM5_v2',\
        'RCA4_v1',\
        'RCA4_v1',\
        'RCA4_v1',\
        'CCLM4-8-17_v1',\
        'RCA4_v1',\
        'CCLM4-8-17_v1',\
        'RCA4_v1',\
        'RCA4_v1',\
        'RCA4_v1']

ENSEMBLE=['r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r12i1p1',\
        'r1i1p1',\
        'r3i1p1',\
        'r12i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1',\
        'r1i1p1']

COLOR=['darkred','darkblue','darkgreen','deeppink',\
        'black','orangered','cyan','magenta']


# read CRU data:
if OBS == 'CRU':
    oVar='cld'
    obs1='~/climate/GLOBALDATA/OBSDATA/CRU/3.22/cru_ts3.22.2001.2005.cld.summer.mean.AFR.nc'
else:
# read ISCCP data:
    oVar='cltisccp'
    obs1='/Users/tang/climate/GLOBALDATA/OBSDATA/ISCCP/cltisccp_obs4MIPs_ISCCP_L3_V1.0_200101-200512.summer.mean.AFR.nc'
print obs1
obsfile1=IO.NetCDFFile(obs1,'r')
ObsVar=obsfile1.variables[oVar][0][:][:].copy()




for idx,Model in enumerate(DriModels):
    if OBS == 'CRU':
        infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                'clt_AFR-44_'+Model+'_historical_'+ENSEMBLE[idx]+'_'+RCMs[idx]+\
                '_mon_200101-200512.nc.summer.mean.nc.remap.cru.nc'
            #clt_AFR-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_199101-200012.nc.summer.mean.nc
    else:
        infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                'clt_AFR-44_'+Model+'_historical_'+ENSEMBLE[idx]+'_'+RCMs[idx]+\
                '_mon_200101-200512.nc.summer.mean.nc.remap.nc'
    print infile1

    #open input files
    infile1=IO.NetCDFFile(infile1,'r')

    # read the variables:
    lat = infile1.variables['lat'][:].copy()
    lon = infile1.variables['lon'][:].copy()

    VAR=infile1.variables[VARIABLE][0,:,:].copy()
    print 'the variable tas ===============: ' 
    print VAR

    print np.shape(VAR)
    print np.shape(ObsVar)

    Bias=VAR-ObsVar

    print np.shape(Bias)

    #quit()

    CoLev=10  #number of levels of colorbar
#=================================================== to plot
    fig=plt.subplot(4,4,idx+1,aspect='equal')
    print "============="
    print idx; print Model
    map=Basemap(projection='cyl',llcrnrlat=np.min(lat),urcrnrlat=np.max(lat),\
            llcrnrlon=np.min(lon),urcrnrlon=np.max(lon),resolution='l')
    map.drawcoastlines(linewidth=0.35)
    map.drawparallels(np.arange(-90.,91.,15.),labels=[1,0,0,0],linewidth=0.35)
    map.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],linewidth=0.35)
    map.drawmapboundary()
    x,y=map(lon,lat)
    cmap=plt.get_cmap('bwr')
    #cmap=plt.get_cmap('RdBu_r')
    pic=map.pcolormesh(x,y,Bias,cmap=cmap)
    plt.title(nameGCMs[idx]+' => '+nameRCMs[idx])
    #plt.figtext(0.68,0.73,timestamp, size="small") 

    #set the same colorbar range
    pic.set_clim(vmin=-50,vmax=50)
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.01, 0.8])
    plt.colorbar(cax=cax)

    #if idx > 11:
        #plt.colorbar(orientation='horizontal') # draw colorbar


#plt.legend(loc=2)
plt.show()
quit()







#================================================ CMIP5 models
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
TIME='185001-200512'
YEAR=range(1850,2006)
Nmonth=1872
SumTemp=np.zeros(Nmonth/12)
K=0

for Model in modelist1:
#define the K-th model input file:
    K=K+1 # for average 
    if Model =='CNRM-CM5':
        infile1=DIR+EXPERIMENT+'/'+Model+'/'\
                +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'orical_'+'r3i1p1'+'_'+TIME+'.nc'
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

    print 'NO. of year:',len(YEAR)

    #plot only target models
    if  Model in TargetModel:
        plt.plot(YEAR,TEMP,\
                color=COLOR[TargetModel.index(Model)],linewidth=2)
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


plt.plot(YEAR,AveTemp,label='HIST ensemble mean',color="black",linewidth=4)
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
        plt.plot(YEAR,TEMP,label=Model,\
                color=COLOR[TargetModel.index(Model)],linewidth=2)

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


plt.plot(YEAR,AveTemp,label='RCP8.5 ensemble mean',color="red",linewidth=4)
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
