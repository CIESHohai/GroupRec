# -*- coding: utf-8 -*-#



import random
from util import LoadFile as lf
import Evaluate as eva
import ItemCF as cf
import person_evaluate as pe


class GroupRecMain():
    def __init__(self):
        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

    # 读文件得到“用户-电影”数据
    def get_data(self, filename, pivot=0.25):
        trainSet_len = 0
        testSet_len = 0
        for line in lf.load_file_skip(filename):
            user, movie, rating, timestamp = line.split("::")
            if (random.random() < pivot):
                self.trainSet.setdefault(user, {})
                self.trainSet[user][movie] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        print('拆分训练集和测试集成功！')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)


if __name__ == "__main__":
    rating_file = "./data/ml-1m/ratings.dat"
    groupRec = GroupRecMain()
    groupRec.get_data(rating_file)

    # 评估
    eva.evaluate(groupRec.trainSet,groupRec.testSet)


    # 个性化测试
    # movie_sim_matrix=cf.calc_movie_sim(groupRec.trainSet)
    # pe.evaluate(groupRec.trainSet,groupRec.testSet,movie_sim_matrix)


