#!/bin/bash

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Call: sh FLYCOP.sh <consortiumPrefix> <Y> V<A> <fitnessFunction> <numberOfConfigurations>
# Example: sh FLYCOP.sh 'ecoliLongTerm' 2 V0 'Yield' 10

domainName=$1
id=$2 # '20', '21', ...
templateID=$3 # 'V0', 'V1', 'V2', 'V5' ...
fitness=$4 # 'MaxGR', 'MaxYield'
numOfRuns=$5 # 500, 10

logFile=FLYCOP_${domainName}_${id}_log.txt

cd MicrobialCommunities
smac --scenario-file ../Scripts/${domainName}_confFLYCOP_scenario_v${id}.txt --validation false --numberOfRunsLimit ${numOfRuns} > $logFile
sh ../Scripts/FLYCOPanalyzingResults_${domainName}.sh ${id} ${templateID} $fitness ${numOfRuns}
cd ..


