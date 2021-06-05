from problem_formulation import get_model_for_problem_formulation
from ema_workbench import MultiprocessingEvaluator, SequentialEvaluator, Policy
from ema_workbench.em_framework.evaluators import LHS
from datetime import datetime
import sys

def run(actor="Gorssel", n=5000):
    '''
    Run the program to generate_scen for actor
    '''
    dike_model, planning_steps = get_model_for_problem_formulation(actor)

    #0-policy

    zero_policy = {'DaysToThreat': 0}
    zero_policy.update({'DikeIncrease {}'.format(n): 0 for n in planning_steps})
    zero_policy.update({'RfR {}'.format(n): 0 for n in planning_steps})
    pol0 = {}

    for key in dike_model.levers:
        s1, s2 = key.name.split('_')
        pol0.update({key.name: zero_policy[s2]})

    policy0 = Policy('Policy 0', **pol0)

    with SequentialEvaluator(dike_model) as evaluator:
        experiments, results = evaluator.perform_experiments(scenarios=n, policies=policy0, uncertainty_sampling=LHS)

    for result in results:
        experiments[result] = results[result]

    experiments.to_csv("data/generated/genscen_"+actor+'_'+str(n)+'_'+str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")), index=False)
    print("Done!")

if __name__ == '__main__':
    actor = str(sys.argv[1])
    if actor not in ["Overijssel", "Gorssel", "Deventer"]:
        print("Lol, u dyslectic?")
        exit()
    if not sys.argv[2].isnumeric():
        print("Remember primary?")
        exit()
    n = int(sys.argv[2])
    run(actor, n)