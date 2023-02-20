# %%
# Import Classes and Functions
from functions.others import *
from functions.runner import *
from functions.generators import *
from classes.User import *
from classes.Organization import *
from classes.Reality import *
# Import Libraries
import numpy as np
import random
import matplotlib.pyplot as plt
np.set_printoptions(4)
random.seed(101)


"""
Variables
- rds: rounds
- v: number of votes in each round
- m : number of attributes
- n_u : number of users
- n_o : number of organizations
- n_l: number of leaders
- k : degree of interdependence
- p : participation rate
- t : total number of tokens
- dr: distribution rate of tokens



"""
# Setting Variables

params = {
    'n_l': [0],
    'dr': [0],
    'p': [1],
    'k': [0, 5, 10],
    'rds': [80],
    'v': [10],
    'm': [100],
    'n_u': [100],
    'n_o': [50],
    't': [10000],
}

for config in param_grid(params):
    rds = config.get('rds')
    v = config.get('v')
    m = config.get('m')
    t = config.get('t')
    n_u = config.get('n_u')
    n_o = config.get('n_o')
    n_l = config.get('n_l')
    dr = config.get('dr')
    k = config.get('k')
    p = config.get('p')

    """
    if __name__ == "__main__":
        rds = 80
        v = 10
        m = 100
        n_u = 100
        n_o = 50
        k = 0
        t = 10000
        p = 0.2
        dr = 0.2
        n_l = 10
    """
    method = get_vote_method(n_l)

    # Initiate Reality
    reality = generate_reality(m)

    # Initiate Organizations
    organizations = generate_organizations(m, reality, n_o)

    # Initiate Organization
    users, leaders = generate_users(
        reality, organizations, n_u, n_l, m, k, p, t, dr)

    # Run Simulation - method: "random" or "leader"
    votes, delegations, participations, knowledges, performances, influencers, ginis = run_model(
        reality, organizations, users, leaders, method, rds, v)

    # Mean Results
    mean_votes = mean_result(votes)
    mean_deles = mean_result(delegations)
    mean_knows = mean_result(knowledges)
    mean_perfs = mean_result(performances)
    mean_parts = mean_result(participations)
    mean_ginis = mean_result(ginis)
    mean_infls = mean_influencers(influencers, n_o, rds, v, c_index=0.05)

    # Plot Results
    plot_vote_dele_result(mean_votes, mean_deles, n_u, dr, n_l, p, k)
    plot_know_perf_result(mean_knows, mean_perfs, dr, n_l, p, k)
    plot_part_res(mean_parts, n_u, dr, n_l, p, k)
    plot_gini_res(mean_ginis, dr, n_l, p, k)
    plot_infl_res(mean_infls, dr, n_l, p, k)

   # %%
