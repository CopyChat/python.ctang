#!/bin/bash - 
#======================================================
#
#          FILE: pplot.sh
# 
USAGE="./pplot.sh"
# 
#   DESCRIPTION: to create a python script prepared for plot
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: --- unknown
#         NOTES: ---
#        AUTHOR: |CHAO.TANG| , |chao.tang.1@gmail.com|
#  ORGANIZATION: 
#       CREATED: 05/23/17 22:20
#      REVISION: 1.0
#=====================================================
set -o nounset           # Treat unset variables as an error
. ~/Shell/functions.sh   # ctang's functions

#=================================================== 
filename=${1:-python_plot.py}		#  default
echo $filename

cp ~/Code/Python/template.py ./$filename

