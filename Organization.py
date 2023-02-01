# Import libraries
from attr import attr
import numpy as np
import random

from functions import *


class Organization:
    def __init__(self, m, reality):
        self.m = m
        self.vector = [random.randint(0, 1) for _ in range(self.m)]
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
        print("============================================")
        print("INITIATING A VOTE ON ATTR#{}({})".format(
            vote_on, self.vector[vote_on]))
        print("============================================")
        print()

        vote_result = [0, 0]
        print(">>>>>>>>>>>>>>>>")

        for user in users:
            # re-initiate the values in every vote
            user.p_yn = user.get_p_yn()
            user.voted = False
            user.delegated = False
            user.tokens_delegated = 0
            user.changed = False
            user.vote_ctr = 0
            user.delegate_ctr = 0
            user.vote_anyway_ctr = 0
            self.changed = False
            user.knowledge_calculator(self)
            user.AOD_calculator()

        for user in users:
            print("user#{} initiates voting.".format(user.id))
            # Call vote function - here begins vote, search, and delegate
            result = user.vote(vote_on, users)

            if result == None:
                print("Did not exercise the voting right!")
                print("----------------")
                print()
            else:
                vote_on_value, token = result
                vote_result[vote_on_value] += token
                print("Vote success!")
                print("----------------")
                print()

        print("============================================")
        print("VOTING ENDED")
        print("============================================")
        print()

        return vote_result

    def change_attr(self, vote_result):
        vote_on = self.vote_on
        attr_val_before = self.vector[vote_on]

        # change Organization's attribute
        if vote_result[0] > vote_result[1]:
            self.vector[vote_on] = 0
        else:
            self.vector[vote_on] = 1

        attr_val_after = self.vector[vote_on]

        print("Changing Organization", end="..........")
        if attr_val_before != attr_val_after:
            self.changed = True
        print("Complete!")
        print()

        # change User's attribute
        print("Changing user(s)", end="")
        for user in self.users:
            if user.voted:
                if attr_val_before != attr_val_after:
                    print(".", end="")
                    user.vector[vote_on] = attr_val_after
                    user.changed = True
        print("Complete!")
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

    def show_vote_change(self):
        vote_on = self.vote_on
        print("Regarding ATTR#{}".format(vote_on))
        if self.total_vote_cnts == 0:
            print("No one vote, thus Nothing changed.")
        else:
            if self.changed:
                print("Organization changed.")
                print("== Performance change: {} ===> {}".format(
                    self.performance, self.performance_calculator(self.reality)))
                print()
            else:
                print("Organization did not change.")

            print("Check if user(s) changed.")
            for user in self.users:
                if user.voted and user.changed:
                    print("== user#{} knowledge change: {} ===> {}".format(
                        user.id, user.knowledge, user.knowledge_calculator(self)))
            print("========================")
            print()
            print()
            print("SESSION END")
            print()
            print()

    def vote_category_ctrs(self):
        vote_ctr_sum = 0
        delegate_ctr_sum = 0
        vote_anyway_ctr_sum = 0

        for user in self.users:
            vote_ctr_sum += user.vote_ctr
            delegate_ctr_sum += user.delegate_ctr
            vote_anyway_ctr_sum += user.vote_anyway_ctr

        vot_ctr = vote_ctr_sum
        dele_ctr = delegate_ctr_sum
        vot_any_ctr = vote_anyway_ctr_sum
        return vot_ctr, dele_ctr, vot_any_ctr

    def participation_ctrs(self):
        p_y_cnt = 0
        for user in self.users:
            if user.voted:
                p_y_cnt += 1

        p_n_cnt = len(self.users) - p_y_cnt
        return p_y_cnt, p_n_cnt

    def avg_knowledge(self):
        knowledge_sum = 0
        n = len(self.users)
        for user in self.users:
            knowledge_sum += user.knowledge
        know_avg = round(knowledge_sum/n, 4)
        return know_avg
