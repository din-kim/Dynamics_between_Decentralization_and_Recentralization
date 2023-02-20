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
        whale_number = calculate_whales(n_u, dr)
        users = []
        leaders = []
        if n_l == 0:
            for _ in range(n_u):
                users.append(User(reality, organization, m, k, p, ids, tokens))
        else:
            for _ in range(n_u):
                users.append(User(reality, organization, m, k, p, ids, tokens))

            for i in range(n_u-n_l, n_u):
                leaders.append(users[i])
                users[i].leader = True
                users[i].p = 1
                users[i].vector = generate_leader_vector(reality)
                users[i].get_performance()
                users[i].get_knowledge()

        for j in range(n_u-whale_number, n_u):
            users[j].whale = True

        users_list.append(users)
        leaders_list.append(leaders)
    return users_list, leaders_list
