# -*- coding: utf-8 -*-#


from operator import itemgetter






def get_no_see_movie(group_rank):
    no_see_movie = set()
    for k in group_rank:
        temp=set(list(group_rank[k].keys()))
        for item in temp:
            no_see_movie.add(item)
    for k1 in group_rank:
        for k2 in group_rank:
            if k1==k2:
                continue
            else:
                result_movie=no_see_movie.intersection(set(list(group_rank[k2].keys())))
    return result_movie

def avg_strategy(group_rank, n):
    group_rating = {}
    no_see_movie=get_no_see_movie(group_rank)
    for m in no_see_movie:
        temp = 0
        for u1, v1 in group_rank.items():
            if m in v1.keys():
                print("1")
                temp += v1[m]
            else:
                temp += 2.0
        group_rating[m] = temp / len(group_rank)
    # print('群组评分预测完毕!')
    return sorted(group_rating.items(), key=itemgetter(1), reverse=True)[:n]


def least_strategy(group_rank, n):
    group_rating = {}
    no_see_movie = get_no_see_movie(group_rank)
    for m in no_see_movie:
        temp_list = []
        for u1, v1 in group_rank.items():
            if m in v1.keys():
                print("2")
                temp_list.append(v1[m])
            else:
                temp_list.append(2.0)
        group_rating[m] = min(temp_list)
    # print('群组评分预测完毕!')
    return sorted(group_rating.items(), key=itemgetter(1), reverse=True)[:n]
