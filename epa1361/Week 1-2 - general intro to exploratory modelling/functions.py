import numpy as np
import pandas as pd

def process_data(experiments, outcomes):
    policies = experiments['policy']
    for i, policy in enumerate(np.unique(policies)):
        experiments.loc[policies==policy, 'policy'] = str(i)

    data = pd.DataFrame(outcomes)
    data['policy'] = policies
    return data

def fix_format(dictionary):
    return {'prey': np.reshape(dictionary['prey'], (50, 1461))}