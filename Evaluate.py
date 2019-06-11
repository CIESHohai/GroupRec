# -*- coding: utf-8 -*-#


import GroupGenerate as gg
import ItemCF as ic
import GroupScorePredict as gsp
from util import LoadFile as lf

loop_count = 50
group_count = 8
N = 10
group_sim = 0.3
sim_mix = [[0.0, 1.0], [0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6], [0.5, 0.5], [0.6, 0.4], [0.7, 0.3], [0.8, 0.2],
           [0.9, 0.1], [1.0, 0.0]]


# sim_mix = [[0.0, 1.0], [1.0, 0.0]]

def ev_detail_kg(group_mem, test_set, g_rating, all_rec_movies, sim_score, sim_kg):
    rec_count = N
    hit = 0
    precision = 0
    recall = 0
    for user in group_mem:
        test_moives = test_set.get(user, {})
        test_count = len(test_moives)
        for movie, r in g_rating:
            if str(movie) in test_moives:
                hit += 1
            all_rec_movies.add(movie)
        precision += hit / (1.0 * rec_count)
        recall += hit / (1.0 * test_count)
    precision = precision / group_count
    recall = recall / group_count
    return precision, recall, sim_score, sim_kg


def evaluate(train_set, test_set):
    print('Evaluating start ...')
    kg_sim = {}
    kg_sim_detail = {}
    for line in lf.load_file_all("./data/kg_sim1.txt"):
        temp = line.split("::")
        details = temp[1].replace("{", "").replace("}", "").split(",")
        kg_sim.setdefault(int(temp[0]), {})
        for items in details:
            kv = items.split(":")
            kg_sim_detail[int(kv[0])] = kv[1]
        kg_sim[temp[0]] = kg_sim_detail

    user_sim_matrix = gg.calc_user_sim(train_set)
    movie_sim_matrix = ic.calc_movie_sim(train_set)
    all_rec_movies = set()

    for i in sim_mix:
        sim_score = i[0]
        sim_kg = i[1]
        for j in range(loop_count):
            # group generate
            group_mem = gg.generateGroup(user_sim_matrix, train_set, group_count, group_sim)
            group_rank_kg = ic.kg_ic_predict(movie_sim_matrix, train_set, group_mem, kg_sim, sim_score, sim_kg)

            g_rating_kg_lm = gsp.least_strategy(group_rank_kg, N)
            precision_kg_lm, recall_kg_lm, sim_score, sim_kg = ev_detail_kg(group_mem, test_set, g_rating_kg_lm,
                                                                            all_rec_movies, sim_score, sim_kg)

            g_rating_kg_avg = gsp.avg_strategy(group_rank_kg, N)
            precision_kg_avg, recall_kg_avg, sim_score, sim_kg = ev_detail_kg(group_mem, test_set, g_rating_kg_avg,
                                                                              all_rec_movies, sim_score, sim_kg)
        with open("./data/result_10.txt", "a", encoding="gbk") as f:
            f.write("least_strategy(sim_score=%1f,sim_kg=%1f)： precision=%.4f\trecall=%.4f\t" % (
                sim_score, sim_kg, precision_kg_lm / loop_count, recall_kg_lm / loop_count) + "\n")
        with open("./data/result_10.txt", "a", encoding="gbk") as f:
            f.write("avg_strategy(sim_score=%1f,sim_kg=%1f)： precision=%.4f\trecall=%.4f\t" % (
                sim_score, sim_kg, precision_kg_avg / loop_count, recall_kg_avg / loop_count) + "\n")

    print("执行完毕！")
