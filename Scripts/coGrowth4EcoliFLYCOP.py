#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Example: >>%run coGrowth4EcoliFLYCOP
#          >>avgfitness,sdfitness=coGrowth4EcoliFLYCOP_oneConf(0.25,0.25,0.25,0.25)

# Goal: individual test to improve consortium {4 E.coli auxotrophic for amino acids}
# Run through the function coGrowth4EcoliFLYCOP_oneConf
 
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
from cobra import Reaction

################################################################
### FUNCTION initialize_models #################################    
def initialize_models():
 # Only to run 1st time, to have the models!!
 if not(os.path.exists('ModelsInput/iAF1260.mat')):
     print('ERROR! Not iAF1260.mat files with GEM of consortium strains in ModelsInput!')
 else:    
  path=os.getcwd()
  os.chdir('ModelsInput')
  model=cobra.io.load_matlab_model('iAF1260.mat')
  # Create missing reaction in SteadyCom, and missing in iAF1260, for transporting methionine
  reaction=Reaction('METt3pp')
  reaction.name='L-methionine transport out via proton antiport (cytoplasm to periplasm)'
  reaction.lower_bound=0
  reaction.upper_bound=1000
  reaction.reversibility=False
  reaction.objective_coefficient=0
  reaction.gene_reaction_rule=''
  model.add_reaction(reaction)
  reaction.add_metabolites({'met-L[c]':-1.0, 'h[p]':-1.0, 'met-L[p]':1.0, 'h[c]':1.0})
  reaction.reaction='met-L[c] + h[p] --> met-L[p] + h[c]'
  del(reaction)

  # Define uptakes defined in SteadyCom
  #model.reactions.get_by_id('EX_glc(e)').bounds=(-8,1000) # Already in original model
  model.reactions.get_by_id('GLCtex').bounds=(-1000,8)
  #model.reactions.get_by_id('EX_o2(e)').bounds=(-18.5,1000) # Already in original model
  model.reactions.get_by_id('O2tex').bounds=(-1000,18.5)
  # To avoid stranges cycles intaking fe2 and secreting fe3. Although the important values are not affected. Just for not taking more oxygen than required.
  model.reactions.get_by_id('FEROpp').bounds=(0,0)
  # Save the basic model
  cobra.io.save_matlab_model(model,'iAF1260_cogrowth4Ecoli.mat','model')

  # Inactivate reactions and define amino-acids uptakes in individual models
  # Ec1: In: {met, lys}, Out:arg
  model=cobra.io.load_matlab_model('iAF1260_cogrowth4Ecoli.mat')
  model.reactions.get_by_id('DAPDC').bounds=(0,0)
  model.reactions.get_by_id('HSST').bounds=(0,0)
  model.reactions.get_by_id('PHEt2rpp').bounds=(0,0)
  model.reactions.get_by_id('EX_arg_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('ARGtex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_lys_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('LYStex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_met_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('METtex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_phe_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('PHEtex').bounds=(-1000,0)
  cobra.io.save_matlab_model(model,"iAF1260_Ec1.mat",'model')
  del(model)
  
  # Ec2: In: {arg, phe}, Out:lys
  model=cobra.io.load_matlab_model('iAF1260_cogrowth4Ecoli.mat')
  model.reactions.get_by_id('ARGSL').bounds=(0,0)
  model.reactions.get_by_id('PPNDH').bounds=(0,0)
  model.reactions.get_by_id('METt3pp').bounds=(0,0)
  model.reactions.get_by_id('EX_arg_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('ARGtex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_lys_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('LYStex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_met_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('METtex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_phe_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('PHEtex').bounds=(-1000,1)
  cobra.io.save_matlab_model(model,"iAF1260_Ec2.mat",'model')
  del(model)
  
  # Ec3: In: {arg, phe}, Out:met
  model=cobra.io.load_matlab_model('iAF1260_cogrowth4Ecoli.mat')
  model.reactions.get_by_id('ARGSL').bounds=(0,0)
  model.reactions.get_by_id('PPNDH').bounds=(0,0)
  model.reactions.get_by_id('LYSt3pp').bounds=(0,0)
  model.reactions.get_by_id('EX_arg_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('ARGtex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_lys_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('LYStex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_met_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('METtex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_phe_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('PHEtex').bounds=(-1000,1)
  cobra.io.save_matlab_model(model,"iAF1260_Ec3.mat",'model')
  del(model)

  # Ec4: In: {met, lys}, Out:phe
  model=cobra.io.load_matlab_model('iAF1260_cogrowth4Ecoli.mat')
  model.reactions.get_by_id('DAPDC').bounds=(0,0)
  model.reactions.get_by_id('HSST').bounds=(0,0)
  model.reactions.get_by_id('ARGt3pp').bounds=(0,0)
  model.reactions.get_by_id('EX_arg_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('ARGtex').bounds=(-1000,0)
  model.reactions.get_by_id('EX_lys_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('LYStex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_met_L(e)').bounds=(-1,1000)
  model.reactions.get_by_id('METtex').bounds=(-1000,1)
  model.reactions.get_by_id('EX_phe_L(e)').bounds=(0,1000)
  model.reactions.get_by_id('PHEtex').bounds=(-1000,0)
  cobra.io.save_matlab_model(model,"iAF1260_Ec4.mat",'model')
  del(model)
  #
  os.chdir(path)
# end-def
################################################################


################################################################    
### FUNCTION mat_to_comets #####################################    
# mat_to_comets(modelPath)
def mat_to_comets(matInputFile):
    model=cobra.io.load_matlab_model(matInputFile)
    # Open output file:
    with open(matInputFile+'.cmt', mode='w') as f:
        # Print the S matrix
        f.write("SMATRIX  "+str(len(model.metabolites))+"  "+str(len(model.reactions))+"\n")
        for x in range(len(model.metabolites)):
            for y in range(len(model.reactions)):
                if (model.metabolites[x] in model.reactions[y].metabolites):
                    coeff=model.reactions[y].get_coefficient(model.metabolites[x])
                    f.write("    "+str(x+1)+"   "+str(y+1)+"   "+str(coeff)+"\n")
        f.write("//\n")
        
        # Print the bounds
        f.write("BOUNDS  -1000  1000\n");
        for y in range(len(model.reactions)):
            lb=model.reactions[y].lower_bound
            up=model.reactions[y].upper_bound
            f.write("    "+str(y+1)+"   "+str(lb)+"   "+str(up)+"\n")
        f.write("//\n")
        
        # Print the objective reaction
        f.write('OBJECTIVE\n')
        for y in range(len(model.reactions)):
            if (model.reactions[y] in model.objective):
                indexObj=y+1
        f.write("    "+str(indexObj)+"\n")
        f.write("//\n")
        
        # Print metabolite names
        f.write("METABOLITE_NAMES\n")
        for x in range(len(model.metabolites)):
            f.write("    "+model.metabolites[x].id+"\n")
        f.write("//\n")

        # Print reaction names
        f.write("REACTION_NAMES\n")
        for y in range(len(model.reactions)):
            f.write("    "+model.reactions[y].id+"\n")
        f.write("//\n")

        # Print exchange reactions
        f.write("EXCHANGE_REACTIONS\n")
        for y in range(len(model.reactions)):
            if (model.reactions[y].id.find('EX_')==0):
                f.write(" "+str(y+1))
        f.write("\n//\n")                
### end-function-mat_to_comets    
################################################################


################################################################
### FUNCTION compute_ratioGR ###################################    
def compute_ratioGR(GRa,GRb):
    f1=0
    f2=0
    if(GRb != 0.0):
        f1=GRa/GRb
    if(GRa != 0.0):
        f2=GRb/GRa
    if(f1<f2):
        ratio=f1
    else:
        ratio=f2
    return ratio    
### end-function-compute_ratioGR
###############################################################


################################################################
### FUNCTION coGrowth4EcoliFLYCOP_oneConf ######################
def coGrowth4EcoliFLYCOP_oneConf(biomass1,biomass2,biomass3,biomass4,arg,lys,met,phe,fitFunc='ratioGRavgGR',dirPlot='',repeat=3):
  '''
  Call: avgFitness, sdFitness = coGrowth4Ecoli_oneConf(biomass1,biomass2,biomass3,biomass4,arg,lys,met,phe)

  INPUTS: biomass1: biomass of Ecoli Ec1, according to [Chan,2017]. In: {met, lys}, Out:arg
          biomass2: biomass of Ecoli Ec2, according to [Chan,2017]. In: {arg, phe}, Out:lys
          biomass3: biomass of Ecoli Ec3, according to [Chan,2017]. In: {arg, phe}, Out:met
          biomass4: biomass of Ecoli Ec4, according to [Chan,2017]. In: {met, lys}, Out:phe
          arg: rate of arginine to secrete by Ec1, as proportion of BOF flux.
          lys: rate of lysine to secrete by Ec2, as proportion of BOF flux.
          met: rate of metionine to secrete by Ec3, as proportion of BOF flux.
          phe: rate of phenilalanine to secrete by Ec4, as proportion of BOF flux.
          fitFunc: fitness function to optimize.
          dirPlot: copy of the graphs with several run results.
          repeat: number of runs with the same configuration.
  OUTPUT: avgFitness: average fitness of 'repeat' COMETS runs with the same configuration (due to it is not deterministic)
          sdFitness: standard deviation of fitness during 'repeat' COMETS runs (see above)
  '''

  if not(os.path.exists('ModelsInput/iAF1260_Ec1.mat')):
      initialize_models()

  title=str(biomass1)+'_'+str(biomass2)+'_'+str(biomass3)+'_'+str(biomass4)

  maxBiomass=2 # maximum to normalize increment in biomass in fitBiomass as part of fitness function.
  iniBiomass=0.1
  mass1=iniBiomass*biomass1
  mass2=iniBiomass*biomass2
  mass3=iniBiomass*biomass3
  mass4=iniBiomass*biomass4

  print("Fitness function:"+fitFunc)
  

  # Single GEMs parameter modifications
  # ===================================
  if not(os.path.exists('iAF1260_Ec1_tmp.mat.cmt')):      
    # 1.1.- [COBRApy] Establish modifications in model 1
    model=cobra.io.load_matlab_model('ModelsInput/iAF1260_Ec1.mat')
    # New: add the extracellular(e) metabolite to secrete to the right side of BOF rxn, and the same amount of intracellular(c) metabolite to the left side of BOF rxn.  Preserving open bounds in EX_* and *tex rxns.
    # [Harcombe, 2014] "A mutant S. enterica model was constructed that excreted methionine at a rate consistent with empirical observations. To achieve this, we added on the right side of the growth reaction 0.5 mmol/gDW of excreted extracellular methionine, balanced by an equal amount of intracellular methionine consumed (at the left side of the reaction equation)."
    idBOFrxn=list(model.objective.keys())[0].id
    coeff=arg
    # 'subtract_metabolite' adds a term with the metabolite coefficient with the given value*-1. So, on the right side you put -coeff (-*-1=+) and on the left side coeff (+*-1=-).
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('arg-L[c]'): coeff})
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('arg-L[e]'): -coeff})
    cobra.io.save_matlab_model(model,'iAF1260_Ec1_tmp.mat','model')
    del(model)      
    # 1.2.- [COBRApy] Establish modifications in model 2
    model=cobra.io.load_matlab_model('ModelsInput/iAF1260_Ec2.mat')
    idBOFrxn=list(model.objective.keys())[0].id
    coeff=lys
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('lys-L[c]'): coeff})
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('lys-L[e]'): -coeff})
    cobra.io.save_matlab_model(model,'iAF1260_Ec2_tmp.mat','model')
    del(model)      
    # 1.3.- [COBRApy] Establish modifications in model 3
    model=cobra.io.load_matlab_model('ModelsInput/iAF1260_Ec3.mat')
    idBOFrxn=list(model.objective.keys())[0].id
    coeff=met
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('met-L[c]'): coeff})
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('met-L[e]'): -coeff})
    cobra.io.save_matlab_model(model,'iAF1260_Ec3_tmp.mat','model')
    del(model)      
    # 1.4.- [COBRApy] Establish modifications in model 4
    model=cobra.io.load_matlab_model('ModelsInput/iAF1260_Ec4.mat')
    idBOFrxn=list(model.objective.keys())[0].id
    coeff=phe
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('phe-L[c]'): coeff})
    model.reactions.get_by_id(idBOFrxn).subtract_metabolites({model.metabolites.get_by_id('phe-L[e]'): -coeff})
    cobra.io.save_matlab_model(model,'iAF1260_Ec4_tmp.mat','model')
    del(model)      
    
    # 2.- [python]
    mat_to_comets('iAF1260_Ec1_tmp.mat')
    mat_to_comets('iAF1260_Ec2_tmp.mat')
    mat_to_comets('iAF1260_Ec3_tmp.mat')
    mat_to_comets('iAF1260_Ec4_tmp.mat')

    # Community parameter modifications
    # =================================    
    # 4.- [shell script] Write automatically the COMETS parameter about initial biomass of 4 strains, depending on proportions.
    massedit.edit_files(['coGrowth4Ecoli_layout_template.txt'],["re.sub(r'WWW','"+str(mass1)+"',line)"], dry_run=False)
    massedit.edit_files(['coGrowth4Ecoli_layout_template.txt'],["re.sub(r'XXX','"+str(mass2)+"',line)"], dry_run=False)
    massedit.edit_files(['coGrowth4Ecoli_layout_template.txt'],["re.sub(r'YYY','"+str(mass3)+"',line)"], dry_run=False)
    massedit.edit_files(['coGrowth4Ecoli_layout_template.txt'],["re.sub(r'ZZZ','"+str(mass4)+"',line)"], dry_run=False)

    
  # 5.- [COMETS by command line] Run COMETS
  # Compute no.rxn Growth Rate
  numRxnGR1=int(subprocess.check_output(['egrep -A1 "OBJECTIVE" iAF1260_Ec1_tmp.mat.cmt | tail -1 | tr -d \[:space:\]'], shell=True))
  numRxnGR2=int(subprocess.check_output(['egrep -A1 "OBJECTIVE" iAF1260_Ec2_tmp.mat.cmt | tail -1 | tr -d \[:space:\]'], shell=True))
  numRxnGR3=int(subprocess.check_output(['egrep -A1 "OBJECTIVE" iAF1260_Ec3_tmp.mat.cmt | tail -1 | tr -d \[:space:\]'], shell=True))
  numRxnGR4=int(subprocess.check_output(['egrep -A1 "OBJECTIVE" iAF1260_Ec4_tmp.mat.cmt | tail -1 | tr -d \[:space:\]'], shell=True))

  if not(os.path.exists('IndividualRunsResults')):
    os.makedirs('IndividualRunsResults')
  totfitness=0
  sumTotCycle=0
  sumAvgGR=0
  sumAvgRatioGR=0
  sumAvgFitBiomass=0
  sumGR1=0
  sumGR2=0
  sumGR3=0
  sumGR4=0
  fitnessList=[]
  # To repeat X times, due to random behaviour in COMETS:
  for i in range(repeat):
        with open("output.txt", "w") as f:
            subprocess.call(['./comets_scr','comets_script_template'], stdout=f)
    
        # 6.- [R call] Run script to generate one graph: 4 strains versus 4 aminoacids
        subprocess.call(['../../Scripts/plot_biomassX4_vs_4mediaItem.sh','template','arg-L','lys-L','met-L','phe-L','Ec1','Ec2','Ec3','Ec4'])
        subprocess.call(['../../Scripts/plot_biomassX4_vs_mediaItem.sh','template','glc-D','Ec1','Ec2','Ec3','Ec4'])
        # 7.- Compute fitness (measure to optimize):
        print('computing fitness...')
        # 7.1.- Determine endCycle:  When glc is exhausted
        with open("biomass_vs_glc-D_template.txt", "r") as sourcesGLC:
            linesGLC = sourcesGLC.readlines()
            endCycle=0
            for lineGLC in linesGLC:
                glcConc=float(lineGLC.split()[5])
                if (glcConc<0.001):
                    endCycle=int(lineGLC.split()[0])
                    break;
            if(endCycle==0):
                endCycle=int(lineGLC.split()[0])
        # Compute cycle of exponential grow
        expCycle=int(endCycle-1)
        iniExpCycle=int(0.85*endCycle)
        numCycles=int(expCycle-iniExpCycle)
        # 7.2.- Compute fitness elements
        finalBiomassV=linesGLC[expCycle].split()
        finalBiomass=float(finalBiomassV[1])+float(finalBiomassV[2])+float(finalBiomassV[3])+float(finalBiomassV[4])
        GR1=0
        GR2=0
        GR3=0
        GR4=0
        try:
            GR1=float(subprocess.check_output(['egrep "fluxes\{.*\}\{1\}\{1\}\{1\}" flux_log_template.txt | egrep -A'+str(numCycles)+' "fluxes\{"'+str(iniExpCycle)+'"\}\{1\}\{1\}\{1\}" | cut -d"=" -f2 | cut -d" " -f'+str(numRxnGR1+1)+' | awk \'{if($1>0){sum+=$1}} END {if(NR>0){print sum/NR}}\''], shell=True))
            if(GR1<0.0):
                GR1=0.0
        except:
            GR1=0.0
        try:
            GR2=float(subprocess.check_output(['egrep "fluxes\{.*\}\{1\}\{1\}\{2\}" flux_log_template.txt | egrep -A'+str(numCycles)+' "fluxes\{"'+str(iniExpCycle)+'"\}\{1\}\{1\}\{2\}" | cut -d"=" -f2 | cut -d" " -f'+str(numRxnGR2+1)+' | awk \'{if($1>0){sum+=$1}} END {if(NR>0){print sum/NR}}\''], shell=True))
            if(GR2<0.0):
                GR2=0.0
        except:
            GR2=0.0
        try:
            GR3=float(subprocess.check_output(['egrep "fluxes\{.*\}\{1\}\{1\}\{3\}" flux_log_template.txt | egrep -A'+str(numCycles)+' "fluxes\{"'+str(iniExpCycle)+'"\}\{1\}\{1\}\{3\}" | cut -d"=" -f2 | cut -d" " -f'+str(numRxnGR3+1)+' | awk \'{if($1>0){sum+=$1}} END {if(NR>0){print sum/NR}}\''], shell=True))
            if(GR3<0.0):
                GR3=0.0
        except:
            GR3=0.0
        try:
            GR4=float(subprocess.check_output(['egrep "fluxes\{.*\}\{1\}\{1\}\{4\}" flux_log_template.txt | egrep -A'+str(numCycles)+' "fluxes\{"'+str(iniExpCycle)+'"\}\{1\}\{1\}\{4\}" | cut -d"=" -f2 | cut -d" " -f'+str(numRxnGR4+1)+' | awk \'{if($1>0){sum+=$1}} END {if(NR>0){print sum/NR}}\''], shell=True))
            if(GR4<0.0):
                GR4=0.0
        except:
            GR4=0.0
                
        print("exp cycle range ("+str(iniExpCycle)+","+str(expCycle)+"): GR1: "+str(GR1)+" GR2: "+str(GR2)+" GR3: "+str(GR3)+" GR4: "+str(GR4))
        avgGR=float((GR1+GR2+GR3+GR4)/4)
        #
        sumRatioGR=0                
        sumRatioGR=sumRatioGR+compute_ratioGR(GR1,GR2)
        sumRatioGR=sumRatioGR+compute_ratioGR(GR1,GR3)
        sumRatioGR=sumRatioGR+compute_ratioGR(GR1,GR4)
        sumRatioGR=sumRatioGR+compute_ratioGR(GR2,GR3)
        sumRatioGR=sumRatioGR+compute_ratioGR(GR2,GR4)
        sumRatioGR=sumRatioGR+compute_ratioGR(GR3,GR4)
        ratioGR=float(sumRatioGR/6)
        #
        fitBiomass=float((finalBiomass-iniBiomass)/maxBiomass)

        if(fitFunc=='ratioGRavgGR'):
            fitness=float(0.5*ratioGR+0.5*avgGR)
        elif(fitFunc=='ratioGR'):
            fitness=ratioGR
        elif(fitFunc=='ratioGRratioBiomass'):
            fitness=float(0.5*ratioGR+0.5*fitBiomass)
        elif(fitFunc=='ratioGR40_Biomass60'):
            fitness=float(0.4*ratioGR+0.6*fitBiomass)
        elif(fitFunc=='ratioGR30_Biomass70'):
            fitness=float(0.3*ratioGR+0.7*fitBiomass)
        elif(fitFunc=='ratioGR20_Biomass80'):
            fitness=float(0.2*ratioGR+0.8*fitBiomass)
                        
        print(" Total fitness: "+str(round(fitness,6))+", avgGR: "+str(round(avgGR,6))+", ratioGR: "+str(round(ratioGR,6))+" in cycle "+str(iniExpCycle)+" to "+str(expCycle))

        totfitness=totfitness+fitness
        fitnessList.append(fitness)
        sumTotCycle=sumTotCycle+expCycle
        sumAvgGR=sumAvgGR+avgGR
        sumAvgRatioGR=sumAvgRatioGR+ratioGR
        sumAvgFitBiomass=sumAvgFitBiomass+fitBiomass
        sumGR1=sumGR1+GR1
        sumGR2=sumGR2+GR2
        sumGR3=sumGR3+GR3
        sumGR4=sumGR4+GR4
        
        # Copy individual solution
        file='IndividualRunsResults/'+'biomass_run'+str(i)+'_'+str(fitness)+'_'+str(expCycle)+'.pdf'
        shutil.move('biomass_vs_arg-L_lys-L_met-L_phe-L_template_plot.pdf',file)
        if(dirPlot != ''):
            file2=dirPlot+'biomass_'+str(biomass1)+'_'+str(biomass2)+'_'+str(biomass3)+'_'+str(biomass4)+'_'+str(arg)+'_'+str(lys)+'_'+str(met)+'_'+str(phe)+'_run'+str(i)+'_'+str(fitness)+'_'+str(expCycle)+'.pdf'
            shutil.copy(file,file2)
        file='IndividualRunsResults/'+'total_biomass_log_run'+str(i)+'.txt'
        shutil.move('total_biomass_log_template.txt',file)
        file='IndividualRunsResults/'+'media_log_run'+str(i)+'.txt'
        shutil.move('media_log_template.txt',file)
        file='IndividualRunsResults/'+'flux_log_run'+str(i)+'.txt'
        shutil.move('flux_log_template.txt',file)   
    
  avgfitness=totfitness/repeat
  sdfitness=statistics.stdev(fitnessList)
  avgAvgGR=sumAvgGR/repeat
  avgRatioGR=sumAvgRatioGR/repeat
  avgFitBiomass=sumAvgFitBiomass/repeat
  avgCycle=sumTotCycle/repeat
  avgGR1=sumGR1/repeat
  avgGR2=sumGR2/repeat
  avgGR3=sumGR3/repeat
  avgGR4=sumGR4/repeat
  
  print("Fitness_function\tconfiguration\tfitness\tsd\tavgGR\tratioGR\tfitBiomass\tGR1\tGR2\tGR3\tGR4\texpCycle")
  print(fitFunc+"\t"+str(biomass1)+','+str(biomass2)+','+str(biomass3)+','+str(biomass4)+','+str(arg)+','+str(lys)+','+str(met)+','+str(phe)+"\t"+str(round(avgfitness,6))+"\t"+str(round(sdfitness,6))+"\t"+str(round(avgAvgGR,6))+"\t"+str(round(avgRatioGR,6))+"\t"+str(round(avgFitBiomass,6))+"\t"+str(round(avgGR1,6))+"\t"+str(round(avgGR2,6))+"\t"+str(round(avgGR3,6))+"\t"+str(round(avgGR4,6))+"\t"+str(round(avgCycle,1)))
  with open(dirPlot+"configurationsResults"+fitFunc+".txt", "a") as myfile:
      myfile.write("Fitness_function\tconfiguration\tfitness\tsd\tavgGR\tratioGR\tfitBiomass\tGR1\tGR2\tGR3\tGR4\texpCycle\n")
      myfile.write(fitFunc+"\t"+str(biomass1)+','+str(biomass2)+','+str(biomass3)+','+str(biomass4)+','+str(arg)+','+str(lys)+','+str(met)+','+str(phe)+"\t"+str(round(avgfitness,6))+"\t"+str(round(sdfitness,6))+"\t"+str(round(avgAvgGR,6))+"\t"+str(round(avgRatioGR,6))+"\t"+str(round(avgFitBiomass,6))+"\t"+str(round(avgGR1,6))+"\t"+str(round(avgGR2,6))+"\t"+str(round(avgGR3,6))+"\t"+str(round(avgGR4,6))+"\t"+str(round(avgCycle,1))+"\n")
  
  print("Avg.fitness(sd):\t"+str(avgfitness)+"\t"+str(sdfitness)+"\n")
  if(sdfitness>0.1):
      avgfitness=0.0
  
  return avgfitness,sdfitness
# end-def coGrowth4EcoliFLYCOP_oneConf
################################################################






