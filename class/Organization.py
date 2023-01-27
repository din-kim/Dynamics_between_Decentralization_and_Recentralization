"""
Organization
"""


class Organization:
    def __init__(self, m, reality):
        self.m = m
        self.vector = [random.randint(0, 1) for _ in range(self.m)]
        self.performance = performance_calculator(self, reality)

    def collect_votes(self, users, vote_on):
        sum_list = [0, 0]
        for user in users:
            sum_list[self.vector[vote_on-1]] += user.vote(self, vote_on)
        return sum_list
