from ema_workbench import Scenario, Policy, MultiprocessingEvaluator, ema_logging, load_results
from ema_workbench.analysis import prim
from problem_formulation import get_model_for_problem_formulation
from ema_workbench.em_framework.evaluators import BaseEvaluator
from ema_workbench.em_framework.optimization import (HyperVolume,
                                                     EpsilonProgress)
import pandas as pd
import numpy as np
from ema_workbench.analysis import parcoords
import seaborn as sns

def get_cases(actor, n_scenarios=1000):
    """
    Obtain the cases used from optimisation
    """
    du_experiments, _ = load_results(
        "data/optimisation/du_scen_" + str(n_scenarios) + "_" + actor + ".tar.gz")

    cases_set = set()

    for policy in du_experiments.policy.unique():
        cases_set.add(' '.join(policy.split(' ')[1:-2]))

    cases = {}

    for i, case in enumerate(cases_set):
        cases[i] = case
    return cases

def get_opti_results(actor, n_scenarios=1000):
    """
    Obtain the optimisation results (paretto front) stored for a given actor
    """

    cases = get_cases(actor, n_scenarios)

    read_results = []

    for _, case in cases.items():
        temp = pd.read_csv("data/optimisation/" + actor + "/results_" + case + ".csv")
        temp_ = pd.read_csv("data/optimisation/" + actor + "/convergence_" + case + ".csv")
        read_results.append([temp, temp_])

    # opt_df = pd.DataFrame()
    #
    # for i, (result, convergence) in enumerate(read_results):
    #     opt_df = pd.concat([opt_df, result], axis=0)
    #
    # return opt_df

    return read_results

def get_opti_policies(actor, n_scenarios=1000):
    """
    Obtain paretto front policies
    """

    dike_model, _ = get_model_for_problem_formulation(actor)
    levers = [lever.name for lever in dike_model.levers]
    policies = []
    read_results = get_opti_results(actor, n_scenarios)
    cases = get_cases(actor, n_scenarios)

    for i, (result, _) in enumerate(read_results):
        result = result.loc[:, levers]
        # print(result)
        for j, row in result.iterrows():
            # print(f'scenario {cases[i]} option {j}')
            policy = Policy(f'scenario {cases[i]} option {j}', **row.to_dict())
            policies.append(policy)

    return policies

# EOF