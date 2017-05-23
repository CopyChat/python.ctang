#!/usr/bin/python

import os
from ecmwfapi import ECMWFDataServer



server = ECMWFDataServer()
time=["06"]
year=["2013"]
param=["129.128","130.128","131.128","132.128","157.128","151.128"]
nam=["hgt","air","uwnd","vwnd","rhum","psl"]
#month=["01","02","03","04","05","06","07","08","09","10","11","12"]

for y in year:
	#for m in month:
	for p in range(len(param)):
		for t in time:
			date=y+"-01-01/to/"+y+"-12-31"
			print date
			print  nam[p]+"."+y+"."+t+".nc"
			os.system('echo "############################################################# ^_^"')
			server.retrieve({
				'dataset' : "interim",
				'levelist' : "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
				'step'    : "0",
				'number'  : "all",
				'levtype' : "pl",   # set to "sl" for surface level
				'date' 	  : date,
				'time'    : t ,
				'origin'  : "all",
				'type'    : "an",
				'param'   : "129.128/130.128/131.128/132.128/157.128",
				'param'   : param[p],
				'area'    : "0/0/-40/100",  # Four values as North/West/South/East
				'grid'    : "1.5/1.5",   	# Two values: West-East/North-South increments 0.75/0.75
				'format'  : "netcdf",       # if grib, just comment this line 
				'target'  : nam[p]+"."+y+"."+t+".nc"
							})

