# -*- coding: utf-8 -*-#



import random
import math

user_sim_matrix = {}
group_mem = set()


# 计算用户之间的相似度
def calc_user_sim(train_set):
    # 构建“电影-用户”倒排索引
    movie_user = {}
    for user, movies in train_set.items():
        for movie in movies:
            if movie not in movie_user:
                movie_user[movie] = set()
            movie_user[movie].add(user)

    for movie, users in movie_user.items():
        for u in users:
            for v in users:
                if u == v:
                    continue
                user_sim_matrix.setdefault(u, {})
                user_sim_matrix[u].setdefault(v, 0)
                user_sim_matrix[u][v] += 1

    # 计算相似性
    for u, related_users in user_sim_matrix.items():
        for v, count in related_users.items():
            user_sim_matrix[u][v] = count / math.sqrt(len(train_set[u]) * len(train_set[v]))

    return user_sim_matrix


group_mem = set()


def generateGroup(user_sim_matrix, train_set, group_count, group_sim):
    user_sim_matrix = user_sim_matrix
    n = 0
    group_mem.clear()
    temp = random.choice(list(user_sim_matrix))
    for user, relation_matric in user_sim_matrix.items():
        for u, r in relation_matric.items():
            if (temp == u and r > group_sim and n < group_count):
                group_mem.add(user)
                n = n + 1
    if (len(group_mem) < group_count):
        generateGroup(user_sim_matrix, train_set, group_count, group_sim)
    # else:
    #     print("群组成员的组内相似度为%.1f 及其以上。" % (group_sim))
    #     print(group_mem)
    return group_mem
