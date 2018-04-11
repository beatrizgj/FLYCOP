#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Running an individual test, for a particular consortium configuration given by arguments
#cp -p -R ecoliLongTerm_TemplateOptimizeConsortiumV0 ecoliLongTerm_TestXX
#cd ecoliLongTerm_TestXX
#python3 ../../Scripts/ecoliLongTerm_individualTestFLYCOP.py -10 -16 -11 -12 -6 -16 'Yield'

import sys
import importlib
sys.path.append('../../Scripts')
import ecoliLongTermFLYCOP

glu1 = int(sys.argv[1])
ac1 = float(sys.argv[2])
o21 = float(sys.argv[3])
glu2 = int(sys.argv[4])
ac2 = float(sys.argv[5])
o22 = float(sys.argv[6])
fitness = sys.argv[7]

ecoliLongTermFLYCOP.ecoliLongTermFLYCOP_oneConf(glu1,ac1,o21,glu2,ac2,o22,fitness,'./IndividualRunsResults/',3)
