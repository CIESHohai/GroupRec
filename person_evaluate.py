# -*- coding: utf-8 -*-#


from operator import itemgetter


def recommend(user,trainSet,movie_sim_matrix):
    K =20
    N = 10
    rank = {}
    watched_movies = trainSet[user]

    for movie, rating in watched_movies.items():
        for related_movie, w in sorted(movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
            if related_movie in watched_movies:
                continue
            rank.setdefault(related_movie, 0)
            rank[related_movie] += w * float(rating)
    return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

def evaluate(trainSet,testSet,movie_sim_matrix):
    print('Evaluating start ...')
    N =10
    # 准确率和召回率
    hit = 0
    rec_count = 0
    test_count = 0
    # 覆盖率
    all_rec_movies = set()

    for i, user in enumerate(trainSet):
        test_moives = testSet.get(user, {})
        rec_movies = recommend(user,trainSet,movie_sim_matrix)
        for movie, w in rec_movies:
            if movie in test_moives:
                hit += 1
            all_rec_movies.add(movie)
        rec_count += N
        test_count += len(test_moives)

    precision = hit / (1.0 * rec_count)
    recall = hit / (1.0 * test_count)
    print('precisioin=%.4f\trecall=%.4f' % (precision, recall))
