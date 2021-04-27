from ema_workbench import Model, RealParameter, ScalarOutcome
import zlakemodel_function as lmf

def main():
    model = Model('Lakemodel', function=lmf.lake_problem)

    model.uncertainties = [RealParameter('mean', 0.01, 0.5),
                           RealParameter('stdev', 0.001, 0.005),
                           RealParameter('b', 0.1, 0.45),
                           RealParameter('q', 2, 4.5),
                           RealParameter('delta', 0.93, 0.99)]

    model.levers = [RealParameter("l" + str(number),0,0.1) for number in range(0,100)]

    model.outcomes = [ScalarOutcome('max_P'),
                      ScalarOutcome('utility'),
                      ScalarOutcome('intertia'),
                      ScalarOutcome('reliability')]

    from ema_workbench import (MultiprocessingEvaluator, ema_logging,
                               perform_experiments)
    ema_logging.log_to_stderr(ema_logging.INFO)

    with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
        experiments, outcomes = evaluator.perform_experiments(scenarios=1000, policies=4)

if __name__ == '__main__':
    main()