import numpy as np
import random
from Organization import Organization

from functions import generate_user_vector, knowledge_calculator


class User:
    def __init__(self, m, k, p, organization, ids, tokens):
        self.id = ids.pop(0)
        self.m = m
        self.k = k
        self.vector = generate_user_vector(organization)
        self.p = p
        self.p_yn = self.p > random.random()
        self.knowledge = knowledge_calculator(self, organization)
        self.token = tokens.pop()
        self.tokens_delegated = 0
        self.organization = organization
        self.voted = False
        self.delegated = False
        self.changed = False
        self.vote_ctr = 0
        self.delegate_ctr = 0

    def knowledge_calculator(self, organization):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == organization.vector[i]:
                cnt += 1
        self.knowledge = cnt/self.m
        return self.knowledge

    def get_p_yn(self):
        return self.p > random.uniform(0, 1)

    def vote(self, vote_on):
        self.vote_ctr += 1
        self.voted = True
        return self.vector[vote_on], self.token

    def delegate(self, delegatee):
        self.delegate_ctr += 1
        self.voted = True
        delegatee.delegated = True
        delegatee.tokens_delegated = self.token
        return delegatee.vector[self.vote_on], delegatee.tokens_delegated

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

    def search(self, vote_on):
        self.vote_on = vote_on
        if self.delegated:
            return self.vote(vote_on)
        else:
            search = random.sample(self.organization.users, round(
                len(self.organization.users)*self.p))
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
                delegatee = self.organization.users[max_idx]
                return self.delegate(delegatee)
            elif self.knowledge >= max_knowledge:
                if self.p_yn:
                    return self.vote(vote_on)
                else:
                    return
