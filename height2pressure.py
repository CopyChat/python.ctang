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
# Pyhsics Constant:
g=9.8 #m/s^2

#GAS constant
R=287 # J/(K*kg)

con=g/R
print con

T0=-273.15
#quit()
#===================================================  Read Data

#--------------------------------------------------- Reanalysis EIN75: pressure levels
RELYinputf='q_EIN75.198412010000-198503010000.nc.remap.nc'
RELYf=Dataset(RELYinputf,'r') # r is for read only

P_Levels=RELYf.variables[u'level']
print P_Levels[:]

len_p_level=len(P_Levels)
print len_p_level

RELYvar='q'

#--------------------------------------------------- GCM Ta: height
GCMvar='hus'

GCMinputf='ta_6hrLev_HadGEM2-ES_historical_r1i1p1_198412010600-198503010000.nc'
GCMf=Dataset(GCMinputf,'r') # r is for read only

print GCMf.variables.keys() 
H_Levels=GCMf.variables['lev'][:]

print H_Levels[:]

len_h_level=len(H_Levels)
print len_h_level


#T=GCMf.variables['ta'][:]
#print T.shape

T_ocean=GCMf.variables['ta'][1,:,70,100]+T0
T_ocean=GCMf.variables['ta'][1,:,70,100]
print T_ocean
print len(T_ocean)

#=================================================== test the log profile:
# Heights in m
Hm=[  2.00003376e+01  ,8.00013504e+01   ,1.79999115e+02   ,3.20001465e+02
           ,5.00000580e+02   ,7.20000366e+02   ,9.80000854e+02   ,1.27999805e+03
              ,1.61999988e+03   ,1.99999841e+03   ,2.42000171e+03   ,2.88000146e+03
                 ,3.37999829e+03   ,3.91999951e+03   ,4.50000146e+03   ,5.12000000e+03 
                    ,5.77999951e+03   ,6.47999951e+03   ,7.22000000e+03   ,8.00000146e+03
                       ,8.82000000e+03   ,9.67999902e+03   ,1.05799980e+04   ,1.15199980e+04
                          ,1.24999990e+04   ,1.35200010e+04   ,1.45807998e+04   ,1.56946396e+04
                             ,1.68753105e+04   ,1.81386270e+04   ,1.95030098e+04   ,2.09901875e+04
                                ,2.26260820e+04   ,2.44582852e+04   ,2.65836406e+04   ,2.92190801e+04
                                   ,3.29086914e+04   ,3.92548320e+04]
H=[x/1 for x in Hm]
print H[:]

# Pressure in millibars = hPa
P=[    1. ,   2.  ,  3. ,   5.   , 7. ,  10.,   20. ,  30. ,  50. ,  70.,
       100. , 125. , 150. , 175.,  200. , 225. , 250.  ,300. , 350. , 400.,
          450. , 500. , 550. , 600. , 650. , 700. , 750. , 775. , 800. , 825.,
             850. , 875. , 900.,  925. , 950.,  975., 1000.]
print P

logP=[np.log10(x) for x in P]
print logP


Surface_H=0


#--------------------------------------------------- GCM Hus : height
GCMvar='hus'

GCMinputf='hus_6hrLev_HadGEM2-ES_historical_r1i1p1_198412010600-198503010000.nc'
GCMf=Dataset(GCMinputf,'r') # r is for read only

print GCMf.variables.keys() 
H_Levels=GCMf.variables['lev'][:]

print H_Levels[:]

len_h_level=len(H_Levels)
print len_h_level

#--------------------------------------------------- GCM Hus : surface height

H0=GCMf.variables['orog'][:,:]
print ' surface height'
print H0[70,100]

#GCMvar4D=GCMf.variables[GCMvar][:,:,:,:]
#print GCMvar4D.shape


#--------------------------------------------------- GCM psl: surface level pressure

PSLinputf='psl_6hrLev_HadGEM2-ES_historical_r1i1p1_198412010600-198503010000.nc'
PSLf=Dataset(PSLinputf,'r')

Surface_P=PSLf.variables['psl'][1,70,100]

print Surface_P


PSL3D=PSLf.variables['psl'][:,:,:]
print PSL3D.shape




#=================================================== calculate:

#p2=p1*exp[-((g/R)/T)*(z2-z1)]
P=range(1,len(H))
P[0]=Surface_P


print "surface_P=",Surface_P
print "surface_H=",Surface_H
print "38H=",H
print "38T=",T_ocean


for k in range(0,len(H)-1):
    if k==0:
        P[k]=Surface_P*math.exp(-((g/R)/T_ocean[k-1])*(H[k]-Surface_H))
    else:
        P[k]=P[k-1]*math.exp(-((g/R)/(T_ocean[k]))*(H[k]-H[k-1]))
    print P[k]
    #if k==0:
        #P[k]=Surface_P*math.exp(-(H[k]-Surface_H)/(29.3*T_ocean[k]))
    #else:
        #P[k]=P[k-1]*math.exp(-(H[k]-H[k-1])/(29.3*T_ocean[k]))
    #print P[k]



quit()










#--------------------------------------------------- GCM ta: atmosphere temperature

TAinputf='ta_6hrLev_HadGEM2-ES_historical_r1i1p1_198412010600-198503010000.nc'

TAf=Dataset(TAinputf,'r')

#TA4D=TAf.variables['ta'][:,:,:,:]  ### NOTE: time,lev,lat,lon
#print TA4D.shape

GCMvar3D=GCMf.variables[GCMvar][:,:,:]
RELYvar3D=RELYf.variables[RELYvar][:,:,:]
TIME2=len(RELYvar3D[:,0,0])


#=================================================== 
#=================================================== calculate the pressure levels
# P2=P1*exp(-(con/T)*(z2-z1))

for time in [1,2]:
    for lat in [1,2]:
        for lon in [3,4]:
            print "t="+str(time)+" lat="+str(lat)+" lon="+str(lon)
            var4D = GCMf.variables['lev'][time,:,lat,lon]
            H_Levels=var4D[time,:,lat,lon]
            print H_Levels




quit()









GCMvar2='ta'


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

#=================================================== final correction
#=================================================== final correction
# produce the corrected GCM LBC: by MeanBias + future GCM

Futureinputf=('/Users/tang/climate/Bias-Correction/Future/'
    'psl_6hrPlev_HadGEM2-ES_historical_r1i1p1_199412010600-199512010000.nc')
Futuref=Dataset(Futureinputf,'r+') # r is for read only

# Extract data from NetCDF file
print Futuref.variables.keys() 
print Futuref.dimensions.keys() 

FutureLBC=np.add(Futuref.variables[GCMvar][:,:,:], MeanBias)
print " shape of FutureLBC "+str(FutureLBC.shape)

print " starting to write... "

Futuref.variables[GCMvar][:,:,:] = FutureLBC

Futuref.close()
#=================================================== end of writing

#=================================================== delete the in processing file
quit()
