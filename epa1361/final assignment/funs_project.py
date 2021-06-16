from ema_workbench import Scenario, Policy, MultiprocessingEvaluator, ema_logging, load_results
from problem_formulation import get_model_for_problem_formulation
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing

gcases = {0: "best", 1: "low", 2: "middle", 3: "high", 4: "worst deaths", 5: "absolute worst"}
ocases = {0: "best", 1: "low", 2: "middle", 3: "high", 4: "worst deaths", 5: "absolute worst"}
dcases = {0: "best", 1: "low", 2: "middle", 3: "high", 4: "absolute worst", 5: "worst damage"}


n_overijssel = 1.16e6
n_deventer = 100719
n_lochem = 33590

thresholds_overijssel = {'Gorssel and Deventer Expected Annual Damage': 1.53e6,
                         'Gorssel and Deventer Expected Number of Deaths': (1e-5*n_overijssel),
                         'Gorssel and Deventer Total Costs': 1.53e7}
thresholds_deventer = {'Deventer Expected Annual Damage': 1.1e6,
                       'Deventer Expected Number of Deaths': (1e-5*n_deventer),
                       'Deventer Total Costs': 1.1e7}
thresholds_gorssel = {'Gorssel Expected Annual Damage': 5.4e5,
                      'Gorssel Expected Number of Deaths': (1e-5*n_lochem),
                      'Gorssel Total Costs': 5.4e6}

def the_cases(actor):
    if actor == "Overijssel":
        return ocases
    elif actor == "Gorssel":
        return gcases
    elif actor == "Deventer":
        return dcases
    else:
        print("Error")
        return 0

def crude_policy_selection(actor, clusters):
    """"
    make a crude policy selection by clustering the dataframe, normalising each cluster, and selecting the policies
    with the worst sum over each row.
    """
    # read in results from optimisation
    results = []

    for _, case in the_cases(actor).items():
        temp = pd.read_csv("simulation/optimisation/" + actor + "/results_" + case + ".csv")
        temp_ = pd.read_csv("simulation/optimisation/" + actor + "/convergence_" + case + ".csv")
        results.append([temp, temp_])

    # collapse in 1 dataframe
    opt_df = pd.DataFrame()
    for i, (result, convergence) in enumerate(results):
        result["scenario"] = i
        opt_df = pd.concat([opt_df, result], axis=0)

    # clean up
    opt_df.reset_index(inplace=True, drop=True)
    opt_df.drop_duplicates(inplace=True)

    # select policies + add scenario back
    policies = opt_df.iloc[:, :-4]
    policies = pd.concat([policies, opt_df["scenario"]], axis=1)

    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(policies.iloc[:, :-1])

    # get all policies in each cluster
    policies['cluster'] = kmeans.labels_
    groups = policies.groupby(by="cluster")
    groups = groups.obj.sort_values("cluster", ascending=True)

    # assign values to each policy in each  cluster
    groups["value"] = 0
    for i in range(clusters):
        group = groups.loc[groups["cluster"] == i]
        group = group.iloc[:, :-3]
        scaler = preprocessing.MinMaxScaler().fit(group)
        data_scaled = scaler.transform(group)
        groups.at[group.index.values, 'value'] = data_scaled.sum(axis=1)

    # get the most extreme two per cluster
    idx = []
    for cluster in range(clusters):
        idx.extend(groups.loc[groups["cluster"] == cluster].sort_values(by="value", ascending=False)[:2].index.values.tolist())

    return opt_df.iloc[idx]

def get_cases(actor, n_scenarios=1000):
    """
    Obtain the cases used from optimisation
    """
    du_experiments, _ = load_results(
        "simulation/optimisation/du_scen_" + str(n_scenarios) + "_" + actor + ".tar.gz")

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
        temp = pd.read_csv("simulation/optimisation/" + actor + "/results_" + case + ".csv")
        temp_ = pd.read_csv("simulation/optimisation/" + actor + "/convergence_" + case + ".csv")
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

def get_selected_policies(actor):
    """
    Obtain narrowed down policies selected for a specific actor
    """
    dike_model, _ = get_model_for_problem_formulation(actor)
    levers = [lever.name for lever in dike_model.levers]
    policies_df = pd.read_csv('simulation/selected/selected_policies_' + actor + '.csv')
    policies_df = policies_df.loc[:, levers]
    policies = []

    for i, row in policies_df.iterrows():
        policy = Policy(f'Policy {i}', **row.to_dict())
        policies.append(policy)

    return policies

# EOF
