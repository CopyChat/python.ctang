"""
my python functions:
"""
print ("__name__ :", __name__)

import netCDF4
import matplotlib.pyplot as plt
import Scientific.IO.NetCDF as IO

#--------------------------------------------------- read var from time series
def read_time_netcdf(var,netcdf):
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the time to datetime
    TIME=netCDF4.num2date(infile.variables['time'][:],\
            infile.variables['time'].units,\
            calendar=infile.variables['time'].calendar)

    #TIME=[t.year for t in TIME]
    #TIME=[t.strftime("%Y-%m") for t in TIME]
    #TIME=mpl.dates.date2num(TIME)

    # read the variable
    SSR=infile.variables[var][:,0,0].copy()
    #                   time  spaces

    return SSR
