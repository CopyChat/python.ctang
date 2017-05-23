########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import datetime as DT
from datetime import datetime 
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
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

########################## read data
#open input files

#=================================================== read MEI
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


#=================================================== to plot

fig, ax = plt.subplots()

sstS=Series(AnomalySST,index=AbstimeSST[:])
#ts=ts.cumsum()
sstS.plot(style='k--')
print sstS
rolling_mean(sstS,3).plot(label="Anomaly SST SWIO",color='green', linewidth=3)

rsdsS=Series(AnomalyRSDS,index=Abstime[:])
print rsdsS
rsdsS.plot(style='k--')
rolling_mean(rsdsS,3).plot(label="Anomaly RSDS SWIO",color='red', linewidth=3)
#ax.plot(Abstime[:], AnomalyRSDS,label="Anomaly RSDS SWIO", color='red',linewidth=3)

#ax.plot(AbstimeSST[:], AnomalySST,label="Anomaly SST SWIO",color='green', linewidth=3)
ax.plot(timeMei, mei,color='blue',label="MEI index",linewidth=3)
#ax.fill_between(timeMei,0,mei,color='black',alpha=0.3)

date1 = datetime( 1989, 1, 1)
date2 = datetime( 2016, 1, 1)
delta = DT.timedelta(days=365.25)
dates = drange(date1, date2, delta)

#ax.set_xlim( Abstime[0], Abstime[-1] )
ax.set_xlim( dates[0], dates[-1] )
#ax.set_ylim(-6,6)

ax.xaxis.set_major_formatter( DateFormatter('%Y') )
#ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )

ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()
ax.grid()

plt.xlabel('Year',fontsize=16)  
plt.ylabel('MEI index/ K / W m-2',fontsize=16)
plt.title("MEI index",fontsize=18)


# draw corrcoef
ax.text(DT.datetime(1994,4,1),4,'Mei vs SST corrcoef: '+str(float('%.2f'%cor)),size=16,rotation=0.,
        ha="center",va="center",
        #color='orange',
        bbox = dict(boxstyle="round",
        ec=(1., 0.5, 0.5),
        fc=(1., 0.8, 0.8),
        ))



ax.legend(loc=3)
plt.show()

quit()

