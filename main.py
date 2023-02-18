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
rds = 80
v = 10
m = 100
n_u = 100
n_o = 50
k = 10
p = 0.2  # random.uniform(0, 1)
t = 10000
dr = 1
n_l = 0
method = get_vote_method(n_l)

if __name__ == "__main__":
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
    plot_vote_dele_result(mean_votes, mean_deles, n_u)
    plot_know_perf_result(mean_knows, mean_perfs)
    plot_part_res(mean_parts, n_u)
    plot_gini_res(mean_ginis)
    plot_infl_res(mean_infls)

# %%
