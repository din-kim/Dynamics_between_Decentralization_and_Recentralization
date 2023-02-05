# Import libraries
from cProfile import label
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


"""
(2) Calculators
- Performance calculator: Sum up the matches of vectors between Reality and Organization
- Knowledge calculator: Sum up the matches of vectors between User and Organization
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


"""
(3) Distributing tokens 
- This function draws a random number in an uniform distribution.
- If dr(distribution rate) does not equals to 1, two groups of users hold different amount of tokens. 
- 'dr' decides the size of the first group and that group owns (1-dr) tokens.
- '1-dr' of the remaining group owns the rest tokens(dr).
- Example) if dr=0.2, 20% of users owns 80% of tokens and the remaining 80% of users owns 20% of tokens.
"""


def distribute_tokens(n, t, dr):
    if dr == 1:
        return np.random.dirichlet(np.ones(n)) * t
    else:
        a = np.random.dirichlet(np.ones(int(n*dr))) * ((1-dr)*t)
        b = np.random.dirichlet(np.ones(int(n*(1-dr)))) * (dr*t)
        return np.concatenate((a, b))


"""
(4) Generate a vote list
- Sampling random voting targets from the number of m. NO repeatition.
"""


def generate_vote_list(m, v):
    vote_list = random.sample(list(range(m)), v)
    return vote_list


"""
(5) Vote handler
- Sampling random voting targets from the number of m. NO repeatition.
"""


def vote_handler(reality, organization, users, vote_list):
    vote_sum_list = []
    dele_sum_list = []
    dele_cnt_list = []
    part_list = []
    know_list = []
    perf_list = []

    for vote_target in vote_list:
        vote_result, chosen_value = organization.initiate_vote_on(
            vote_target, users)
        perf_before, perf_after = organization.change_org_attr(chosen_value)
        knows = organization.change_usr_attr(chosen_value)

        vot_ctr_sum, dele_ctr_sum = organization.vote_category_ctrs()
        vote_sum_list.append(vot_ctr_sum)
        dele_sum_list.append(dele_ctr_sum)

        dele_cnt_per_user = organization.record_dele_cnts()
        dele_cnt_list.append(dele_cnt_per_user)

        part = organization.participation_ctrs()
        part_list.append(part)

        know_list.append(organization.avg_knowledge())
        perf_list.append(organization.performance_calculator(reality))

    return vote_sum_list, dele_sum_list, dele_cnt_list, part_list, know_list, perf_list


def mean_vote_result(var, n_o):
    var = np.array(var)
    if n_o == 1:
        var = var.ravel()
        return var
    else:

        if len(var) > 1:
            x = var[0].ravel()
            for i in range(1, len(var)):
                y = var[i].ravel()
                x = [x+y for x, y in zip(x, y)]
        res = np.array(x)/n_o
        return res


def mean_know_perf_part_result(var):
    res = np.array(var).ravel()
    return res


"""
(6) Plotting
"""


def plot_vote_dele_result(vote_res, dele_res):
    plt.figure(figsize=(12, 6))
    plt.plot(vote_res, label='Vote', color='tab:orange', marker='o', ls='--')
    plt.plot(dele_res, label='Delegate',
             color='tab:blue', marker='o', ls='--')
    plt.xlabel('votes/rounds')
    plt.ylabel('counts')
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')


def plot_know_perf_result(know_res, perf_res):
    plt.figure(figsize=(12, 6))
    plt.plot(know_res, label='Knowledge', color='red', marker='o', ls='--')
    plt.plot(perf_res, label='Performance',
             color='green', marker='*', ls='--')
    plt.xlabel('votes/rounds')
    plt.ylabel('counts')
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='upper left')


def plot_part_res(res, n):
    plt.figure(figsize=(12, 6))
    plt.plot(res, label='participated',
             color='purple', marker='o', ls='--')
    plt.title('Participation')
    plt.xlabel('votes')
    plt.ylabel('counts')
    plt.ylim(0, n)
    plt.grid(axis='x', alpha=0.5, ls=':')
    plt.legend(loc='lower left')
