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
import pandas as pd
import random
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
rds = 80
v = 10
m = 100
n_u = 100
n_o = 50
t = 10000
dr = 1
n_l = 0

params = {
    # 'n_l': [0],
    # 'dr': [1],
    'p': [0.2, 0.5, 1],
    'k': [0, 5, 10],
    'dele_size': [5, 10, 20, 50],
    'dele_duration': [1, 5, 10, 20, 50]
}

vote_df = pd.DataFrame()
dele_df = pd.DataFrame()
perf_df = pd.DataFrame()
part_df = pd.DataFrame()
infl_df = pd.DataFrame()
gini_df = pd.DataFrame()

for config in param_grid(params):
    #n_l = config.get('n_l')
    #dr = config.get('dr')
    k = config.get('k')
    p = config.get('p')
    dele_size = config.get('dele_size')
    dele_duration = config.get('dele_duration')

    method = get_vote_method(n_l)

    # Initiate Reality
    reality = generate_reality(m)

    # Initiate Organizations
    organizations = generate_organizations(m, reality, n_o)

    # Initiate Organization
    users, leaders = generate_users(
        reality, organizations, n_u, n_l, m, k, p, t, dr)

    # Run Simulation - method: "random" or "leader"
    votes, delegations, participations, performances, influencers, ginis = run_model(
        reality, organizations, users, leaders, method, rds, v, dele_size, dele_duration)

    # Mean Results
    mean_votes = mean_result(votes)
    mean_deles = mean_result(delegations)
    mean_perfs = mean_result(performances)
    mean_parts = mean_result(participations)
    mean_ginis = mean_result(ginis)
    mean_infls = mean_influencers(influencers, n_o, rds, v, c_index=0.05)

    dele_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_deles)
    vote_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_votes)
    perf_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_perfs)
    part_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_parts)
    gini_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_ginis)
    infl_df['p={}, k={}, size={}, dur={}'.format(
        p, k, dele_size, dele_duration)] = pd.Series(mean_infls)

vote_df.to_csv('result/vote.csv')
dele_df.to_csv('result/dele.csv')
perf_df.to_csv('result/perf.csv')
part_df.to_csv('result/part.csv')
infl_df.to_csv('result/infl.csv')
gini_df.to_csv('result/gini.csv')

# %%
