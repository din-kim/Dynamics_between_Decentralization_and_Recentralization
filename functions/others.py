# Import libraries
import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import product

# FUNCTIONS


"""
(1) Generate random vectors
- Generate vectors based on the uniform distribution.
- After having knowledge/performance value first, then match user or organization's attribute value according to the value assigned
- so that we prevent the situation where the most of user/organization have its knowledge/performance of very near to 0.5.
"""


def generate_user_vector(organization):
    m = len(organization.vector)
    nums = list(range(m))
    random_perf = random.uniform(0, 1)
    idxs = random.sample(nums, int(np.floor(random_perf*m)))
    user_vector = [None] * m

    # match values between user and organization as random performance value
    for idx in idxs:
        user_vector[idx] = organization.vector[idx]
    # then unmatch the rest values
    for i in range(m):
        if user_vector[i] == None:
            user_vector[i] = int(not(organization.vector[i]))
    return user_vector


def generate_org_vector(reality):
    m = len(reality.vector)
    nums = list(range(m))
    random_perf = random.uniform(0, 1)
    idxs = random.sample(nums, int(np.floor(random_perf*m)))
    org_vector = [None] * m

    # match values between user and reality as random knowledge value
    for idx in idxs:
        org_vector[idx] = reality.vector[idx]
    # then unmatch the rest values
    for i in range(m):
        if org_vector[i] == None:
            org_vector[i] = int(not(reality.vector[i]))
    return org_vector


def generate_leader_vector(reality):
    m = len(reality.vector)
    nums = list(range(m))
    random_perf = random.uniform(0.5, 1)
    idxs = random.sample(nums, int(np.floor(random_perf*m)))
    leader_vector = [None] * m

    # match values between user and reality as random knowledge value
    for idx in idxs:
        leader_vector[idx] = reality.vector[idx]
    # then unmatch the rest values
    for i in range(m):
        if leader_vector[i] == None:
            leader_vector[i] = int(not(reality.vector[i]))
    return leader_vector


"""
(2) Calculators
- Performance calculator: Sum up the matches of vectors between Reality and Organization
- Knowledge calculator: Sum up the matches of vectors between User and Organization
- Whale calculator: Return the number of whales given n and dr
"""


def get_performance(organization, reality):
    cnt = 0
    for i in range(organization.m):
        if reality.vector[i] == organization.vector[i]:
            cnt += 1
    performance = cnt/organization.m
    return performance


def calculate_whales(n, dr):
    if dr != 1:
        whale_number = int(n*dr)
    else:
        whale_number = 0
    return whale_number


"""
(3) Distributing tokens
- This function draws a random number in an uniform distribution.
- If dr(distribution rate) does not equals to 1, two groups of users hold different amount of tokens.
- 'dr' decides the size of the first group and that group owns (1-dr) tokens.
- '1-dr' of the remaining group owns the rest tokens(dr).
- Example) if dr=0.2, 20% of users owns 80% of tokens and the remaining 80% of users owns 20% of tokens.
"""


def distribute_tokens(n, t, dr):
    if dr == 0:
        return [int(t/n)] * n
    if n*dr < 1:
        raise Exception("ValueError: n*dr should be larger than 1.")
    elif dr == 1:
        return np.random.dirichlet(np.ones(n)) * t
    else:
        a = np.random.dirichlet(np.ones(int(n*dr))) * ((1-dr)*t)
        b = np.random.dirichlet(np.ones(int(n*(1-dr)))) * (dr*t)
        return np.concatenate((a, b))


"""
(4) Generate a vote list
- Sampling random voting targets from the number of m. NO repeatition.
- Sampling leader's voting targets from leaders randomly chosen.
  They decide what to vote only if more than half of the leaders share the same attribute values.
"""


def generate_random_vote_list(m, v):
    vote_list = random.sample(list(range(m)), v)
    return vote_list


def generate_leaders_vote_list(leaders, m, v):
    rounds = 0
    n_l = len(leaders)
    confirmed_targets = []

    while len(confirmed_targets) <= v:
        leaders = random.sample(leaders, n_l)
        target = random.randint(0, m-1)
        cnt = 0
        tmp = leaders[0].vector[target]

        while cnt <= n_l//2:
            for leader in leaders:
                if tmp == leader.vector[target]:
                    cnt += 1
                    rounds += 1

                if cnt == n_l//2:
                    confirmed_targets.append(target)
                    if len(confirmed_targets) == v:
                        return confirmed_targets
                    break
            if cnt < n_l:
                break
        if rounds > 300:
            return confirmed_targets


"""
(5) Mean results
- mean result: mean results of votes, delegations, knowledges, performances and participations
- mean influencers: mean results of influencer counts
"""


def mean_result(var):
    var = np.array(var)
    n_o = len(var)
    if n_o == 1:
        var = var.ravel()
        return var
    else:
        x = var[0].ravel()
        for i in range(1, len(var)):
            y = var[i].ravel()
            x = [x+y for x, y in zip(x, y)]
    res = np.array(x)/n_o
    return res


def mean_influencers(var, n_o, rds, v, c_index):
    org_cnts = []
    for i in range(n_o):
        rd_cnts = []
        for j in range(rds):
            for k in range(v):
                cnts = 0
                infs = var[i][j][k]
                for inf in infs:
                    if inf >= c_index:
                        cnts += 1
                rd_cnts.append(cnts)
        org_cnts.append(rd_cnts)
    res = np.array(org_cnts)
    tmp = res[0]
    for i in range(1, n_o):
        tmp += res[i]
    avg = tmp/n_o
    return avg


"""
(6) Plotting
"""


def plot_vote_dele_result(vote_res, dele_res, n_u, dr, n_l, p, k):
    plt.figure(figsize=(12, 6))
    plt.plot(vote_res, label='Vote', color='black', ls="--")
    plt.plot(dele_res, label='Delegate', color='black')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, n_u)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
    plt.savefig("images/dr({dr})_n_l({n_l})_p({p})_k({k})__vote_dele.png".format(
        dr=dr, n_l=n_l, p=p, k=k))


def plot_perf_result(perf_res, dr, n_l, p, k):
    plt.figure(figsize=(12, 6))
    plt.plot(perf_res, label='Performance',
             color='black', ls='dotted')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, 1)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
    plt.savefig("images/dr({dr})_n_l({n_l})_p({p})_k({k})__know_perf.png".format(
        dr=dr, n_l=n_l, p=p, k=k))


def plot_part_res(res, n_u, dr, n_l, p, k):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='Participation', color='black')
    plt.xlabel('Rounds')
    plt.ylabel('Rate')
    plt.ylim(0, n_u+5)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
    plt.savefig("images/dr({dr})_n_l({n_l})_p({p})_k({k})__part_res.png".format(
        dr=dr, n_l=n_l, p=p, k=k))


def plot_infl_res(res, dr, n_l, p, k):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='Influencers', color='black')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, 10)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
    plt.savefig("images/dr({dr})_n_l({n_l})_p({p})_k({k})__infl_res.png".format(
        dr=dr, n_l=n_l, p=p, k=k))


def plot_gini_res(res, dr, n_l, p, k):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='Gini Coefficient', color='black')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, 1)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
    plt.savefig("images/dr({dr})_n_l({n_l})_p({p})_k({k})__gini_res.png".format(
        dr=dr, n_l=n_l, p=p, k=k))


"""
(7) Others
- Generate paramter grids
- Get vote method 
"""


def param_grid(params):
    for vcomb in product(*params.values()):
        yield dict(zip(params.keys(), vcomb))


def get_vote_method(l):
    if l > 0:
        method = "leader"
    else:
        method = "random"
    return method
