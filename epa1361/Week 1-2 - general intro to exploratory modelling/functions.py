import numpy as np
import pandas as pd

def process_data(experiments, outcomes):
    policies = experiments['policy']
    for i, policy in enumerate(np.unique(policies)):
        experiments.loc[policies==policy, 'policy'] = str(i)

    data = pd.DataFrame(outcomes)
    data['policy'] = policies
    return data

def process_data2(experiments, outcomes):
    df = pd.DataFrame.from_dict(outcomes)
    df = df.assign(policy=experiments['policy'])
    df['policy'] = df['policy'].map({p: i for i, p in enumerate(set(experiments['policy']))})
    return df