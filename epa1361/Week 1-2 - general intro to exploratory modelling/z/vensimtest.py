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

    vensim_model = PysdModel(name= "PredPrey", mdl_file=r'../model/PredPrey.mdl')
    excel_model = ExcelModel(name="PredPrey", wd=r'../model/', model_file=r'../model/PredPrey.xlsx')
    netlogo_model = NetLogoModel(name="PredPrey", wd=r'../model/', model_file=r'../model/PredPrey.nlogo')

    models = [vensim_model, excel_model, netlogo_model]
    for model in models:
        model.uncertainties = uncertainties
        model.constants = constants
        model.outcomes = outcomes

    from ema_workbench import MultiprocessingEvaluator


    # results = pd.DataFrame()
    # for model in models:
    #     with MultiprocessingEvaluator(model) as evaluator:
    #         results = evaluator.perform_experiments(50)

    for model in models:
        with MultiprocessingEvaluator(vensim_model) as evaluator:
            results = evaluator.perform_experiments(50)

    print(results)
if __name__ == '__main__':
    main()