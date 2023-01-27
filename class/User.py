"""
User
"""


class User:
    def __init__(self, m, organization):
        self.id = ids.pop(0)
        self.m = m
        self.vector = [random.randint(0, 1) for _ in range(self.m)]
        self.p = random.uniform(0, 1)
        self.p_yn = self.p > random.random()
        self.knowledge = knowledge_calculator(self, organization)
        self.token = tokens.pop()
        self.AOD = self.p * self.knowledge

    def knowledge_calculator(self, organization):
        cnt = 0
        for i in range(self.m):
            if self.vector[i] == organization.vector[i]:
                cnt += 1
        self.knowledge = cnt/self.m

    def vote(self, organization, vote_on):
        if self.p_yn:
            if self.vector[vote_on-1] == organization.vector[vote_on-1]:
                return self.token
            else:
                return 0
        else:
            return 0

    def search(self):
        for user in Users:
            search = random.sample(Users, round(n*self.p))
            # Search 대상에서 자기 자신 제거
            while user in search:
                search = random.sample(Users, round(n*self.p))
# 여기서 k값 검증해줘야 하지만 일단 패스
        print("User#{} is going to search {} firms.".format(self.id, len(search)))
        # Search 대상 유저 중에서
        print("Start Searching...")
        maximum_AOD = 0
        for i in range(len(search)):
            # 그 AOD가 Search 주체 유저의 knowledge보다 높으면
            if search[i].AOD > maximum_AOD:
                # 해당 인덱스를 가져와서
                maximum_AOD = search[i].AOD
                maximum_index = search[i].id

        if maximum_AOD < self.knowledge:
            print("Search Failure")
            print("=====================")
            print()
            return
        else:
            print("Search Success: Search #{}".format(maximum_index))
            print("user's knowledge: {}".format(self.knowledge))
            print("user{}'s AOD: {}".format(
                Users[maximum_index].id, Users[maximum_index].AOD))
            print("=====================")
            print()
