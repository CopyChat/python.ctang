########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import datetime as DT
from datetime import datetime 
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
from dateutil.relativedelta import relativedelta
from numpy import arange
import numpy as np
import pylab as pl
import parser
import pandas as pd
from pandas import *
from datetime import timedelta
import Scientific.IO.NetCDF as IO
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.lines as lines
import matplotlib.dates as dates
from matplotlib.dates import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
import textwrap
pl.close('all')

########################### units of time
#=================================================== 
dates = pd.date_range('1951-01-01', '2014-12-31', freq='M')

Abstimestamp=[t.strftime("%d %B %Y") for t in dates]
print Abstimestamp

#=================================================== default setting

threshold=0.4
########################## read data
#open input files

#Had_his="/Users/tang/climate/CMIP5/SST/\
#tos_Omon_HadGEM2-ES_historical_r1i1p1_195101-200512.monmean.nino3.4.nc"
#GFDL_hisf="/Users/tang/climate/CMIP5/SST/\
        #tos_Omon_GFDL-ESM2M_historical_r1i1p1_195101-200512.monmean.nino3.4.nc"

#Had_his="/Users/tang/climate/ENSO/OBS/\
#COBE.sst.monmean.195101-200512.nino3.4.nc"

Had_his="/Users/tang/climate/ENSO/OBS/\
ersst_V3b.195101-201412.nino3.4.nc"

sst_Had_his=IO.NetCDFFile(Had_his,'r').variables['sst'][:,:,:].copy()
print "missing value:" + str(IO.NetCDFFile(Had_his,'r').variables['sst']._FillValue)
y=np.ma.masked_where(sst_Had_his > 1000, sst_Had_his)
sst_mask = np.ma.masked_array(sst_Had_his, mask=y.mask)

sst_Had_his_arr=sst_mask.mean(axis=1).mean(axis=1).mean(axis=1)
print sst_Had_his_arr
print sst_Had_his_arr.shape

print IO.NetCDFFile(Had_his,'r').variables['time'].units

print sst_Had_his

#=================================================== ymonmean
sst_Had_his_Series=pd.DataFrame(sst_Had_his_arr,index=dates,columns=['sst']) 

print sst_Had_his_Series.columns.values.tolist()
#print sst_Had_his_Series.groupby('0')
print sst_Had_his_Series.sst

sst_Had_his_Series['mon'] = sst_Had_his_Series.index.month
sst_Had_his_monmean = sst_Had_his_Series['1951':'2014'].groupby('mon').aggregate(np.mean)
sst_Had_his_monmean.plot(kind='bar')

#plt.show()

sst_Had_his_monmean=pd.DataFrame(np.asarray(sst_Had_his_monmean),columns=['sst'])

print sst_Had_his_monmean
print sst_Had_his_Series
print sst_Had_his_monmean.shape
print sst_Had_his_monmean.columns.values.tolist()

print sst_Had_his_monmean.sst
print sst_Had_his_Series.shape
print range(0,len(sst_Had_his_monmean.sst))
print range(0,len(sst_Had_his_Series.sst))

print sst_Had_his_Series.sst[0]
print sst_Had_his_monmean.sst[0]

#=================================================== Anomaly
AnomalySST_Had_his=np.asarray([sst_Had_his_Series.sst[i]-sst_Had_his_monmean.sst[i%12] for i in range(0,len(sst_Had_his_Series.sst))],dtype=float).reshape(len(sst_Had_his_Series.sst))

print AnomalySST_Had_his

sst_Had_his_std= np.std(AnomalySST_Had_his[20:50])
print sst_Had_his_std

AnomalySST_Had_his=np.asarray([t/sst_Had_his_std for t in AnomalySST_Had_his])

print AnomalySST_Had_his.shape




#=================================================== for cmip5

sst_cmip5f_ceres="/Users/tang/climate/CMIP5/SST/\
ts_Amon_GFDL-ESM2M_historical_r1i1p1_195101-200512.monmean.nino3.4.nc"
#tos_Omon_HadGEM2-ES_historical_r1i1p1_195101-200512.monmean.nino3.4.nc"

dates_sst_cmip5 = pd.date_range('1951-01-01', '2005-12-31', freq='M')

sst_cmip5_his=IO.NetCDFFile(sst_cmip5f_ceres,'r').variables['ts'][:,:,:].copy()
print "missing value:" + str(IO.NetCDFFile(sst_cmip5f_ceres,'r').variables['ts']._FillValue)


y=np.ma.masked_where(sst_cmip5_his > 1000, sst_cmip5_his)
sst_cmip5_mask = np.ma.masked_array(sst_cmip5_his, mask=y.mask)

sst_cmip5_arr=sst_cmip5_mask.mean(axis=1).mean(axis=1)
print sst_cmip5_arr
print sst_cmip5_arr.shape

print IO.NetCDFFile(sst_cmip5f_ceres,'r').variables['time'].units



#================================ ymonmean
sst_cmip5_Series=pd.DataFrame(sst_cmip5_arr,index=dates_sst_cmip5,columns=['sst_cmip5']) 

print sst_cmip5_Series.columns.values.tolist()
#print sst_Had_his_Series.groupby('0')
print sst_cmip5_Series

sst_cmip5_Series['mon'] = sst_cmip5_Series.index.month
sst_cmip5_monmean = sst_cmip5_Series['1951':'2005'].groupby('mon').aggregate(np.mean)
sst_cmip5_monmean.plot(kind='bar')

#plt.show()

sst_cmip5_monmean=pd.DataFrame(np.asarray(sst_cmip5_monmean),columns=['sst_cmip5'])

print sst_cmip5_monmean 
print sst_cmip5_Series
print sst_cmip5_monmean.shape
print sst_cmip5_monmean.columns.values.tolist()

print sst_cmip5_monmean.sst_cmip5
print sst_cmip5_Series.shape
print range(0,len(sst_cmip5_Series.sst_cmip5))
print range(0,len(sst_cmip5_monmean.sst_cmip5))


print sst_cmip5_Series.sst_cmip5[0]
print sst_cmip5_monmean.sst_cmip5[0]

#=================================================== Anomaly
AnomalySST_cmip5_ceres=np.asarray([sst_cmip5_Series.sst_cmip5[i]-sst_cmip5_monmean.sst_cmip5[i%12] for i in range(0,len(sst_cmip5_Series.sst_cmip5))],dtype=float).reshape(len(sst_cmip5_Series.sst_cmip5))

print AnomalySST_cmip5_ceres

sst_cmip5_std= np.std(AnomalySST_cmip5_ceres[0:len(sst_cmip5_arr)])
print sst_cmip5_std

AnomalySST_cmip5_ceres=np.asarray([t/sst_cmip5_std for t in AnomalySST_cmip5_ceres])

print AnomalySST_cmip5_ceres.shape


sst_cmip5S=Series(AnomalySST_cmip5_ceres+5,index=dates_sst_cmip5[:])


print sst_cmip5S





#=================================================== to plot

fig, ax = plt.subplots()

sstS=Series(AnomalySST_Had_his,index=dates[:])
#ts=ts.cumsum()
#ax.plot(rsdsS,label='RSDS from CERES in SWIO',color='k',linestyle='--')
#sst_cmip5S.plot(label='standardized SST Anomaly from cmip5 in nino 3.4 region',color='k',linestyle='-')




sstS.plot(label='Anomaly SST from ERSST V3b',style='k--')

print sstS
rolling_mean(sstS,5).plot(label="standardized SST Anomaly from ERSST V3b five-month running mean",color='k', linewidth=2)
rolling_mean(sst_cmip5S,5).plot(label="standardized SST Anomaly in CMIP5 five-month running mean",\
    linestyle='-',color='k', linewidth=2)

ax.set_xlim( dates[0], dates[-1] )
ax.set_ylim(-10,10)

#ax.xaxis.set_major_formatter( DateFormatter('%Y') )
#ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )

#ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()

plt.xlabel('Year',fontsize=16)  
plt.ylabel(' Oceanic Nino Index in Nino 3.4 region / K / W m-2',fontsize=16)
plt.title(" Oceanic Nino Index in Nino 3.4 region",fontsize=18)
#plt.title(" Oceanic Nino Index in Nino 3.4 region vs rsds in SWIO",fontsize=18)


plt.axhline(y=threshold, xmin=dates[1], xmax=dates[-1],label='threshold in nino3.4 region ='+str(threshold), linewidth=1,linestyle='--', color = 'red')
plt.axhline(y=threshold*(-1), xmin=dates[1], xmax=dates[-1],label='threshold in nino3.4 region ='+ str(threshold*(-1)), linewidth=1,linestyle='--', color = 'blue')
plt.axhline(y=threshold*(12.5), xmin=dates[1], xmax=dates[-1],label='zero for rsds', linewidth=1,linestyle='-', color = 'r')


plt.fill_between(dates,rolling_mean(AnomalySST_Had_his,5),threshold,\
    where=rolling_mean(AnomalySST_Had_his,5)>=.5,color='r',alpha=0.7)
plt.fill_between(dates,rolling_mean(AnomalySST_Had_his,5),threshold*(-1),\
    where=rolling_mean(AnomalySST_Had_his,5)<=-.5,color='blue',alpha=0.7)

cor=np.corrcoef(sst_Had_his_arr[0:660],sst_cmip5_arr[0:660])[0, 1]

# draw corrcoef
ax.text(DT.datetime(2000,8,1),8,'cmip5 vs obs correlation:  '+str(float('%.2f'%cor)),size=16,rotation=0.,
        #ha="center",va="center",
        ##color='orange',
        #bbox = dict(boxstyle="round",
        #ec=(1., 0.5, 0.5),
        #fc=(1., 0.8, 0.8),
        #))
        )


ax.legend(loc=3)
ax.grid()
ax.grid()

plt.show()
quit()

#=================================================== 
#=================================================== 
#=================================================== 
#=================================================== 
#=================================================== 
#=================================================== 
#=================================================== 
time1,mei= np.loadtxt("mei.1989.01_2015.03", dtype=(np.str_,np.float),skiprows=0,\
        delimiter=' ', usecols=(0,1),unpack=True)

mei=np.array(mei,dtype=float)
#dt_obj = datetime.strptime(dt_str, '%m/%d/%Y %I:%M:%S %p')
timeMei = [datetime.strptime(t, '%Y-%m') for t in time1]


#=================================================== read OBS

rsdsinput="/Users/tang/climate/ENSO/rsds_CERES-EBAF_L3B_Ed2-8_200003-201405.monmean.fldmean.SWIO.nc"

rsdsf=IO.NetCDFFile(rsdsinput,'r')
rsds=rsdsf.variables['rsds'][:,:,0].copy()
print rsdsf.variables['time'].units

# units of time
date0=DT.date(2000,3,1) 
Abstime=[date0 + DT.timedelta(days=t) for t in rsdsf.variables['time'][:]]
print Abstime

Abstimestamp=[t.strftime("%d %B %Y") for t in Abstime]
print Abstimestamp

#================================== for Anomaly 
rsdsinput0="/Users/tang/climate/ENSO/rsds_CERES-EBAF_L3B_Ed2-8_200003-201405.ymonmean.fldmean.SWIO.nc"
rsdsf0=IO.NetCDFFile(rsdsinput0,'r')

Avgrsds=rsdsf0.variables['rsds'][:,:,0].copy()
AnomalyRSDS=np.asarray([rsds[i]-Avgrsds[i%12] for i in range(0,len(rsds))],dtype=float).reshape(len(rsds))

print AnomalyRSDS


#=================================================== read sst

sstinput="/Users/tang/climate/ENSO/sst.ERAIN.1979-2009.monmean.fldmean.SWIO.nc"

sstf=IO.NetCDFFile(sstinput,'r')
sst=sstf.variables['sst'][:,:,0].copy()
print sstf.variables['time'].units


# units of time
date0=DT.date(1900,1,1) 
AbstimeSST=[date0 + DT.timedelta(hours=t) for t in sstf.variables['time'][:]]
print AbstimeSST

AbstimestampSST=[t.strftime("%d %B %Y") for t in AbstimeSST]
print AbstimestampSST

#================================== for Anomaly 
sstinput0="/Users/tang/climate/ENSO/sst.ERAIN.1979-2009.ymonmean.fldmean.SWIO.nc"
sstf0=IO.NetCDFFile(sstinput0,'r')

Avgsst=sstf0.variables['sst'][:,:,0].copy()
AnomalySST=np.asarray([sst[i]-Avgsst[i%12] for i in range(0,len(sst))],dtype=float).reshape(len(sst))

print AnomalySST

#AnomalySST=np.asarray(AnomalySST)
#=================================================== correlation


#print np.correlate(mei[0:len(AnomalySST)], AnomalySST[:])

print AnomalySST.shape
print mei


#print np.correlate(mei[0:len(AnomalySST)], mei[0:len(AnomalySST)],'same')
print "corrcoef="
cor=np.corrcoef(mei,AnomalySST[0:len(mei)])[0, 1]
print np.corrcoef(mei,AnomalySST[0:len(mei)])



