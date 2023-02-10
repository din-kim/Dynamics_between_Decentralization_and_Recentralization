from classes.Reality import *
from classes.Organization import *
from classes.User import *
from functions.others import *


def generate_reality(m):
    reality = Reality(m)
    return reality


def generate_organizations(m, reality, n_o):
    organizations = []
    for i in range(n_o):
        organizations.append(Organization(m, reality))
    return organizations


def generate_users(reality, organizations, n_u, n_l, m, k, p, t, dr):
    # Initiate Users
    users_list = []
    leaders_list = []

    for organization in organizations:
        tokens = list(distribute_tokens(n_u, t, dr))
        ids = list(range(n_u))
        whale_number = whale_calculator(n_u, dr)
        users = []
        leaders = []
        if n_l == 0:
            for i in range(n_u):
                users.append(User(reality, organization, m, k, p, ids, tokens))
        else:
            for i in range(n_u):
                users.append(User(reality, organization, m, k, p, ids, tokens))

            for j in range(n_u-n_l, n_u):
                leaders.append(users[j])
                users[j].leader = True
                users[j].p = 1
                users[j].vector = generate_leader_vector(reality)
                users[j].performance_calculator(reality)
                users[j].knowledge_calculator(organization)

        for k in range(whale_number):
            users[k].whale = True
        users_list.append(users)
        leaders_list.append(leaders)
    return users_list, leaders_list
