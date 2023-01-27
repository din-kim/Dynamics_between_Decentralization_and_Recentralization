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
    for i in range(m):
        if reality.vector[i] == organization.vector[i]:
            cnt += 1
    performance = cnt/m
    return performance


def knowledge_calculator(user, organization):
    cnt = 0
    for i in range(m):
        if user.vector[i] == organization.vector[i]:
            cnt += 1
    knowledge = cnt/m
    return knowledge


def AOD_calculator(user):
    AOD = user.p * user.knowledge
    return AOD
