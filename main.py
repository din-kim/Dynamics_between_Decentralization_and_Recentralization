# Import Classes
import random
from Reality import *
from Organization import *
from User import *
from functions import *

# Import libraries
import numpy as np
np.set_printoptions(4)
random.seed(101)


"""
Variables
- m : number of attributes
- n : number of users
- p : participation rate
- k : degree of interdependence
- t : total number of tokens
- dr: distribution rate of tokens
"""

rds = 1
v = 10
m = 10
n = 5
k = 0
t = 100
dr = 1
tokens = list(distribute_tokens(n, t, dr))
ids = list(range(n))

# Initiate Reality and Organization
r = Reality(m)
o = Organization(m, r)

# Initiate Users
users = []
for i in range(n):
    globals()['user{}'.format(i)] = User(m, k, o, ids, tokens)
    users.append(globals()['user{}'.format(i)])


if __name__ == '__main__':
    for rd in range(rds):
        vote_list = generate_vote_list(m, v)
        ctr_list, know_list, perf_list = vote_handler(
            r, o, users, vote_list, show_vote_result='y', show_vote_change='y')
