# FLYCOP

---
title: "FLYCOP"
author: "Beatriz García-Jiménez"
date: "April, 2018"
---

FLYCOP (FLexible sYnthetic Consortium OPtimization) is a framework that improves the understanding of the metabolic behaviour of microbial consortia and to automatize the modeling of those communities, by designing and optimizing enginered microbial consortia given a particular goal.

FLYCOP contributes with multiple and assorted applications, such as simulating different scenarios before in-vivo experiments; defining medium composition and detecting limiting nutrients; discovering the biological metric optimized in an evolutionary process; optimizing cross-feeding relationships; optimizing strain ratios in the consortium; etc.

This repository contains the code and configuration files reproducing the study cases described in:

_**FLYCOP: metabolic modeling-based analysis and engineering microbial communities.**_
Beatriz García-Jiménez, José Luis García and Juan Nogales (2018) *(Submitted)* 

So far, FLYCOP has been applied to design and optimize 3 different microbial consortia:

* Co-growth 4 auxotrophic *E. coli* [*coGrowth4Ecoli*]  
* Describing microbial community evolution, in *E. coli* polimorphism [*ecoliLongTerm*]  
* *S. elongatus-P. putida* synthetic consortium producing bio-plastic (polyhydroxyalkanoate, PHA)  [*synKtPHA*]   


***
### Pre-requisites
FLYCOP pipeline uses some software, which must be installed before:

* [COBRApy](https://opencobra.github.io/cobrapy/): python package (checked with v0.5.11)  
* [COMETS](http://www.bu.edu/segrelab/comets/) (v2.0.3) (faster with gurobi solver)  
* [SMAC](http://www.cs.ubc.ca/labs/beta/Projects/SMAC/) (in Java, v2.10.03)   
Additionally, [R software](https://www.r-project.org/) is required.

FLYCOP is an under development software, to run LINUX OS.


***
### Input and output description

After required software installation, you can run FLYCOP for the 3 microbial consortia where FLYCOP was applied with the files provided in this site.
If you want to apply FLYCOP to design and optimize a new consortium, you could take as template the available files from one of the optimized consortia, and then to code the following required inputs to FLYCOP, described here:

####  *INPUT:*
  
  1. **FLYCOP pipeline _ad-hoc_ for a specific microbial consortium** [consortiumPrefixFLYCOP.py]: it means a python script to run a single configuration, including how to: 1) dynamically update single models and community parameters depending on the parametrized consortium configuration, 2) simulate that configured consortium in a dynamic way, and 3) evaluate the quality of the given consortium using a fitness function. This file also must include the method *initialize_models()* to update the original single strain genome scale metabolic models (GEMs) to use as base in the consortium optimization.
  2. **ConsortiumPrefix_TemplateFolder** [ConsortiumPrefix_TemplateOptimizeConsortiumV\<A>]: a directory including a layout file with the culture medium definition, the original GEMs (in matlab format) and the consortium simulation configuration.
  3. **Optimization configuration** [consortiumPrefix_confFLYCOP_scenario_v\<Y>.txt]: it defines the number of consortium configurations to evaluate (numberOfRunsLimit) and identifies the two files describing the consortium optimization:  
    + **Parameter values** [consortiumPrefix_confFLYCOP_params_v\<Z>.pcs]: it lists the range of values per parameter (in SMAC format), among those to choose by the Stochastic Local Search procedure.  
    + **Wrapper file** [consortiumPrefix_wrapperFLYCOP_v\<Y>.py]: to select the fitness function to optimize, to define the 'version identifier' for all results files, and to call the FLYCOP pipeline.  
  
"ConsortiumPrefix_TemplateFolder" must be located in *MicrobialCommunities/* directory, and the remaining input files in *Scripts/* directory.

##### Genome-scale models

GEMs used by FLYCOP cases of study can be obtained from [BiGG models database](http://bigg.ucsd.edu/) or from their respective publications (in matlab format):  

* iAF1260 [[Feist et al., 2007]](https://doi.org/10.1038/msb4100155)  
* iJO1366 [[Orth et al.,2011]](https://doi.org/10.1038/msb.2011.65)  
* iJB785 [[Broddrick et al.,2016]](https://doi.org/10.1073/pnas.1613446113)  
* iJN1411  [[Nogales et al.,2017]](https://doi.org/10.1101/139121)  


####  *OUTPUT:*  
FLYCOP provides different resources for robustness, sensitivity and data analysis support, being the most relevant the following ones:  

* Best configuration given the strains, media, fitness function and parameter configuration  
* Scatterplot showing explored values by each parameter  
* Correlation values and ellipse plots between different parameter and fitness values 
* Tab file with all configurations including parameter and fitness values, and some other interesting metrics (such as medium concentration of some relevant metabolites). This output would be important for further data analysis.  
* Growth curves of all explored consortium configurations  

***
### Running FLYCOP
After defining the required files for a specific microbial consortium design (see INPUT section below), you can search the best configuration with FLYCOP. This call includes an automatic data analysis of the resulting evaluated multiple consortium configurations.
```{sh eval=FALSE}
sh FLYCOP.sh <consortiumPrefix> <Y> V<A> <fitnessFunction> <numberOfConfigurations>
```
For example (for a short run with only 10 configurations):
```{sh eval=FALSE}
sh FLYCOP.sh 'ecoliLongTerm' 2 V0 'Yield' 10
```

Also, a particular consortium configuration can be simulated with:
```{sh eval=FALSE}
cd MicrobialCommunities
cp -p -R ConsortiumPrefix_TemplateOptimizeConsortiumV<A> ConsortiumPrefix_Test<Y>
cd ConsortiumPrefix_Test<Y>
python3 ../../Scripts/consortiumPrefix_individualTestFLYCOP.py <arg1> ... <argN>
```
where:

* *consortiumPrefix* could take value in {*synKtPHA*, *coGrowth4Ecoli*, *ecoliLongTerm*} for the already 3 FLYCOP designed consortia
* *\<arg1> ... \<argN>* represents the user-given configuration values for this particular consortium which is going to be simulated and evaluated.  

For example:
```{sh eval=FALSE}
cd MicrobialCommunities
cp -p -R ecoliLongTerm_TemplateOptimizeConsortiumV0 ecoliLongTerm_Test2
cd ecoliLongTerm_Test2
python3 ../../Scripts/ecoliLongTerm_individualTestFLYCOP.py -10 -16 -11 -12 -6 -16 'Yield'
```

Several exploratory individual consortium simulations are recommended before running the complete FLYCOP pipeline.

***
### Runtime

An individual configuration takes some minutes. However, a complete FLYCOP run usually take several hours, depending on several parameters. The main one is the number of different consortium configurations to evaluate, defined in 'consortiumPrefix_confFLYCOP_scenario_v\<Y>.txt'. For 500 configurations, FLYCOP usually takes around 10-12 hours in a 16GB RAM computer. Other parameters with less influence on runtime are the number of cycles over the consortium configuration is simulated (defined in ConsortiumPrefix_TemplateOptimizeConsortiumV\<A>/consortiumPrefix_layout_template.txt).

***

