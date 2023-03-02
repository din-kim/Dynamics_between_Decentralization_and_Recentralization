from functions.others import *

"""
(5) Vote handler
- Sampling random voting targets from the number of m. NO repeatition.
"""


def vote_handler(organization, users, vote_list):
    vote_ctr_sum_list = []
    dele_ctr_sum_list = []
    part_list = []
    perf_list = []
    new_perf_list = []
    infl_list = []
    gini_list = []

    for vote_target in vote_list:
        vote_result, chosen_value = organization.initiate_vote_on(
            vote_target, users)

        infl = organization.get_user_influence(vote_result, chosen_value)
        infl_list.append(infl)

        perf_before, perf_after = organization.change_org_attr(chosen_value)
        perfs = organization.change_usr_attr(chosen_value)

        vot_ctr_sum, dele_ctr_sum = organization.get_vote_ctrs()
        vote_ctr_sum_list.append(vot_ctr_sum)
        dele_ctr_sum_list.append(dele_ctr_sum)

        part = organization.get_participation_ctrs()
        part_list.append(part)

        new_perf = organization.get_org_performance()
        new_perf_list.append(new_perf)

        perf = organization.get_performance()
        perf_list.append(perf)

        gini = organization.get_gini_coefficient(users)
        gini_list.append(gini)

    return vote_ctr_sum_list, dele_ctr_sum_list, part_list, new_perf_list, perf_list, infl_list, gini_list


def run_model(reality, organizations, users_list, leaders_list, vote_method, rds, v):
    m = reality.m
    n_o = len(organizations)
    # Create empty info list
    votes_fn = []
    deles_fn = []
    parts_fn = []
    perfs_fn = []
    nperf_fn = []
    infls_fn = []
    ginis_fn = []

    for i in range(n_o):
        votes = []
        deles = []
        parts = []
        perfs = []
        infls = []
        ginis = []
        nperf = []

        # Initiate Vote
        for _ in range(rds):
            if vote_method == "random":
                vote_list = generate_random_vote_list(m, v)
            elif vote_method == "leader":
                vote_list = generate_leaders_vote_list(leaders_list[i], m, v)

            vs, ds, ps, npfs, pfs, infs, gs = vote_handler(
                organizations[i], users_list[i], vote_list)

            votes.append(vs)
            deles.append(ds)
            parts.append(ps)
            nperf.append(npfs)
            perfs.append(pfs)
            infls.append(infs)
            ginis.append(gs)

        votes_fn.append(votes)
        deles_fn.append(deles)
        parts_fn.append(parts)
        nperf_fn.append(nperf)
        perfs_fn.append(perfs)
        infls_fn.append(infls)
        ginis_fn.append(ginis)

    return votes_fn, deles_fn, parts_fn, nperf_fn, perfs_fn, infls_fn, ginis_fn
