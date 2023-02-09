from time import perf_counter_ns
from Reality import *
from Organization import *
from User import *
from functions import *


def generate_reality(m):
    reality = Reality(m)
    return reality


def generate_organizations(m, reality, n_o):
    organizations = []
    for i in range(n_o):
        globals()['org{}'.format(i)] = Organization(m, reality)
        organizations.append(globals()['org{}'.format(i)])
    return organizations


def generate_users(reality, organizations, n_u, n_l, m, k, p, t, dr):
    # Initiate Users
    for organization in organizations:
        tokens = list(distribute_tokens(n_u, t, dr))
        ids = list(range(n_u))
        whale_number = whale_calculator(n_u, dr)

        users = []
        leaders = []

        if n_l == 0:
            for i in range(n_u):
                globals()['user{}'.format(i)] = User(
                    m, k, p, organization, ids, tokens)
                users.append(globals()['user{}'.format(i)])
        else:
            for i in range(n_u-n_l):
                globals()['user{}'.format(i)] = User(
                    m, k, p, organization, ids, tokens)
                users.append(globals()['user{}'.format(i)])

            for j in range(n_u-n_l, n_u):
                globals()['user{}'.format(j)] = User(
                    m, k, p, organization, ids, tokens)
                users.append(globals()['user{}'.format(j)])

            for k in range(n_u-n_l, n_u):
                leaders.append(users[k])
                users[k].leader = True
                users[k].vector = generate_leader_vector(reality)
                users[k].performance = performance_calculator(
                    users[k], reality)
                users[k].knowledge_calculator(organization)

        if whale_number != 0:
            for i in range(whale_number):
                users[i].whale = True

    return users, leaders


def run_model(reality, organizations, users, leaders, vote_list_method, m, rds, v):
    # Create empty info list
    votes_fn = []
    deles_fn = []
    parts_fn = []
    knows_fn = []
    perfs_fn = []
    infls_fn = []

    for organization in organizations:
        votes = []
        deles = []
        parts = []
        knows = []
        perfs = []
        infls = []

        # Initiate Vote
        for _ in range(rds):
            if vote_list_method == "random":
                vote_list = generate_random_vote_list(m, v)
            elif vote_list_method == "leader":
                vote_list = generate_leaders_vote_list(leaders, m, v)

            vs, ds, ps, kns, pfs, infs = vote_handler(
                reality, organization, users, vote_list)

            votes.append(vs)
            deles.append(ds)
            parts.append(ps)
            knows.append(kns)
            perfs.append(pfs)
            infls.append(infs)

        votes_fn.append(votes)
        deles_fn.append(deles)
        parts_fn.append(parts)
        knows_fn.append(knows)
        perfs_fn.append(perfs)
        infls_fn.append(infls)

    return votes_fn, deles_fn, parts_fn, knows_fn, perfs_fn, infls_fn
