#!/usr/bin/env python
########################################
# to modify the NetCDF files
########################################
#First import the netcdf4 library
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import numpy as np
import sys,getopt

import sys 
sys.path.append('/Users/ctang/Code/Python/')
import ctang

#=================================================== get opts input file
var=str(sys.argv[1:][0])
netcdf=str(sys.argv[1:][1])
#=================================================== 

Value=ctang.read_time_netcdf(var,netcdf)
#Value=np.array(ctang.read_time_netcdf(var,netcdf)).astype(float)

#for v in Value:
    #printf( "%s,", v)
print(','.join([str(i) for i in Value]))


