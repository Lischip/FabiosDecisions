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


def opti_results(actor, cases={0: "best", 1: "low", 2: "middle", 3: "high", 4: "worst deaths", 5: "absolute worst"}):
    """
    Obtain the optimisation results stored for a given actor
    """

    read_results = []

    for _, case in cases.items():
        temp = pd.read_csv("simulation/optimisation/" + actor + "/results_" + case + ".csv")
        temp_ = pd.read_csv("simulation/optimisation/" + actor + "/convergence_" + case + ".csv")
        read_results.append([temp, temp_])

        opt_df = pd.DataFrame()

        for i, (result, convergence) in enumerate(read_results):
            opt_df = pd.concat([opt_df, result], axis=0)

    return opt_df

# Other functions? Don't get what Lisette meant

# EOF
