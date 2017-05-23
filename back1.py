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
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
import textwrap

pl.close('all')

########################## input CMIP5 data

DIR='/Users/tang/climate/CMIP5/'
VARIABLE='tas'
PRODUCT='Amon'
model='CanESM2'
EXPERIMENT='rcp85'
ENSEMBLE='r1i1p1'
TIME='200601-210012'
# tas_Amon_CanESM2_rcp85_r1i1p1_200601-210012.nc &  this file was copied locally for tests in this book
infile1=DIR+EXPERIMENT+'/'+model+'/'+VARIABLE+'_'+PRODUCT+'_'+model+'_'+EXPERIMENT+'_'+ENSEMBLE+'_'+TIME+'.nc'
print('the file is ======================= ' +infile1)


# open input files
infile=IO.NetCDFFile(infile1,'r')

timeValue=infile.variables['time'][:].copy()
YEAR1=(timeValue//365.+1850)
print YEAR1
#YEAR = list(set(YEAR1))
#YEAR.sort(key=YEAR1.index)

YEAR = []
[YEAR.append(i) for i in YEAR1 if not i in YEAR]



TEMP=infile.variables[VARIABLE][:,:,:].copy()

print TEMP

mask=np.ones(TEMP.shape); print mask

b=np.arange(10,50,5).reshape(2,4)
print b



TAS=np.mean(TEMP[0:11][:][:])-273.5

print TAS

arr = [i for i in range(10), 9,[]]
arr = [i for i in np.mean(TEMP[0:11][:][:]), np.mean(TEMP[12:23][:][:]),[]]

print arr



k=range(0,len(YEAR1),12)
print k
for  v in range(0,len(YEAR1),12):
    print v
    k[v/12]=np.mean(TEMP[v:v+11][:][:])
print k

#=================================================== to plot
print "======== to plot =========="

print len(YEAR)
print len(k)

print YEAR
print k
fig1=plt.figure(figsize=(16,9))
k2=np.ones(len(k))

plt.plot(YEAR,k,label=model,color="red",linewidth=2)
plt.plot(YEAR,k+k2,label=model,color="green",linewidth=2)
plt.show()

print "==============================================="

quit()

plt.savefig(ofile1)

#print np.where(b[1][:])
#print np.mean(np.where(b[1][:]))





#print TEMP[0:11,12][:][:]

#print (TEMP[0:11,12][:][:]).shape

#MeanTEMP[]=[i for i < 120; i=np.mean(TEMP[0+12*i:11+12*i][:][:])


# get all the dimensions variables
allDimNames = file1.dimensions.keys() 
print allDimNames

# get the whole of time
t=file1.variables['time'][:].copy()
print t

# Get the value of a netCDF dimension
dimValue = file1.dimensions['lon']
print dimValue

# Get all global attributes for a netCDF file
globalAttList = dir(file1)
print globalAttList


# Get the value of a global attribute
globalAttValue = getattr(file1, 'Conventions') 
print globalAttValue


# Inquire whether a global attribute exists
attName = 'Conventions' 
if hasattr(file1, attName):
    print attName, "exists in this netCDF file." 

# Flush all data to disk
file1.sync()


#=================================================== for variables
# Get all variables
allVar=file1.variables.copy() # not only names
print allVar

# or
print file1.variables.keys()

# read a variable
tas1=file1.variables[VARIABLE][1,:,:].copy()

# Get a list of all netCDF variable attributes
attList = dir('tas')  #  attList contains all of the attributes for "var" and the entries: "assignValue", "getValue", "typecode". 
print 'all attributes of tas is:' 
print attList


#Get the "shape" of a netCDF variable
tasShape = tas1.shape 
print tasShape

#Get the value of a netCDF variable attribute
attData = getattr(file1.variables['tas'], 'units') 
print 'units is '
print attData



#deciding on date to be plotted



srad0 = nc_file1.variables['rtnscl'][5,:,:].copy()
srads = nc_file1.variables['rsnscl'][5,:,:].copy()
trad0 = nc_file1.variables['rtnlcl'][5,:,:].copy()
trads = nc_file1.variables['rsnlcl'][5,:,:].copy()

lat = nc_file1.variables['xlat'][:].copy()
lon = nc_file1.variables['xlon'][:].copy()


#set tas to be plotted
netrad0=(srad0+trad0)
netrads=(srads+trads)



#for output

ofile1='netrad0_map_'+exp1+'_'+date+'.png'
ofile2='netrads_map_'+exp1+'_'+date+'.png'
print('save as: '+ofile1)
print('save as: '+ofile2)

title1='Net radiation energy fluxes at TOA ('+exp1+')'
title2='Net radiation energy fluxes at surface ('+exp1+')'
nol=10  #number of levels of colorbar

##########################

##for flexibel colorbar
##min and max values
netrad0max=np.max(netrad0)
netrad0min=np.min(netrad0)
netradsmax=np.max(netrads)
netradsmin=np.min(netrads)

#get minmax for colorbar
if abs(netrad0min)>abs(netrad0max):
       minmax=math.ceil(abs(netrad0min))
else: minmax=math.ceil(abs(netrad0max))
minnetrad0=minmax*(-1)
maxnetrad0=minmax

if abs(netradsmin)>abs(netradsmax):
       minmax=math.ceil(abs(netradsmin))
else: minmax=math.ceil(abs(netradsmax))
minnetrads=minmax*(-1)
maxnetrads=minmax

print minmax

##for fixed colorbar
#minnetrad0=-80
#maxnetrad0=80
#minnetrads=-80
#maxnetrads=80

# plot figure netrad0
fig1=plt.figure(figsize=(16,9))
map=Basemap(projection='cyl',llcrnrlat=-40,urcrnrlat=0,\
         llcrnrlon=0,urcrnrlon=100,resolution='l')
map.drawcoastlines(linewidth=0.35)
map.drawparallels(np.arange(-90.,91.,15.),labels=[1,0,0,0],linewidth=0.35)
map.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],linewidth=0.35)
map.drawmapboundary()
x,y=map(lon,lat)
#cmap=plt.get_cmap('seismic')
cmap=plt.get_cmap('jet')
#cmap=plt.get_cmap('RdBu_r')
pic=map.pcolormesh(x,y,netrad0,cmap=cmap)

plt.title("\n".join(textwrap.wrap(title1,55)))
plt.figtext(0.68,0.73,timestamp, size="small")



plt.colorbar(orientation='horizontal') # draw colorbar
print minnetrad0
# for the colorbar
#fig1 = plt.figure(figsize=(8,3))
#ax1 = fig1.add_axes([0.05, 0.060, 0.9, 0.05]) # position of the cbar
#cmap1 = mpl.cm.cool
#norm1 = mpl.colors.Normalize(vmin=minnetrad0, vmax=maxnetrad0)
#cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap1,
                                   #norm=norm1,
                                   #orientation='horizontal')
#cb1.set_clim(vmin=minnetrad0,vmax=maxnetrad0)
#cb1.set_label('W/m^2')




#cb = fig1.colorbar(pic,shrink=0.8)
#cb.set_clim(vmin=minnetrad0,vmax=maxnetrad0)
##cb.set_clim(vmin=110,vmax=1000)
#cb.set_label('W/m^2')



#plot figure netrads
fig2=plt.figure(figsize=(8,5))
map=Basemap(projection='cyl',llcrnrlat=-40,urcrnrlat=0,\
         llcrnrlon=0,urcrnrlon=100,resolution='l')
map.drawcoastlines(linewidth=0.35)
map.drawparallels(np.arange(-90.,91.,15.),labels=[1,0,0,0],linewidth=0.35)
map.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],linewidth=0.35)
map.drawmapboundary()
x,y=map(lon,lat)
cmap=plt.get_cmap('RdBu_r')
pic=map.pcolormesh(x,y,netrads,cmap=cmap)

plt.title("\n".join(textwrap.wrap(title2,55)))
plt.figtext(0.68,0.73,timestamp, size="small")

cb = fig2.colorbar(pic,shrink=0.5)
cb.set_clim(vmin=minnetrads,vmax=maxnetrads)
cb.set_label('W/m^2')
#plt.colorbar()

plt.savefig(ofile2)
plt.show()















