# EPA-simmodel

For data_generation open your terminal and cd to the final assignment folder
and type command 'python gen_scen.py' there are 2 optional parameters, the first being the actor of interest, and the
second the number of scenarios. Their default values are Gorssel and 5000 respectively.
If one were to generate 40 scenarios for Overijssel, one were to type: 'python gen_scen.py Overijssel 40' in the
terminal.

# Authors
| Name                | Student number| 
| ------------------- |:-------------:|
| Elias Bach          | 5379229       |
| Luka Janssens       | 5415268       |
| David Matheus       | 5242223       |
| Menghua Prisse      | 4454308       |
| Emily Ryan          | 5218713       |
| Lisette de Schipper | 5420296       |

## Introduction
BLABLA

## File structure

```
epa1361 
│
└───final assignment 
│   │ 
│   └─── data <-- contains the datafiles neccesary to run the model
│   │
│   └───results <-- contains the results of our analysis
│   │   │   scenario0.csv
│   │   │   scenario1.csv
│   │   │   scenario2.csv
│   │   │   scenario3.csv
│   │   │   scenario4.csv
│   │   │   simulation.csv
│   │   │   total_waiting_time.xlsx
│   └─── simulation <-- contains the results of our analysis
│   │   └─── generated
│   │   └─── optimisation
│   │   └─── sa
│   │   └─── selected
│   │   └─── synthesis
│   __init__.py
│   dike_model_function.py
│   dike_model_optimization.py
│   extra_trees.py
│   funs_dikes.py
│   funs_economy.py
│   funs_generate_network.py
│   funs_hydrostat.py
│   funs_project.py
│   gen_scen.py
│   opt_proc_deventer.ipynb
│   opt_proc_gorssel.ipynb
│   opt_proc_overijssel.ipynb
│   optimisation_deventer.ipynb
│   optimisation_gorssel.ipynb
│   
│   
```

## Usage