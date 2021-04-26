def main():
    import numpy as np
    import matplotlib.pyplot as plt

    from ema_workbench import (Model, RealParameter, TimeSeriesOutcome, perform_experiments,
                               ema_logging)

    from ema_workbench.connectors.netlogo import NetLogoModel
    from ema_workbench.connectors.excel import ExcelModel
    from ema_workbench.connectors.pysd_connector import PysdModel

    from ema_workbench.em_framework.evaluators import LHS, SOBOL, MORRIS

    from ema_workbench.analysis.plotting import lines, Density


    def PredPrey(prey_birth_rate=0.025, predation_rate=0.0015, predator_efficiency=0.002,
                 predator_loss_rate=0.06, initial_prey=50, initial_predators=20, dt=0.25, final_time=365, reps=1):
        # Initial values
        predators, prey, sim_time = [np.zeros((reps, int(final_time / dt) + 1)) for _ in range(3)]

        for r in range(reps):
            predators[r, 0] = initial_predators
            prey[r, 0] = initial_prey

            # Calculate the time series
            for t in range(0, sim_time.shape[1] - 1):
                dx = (prey_birth_rate * prey[r, t]) - (predation_rate * prey[r, t] * predators[r, t])
                dy = (predator_efficiency * predators[r, t] * prey[r, t]) - (predator_loss_rate * predators[r, t])

                prey[r, t + 1] = max(prey[r, t] + dx * dt, 0)
                predators[r, t + 1] = max(predators[r, t] + dy * dt, 0)
                sim_time[r, t + 1] = (t + 1) * dt

        # Return outcomes
        return {'TIME': sim_time,
                'predators': predators,
                'prey': prey}

    from ema_workbench import Model, RealParameter, ScalarOutcome, Constant

    uncertainties = [RealParameter('prey_birth_rate', 0.015, 0.035),
                           RealParameter('predation_rate', 0.0005, 0.003),
                           RealParameter('predator_efficiency', 0.001, 0.004),
                          RealParameter('predator_loss_rate', 0.04, 0.08)]

    constants = [Constant('Final Time', 365),
                      Constant('Time step', 0.25)]

    outcomes = [TimeSeriesOutcome('TIME'),
                      TimeSeriesOutcome('predators'),
                      TimeSeriesOutcome('prey')]

    constants2 = [Constant('dt', 0.25)]

    constants3 = [Constant('final_time', 365),
                  Constant('dt', 0.25)]

    #vensim_model = PysdModel(name= "Vensim", mdl_file=r'../model/PredPrey.mdl')
    excel_model = ExcelModel(name="Excel", wd='../model/', model_file='../model/PredPrey.xlsx', default_sheet="Sheet1")

    netlogo_model = NetLogoModel(name="Netlogo", wd=r'../model/', model_file=r'../model/PredPrey.nlogo')
    netlogo_model.run_length = 365
    netlogo_model.replications = 1

    # vensim_model.uncertainties = uncertainties
    # vensim_model.constants = constants
    # vensim_model.outcomes = outcomes

    excel_model.uncertainties = uncertainties
    excel_model.constants = constants2
    excel_model.outcomes = outcomes

    netlogo_model.uncertainties = uncertainties
    netlogo_model.constants = constants2
    netlogo_model.outcomes = outcomes

    import sys
    sys.path.insert(0, '../model/')
    import PredPreyCode as PP

    py_model = Model('Py', function=PP.PredPrey)

    py_model.uncertainties = uncertainties
    py_model.constants = constants3
    py_model.outcomes = outcomes

    #models = [vensim_model, excel_model, netlogo_model]

    from ema_workbench import MultiprocessingEvaluator, SequentialEvaluator
    import pandas as pd
    with MultiprocessingEvaluator(excel_model) as evaluator:
    #with SequentialEvaluator(excel_model) as evaluator:
        temp = evaluator.perform_experiments(scenarios=50, reporting_interval=1)
    #
    # results = pd.DataFrame()
#     for model in models:
#         with MultiprocessingEvaluator(model) as evaluator:
#             temp = evaluator.perform_experiments(50)
#             temp = pd.DataFrame.from_records(temp)
#             temp = temp.iloc[:1]
#             results = pd.concat([results, temp])
    #print(results)

    print(temp)
if __name__ == '__main__':
    main()