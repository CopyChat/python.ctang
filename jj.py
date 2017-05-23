#!/usr/bin/env python
"""
========
Ctang, A bar plot of time variability changes projection 
        from CORDEX AFR-44, in Southern Africa
        Data was restored on titan
========
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd

import textwrap
import datetime
import ctang

from mpl_toolkits.basemap import Basemap 

from matplotlib.ticker import AutoMinorLocator
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

import math
from scipy import stats
import subprocess

pl.close('all')
#=================================================== define a array
# define a plot array
plot_array = np.array(np.column_stack((N_month,lats,station_name,meanbias,meanbias1,meanbias2,mab)))

# sort by lat, and inverse by [::-1]
plot_array=plot_array[np.argsort(lats)][::-1]

#=================================================== save mat and read
# read from mat
Valid=ctang.Loadmat(DIR+Valid_file+'.mat')

#=================================================== range of data:
dates=pd.date_range((pd.datetime(1969,12,1) +pd.DateOffset(months=1)), periods=360, freq='MS')

#=================================================== 
# define subplots
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14,12),\
        facecolor='w', edgecolor='k') # figsize=(w,h)
fig.subplots_adjust(left=0.3,bottom=0.1,right=0.9,\
        hspace=0.15,top=0.9,wspace=0.43)

# for each subplot:
## active shis subplot for GCM
plt.sca(axes[m,k]) 

#=================================================== set plot

# set limits
ax.set_xlim( dates[0], dates[-1] )

# set grid
ax.yaxis.grid(color='gray', linestyle='dashed')
ax.xaxis.grid(color='gray', linestyle='dashed')

# big title
plt.suptitle(Title)

# The hour locator takes the hour or sequence of hours you want to
# tick, not the base multiple

ax.xaxis.set_major_formatter( DateFormatter('%Y-%m') )
ax.fmt_xdata = DateFormatter('%Y-%m')
fig.autofmt_xdate()

#=================================================== others
ax.legend()


#=================================================== cbar
plt.colorbar(cax,cmap=plt.cm.bwr,orientation='horizontal',shrink=0.9) 
#=================================================== output

# save image
Out_Image='out_image'

plt.savefig(Out_Image+'.eps',format='eps')
plt.savefig(Out_Image+'.png')

plt.show()
