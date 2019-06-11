# -*- coding: utf-8 -*-#



import math
from operator import itemgetter

movie_sim_matrix = {}
movie_popular = {}
movie_count = 0
n_sim_movie = 20
group_rank = {}


# 计算电影之间的相似度
def calc_movie_sim(train_set):
    for user, movies in train_set.items():
        for movie in movies:
            if movie not in movie_popular:
                movie_popular[movie] = 0
            movie_popular[movie] += 1

    for user, movies in train_set.items():
        for m1 in movies:
            for m2 in movies:
                if m1 == m2:
                    continue
                movie_sim_matrix.setdefault(m1, {})
                movie_sim_matrix[m1].setdefault(m2, 0)
                movie_sim_matrix[m1][m2] += 1

    for m1, related_movies in movie_sim_matrix.items():
        for m2, count in related_movies.items():
            # 0向量
            if movie_popular[m1] == 0 or movie_popular[m2] == 0:
                movie_sim_matrix[m1][m2] = 0
            else:
                movie_sim_matrix[m1][m2] = count / math.sqrt(movie_popular[m1] * movie_popular[m2])
    print('电影相似度矩阵计算成功!')
    return movie_sim_matrix


def ic_predict(movie_sim_matrix, train_set, group_mem):
    movie_sim_matrix = movie_sim_matrix
    K = n_sim_movie
    for user in group_mem:
        rank = {}
        watched_movies = train_set[user]
        for movie, rating in watched_movies.items():
            for related_movie, w in sorted(movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_movie in watched_movies:
                    continue
                else:
                    rank.setdefault(related_movie, 0)
                    rank[related_movie] += w * float(rating)
        group_rank[user] = rank
    # for u,r in group_rank.items():
    #     print(u,r)
    return group_rank


def kg_ic_predict(movie_sim_matrix, train_set, group_mem, kg_sim, sim_score, sim_kg):
    movie_sim_matrix = movie_sim_matrix
    K = n_sim_movie
    for user in group_mem:
        rank = {}
        watched_movies = train_set[user]
        k_detail = 0.0
        for movie, rating in watched_movies.items():
            for related_movie, w in sorted(movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_movie in watched_movies:
                    continue
                else:
                    related_movie = int(related_movie)
                    rank.setdefault(related_movie, 0)
                    temp = kg_sim[movie]
                    for k, v in temp.items():
                        if k == int(related_movie):
                            k_detail = v
                            break
                    rank[related_movie] += sim_kg * float(k_detail) * float(rating) + sim_score * w * float(rating)
        group_rank[user] = rank
    # for u,r in group_rank.items():
    #     print(u,r)
    return group_rank
