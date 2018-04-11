#!/usr/bin/python3

# See SMAC documentation for more details about *wrapper_vX.py, wrapper_scenario_vX.txt and *wrapper_params_vX.pcs

src='synKtPHA_TemplateOptimizeConsortiumV0/'
dst='synKtPHA_TestTempV0'
dirPlots='../smac-output/synKtPHA_PlotsScenario0/'

import cobra
import pandas as pd
import tabulate
import re
import sys
import getopt
import os.path
import copy
import csv
import math
import cobra.flux_analysis.variability
import massedit
import subprocess
import shutil, errno
import statistics
import importlib

# Load code of individual run
sys.path.append('../Scripts')
import synKtPHAFLYCOP

    
# Parsing parameters:
# Reading the first 5 arguments in SMAC
instance = sys.argv[1]
specifics = sys.argv[2]
cutoff = int(float(sys.argv[3]) + 1)
runlength = int(sys.argv[4])
seed = int(sys.argv[5])
# Reading this case study parameters to optimize by SMAC
sucrPer = float(sys.argv[7])
biomassSynecho = float(sys.argv[9])
biomassKT = float(sys.argv[11])
nh4 = float(sys.argv[13])


# Copy the template directory
if (os.path.exists(dst)):
    shutil.rmtree(dst)
try:
    shutil.copytree(src, dst)
except OSError as exc: # python >2.5
    if exc.errno == errno.ENOTDIR:
        shutil.copy(src, dst)
    else: raise
    
os.chdir(dst)

if not os.path.exists(dirPlots):
    os.makedirs(dirPlots)
    

# At a higher level: Running the wrapper-script in SMAC: 
avgfitness,sdfitness=synKtPHAFLYCOP.synKtPHAFLYCOP_oneConf(sucrPer,biomassSynecho,biomassKT,nh4,'MaxPHA',1000,dirPlots,3)

# Print wrapper Output:
print('Result of algorithm run: SAT, 0, 0, '+str(1-avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness maximize
#print('Result of algorithm run: SAT, 0, 0, '+str(avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness minimize

# Remove the temporal dir for this run result
os.chdir('..')
shutil.rmtree(dst)


