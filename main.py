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

rds = 80
v = 10
m = 100
n_u = 100
n_o = 50
t = 10000

params = {
    'n_l': [0, 10],
    'dr': [1, 0.2],
    'p': [1, 0.5, 0.2],
    'k': [0, 5, 10]
}

vote_df_fn = pd.DataFrame()
dele_df_fn = pd.DataFrame()
perf_df_fn = pd.DataFrame()
nperf_df_fn = pd.DataFrame()
part_df_fn = pd.DataFrame()
infl_df_fn = pd.DataFrame()
gini_df_fn = pd.DataFrame()

for config in param_grid(params):
    n_l = config.get('n_l')
    dr = config.get('dr')
    k = config.get('k')
    p = config.get('p')

    method = get_vote_method(n_l)

    # Initiate Reality
    reality = generate_reality(m)

    # Initiate Organizations
    organizations = generate_organizations(m, reality, n_o)

    # Initiate Organization
    users, leaders = generate_users(
        reality, organizations, n_u, n_l, m, k, p, t, dr)

    # Run Simulation - method: "random" or "leader"
    votes, delegations, participations, new_performances, performances, influencers, ginis = run_model(
        reality, organizations, users, leaders, method, rds, v)

    # Mean Results
    mean_votes = mean_result(votes)
    mean_deles = mean_result(delegations)
    mean_perfs = mean_result(performances)
    mean_nperfs = mean_result(new_performances)
    mean_parts = mean_result(participations)
    mean_ginis = mean_result(ginis)
    mean_infls = mean_influencers(influencers, n_o, rds, v, c_index=0.05)

    vote_df = pd.DataFrame(mean_votes)
    dele_df = pd.DataFrame(mean_deles)
    perf_df = pd.DataFrame(mean_perfs)
    nperf_df = pd.DataFrame(mean_nperfs)
    part_df = pd.DataFrame(mean_parts)
    infl_df = pd.DataFrame(mean_infls)
    gini_df = pd.DataFrame(mean_ginis)

    df_list = [vote_df, dele_df, perf_df, nperf_df, part_df, infl_df, gini_df]
    for df in df_list:
        df['n_l'] = n_l
        df['dr'] = dr
        df['p'] = p
        df['k'] = k

    """
    # Plot Results
    plot_vote_dele_result(mean_votes, mean_deles, n_u, dr, n_l, p, k)
    plot_perf_result(mean_perfs, dr, n_l, p, k)
    plot_part_res(mean_parts, n_u, dr, n_l, p, k)
    plot_gini_res(mean_ginis, dr, n_l, p, k)
    plot_infl_res(mean_infls, dr, n_l, p, k)
    """
    vote_df_fn = vote_df_fn.append(vote_df)
    dele_df_fn = dele_df_fn.append(dele_df)
    perf_df_fn = perf_df_fn.append(perf_df)
    nperf_df_fn = nperf_df_fn.append(nperf_df)
    part_df_fn = part_df_fn.append(part_df)
    infl_df_fn = infl_df_fn.append(infl_df)
    gini_df_fn = gini_df_fn.append(gini_df)

vote_df_fn.to_csv('result/vote.csv')
dele_df_fn.to_csv('result/dele.csv')
perf_df_fn.to_csv('result/perf.csv')
nperf_df_fn.to_csv('result/nperf.csv')
part_df_fn.to_csv('result/part.csv')
infl_df_fn.to_csv('result/infl.csv')
gini_df_fn.to_csv('result/gini.csv')
# %%
