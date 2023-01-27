import random
import pandas as pd
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

m = 100
n = 100
k = 0
t = 100000
dr = 1


# Initate the Reality, Organization
r = Reality(m)
o = Organization(m, r)

# Create random token list
tokens = list(distribute_tokens(n, t, dr))
ids = list(range(n))

# Initate Users in a dictionary
Users = []
for n in range(n):
    globals()['u{}'.format(n)] = User(m, o)
    Users.append(globals()['u{}'.format(n)])
