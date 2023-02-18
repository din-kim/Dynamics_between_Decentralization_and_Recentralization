import random
from functions.others import *


class User:
    def __init__(self, reality, organization, m, k, p, ids, tokens):
        self.id = ids.pop(0)
        self.m = m
        self.k = k
        self.vector = generate_user_vector(organization)
        self.p = p
        self.p_yn = self.p > random.random()
        self.knowledge = get_knowledge(self, organization)
        self.performance = get_performance(self, organization)
        self.token = tokens.pop(0)
        self.tokens_delegated = 0
        self.total_tokens = 0
        self.reality = reality
        self.organization = organization
        self.voted = False
        self.delegated = False
        self.changed = False
        self.whale = False
        self.leader = False
        self.vote_ctr = 0
        self.delegate_ctr = 0

    def get_performance(self):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == self.reality.vector[i]:
                cnt += 1
        self.performance = cnt/self.m
        return self.performance

    def get_knowledge(self):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == self.organization.vector[i]:
                cnt += 1
        self.knowledge = cnt/self.m
        return self.knowledge

    def get_p_yn(self):
        return self.p > random.uniform(0, 1)

    def vote(self, vote_on):
        self.voted = True
        self.vote_ctr += 1
        self.total_tokens = self.token + self.tokens_delegated
        return self.vector[vote_on], self.total_tokens

    def delegate(self, delegatee):
        self.voted = True
        self.delegate_ctr += 1
        delegatee.delegated = True
        delegatee.tokens_delegated += self.token
        return

    def check_interdependence(self, candidate):
        cnt = 0
        idxs = list(range(self.m))
        idxs.pop(self.vote_on)
        chosen_idxs = random.sample(idxs, self.k)

        for idx in chosen_idxs:
            if self.vector[idx] == candidate.vector[idx]:
                cnt += 1
        if self.k == cnt:
            return True
        else:
            return False

    def search(self, users, vote_on):
        n_u = len(users)
        self.vote_on = vote_on
        if self.delegated:
            return self.vote(vote_on)
        elif self.whale:
            return self.vote(vote_on)
        elif self.leader:
            return self.vote(vote_on)
        else:
            search = random.sample(users, round(n_u*self.p))
            if self in search:
                search.remove(self)

            max_knowledge = 0
            for s in search:
                if s.p_yn:
                    if self.check_interdependence(s):
                        if s.knowledge > max_knowledge:
                            max_knowledge = s.knowledge
                            max_idx = s.id

            if self.knowledge < max_knowledge:
                delegatee = users[max_idx]
                return self.delegate(delegatee)
            elif self.knowledge >= max_knowledge:
                if self.p_yn:
                    return self.vote(vote_on)
                else:
                    return
