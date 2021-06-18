# EPA-simmodel

## Authors
| Name                | Student number| 
| ------------------- |:-------------:|
| Elias Bach          | 5379229       |
| Luka Janssens       | 5415268       |
| David Matheus       | 5242223       |
| Menghua Prisse      | 4454308       |
| Emily Ryan          | 5218713       |
| Lisette de Schipper | 5420296       |

## Introduction

This repository pertains the final assignment for EPA1361, a course from the EPA programme at TU Delft. This file outlines the file structure and how to use the model for flood risk management in the Netherlands.


## File structure

```
FabiosDecisions
│
└─── epa1361 <-- includes all the operational files needed to run the models
│    │
│    └───final assignment 
│    │   │ 
│    │   └─── data <-- contains the datafiles neccesary to run the model
│    │   │
│    │   └───results <-- contains the results of our analysis
│    │   │   └───scenario0.csv
│    │   │   └───scenario1.csv
│    │   │   └───scenario2.csv
│    │   │   └───scenario3.csv
│    │   │   └───scenario4.csv
│    │   │   └───simulation.csv
│    │   │   └───total_waiting_time.xlsx
│    │   └─── simulation <-- contains the results of our analysis
│    │   │   └─── generated
│    │   │   └─── optimisation
│    │   │   └─── sa
│    │   │   └─── selected
│    │   │   └─── synthesis
│    │   __init__.py
│    │   dike_model_function.py
│    │   dike_model_optimization.py
│    │   extra_trees.py
│    │   funs_dikes.py
│    │   funs_economy.py
│    │   funs_generate_network.py
│    │   funs_hydrostat.py
│    │   funs_project.py
│    │   gen_scen.py
│    │   opt_proc_deventer.ipynb
│    │   opt_proc_gorssel.ipynb
│    │   opt_proc_overijssel.ipynb
│    │   optimisation_deventer.ipynb
│    │   optimisation_gorssel.ipynb
└─── report   <-- includes all files necessary to compile report using LaTeX
│    └───chapters
│    └───figures
│    │    └───results
```

## Usage

### Problem formulation

The problem_formulation file contains the get_model_for_problem_formulation function that allows for easy access to the model, set with the uncertainties and levers for a selected actor (Gorssel, Deventer, or Overijssel).

### Scenario generation

For scenario generation open your terminal and cd to the final assignment folder
and type command 'python gen_scen.py' there are 2 optional parameters, the first being the actor of interest, and the
second the number of scenarios. Their default values are Gorssel and 5000 respectively.
If one were to generate 40 scenarios for Overijssel, one were to type: 'python gen_scen.py Overijssel 40' in the
terminal.

### Scenario selection

Scenario selection is done for every actor before optimisation. The optimisation_actorname notebooks select scenarios before running optimisation, based on a variety of outcomes. This process can also be informed with use of the scen_discovery_actorname notebooks.

### Optimisation

A set of preferred policies is found for every actor in the optimisation_actorname notebooks, where policies are found that perform well under the selected scenarios and then re-evaluated under deep uncertainty.

### Policy selection

A subset of the optimised policies is selected by processing the optimisation results in the opt_proc_actorname notebooks. A new file, called funs_project.py, where a few useful functions were stored, including crude_policy_selection, which performs this function. 

### Robustness analysis

The selected policies are then tested under satisficing and regret-based robustness metrics in the opt_proc_actorname notebooks. 

### Sensitivity analysis or uncertainty analysis

We evaluate the sensitivity of the different outcomes of interests for every actor to the uncertainty ranges in the model, with the selected subset of policies. This is done with feature scoring in the extra_trees.py file. To use it, you need to  open your terminal and cd to the final assignment folder and type command 'python extra_trees.py' there are 2 optional parameters, the first being the actor of interest, and the second the number of scenarios. If one were to perform the analysis for 100 scenarios for Overijssel, one were to type: 'python extra_trees.py Overijssel 100' in the terminal.

### Re-evaluate with other formulations

To evaluate the feasibility of an actor proposing a policy to other actors, the synthesis.py was generated, which evaluates the performance of policies from one actor in terms of the outcomes of interest of the other actors. The outcome of this is then processed in the Outcome_spread_plots notebook to produce visualisations useful for analysis.

**Note: actorname in file names stands for the uncapitalised name of the actor**

