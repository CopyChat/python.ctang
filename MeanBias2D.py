#!/usr/bin/env python
########################################
# to modify the NetCDF files
########################################
#First import the netcdf4 library
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import numpy as np
import sys,getopt
import math
import datetime as DT
import netcdftime 
from netcdftime import utime
from datetime import datetime 
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
from dateutil.relativedelta import relativedelta
from numpy import arange
import numpy as np
import pylab as pl
import parser
import pandas as pd
from pandas import *
import os
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


#=================================================== get opts input file
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o," "--ofile"):
            outputfile = arg
    print 'INputfile:', inputfile
    print 'Outputfile:', outputfile
if __name__ == "__main__":
    main(sys.argv[1:])
#=================================================== 
GCMvar='psl'
RELYvar='msl'
GCMinputf='psl_6hrPlev_HadGEM2-ES_historical_r1i1p1_198412010600-198512010000.nc'
#GCMinputf='psl_6hrPlev_HadGEM2-ES_historical_r1i1p1_198412010600-198512010000.standard.nc'
RELYinputf='msl_EIN75.198412010000-198512010000.nc.remap.nc.360.nc'
#RELYinputf='msl_EIN75.198412010000-198512010000.nc.remap.nc'
#=================================================== 

########################### units of time
#=================================================== 


#=================================================== to read
# Read en existing NetCDF file and create a new one
# f is going to be the existing NetCDF file from where we want to import data

GCMf=Dataset(GCMinputf,'r+') # r is for read only
RELYf=Dataset(RELYinputf,'r') # r is for read only

# Extract data from NetCDF file
print GCMf.variables.keys() 
print GCMf.dimensions.keys() 

GCMvar3D=GCMf.variables[GCMvar][:,:,:]
RELYvar3D=RELYf.variables[RELYvar][:,:,:]

LATITUDE=len(GCMvar3D[0,:,0])
LONGITUDE=len(GCMvar3D[0,0,:])
TIME=len(GCMvar3D[:,0,0])

TIME2=len(RELYvar3D[:,0,0])
#print Latitude,Longitude,Timesize

#=================================================== set up variables to use
GCMvar2D=GCMvar3D.reshape(TIME,-1)
RELYvar2D=RELYvar3D.reshape(TIME2,-1)

# create a 3D variable to hold the Mean bias as GCMvar3D in size.
#MeanBias=GCMvar3D
# NOTE: this method leading to error: when create the second GCMdf in the loop
#       (t=2) GCMvar3D changes their value of first month to that of MonthlyMeanBias
#       really bizarre. So, create it as 3D zeros array and then reshape it
MeanBias=np.zeros(TIME*LATITUDE*LONGITUDE).reshape(TIME,LATITUDE,LONGITUDE)
print MeanBias.shape


#--------------------------------------------------- 
# to test the reshap is working well or not
print '======== 3D :======='
print RELYvar3D
print '======== 2D :======='
print RELYvar2D
print '======== 2D reshape:======='
RELYvar2DT=RELYvar2D.reshape(TIME2,LATITUDE,LONGITUDE)
print RELYvar2DT
if (RELYvar3D.all()==RELYvar2DT.all()):
    print 'OKOKOKOK'
#quit()
#--------------------------------------------------- 

#quit()
#=================================================== to datetime
GCMtime=netcdftime.num2date(GCMf.variables['time'][:],GCMf.variables['time'].units,calendar='360_day')
#GCMtime=netcdftime.num2date(GCMf.variables['time'][:],GCMf.variables['time'].units)
#print GCMtime[9].year
print type(GCMtime)
#print  [str(i) for i in GCMtime[:]]
#GCMindex=[DT.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in [str(i) for i in GCMtime[:]]]
#print GCMindex
#print DT.datetime.strptime('2002-02-30 4:00:09','%Y-%m-%d %H:%M:%S') 
# NOTE: this day donot exits in Python

#=================================================== to datetime
# NOTE: when I use the kew word 'calendar='360_day', it gives 
#       wrong value for ONLY this netcdf file, GCMtime is quite OK.

#cdftime = utime(RELYf.variables['time'].units,calendar='360_day')
#cdftime = utime(RELYf.variables['time'].units)
#RELYtime=[cdftime.num2date(t) for t in RELYf.variables['time'][:]]

RELYtime=netcdftime.num2date(RELYf.variables['time'][:],RELYf.variables['time'].units,calendar='360_day')
#RELYtime=netcdftime.num2date(RELYf.variables['time'][:],RELYf.variables['time'].units)
#print type(RELYtime)
#RELYindex=[DT.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in [str(i) for i in RELYtime[:]]]
#print type(RELYindex)

#d={'gcm':pd.Series(GCMvar2D,index=GCMtime),'rely':pd.Series(RELYvar2D,index=RELYtime)}
#ddf=pd.DataFrame(d) 
# Series should be one dimension

#quit()

#for j in range(10,len(GCMvar3D[0,:,0])):
#=================================================== to DataFrame
#GCMdf=pd.DataFrame({'year':[t.year for t in GCMtime],
    #'month':[t.month for t in GCMtime],
    #'day':[t.day for t in GCMtime],
    #'hour':[t.hour for t in GCMtime],
    #'sdfj':GCMf.variables[GCMvar][:,j,:]})
# NOTE: this method is too time cosuming, about 7 hours to finish this code
#GCMdf=pd.DataFrame(GCMf.variables[GCMvar][:,0,0],GCMindex)
# NOTE: cannot convert 360_day np.arrary objects read from netcdf
#       to datetime objects
#quit()

#--------------------------------------------------- 
GCMdf=pd.DataFrame(GCMvar2D)
GCMdf['year']=[t.year for t in GCMtime]
GCMdf['month']=[t.month for t in GCMtime]
GCMdf['day']=[t.day for t in GCMtime]
GCMdf['hour']=[t.hour for t in GCMtime]

#print GCMdf.dtypes
#print GCMdf.loc[0:9,['year','month','day','hour']]
#print 'GCMdf'
#print GCMdf.iloc[0:60,:]
#quit()
#=================================================== to DataFrame
    #RELYdf=pd.DataFrame({'year':[t.year for t in RELYtime],
        #'month':[t.month for t in RELYtime],
        #'day':[t.day for t in RELYtime],
        #'hour':[t.hour for t in RELYtime],
        #RELYvar:RELYf.variables[RELYvar][:,j,:]})
    # NOTE: this method is too time cosuming, about 7 hours to finish this code
    #RELYdf=pd.DataFrame(RELYf.variables[RELYvar][:,0,0],RELYindex)
    # NOTE: cannot convert 360_day np.arrary objects read from netcdf
    #       to datetime objects
RELYdf=pd.DataFrame(RELYvar2D,dtype='float32')
RELYdf['year']=[t.year for t in RELYtime]
RELYdf['month']=[t.month for t in RELYtime]
RELYdf['day']=[t.day for t in RELYtime]
RELYdf['hour']=[t.hour for t in RELYtime]
#print 'RELYdf'
#print RELYdf.iloc[2,:]
#print GCMdf.loc[0:9,['year','month','day','hour']]
#quit()



#=================================================== calculate
#print GCMdf.stack(0)
#print RELYdf.asfreq('6H',method='pad',calendar='360_day')
# NOTE: asfreq and stack are not satisfactory to this task.
#       for the fromer is because of 360_day calendar.
print "---------"
##=================================================== for test calculation
#print RELYdf.loc[0]
## get monthly msl value
#print RELYdf.loc[0][:] 
## get value of psl in the same year & month
#print GCMdf[(GCMdf['year'] == RELYdf['year'][0]) & (GCMdf['month'] == RELYdf['month'][0])][:]
##quit()
## values = value
#print GCMdf.dtypes
#print RELYdf.dtypes
#print RELYdf.iloc[0,:]
#print RELYdf.iloc[0,0:LONGITUDE*LATITUDE].shape #196
##quit()
#print np.array(GCMdf[(GCMdf['year'] == RELYdf['year'][0]) 
#& (GCMdf['month'] == RELYdf['month'][0])])
#print np.array(GCMdf[(GCMdf['year'] == RELYdf['year'][0]) 
#& (GCMdf['month'] == RELYdf['month'][0])])[:,0:LONGITUDE*LATITUDE].shape # 119
##quit()
#--------------------------------------------------- 
    ##print [t for t in np.array(GCMdf[(GCMdf['year'] == RELYdf['year'][0]) 
        ##& (GCMdf['month'] == RELYdf['month'][0])][:])]
    #print np.array([np.subtract(t,RELYdf.iloc[0,0:LONGITUDE*LATITUDE]) 
        #for t in np.array(GCMdf[(GCMdf['year'] == RELYdf['year'][0]) 
            #& (GCMdf['month'] == RELYdf['month'][0])])[:,0:LONGITUDE*LATITUDE]])
    #print np.array([np.subtract(t,RELYdf.iloc[0,0:LONGITUDE*LATITUDE]) 
        #for t in np.array(GCMdf[(GCMdf['year'] == RELYdf['year'][0]) 
            #& (GCMdf['month'] == RELYdf['month'][0])])[:,0:LONGITUDE*LATITUDE]]).shape

#--------------------------------------------------- 
#print RELYdf.iloc[1,:LONGITUDE*LATITUDE]
#print GCMdf.iloc[1,:LONGITUDE*LATITUDE]
#quit()

#=================================================== loop in time series: 
K=0
for t in RELYdf.index:
#for t in [1,2]:
#print RELYdf.index
    MonthlyMeanBias=np.array([np.subtract(x,RELYdf.iloc[t,0:LONGITUDE*LATITUDE]) 
        for x in np.array(GCMdf[
        (GCMdf['year'] == RELYdf['year'][t]) &
        (GCMdf['month'] == RELYdf['month'][t]) &
        (GCMdf['hour'] == RELYdf['hour'][t])
        ])[:,0:LONGITUDE*LATITUDE]])

#--------------------------------------------------- 
    #print "GCMvar3D2:"
    #print [x for x in GCMvar3D[0:30,:]] # right
    #print "GCMdf:wrong"
    #print GCMdf.iloc[0:60,:] # the first month is wrong
    #print GCMdf.values
#--------------------------------------------------- petit test:
    #print " GCM values in this month =======121"
    #print np.array([x for x in np.array(GCMdf[
        #(GCMdf['year'] == RELYdf['year'][t]) &
        #(GCMdf['month'] == RELYdf['month'][t]) &
        #(GCMdf['hour'] == RELYdf['hour'][t])
        #])]).shape
    #print np.array([x for x in np.array(GCMdf[
        #(GCMdf['year'] == RELYdf['year'][t]) &
        #(GCMdf['month'] == RELYdf['month'][t]) &
        #(GCMdf['hour'] == RELYdf['hour'][t])
        #])]).shape
    #print " GCM values in this month =======212"
    #GCMvalue= np.array([x for x in np.array(GCMdf[
        #(GCMdf['year'] == RELYdf['year'][t]) &
        #(GCMdf['month'] == RELYdf['month'][t]) &
        #(GCMdf['hour'] == RELYdf['hour'][t])
        #])])
        ##])[:,0:LONGITUDE*LATITUDE]])
    #print GCMvalue
    #print GCMvalue.shape
#--------------------------------------------------- 
    ##quit()
    #print "RELY values in this month ======="
    #print np.array(RELYdf.iloc[t,0:LONGITUDE*LATITUDE]) 
    #print np.array(RELYdf.iloc[t,:])
    #print np.array(RELYdf.iloc[t,:]).shape
    #print "MonthlyMeanBias           ======="
    #print MonthlyMeanBias
    print MonthlyMeanBias.shape
    #quit()
#---------------------------------------------------  end of petit test:
    L=len(MonthlyMeanBias[:,0])
    MeanBias[K:K+L,:]=MonthlyMeanBias.reshape(L,LATITUDE,LONGITUDE)
    #print " MeanBias           ======="
    #print MeanBias[K:K+L,j,:]
    print " time = "+str(RELYtime[t])+" t= "+str(t)+", L= "+str(L)+", MeanBias len= "+str(len(MeanBias[K:K+L,0,0]))+" k= " +str(K)+", end= "+str(K+L) 
    K=K+L
    # NOTE:needed to be reseted to zeros
    
    #quit()
    #=================================================== check the calculation
    #NOTE: this examination is running in time and Lat(j) dimensions.
    #print " NOTE: examination in Day (in month) and Latitude(j) dimensions."
    #dateindex1=np.random.randint(0,L/2)
    #lonindex1=np.random.randint(0,LONGITUDE*LATITUDE/2)
    #dateindex2=np.random.randint(L/2,L)
    #lonindex2=np.random.randint(L/2,LONGITUDE*LATITUDE)
    #print "random Day index  = " +str(dateindex1)
    #print "random lonindex   = " +str(lonindex1)
    #lonindex1=43
    #GCMvalue=np.array(GCMdf[
        #(GCMdf['year'] == RELYdf['year'][t]) &
        #(GCMdf['month'] == RELYdf['month'][t]) &
        #(GCMdf['hour'] == RELYdf['hour'][t])
        #])[dateindex1:dateindex2,lonindex1:lonindex2]
        #])[:,lonindex1:lonindex1+20]
    #print GCMvalue.shape
    #MeanBiasValue=np.array([x for x in np.array(MonthlyMeanBias)]
            #)[:,lonindex1:lonindex1+20]
            #)[dateind,x1:dateindex2,lonindex1:lonindex2]
    #print '============='
    #print '============= GCM values'
    #print GCMvalue[:,lonindex1:lonindex1+20]
    #print '============='
    #print '============= MonthlyMeanBias'
    #print MonthlyMeanBias[:,lonindex1:lonindex1+20]
    #print '============='
    #print '============='
    #print "GCM value - MeanBiasValue     =  "+str(GCMvalue[:,0:LONGITUDE]-MonthlyMeanBias)
    #print "Defaule         RELYvalue     =  "+str(RELYdf.iloc[t,lonindex1:lonindex1+20])
        #for x in np.array(MonthlyMeanBias)[:,:]])[np.random.randint(0,L),np.random.randint(0,LONGITUDE*LATITUDE)]
#=================================================== print results
print "========================= GCM data:=========================="
print GCMvar3D
print "========================= Reanalysis Data:=========================="
print RELYvar3D
print "========================= montly Mean Bias:=========================="
print MeanBias
print "========================= Corrected GCM data:=========================="



#=================================================== check before WRITING:
print " GCMvar3D shape = " + str(GCMvar3D.shape)
print " MeanBias shape = " + str(MeanBias.shape)
#=================================================== Writing
GCMf.variables[GCMvar][:,:,:] = MeanBias




GCMf.close()
RELYf.close()
quit()
