#!/bin/bash

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

# Call:
#sh plot_biomassX4_vs_4mediaItem.sh <suffix> <met1 (without [e])> <met2> <met3> <met4> <strain1> <strain2> <strain3> <strain4>
#sh plot_biomassX4_vs_4mediaItem.sh "coGrowth4Ecoli" 'arg' 'lys' 'met' 'phe' 'Ec1' 'Ec2' 'Ec3' 'Ec4'

dirScripts="../../Scripts"


suffix=$1
met1=$2
met2=$3
met3=$4
met4=$5
strain1=$6
strain2=$7
strain3=$8
strain4=$9

outFile="biomass_vs_"${met1}_${met2}_${met3}_${met4}_${suffix}".txt"
plotFile="biomass_vs_"${met1}_${met2}_${met3}_${met4}_${suffix}"_plot.pdf"

numMet1=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met1} | cut -d: -f1`
numMet2=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met2} | cut -d: -f1`
numMet3=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met3} | cut -d: -f1`
numMet4=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met4} | cut -d: -f1`

met1File="media_log_substrate_"${met1}".txt"
egrep '\{'$numMet1'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet1}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met1File
met2File="media_log_substrate_"${met2}".txt"
egrep '\{'$numMet2'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet2}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met2File
met3File="media_log_substrate_"${met3}".txt"
egrep '\{'$numMet3'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet3}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met3File
met4File="media_log_substrate_"${met4}".txt"
egrep '\{'$numMet4'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet4}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met4File

paste -d'\t' total_biomass_log_${suffix}.txt ${met1File} ${met2File} ${met3File} ${met4File} > $outFile
rm ${met1File} ${met2File} ${met3File} ${met4File}

Rscript --vanilla ${dirScripts}/plot.biomassX4.vs.4substrate.r $outFile $plotFile $met1 $met2 $met3 $met4 $strain1 $strain2 $strain3 $strain4



