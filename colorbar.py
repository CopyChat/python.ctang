#!/usr/bin/env python

########################################
#Globale Karte fuer tests
########################################
from mpl_toolkits.axes_grid1 import ImageGrid
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

my_values= np.array([0.,1.,2.,3.,4.,5.,6.])
x= np.array([0.,1.2,2.3,3.4,4.4,5.4,64.])
y= np.array([0.,1.,2.,3.,4.,5.,6.])
c= np.array([0.,1.,2.,3.,4.,5.,6.])
cmap=plt.get_cmap('jet')
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
bounds = np.linspace(0,len(my_values),len(my_values)+1)
#where my_values is

#Let's assume we have two arrays, x and y, that represent the position of random points. A third array, c, is associated to each point and can only take values from my_values.

#The following code will plot a scatter plot and the colorbar is divided into 7 discrete levels.

plt.scatter(x,y,c=c)
plt.colorbar(boundaries=bounds)
#plt.show()


grid_top = ImageGrid(fig, 211, nrows_ncols = (1, 3),
		cbar_location = "right",cbar_mode="single",cbar_pad=.2) 

for n in xrange(3):
	im1 = grid_top[n].pcolor(data_top[n], 
			interpolation='nearest', vmin=0, vmax=5)
#plt.show()
data_top = []
for i in range(3):
    data_top.append(np.random.random((5,5)))


fig = plt.figure(1,(8.,8.))

grid_top = ImageGrid(fig, 211, nrows_ncols = (1, 3),
                     cbar_location = "right",
                     cbar_mode="single",
                     cbar_pad=.2)

for g, d in zip(grid_top,data_top):
    plt.sca(g)
    M = Basemap(projection='ortho',lon_0=10.0,lat_0=50.0,resolution='l')
    M.drawcoastlines()
    M.drawparallels(np.arange(-90.,120.,30.))
    M.drawmeridians(np.arange(0.,360.,60.))
    I = M.imshow(d,vmin=0,vmax=1,interpolation="nearest")
grid_top.cbar_axes[0].colorbar(I)
