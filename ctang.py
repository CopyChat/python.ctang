"""
my python functions:
"""

import netCDF4
import datetime
import scipy.io
import io
from mpl_toolkits.basemap import Basemap , addcyclic
import numpy as np
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
    #TIME=[t.year for t in TIME]
    #TIME=[t.strftime("%Y-%m") for t in TIME]
    #TIME=datetime.date2num(TIME)

    # read the variable
    SSR=infile.variables[var][:,0,0].copy()
    #                   time  spaces

    return SSR

def get_netcdf_time(netcdf):
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the time to datetime
    TIME=netCDF4.num2date(infile.variables['time'][:],\
            infile.variables['time'].units,\
            calendar=infile.variables['time'].calendar)

    # TIME=[t.year for t in TIME]
    # TIME=[t.strftime("%Y-%m") for t in TIME]
    # TIME=datetime.datetime.date2num(TIME)

    # read the variable
    #SSR=infile.variables[var][:,0,0].copy()
    #                   time  spaces

    return TIME

def read_lonlatmap_netcdf(var,netcdf):
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the time to datetime
    #TIME=netCDF4.num2date(infile.variables['time'][:],\
            #infile.variables['time'].units,\
            #calendar=infile.variables['time'].calendar)

    #TIME=[t.year for t in TIME]
    #TIME=[t.strftime("%Y-%m") for t in TIME]
    #TIME=mpl.dates.date2num(TIME)

    # read the variable
    SSR=infile.variables[var][0,:,:].copy()
    #                   time  spaces

    return np.array(SSR)

def read_lonlat_netcdf(netcdf):
# where the lon is 2D : lon = (lon,lat)
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the variable
    lon=infile.variables['lon'][:].copy()
    lat=infile.variables['lat'][:].copy()
    #                   time  spaces

    return lon, lat

### Running mean/Moving average
def running_mean(l, N):
    sum = 0
    result = list( 0 for x in l)

    for i in range( 0, N ):
        sum = sum + l[i]
        result[i] = sum / (i+1)

    for i in range( N, len(l) ):
        sum = sum - l[i-N] + l[i]
        result[i] = sum / N

    return result

#=================================================== 
def running_mean2(array,N,mode='valid'):
    return np.convolve(array, N, mode=mode)
# http://stackoverflow.com/questions/13728392/moving-average-or-running-mean

def running_mean3(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 


#=================================================== 
#only with rsds and tas # follow Martin 2015
def PVpot(rsds,tas):
    if tas.max() > 200:
        tas=tas-273.5
    return rsds*(1-0.0045*(tas-25))+0.1*np.log10(rsds)
    #'define a1=rsds1*(1-0.0045*(tas1-25))+0.1*log10(rsds1)'
#=================================================== 
#=================================================== 
#only with rsds and tas # follow Jerez S, 2015
def PVpot2(rsds,tas,sfcWind):
    if tas.max() > 200:
        tas=tas-273.5

    # define parameters
    a1=1.1035e-3
    a2=-1.4e-7
    a3=-4.715e+6
    a4=7.64e+6

    PVpot=a1*rsds+a2*rsds*rsds+a3*rsds*tas+a4*rsds*sfcWind
    return PVpot
#=================================================== 
def get_axis_limits(ax, scale=.8):
    return ax.get_xlim()[1]*scale, ax.get_ylim()[1]*scale


#=================================================== to read lon lat from GCM
# where the lon is 1D : lon = (lon)
def read_lonlat_netcdf_1D(netcdf):
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the variable
    lon=infile.variables['lon'][:].copy()
    lat=infile.variables['lat'][:].copy()
    #                   time  spaces



    lon2D=np.zeros((len(lat),len(lon)))
    lat2D=np.zeros((len(lat),len(lon)))

    for i in range(len(lat)):
        lon2D[i,:]=lon
    for i in range(len(lon)):
        lat2D[:,i]=lat

    return lon2D, lat2D

#print np.array(read_lonlat_netcdf_1D('/Users/ctang/Code/CORDEX_AFR_studies/data/rsds_Amon_MIROC5.rcp85.2070-2099.SA.timmean.nc'))[1]

#=================================================== 
def significant_map(mean_change,t_value):
    for v in range(N_var):
        for m in range(N_model):
            for lat in range(mean_change.shape[2]):
                for lon in range(mean_change.shape[3]):
                    if np.abs(stats.ttest_1samp(\
                            mean_change[v,:,lat,lon],mean_change[v,m,lat,lon])[0]) < T:
                        t_value[v,m,lat,lon]=np.NaN
    return t_value
#=================================================== 
def setMap(map):
    map.drawcoastlines(linewidth=1)
    map.drawparallels(np.arange(-90.,91.,10.),labels=[1,0,0,0],linewidth=0.5)
    map.drawmeridians(np.arange(-180.,181.,20.),labels=[0,0,0,1],linewidth=0.5)
    map.drawmapboundary()
    map.drawcountries()
    return map
def write_2D_txt(my_list,the_filename):
    #with open(the_filename, 'w') as f:
        #for s in my_list:
            #f.write(str(s[:])+'\n' )
    with io.open(the_filename, 'wb') as f:
        f.writelines(line for line in my_list)
    #return 0
    #with open(the_filename, 'r') as f:
    #my_list = [line.rstrip(u'\n') for line in f]
#=================================================== 
#D1=[1,2,3]
#D2=[[1,2,3],[4,5,6]]
#L2=((1,2,3),(4,5,6))
#write_3D_txt(D2,'outfile')


def write_3D_txt(the_filename,Array3D):
# Write the array to disk
    with file('test.txt', 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(Array3D.shape))

        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in Array3D:
            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.  
            np.savetxt(the_filename, data_slice, fmt='%-7.2f')
            #print data_slice
            #outfile.write("test")

            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')
# Generate some test data
#data = np.arange(200).reshape((4,5,10))
#write_3D_txt('test.txt',data)

#=================================================== 

def Save2mat(matfile,MyArray):
# Some test data
# Specify the filename of the .mat file
    #matfile = 'test_mat.mat'
# Write the array to the mat file. For this to work, the array must be the value
# corresponding to a key name of your choice in a dictionary
    scipy.io.savemat(matfile, mdict={'out': MyArray}, oned_as='row')
# For the above line, I specified the kwarg oned_as since python (2.7 with 
# numpy 1.6.1) throws a FutureWarning.  Here, this isn't really necessary 
# since oned_as is a kwarg for dealing with 1-D arrays.
def Loadmat(matfile):
    # Now load in the data from the .mat that was just saved
    return  scipy.io.loadmat(matfile)['out']
    # And just to check if the data is the same:

#=================================================== 
degree_sign='0'
def set_degree_sign():
    global degree_sign
    degree_sign= u'\N{DEGREE SIGN}'
#=================================================== to plot an 12months plot
#def MonthPlot(time12file,varname,ax):
#=================================================== 
def NotAvailable(axx):
    axx.set_xticks([])
    #axx.set_yticks([])
    #axx.xaxis.set_visible(False)
    #axx.yaxis.set_visible(False)
    axx.plot(range(10))
    axx.axis('off')
    axx.plot(range(9,-1,-1))
    t='NotAvailable'
    cmap = plt.cm.bwr
    axx.text(5, 5, t, fontsize=8, style='oblique', ha='center',\
                    va='center', wrap=True)


#=================================================== read time lon,lat
def read_3D_netcdf(var,netcdf):
    """
    to read value from a netcdf file for particular variable
    """
    #open input files
    infile=IO.NetCDFFile(netcdf,'r')

    # read the time to datetime
    #TIME=netCDF4.num2date(infile.variables['time'][:],\
            #infile.variables['time'].units,\
            #calendar=infile.variables['time'].calendar)

    #TIME=[t.year for t in TIME]
    #TIME=[t.strftime("%Y-%m") for t in TIME]
    #TIME=mpl.dates.date2num(TIME)

    # read the variable
    SSR=infile.variables[var][:,:,:].copy()
    #                   time  spaces

    return np.array(SSR)

#=================================================== ,TIME
def get_TIME_netCDF(netcdf):
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
    return TIME
#=================================================== 
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

#=================================================== 
def allmylib():
    import pip
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])
    print(installed_packages_list)


#=================================================== 
def empty_plot(ax):

    # Hide axis
    plt.setp(ax.get_xaxis().set_visible(False))
    plt.setp(ax.get_yaxis().set_visible(False))

    # plt.setp(ax.get_xaxis().set_ticks([]))
    # plt.setp(ax.get_yaxis().set_ticks([]))

    # plt.setp(ax.get_yticklabels(),visible=False)
    # plt.setp(ax.get_xticklabels(),visible=False)

    # Hide the right and top spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
#=================================================== 
## two tail = 0.95:
def get_T_value(dof):
    T_value=[\
        12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228,\
        2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086,\
        2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042,\
        2.040, 2.037, 2.035, 2.032, 2.030, 2.028, 2.026, 2.024, 2.023, 2.021,\
        2.020, 2.018, 2.017, 2.015, 2.014, 2.013, 2.012, 2.011, 2.010, 2.009,\
        2.008, 2.007, 2.006, 2.005, 2.004, 2.003, 2.002, 2.002, 2.001, 2.000,\
        2.000, 1.999, 1.998, 1.998, 1.997, 1.997, 1.996, 1.995, 1.995, 1.994,\
        1.994, 1.993, 1.993, 1.993, 1.992, 1.992, 1.991, 1.991, 1.990, 1.990,\
        1.990, 1.989, 1.989, 1.989, 1.988, 1.988, 1.988, 1.987, 1.987, 1.987,\
        1.986, 1.986, 1.986, 1.986, 1.985, 1.985, 1.985, 1.984, 1.984, 1.984]

    if dof < 1:
        return np.nan
        quit()
    # infinity: 
    if dof > 100:
        return 1.960
    else:
        return T_value[dof-1]
#=================================================== 
# one tail t test table:
# dof         0.90    0.95   0.975    0.99   0.995   0.999
# 1.       3.078   6.314  12.706  31.821  63.657 318.313
# 2.       1.886   2.920   4.303   6.965   9.925  22.327
# 3.       1.638   2.353   3.182   4.541   5.841  10.215
# 4.       1.533   2.132   2.776   3.747   4.604   7.173
# 5.       1.476   2.015   2.571   3.365   4.032   5.893
# 6.       1.440   1.943   2.447   3.143   3.707   5.208
# 7.       1.415   1.895   2.365   2.998   3.499   4.782
# 8.       1.397   1.860   2.306   2.896   3.355   4.499
# 9.       1.383   1.833   2.262   2.821   3.250   4.296
# 10.       1.372   1.812   2.228   2.764   3.169   4.143
# 11.       1.363   1.796   2.201   2.718   3.106   4.024
# 12.       1.356   1.782   2.179   2.681   3.055   3.929
# 13.       1.350   1.771   2.160   2.650   3.012   3.852
# 14.       1.345   1.761   2.145   2.624   2.977   3.787
# 15.       1.341   1.753   2.131   2.602   2.947   3.733
# 16.       1.337   1.746   2.120   2.583   2.921   3.686
# 17.       1.333   1.740   2.110   2.567   2.898   3.646
# 18.       1.330   1.734   2.101   2.552   2.878   3.610
# 19.       1.328   1.729   2.093   2.539   2.861   3.579
# 20.       1.325   1.725   2.086   2.528   2.845   3.552
# 21.       1.323   1.721   2.080   2.518   2.831   3.527
# 22.       1.321   1.717   2.074   2.508   2.819   3.505
# 23.       1.319   1.714   2.069   2.500   2.807   3.485
# 24.       1.318   1.711   2.064   2.492   2.797   3.467
# 25.       1.316   1.708   2.060   2.485   2.787   3.450
# 26.       1.315   1.706   2.056   2.479   2.779   3.435
# 27.       1.314   1.703   2.052   2.473   2.771   3.421
# 28.       1.313   1.701   2.048   2.467   2.763   3.408
# 29.       1.311   1.699   2.045   2.462   2.756   3.396
# 30.       1.310   1.697   2.042   2.457   2.750   3.385
# 31.       1.309   1.696   2.040   2.453   2.744   3.375
# 32.       1.309   1.694   2.037   2.449   2.738   3.365
# 33.       1.308   1.692   2.035   2.445   2.733   3.356
# 34.       1.307   1.691   2.032   2.441   2.728   3.348
# 35.       1.306   1.690   2.030   2.438   2.724   3.340
# 36.       1.306   1.688   2.028   2.434   2.719   3.333
# 37.       1.305   1.687   2.026   2.431   2.715   3.326
# 38.       1.304   1.686   2.024   2.429   2.712   3.319
# 39.       1.304   1.685   2.023   2.426   2.708   3.313
# 40.       1.303   1.684   2.021   2.423   2.704   3.307
# 41.       1.303   1.683   2.020   2.421   2.701   3.301
# 42.       1.302   1.682   2.018   2.418   2.698   3.296
# 43.       1.302   1.681   2.017   2.416   2.695   3.291
# 44.       1.301   1.680   2.015   2.414   2.692   3.286
# 45.       1.301   1.679   2.014   2.412   2.690   3.281
# 46.       1.300   1.679   2.013   2.410   2.687   3.277
# 47.       1.300   1.678   2.012   2.408   2.685   3.273
# 48.       1.299   1.677   2.011   2.407   2.682   3.269
# 49.       1.299   1.677   2.010   2.405   2.680   3.265
# 50.       1.299   1.676   2.009   2.403   2.678   3.261
# 51.       1.298   1.675   2.008   2.402   2.676   3.258
# 52.       1.298   1.675   2.007   2.400   2.674   3.255
# 53.       1.298   1.674   2.006   2.399   2.672   3.251
# 54.       1.297   1.674   2.005   2.397   2.670   3.248
# 55.       1.297   1.673   2.004   2.396   2.668   3.245
# 56.       1.297   1.673   2.003   2.395   2.667   3.242
# 57.       1.297   1.672   2.002   2.394   2.665   3.239
# 58.       1.296   1.672   2.002   2.392   2.663   3.237
# 59.       1.296   1.671   2.001   2.391   2.662   3.234
# 60.       1.296   1.671   2.000   2.390   2.660   3.232
# 61.       1.296   1.670   2.000   2.389   2.659   3.229
# 62.       1.295   1.670   1.999   2.388   2.657   3.227
# 63.       1.295   1.669   1.998   2.387   2.656   3.225
# 64.       1.295   1.669   1.998   2.386   2.655   3.223
# 65.       1.295   1.669   1.997   2.385   2.654   3.220
# 66.       1.295   1.668   1.997   2.384   2.652   3.218
# 67.       1.294   1.668   1.996   2.383   2.651   3.216
# 68.       1.294   1.668   1.995   2.382   2.650   3.214
# 69.       1.294   1.667   1.995   2.382   2.649   3.213
# 70.       1.294   1.667   1.994   2.381   2.648   3.211
# 71.       1.294   1.667   1.994   2.380   2.647   3.209
# 72.       1.293   1.666   1.993   2.379   2.646   3.207
# 73.       1.293   1.666   1.993   2.379   2.645   3.206
# 74.       1.293   1.666   1.993   2.378   2.644   3.204
# 75.       1.293   1.665   1.992   2.377   2.643   3.202
# 76.       1.293   1.665   1.992   2.376   2.642   3.201
# 77.       1.293   1.665   1.991   2.376   2.641   3.199
# 78.       1.292   1.665   1.991   2.375   2.640   3.198
# 79.       1.292   1.664   1.990   2.374   2.640   3.197
# 80.       1.292   1.664   1.990   2.374   2.639   3.195
# 81.       1.292   1.664   1.990   2.373   2.638   3.194
# 82.       1.292   1.664   1.989   2.373   2.637   3.193
# 83.       1.292   1.663   1.989   2.372   2.636   3.191
# 84.       1.292   1.663   1.989   2.372   2.636   3.190
# 85.       1.292   1.663   1.988   2.371   2.635   3.189
# 86.       1.291   1.663   1.988   2.370   2.634   3.188
# 87.       1.291   1.663   1.988   2.370   2.634   3.187
# 88.       1.291   1.662   1.987   2.369   2.633   3.185
# 89.       1.291   1.662   1.987   2.369   2.632   3.184
# 90.       1.291   1.662   1.987   2.368   2.632   3.183
# 91.       1.291   1.662   1.986   2.368   2.631   3.182
# 92.       1.291   1.662   1.986   2.368   2.630   3.181
# 93.       1.291   1.661   1.986   2.367   2.630   3.180
# 94.       1.291   1.661   1.986   2.367   2.629   3.179
# 95.       1.291   1.661   1.985   2.366   2.629   3.178
# 96.       1.290   1.661   1.985   2.366   2.628   3.177
# 97.       1.290   1.661   1.985   2.365   2.627   3.176
# 98.       1.290   1.661   1.984   2.365   2.627   3.175
# 99.       1.290   1.660   1.984   2.365   2.626   3.175
# 100.       1.290   1.660   1.984   2.364   2.626   3.174
# infinity   1.282   1.645   1.960   2.326   2.576   3.090
