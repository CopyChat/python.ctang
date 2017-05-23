#!/usr/local/bin python

from Scientific.IO.NetCDF import NetCDFFile
import numpy as np
import math
import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt

## Open the file
file = NetCDFFile('/Users/tang/solar_energy/Modeling/test/output/SWIO_1_RAD.1979010100.nc', 'r')
#ifile2=sys.argv[3]
#exp2=sys.argv[4]

# location of the data
lat = 15
lon = 50
hours = 24

# get the values of dswssr,dswssrd, dlwssr, dlwssrd
# the date to be plotted
sw = file.variables['dswssr'][:,lat,lon].copy()
swd = file.variables['dswssrd'][:,lat,lon].copy()
lw = file.variables['dlwssr'][:,lat,lon].copy()
lwd = file.variables['dlwssrd'][:,lat,lon].copy()
# get data for ONE day
sw1=sw[0:hours]
lw1=lw[0:hours]
swd1=swd[0:hours]
lwd1=lwd[0:hours]

time = np.linspace(1,len(sw1),len(sw1))
units = getattr(file.variables['dswssr'],'units')
print sw1
print lw1

# plot
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(311)
ax.plot(time,sw1,'k--',color='b',label='direct',linewidth=3)
ax.plot(time,swd1,color='g',label='diffuse',linewidth=3)
ax.set_title('SW SSR' )
#ax.set_xlabel('Time (hours)')
ax.set_ylabel('radiation / '+units)
pl.ylim([-10,400])
pl.xlim([0,25])

# add the legend in the middle of the plot
ax.legend(fancybox=True, shadow=True,loc='upper right')
# set the alpha value of the legend: it will be translucent
#ax.legend.set_alpha(0.5)

ax2 = fig.add_subplot(312)
ax2.plot(time,lw1,'k--',color='b',label='direct',linewidth=3)
ax2.plot(time,lwd1,color='g',label='diffuse',linewidth=3)
ax2.set_title('LW SSR' )
#ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('radiation / '+units)
pl.ylim([-10,400])
pl.xlim([0,25])
ax2.legend(fancybox=True, shadow=True,loc='upper right')
#ax2.figtext(0.68,0.73,'diffuse', color='g',weight='bold',size="large")

nlw=lwd1+lw1
nsw=swd1+sw1
ax2 = fig.add_subplot(313)
ax2.plot(time,nlw,'k--',color='b',label='lw',linewidth=3)
ax2.plot(time,nsw,color='g',label='sw',linewidth=3)
ax2.set_title('SSR' )
ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('radiation / '+units)
pl.ylim([-10,800])
pl.xlim([0,25])
ax2.legend(fancybox=True, shadow=True,loc='upper right')
plt.show()

# save a png plot

ofile='Downward_Surface_Solar_Radiation'+'.png'
print('save as: '+ofile)
plt.savefig(ofile)
file.close()






