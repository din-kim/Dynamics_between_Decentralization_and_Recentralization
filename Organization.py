# Import libraries
from attr import attr
import numpy as np
import random

from functions import *


class Organization:
    def __init__(self, m, reality):
        self.m = m
        self.vector = generate_org_vector(reality)
        self.performance = performance_calculator(self, reality)
        self.reality = reality
        self.changed = False

    def performance_calculator(self, reality):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == reality.vector[i]:
                cnt += 1
        # renew performance here
        self.performance = cnt/self.m
        return self.performance

    def initiate_vote_on(self, vote_on, users):
        self.users = users
        self.vote_on = vote_on

        vote_result = [0, 0]

        # re-initiate the values in every vote
        for user in users:
            user.p_yn = user.get_p_yn()
            user.voted = False
            user.delegated = False
            user.tokens_delegated = 0
            user.changed = False
            user.vote_ctr = 0
            user.delegate_ctr = 0
            self.changed = False

        for user in users:
            # Call vote function - here begins vote, search, and delegate
            result = user.search(vote_on)

            if result == None:
                pass
            else:
                vote_on_value, token = result
                vote_result[vote_on_value] += token

        if vote_result[0] > vote_result[1]:
            chosen_value = 0
        else:
            chosen_value = 1

        return vote_result, chosen_value

    def change_org_attr(self, chosen_value):
        attr_val_before = self.vector[self.vote_on]
        attr_val_after = chosen_value

        per_bf = self.performance

        if attr_val_before != attr_val_after:
            self.changed = True
            self.vector[self.vote_on] = attr_val_after

        per_af = self.performance_calculator(self.reality)
        return per_bf, per_af

    def change_usr_attr(self, chosen_value):
        knos = []
        # change User's attribute
        for user in self.users:
            kno_bf = user.knowledge
            if user.voted:
                if user.vector[self.vote_on] != chosen_value:
                    user.vector[self.vote_on] = chosen_value
                    user.changed = True
            kno_af = user.knowledge_calculator(self)
            knos.append([kno_bf, kno_af])
        return knos

    def show_vote_change(self, per_bf, per_af, knos):
        vote_on = self.vote_on
        if self.changed:
            print("Organization changed.")
            print("== Performance change: {} ===> {}".format(per_bf, per_af))
            print()
        else:
            print("Organization did not change.")

        print("Check if user(s) changed.")
        for user in self.users:
            if user.changed:
                print("== user#{} knowledge change: {} ===> {}".format(
                    user.id, knos[user.id][0], knos[user.id][1]))
        print("========================")
        print()
        print()
        print("SESSION END")
        print()
        print()

    def show_vote_result(self, vote_result):
        total_vote_cnts = 0
        for user in self.users:
            if user.voted:
                total_vote_cnts += 1

        self.total_vote_cnts = total_vote_cnts
        n = len(self.users)

        print("Total Voters: {}".format(n))
        print("== Vote: {}".format(total_vote_cnts))
        print("== No Vote: {}".format(n-total_vote_cnts))
        print()

        print("Voting Result")
        print("Value: 0: {}".format(vote_result[0]))
        print("Value: 1: {}".format(vote_result[1]))
        print()

        print("========================")

    def record_dele_cnts(self):
        delegate_ctr_per_user = []
        for user in self.users:
            delegate_ctr_per_user.append([user.id, user.delegate_ctr])
        return delegate_ctr_per_user

    def vote_category_ctrs(self):
        vote_ctr_sum = 0
        delegate_ctr_sum = 0

        for user in self.users:
            vote_ctr_sum += user.vote_ctr
            delegate_ctr_sum += user.delegate_ctr

        return vote_ctr_sum, delegate_ctr_sum

    def participation_ctrs(self):
        p_y_cnt = 0
        for user in self.users:
            if user.voted:
                p_y_cnt += 1
        return p_y_cnt

    def avg_knowledge(self):
        knowledge_sum = 0
        n = len(self.users)
        for user in self.users:
            knowledge_sum += user.knowledge
        know_avg = round(knowledge_sum/n, 4)
        return know_avg
