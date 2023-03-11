# Import libraries
from functions.others import *


class Organization:
    def __init__(self, m, reality):
        self.m = m
        self.reality = reality
        self.vector = generate_org_vector(reality)
        self.performance = get_performance(self, reality)
        self.reality = reality
        self.changed = False

    def get_performance(self):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == self.reality.vector[i]:
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
            user.total_tokens = 0
            user.changed = False
            user.vote_ctr = 0
            user.delegate_ctr = 0
            self.changed = False

        for user in users:
            # Call vote function - here begins vote, search, and delegate
            result = user.search(users, vote_on)
            if result != None:
                vote_on_value, token = result
                vote_result[vote_on_value] += token

        if vote_result[0] > vote_result[1]:
            chosen_value = 0
        else:
            chosen_value = 1
        return vote_result, chosen_value

    def change_org_attr(self, chosen_value):
        current_value = self.vector[self.vote_on]
        if current_value != chosen_value:
            self.changed = True
            self.vector[self.vote_on] = chosen_value
        perf_before = self.performance
        perf_after = self.get_performance()
        return perf_before, perf_after

    def change_usr_attr(self, chosen_value):
        perf_changes = []
        for user in self.users:
            if user.voted:
                if user.vector[self.vote_on] != chosen_value:
                    user.vector[self.vote_on] = chosen_value
                    user.changed = True
            perf_before = user.performance
            perf_after = user.get_performance()
        perf_changes.append([perf_before, perf_after])
        return perf_changes

    def get_vote_ctrs(self):
        vote_ctr_sum = 0
        dele_ctr_sum = 0
        for user in self.users:
            vote_ctr_sum += user.vote_ctr
            dele_ctr_sum += user.delegate_ctr

        return vote_ctr_sum, dele_ctr_sum

    def get_participation_ctrs(self):
        p_cnt = 0
        for user in self.users:
            if user.voted:
                p_cnt += 1
        return p_cnt

    # def get_org_performance(self):
    #     perf_sum = 0
    #     n = len(self.users)
    #     for user in self.users:
    #         perf_sum += user.performance
    #     perf_avg = round(perf_sum/n, 4)
    #     return perf_avg

    def get_user_influence(self, vote_result, chosen_value):
        user_influences = []
        for user in self.users:
            if user.vector[self.vote_on] == chosen_value:
                if sum(vote_result) == 0:
                    user_influence = 0
                else:
                    user_influence = round(
                        user.total_tokens/sum(vote_result), 4)
            else:
                user_influence = 0
            user_influences.append(user_influence)
        return user_influences

    def get_gini_coefficient(self, users):
        tkns_list = []
        for user in users:
            tkns_list.append(user.total_tokens)
        x = np.array(tkns_list)
        x.sort()
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi-x[i:]))
        return total/(len(x)**2 * np.mean(x))
