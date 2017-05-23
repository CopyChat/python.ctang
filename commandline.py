#!/usr/bin/env python
########################################
# to modify the NetCDF files
########################################
#First import the netcdf4 library
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import numpy as np
import sys,getopt


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

# Read en existing NetCDF file and create a new one
# f is going to be the existing NetCDF file from where we want to import data
# and g is going to be the new file.

f=Dataset('tas_Amon_CanESM2_rcp85_r1i1p1_200601-210012.nc','r+') # r is for read only

print "dkfjksfkd----------------s"
f.variables['tas'][:,:,:]= np.full(f.variables['tas'].shape,8)

#print f.variables['tas'][:]
print f.variables['tas'].shape
#a=np.full((22,222,11),5)
#print a

f.close()
quit()
# Read en existing NetCDF file and create a new one
# f is going to be the existing NetCDF file from where we want to import data
# and g is going to be the new file.

f=Dataset('tas_Amon_CanESM2_rcp85_r1i1p1_200601-210012.nc','r+') # r is for read only


f.variables['tas'][:,:,:]= np.full(f.variables['tas'].shape,5)

#print f.variables['tas'][:]
print f.variables['tas'].shape
#a=np.full((22,222,11),5)
#print a

f.close()
quit()

g=Dataset('output.nc','w') # w if for creating a file
                                      # if the file exists it the 
                                      # file will be deleted to write on it


# To copy the global attributes of the netCDF file  

for attname in f.ncattrs():
    setattr(g,attname,getattr(f,attname))

# To copy the dimension of the netCDF file

for dimname,dim in f.dimensions.iteritems():
       # if you want to make changes in the dimensions of the new file
       # you should add your own conditions here before the creation of the dimension.
        g.createDimension(dimname,len(dim))


# To copy the variables of the netCDF file

for varname,ncvar in f.variables.iteritems():
       # if you want to make changes in the variables of the new file
       # you should add your own conditions here before the creation of the variable.
       var = g.createVariable(varname,ncvar.dtype,ncvar.dimensions,fill_value=None)
       #Proceed to copy the variable attributes
       #for attname in ncvar.ncattrs():  
          #setattr(var,'fill_value','i4')
          #setattr(var,attname,getattr(ncvar,attname))
       #Finally copy the variable data to the new created variable
       var[:] = ncvar[:]


f.close()
g.close()

num
