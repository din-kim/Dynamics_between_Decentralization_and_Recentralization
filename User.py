import numpy as np
import random

from sympy import maximum


from functions import generate_user_vector, knowledge_calculator


class User:
    def __init__(self, m, k, organization, ids, tokens):
        self.id = ids.pop(0)
        self.m = m
        self.k = k
        self.vector = generate_user_vector(organization)
        self.p = random.uniform(0, 1)
        self.p_yn = self.p > random.random()
        self.knowledge = knowledge_calculator(self, organization)
        self.token = tokens.pop()
        self.tokens_delegated = 0
        self.AOD = self.p * self.knowledge
        self.organization = organization
        self.voted = False
        self.delegated = False
        self.changed = False
        self.vote_ctr = 0
        self.delegate_ctr = 0
        self.vote_anyway_ctr = 0

    def knowledge_calculator(self, organization):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == organization.vector[i]:
                cnt += 1
        self.knowledge = cnt/self.m
        return self.knowledge

    def AOD_calculator(self):
        self.AOD = self.p * self.knowledge

    def get_p_yn(self):
        return self.p > random.uniform(0, 1)

    def vote(self, vote_on, users):
        self.users = users
        self.vote_on = vote_on
        if self.p_yn:
            if self.vector[vote_on] == self.organization.vector[vote_on]:
                self.vote_ctr += 1
                print("USER -O- MATCH -O- ORGANIZATION")
                self.voted = True
                return self.vector[vote_on], self.token

            elif self.delegated:
                return self.vote_anyway()
            else:
                print("USER -X- UNMATCH -X- ORGANIZATION")
                return self.search(self.k)
        else:
            return

    def vote_anyway(self):
        self.vote_anyway_ctr += 1
        print("Start Voting Anyway!")
        self.voted = True
        return self.vector[self.vote_on], self.token

    def delegate(self, delegatee):
        self.delegate_ctr += 1
        self.voted = True
        delegatee.delegated = True
        delegatee.tokens_delegated = self.token
        print("user#{} delegated {} tokens to user#{}".format(
            self.id, self.token, delegatee.id))
        return delegatee.vector[self.vote_on], delegatee.tokens_delegated

    def check_interdependence(self, k, candidate):
        cnt = 0
        idxs = list(range(self.m))
        idxs.pop(self.vote_on)
        chosen_idxs = random.sample(idxs, k)

        for idx in chosen_idxs:
            if self.vector[idx] == candidate.vector[idx]:
                cnt += 1

        if k == cnt:
            return True
        else:
            return False

    def search(self, k):
        search = random.sample(self.users, round(len(self.users)*self.p))
        if self in search:
            search.remove(self)

        print("= user#{} is searching {} users.".format(self.id, len(search)))
        print("== Start Searching!")

        maximum_AOD = 0
        search_cnt = 0
        inter_cnt = 0
        for s in search:
            # check if a delegatee candidate participates in voting
            if s.p_yn:
                search_cnt += 1
                # check if a delegatee candidate's AOD is higher than a delegator's knowledge
                if s.AOD > maximum_AOD:
                    # check if all interdependent attribute values are all matched between delegatee and delegator.
                    if self.check_interdependence(k, s):
                        inter_cnt += 1
                        maximum_AOD = s.AOD
                        maximum_idx = s.id

        if search_cnt == 0:
            print("== Search Failed: All searched users do not participate.")
            return self.vote_anyway()
        elif inter_cnt == 0:
            print("== Search Failed: user#{} is not interdependent with all searched users.".format(
                self.id))
            return self.vote_anyway()
        elif self.knowledge > maximum_AOD:
            print("== Search Failed: user#{}'s knowledge is higher than other users' AOD.".format(
                self.id))
            return self.vote_anyway()
        elif self.knowledge < maximum_AOD:
            print("== Search Succeed: Start Delegating!")
            delegatee = self.users[maximum_idx]
            return self.delegate(delegatee)
