#!/usr/bin/env python

########################################
#Globale Karte fuer tests
########################################

import numpy as np
import math
import pylab as pl
import Scientific.IO.NetCDF as sion
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
import textwrap

pl.close('all')

##########################

ifile1='SWIO_RAD.2001030100.nc'
exp1='test'
#ifile2=sys.argv[3]
#exp2=sys.argv[4]
timestamp='03_2001'
timestep='120'
date='030106'

timestep=int(timestep)
print timestep 
#print(ifile1)
#input files
nc_file1=sion.NetCDFFile(ifile1,'r')

#nc_file2 = sio.netcdf_file(ifile2,'r')
t=nc_file1.variables['time'][:].copy()

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

plt.savefig(ofile1)
plt.show()


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















