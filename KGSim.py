# -*- coding: utf-8 -*-#


import numpy as np
from util import LoadFile as lf

# filename = "./data/entityVector.txt"
filename1 = "./data/entityVector1.txt"

kg_entity_vec = {}
m_set = set()
kg_sim = {}


def euclidean(vec1, vec2):
    dist = np.linalg.norm(vec1 - vec2)
    sim = 1.0 / (1.0 + dist)  # 归一化
    return sim


def get_kg_sim():
    for line in lf.load_file_all(filename1):
    # for line in lf.load_file_all(filename):
        m_id, m_vec = line.split("\t")
        m_id = int(m_id)
        m_vec_details = []
        temp = m_vec.replace("[", "").replace("]", "").split(",")
        for i in temp:
            m_vec_details.append(i)
        m_set.add(m_id)
        kg_entity_vec[m_id] = np.asarray(m_vec_details, dtype='float32')

    print("len(m_set)):"+str(len(m_set)))
    for m1 in m_set:
        for m2 in m_set:
            m1 = int(m1)
            m2 = int(m2)
            if m1 != m2:
                kg_sim.setdefault(m1, {})
                kg_sim[m1].setdefault(m2, 0)
                kg_sim[m1][m2] = euclidean(kg_entity_vec[m1], kg_entity_vec[m2])
    print("calculate complete!")
    print("len(kg_sim):"+str(len(kg_sim)))
get_kg_sim()

i=1
with open("./data/kg_sim1.txt", "a") as f:
# with open("./data/kg_sim.txt", "a") as f:
    for key, details in kg_sim.items():
        print(i)
        i+=1
        f.write(str(key) + "::" + str(details)+"\n")
    print("print success!")
