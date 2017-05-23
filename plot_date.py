########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import datetime 
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
from numpy import arange
import numpy as np
import pylab as pl
import parser
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

rsdsinput="/Users/tang/climate/ENSO/rsds_CERES-EBAF_L3B_Ed2-8_200003-201405.monmean.fldmean.SWIO.nc"

rsdsf=IO.NetCDFFile(rsdsinput,'r')
rsds=rsdsf.variables['rsds'][:,:,0].copy()
print rsdsf.variables['time'].units

# units of time
date0=datetime.date(2000,3,1) 
Abstime=[date0 + datetime.timedelta(days=t) for t in rsdsf.variables['time'][:]]
print Abstime

Abstimestamp=[t.strftime("%d. %B %Y") for t in Abstime]
print Abstimestamp


#=================================================== to plot

fig, ax = plt.subplots()
ax.plot(Abstime[:], rsds)

# this is superfluous, since the autoscaler should get it right, but
# use date2num and num2date to convert between dates and floats if
# you want; both date2num and num2date convert an instance or sequence

#ax.plot_date(date2num(Abstime[:]), rsds)

ax.set_xlim( Abstime[0], Abstime[-1] )

# The hour locator takes the hour or sequence of hours you want to
# tick, not the base multiple

#ax.xaxis.set_major_locator( DayLocator() )
#ax.xaxis.set_minor_locator( HourLocator(arange(0,25,6)) )
ax.xaxis.set_major_formatter( DateFormatter('%Y') )
#ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()

ax.grid()
plt.show()

quit()
