# Import libraries
import numpy as np
import random
import matplotlib.pyplot as plt


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
    random_know = random.uniform(0, 1)
    idxs = random.sample(nums, int(np.floor(random_know*m)))
    user_vector = [None] * m

    # match values between user and organization as random knowledge value
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


def performance_calculator(organization, reality):
    cnt = 0
    for i in range(organization.m):
        if reality.vector[i] == organization.vector[i]:
            cnt += 1
    performance = cnt/organization.m
    return performance


def knowledge_calculator(user, organization):
    cnt = 0
    for i in range(user.m):
        if user.vector[i] == organization.vector[i]:
            cnt += 1
    knowledge = cnt/organization.m
    return knowledge


def whale_calculator(n, dr):
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
        target = random.randint(0, m-1)
        cnt = 0
        tmp = leaders[0].vector[target]

        while cnt <= n_l:
            for leader in leaders:
                if tmp == leader.vector[target]:
                    cnt += 1
                    rounds += 1
            if cnt == n_l//2:
                confirmed_targets.append(target)
                if len(confirmed_targets) == v:
                    return confirmed_targets
                break
            elif cnt < n_l:
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


def mean_influencers(var, rds, v, c_index):
    n_o = len(var)
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


def plot_vote_dele_result(vote_res, dele_res):
    plt.figure(figsize=(12, 6))
    plt.plot(vote_res, label='Vote', color='tab:orange',
             marker='o', ls='dotted')
    plt.plot(dele_res, label='Delegate',
             color='tab:blue',  ls='dotted')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, 1.1)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')


def plot_know_perf_result(know_res, perf_res):
    plt.figure(figsize=(12, 6))
    plt.plot(know_res, label='Knowledge', color='red', ls='--')
    plt.plot(perf_res, label='Performance',
             color='green', marker='*', ls='--')
    plt.xlabel('Rounds')
    plt.ylabel('Counts')
    plt.ylim(0, 1)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')


def plot_part_res(res):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='Participation Rate',
             color='purple')
    plt.title('Participation')
    plt.xlabel('Rounds')
    plt.ylabel('Rate')
    plt.ylim(0, 1.1)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')


def plot_infl_res(res):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='Influencer Rate',
             color='grey', marker='dotted')
    plt.title('Participation')
    plt.xlabel('Rounds')
    plt.ylabel('Rate')
    plt.ylim(0, 0.5)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')
