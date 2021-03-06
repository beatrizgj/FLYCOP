#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Running an individual test, for a particular consortium configuration given by arguments
#cp -p -R coGrowth4Ecoli_TemplateOptimizeConsortiumV0 coGrowth4Ecoli_TestXX
#cd coGrowth4Ecoli_TestXX
#python3 ../../Scripts/coGrowth4Ecoli_individualTestFLYCOP.py 0.35 0.10 0.15 0.40 1.5 2 1.6 1 'ratioGR'

import sys
import importlib
sys.path.append('../../Scripts')
import coGrowth4EcoliFLYCOP

biomass1 = float(sys.argv[1])
biomass2= float(sys.argv[2])
biomass3 = float(sys.argv[3])
biomass4 = float(sys.argv[4])
arg = float(sys.argv[5])
lys = float(sys.argv[6])
met = float(sys.argv[7])
phe = float(sys.argv[8])
fitness = sys.argv[9]

coGrowth4EcoliFLYCOP.coGrowth4EcoliFLYCOP_oneConf(biomass1,biomass2,biomass3,biomass4,arg,lys,met,phe,fitness,'./IndividualRunsResults/',3)
