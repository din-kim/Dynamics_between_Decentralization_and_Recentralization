from functions.others import *

"""
(5) Vote handler
- Sampling random voting targets from the number of m. NO repeatition.
"""


def vote_handler(organization, users, vote_list):
    vote_ctr_sum_list = []
    dele_ctr_sum_list = []
    part_list = []
    know_list = []
    perf_list = []
    infl_list = []

    for vote_target in vote_list:
        vote_result, chosen_value = organization.initiate_vote_on(
            vote_target, users)

        infl = organization.user_influence(vote_result, chosen_value)
        infl_list.append(infl)

        perf_before, perf_after = organization.change_org_attr(chosen_value)
        knows = organization.change_usr_attr(chosen_value)

        vot_ctr_sum, dele_ctr_sum = organization.vote_dele_ctrs()
        vote_ctr_sum_list.append(vot_ctr_sum)
        dele_ctr_sum_list.append(dele_ctr_sum)

        part = organization.participation_ctrs()
        part_list.append(part)

        know = organization.avg_knowledge()
        know_list.append(know)

        perf = organization.performance_calculator()
        perf_list.append(perf)

    return vote_ctr_sum_list, dele_ctr_sum_list, part_list, know_list, perf_list, infl_list


def run_model(reality, organizations, users_list, leaders_list, vote_method, rds, v):
    m = reality.m
    n_o = len(organizations)
    # Create empty info list
    votes_fn = []
    deles_fn = []
    parts_fn = []
    knows_fn = []
    perfs_fn = []
    infls_fn = []

    for i in range(n_o):
        votes = []
        deles = []
        parts = []
        knows = []
        perfs = []
        infls = []

        # Initiate Vote
        for _ in range(rds):
            if vote_method == "random":
                vote_list = generate_random_vote_list(m, v)
            elif vote_method == "leader":
                vote_list = generate_leaders_vote_list(leaders_list[i], m, v)

            vs, ds, ps, kns, pfs, infs = vote_handler(
                organizations[i], users_list[i], vote_list)

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
