#!/bin/bash

# FLYCOP 
# Author: Beatriz García-Jiménez
# April 2018

dirScripts="../../Scripts"

suffix=$1
met1=$2
met2=$3
met3=$4
endCycle=$5
title=$6
colorSubs1=$7
colorSubs2=$8
colorSubs3=$9
strain1=${10}
strain2=${11}

outFile="biomass_vs_"${met1}_${met2}_${met3}_${suffix}".txt"
plotFile="biomass_vs_"${met1}_${met2}_${met3}_${suffix}"_plot.pdf"

numMet1=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met1} | cut -d: -f1`
numMet2=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met2} | cut -d: -f1`
numMet3=`head -n1 media_log_${suffix}.txt | sed "s/.*{ //" | sed "s/}.*//" | sed "s/'//g" | sed "s/, /\n/g" | egrep -w -n ${met3} | cut -d: -f1`

met1File="media_log_substrate_"${met1}".txt"
egrep '\{'$numMet1'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet1}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met1File
met2File="media_log_substrate_"${met2}".txt"
egrep '\{'$numMet2'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet2}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met2File
met3File="media_log_substrate_"${met3}".txt"
egrep '\{'$numMet3'\}' media_log_${suffix}.txt | sed "s/media_//" | sed "s/{$numMet3}//" | sed "s/(1, 1)//" | sed "s/sparse.*/0.0/" | sed "s/;$//" | sed "s/\ =\ /\t/" | awk -F"\t" 'BEGIN{oldCycle=0;value=-1}{if($1!=oldCycle){print value; oldCycle=$1; value=$2}else{value=$2}}END{print value}' > $met3File
met4File="media_log_substrate_"${met4}".txt"

paste -d'\t' total_biomass_log_${suffix}.txt ${met1File} ${met2File} ${met3File} > $outFile
rm ${met1File} ${met2File} ${met3File}

Rscript --vanilla ${dirScripts}/plot.biomassX2.vs.3substrate.r $outFile $plotFile $met1 $met2 $met3 $endCycle $title $colorSubs1 $colorSubs2 $colorSubs3 $strain1 $strain2



