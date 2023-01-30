# Import libraries
import numpy as np
import random

from psutil import users


# FUNCTIONS

"""
(1) Distributing tokens 
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
(2) Calculators
- Performance calculator: Sum up the matches of vectors between Reality and Organization
- Knowledge calculator: Sum up the matches of vectors between User and Organization
- Adequacy of Delegation Calculator: AoD = p(participation rate ) * knowledge
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
    for i in range(organization.m):
        if user.vector[i] == organization.vector[i]:
            cnt += 1
    knowledge = cnt/organization.m
    return knowledge


def AOD_calculator(user):
    AOD = user.p * user.knowledge
    return AOD


def generate_vote_list(m, v):
    vote_list = random.sample(list(range(m)), v)
    return vote_list


def vote_handler(reality, organization, users, vote_list, show_vote_result='y', show_vote_change='y'):
    print("****************************************")
    print("**************** VOTE TARGET: {} ****************".format(vote_list))
    print("****************************************")
    print()
    print()

    for vote_target in vote_list:
        vote_result = organization.initiate_vote_on(vote_target, users)

        if show_vote_result == 'y':
            organization.show_vote_result(vote_result)
        if show_vote_change == 'y':
            organization.show_vote_change()

    ctrs = organization.collect_ctrs()
    know = organization.avg_knowledge()
    perf = organization.performance_calculator(reality)

    return ctrs, know, perf
