from problem_formulation import get_model_for_problem_formulation
from ema_workbench import MultiprocessingEvaluator, Policy, save_results
from ema_workbench.em_framework.evaluators import LHS
from datetime import datetime
import pandas as pd

def run():
    '''
    Check the policies for other actors
    '''
    n_scen=10000
    dike_model, planning_steps = get_model_for_problem_formulation("Gorssel")

    D_policies = pd.read_csv("simulation/selected/selected_policies_Deventer.csv")
    O_policies = pd.read_csv("simulation/selected/selected_policies_Overijssel.csv")

    D_policies["A.5_DikeIncrease 0"] = 0
    D_policies["A.5_DikeIncrease 1"] = 0
    D_policies["A.5_DikeIncrease 2"] = 0

    policies = []

    actors = {"Deventer": D_policies,
              "Overijssel": O_policies}

    for actor, levers in actors.items():
        for _, row in levers.iterrows():
            policy = Policy(f'Policy {actor} {row.name}', **row.to_dict())
            policies.append(policy)

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.perform_experiments(scenarios=n_scen, policies=policies, uncertainty_sampling=LHS)

    save_results(results, "simulation/synthesis/synthesis_Gorssel_"+ str(n_scen) + "_"+str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S") +".tar.gz"))
    print("Done!")

    dike_model, planning_steps = get_model_for_problem_formulation("Overijssel")

    G_policies = pd.read_csv("simulation/selected/selected_policies_Gorssel.csv")

    policies= []
    for _, row in G_policies.iterrows():
        policy = Policy(f'Policy Gorssel {row.name}', **row.to_dict())
        policies.append(policy)

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.perform_experiments(scenarios=n_scen, policies=policies, uncertainty_sampling=LHS)

    save_results(results, "simulation/synthesis/synthesis_Overijssel_"+ str(n_scen) + "_" + str(
        datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz"))
    print("Done!")

    return

if __name__ == '__main__':

    run()