import math
import sys
import csv
import numpy as np
import time
from typing import List

from data_processing import Data
from LDP.krr import *
# from LDP.sue import *
# from LDP.oue import *
from LDP.krr import *
from LDP.olh import *
from ULDP.ukrr import *
from ULDP.usue import *
from ULDP.uoue import *
from PSULDP.pskrr import *
from PSULDP.pssue import *
from PSULDP.psoue import *
import matplotlib.pyplot as plt
import matplotlib


# 解决中文显示问题
# plt.rcParams['font.sans-serif'] = 'SimHei'   # 使图形中的中文正常编码显示
# plt.rcParams['axes.unicode_minus'] = False


# 得到数据集中的真实概率
def get_true(data: Data, url):
    true_list = [0 for _ in range(len(data.domain))]
    with open(url, 'r') as f:
        for line in f.readlines():
            # 移除头尾换行符
            line = line.strip()
            # 将一行中的数字划分开
            linelist = line.split(' ')
            linelist = [int(x) for x in linelist]
            temp_list = linelist[0]
            true_list[data.domain.index(temp_list)] += 1
    for i in range(len(true_list)):
        true_list[i] /= data.dataNum
    print('真实概率为：')
    print(true_list)
    return true_list


# 计算mse
def get_mse(list1: List, list2: List):
    length = len(list1)
    mse = 0
    for i in range(length):
        mse += (list1[i] - list2[i]) * (list1[i] - list2[i])
    mse /= length
    return mse


def run():
    time1 = time.time()
    # data = Data("data/test.txt")
    data = Data("./data/bank-additional-full.csv")
    # data = Data("./data/e-shop clothing 2008.csv")

    print(data.true_p)
    epsilon = 0.1
    xs = [1, 4, 8, 10]
    xn = [2, 3, 5, 6, 7, 9, 11, 12]
    level_epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    print('KRR')
    # for level_i in range(1, len(level_epsilon) + 1, 1):
    for level_i in range(9, 9 + 1, 1):
        print('level_i=', level_i)
        u_mse = 0
        ps_mse = 0
        ps_notdwsnotdr_mse = 0
        ps_notdws_mse = 0
        ps_notdr_mse = 0
        replication = 100

        for i in range(replication):
            u = UKRR(epsilon, data.domain, data.data, xs, xn)
            u.run()
            u.estimate(u.per_data)

            ps = PSKRR(data.domain, data.data, xs, xn, level_epsilon)
            ps.run(level_i)

            u_mse += get_mse(u.es_data, data.true_p)
            ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
            ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
            ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
            ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)
        u_mse /= replication
        ps_mse /= replication
        ps_notdwsnotdr_mse /= replication
        ps_notdws_mse /= replication
        ps_notdr_mse /= replication

        print('u=', u_mse)
        print('ps=', ps_mse)
        print('ps_notdws=', ps_notdws_mse)
        print('ps_notdr=', ps_notdr_mse)
        print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
        print()
        print()

        print(time.time() - time1)
        plt.figure()
        index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
        value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
        plt.bar(index, value)
        xlabel = 'level ' + str(level_i)
        plt.xlabel(xlabel)
        plt.ylabel('MSE')
        plt.show()
    print('SUE')
    # for level_i in range(1, len(level_epsilon) + 1, 1):
    # for level_i in range(9, 9 + 1, 1):
    #     print('level_i=', level_i)
    #     u_mse = 0
    #     ps_mse = 0
    #     ps_notdwsnotdr_mse = 0
    #     ps_notdws_mse = 0
    #     ps_notdr_mse = 0
    #     replication = 100
    #
    #     for i in range(replication):
    #         u = USUE(epsilon, data.domain, data.data, xs, xn)
    #         u.run()
    #         u.estimate(u.per_data)
    #
    #         ps = PSSUE(data.domain, data.data, xs, xn, level_epsilon)
    #         ps.run(level_i)
    #
    #         u_mse += get_mse(u.es_data, data.true_p)
    #         ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
    #         ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
    #         ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
    #         ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)
    #     u_mse /= replication
    #     ps_mse /= replication
    #     ps_notdwsnotdr_mse /= replication
    #     ps_notdws_mse /= replication
    #     ps_notdr_mse /= replication
    #
    #     print('u=', u_mse)
    #     print('ps=', ps_mse)
    #     print('ps_notdws=', ps_notdws_mse)
    #     print('ps_notdr=', ps_notdr_mse)
    #     print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
    #     print()
    #     print()
    #
    #     print(time.time() - time1)
    #     plt.figure()
    #     index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
    #     value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
    #     plt.bar(index, value)
    #     xlabel = 'level ' + str(level_i)
    #     plt.xlabel(xlabel)
    #     plt.ylabel('MSE')
    #     plt.show()
    print('oue')
    # for level_i in range(1, len(level_epsilon) + 1, 1):
    # for level_i in range(1, 1 + 1, 1):
    #     print('level_i=', level_i)
    #     u_mse = 0
    #     ps_mse = 0
    #     ps_notdwsnotdr_mse = 0
    #     ps_notdws_mse = 0
    #     ps_notdr_mse = 0
    #     replication = 100
    #
    #     for i in range(replication):
    #         u = UOUE(epsilon, data.domain, data.data, xs, xn)
    #         u.run()
    #         u.estimate(u.per_data)
    #
    #         ps = PSOUE(data.domain, data.data, xs, xn, level_epsilon)
    #         ps.run(level_i)
    #
    #         u_mse += get_mse(u.es_data, data.true_p)
    #         ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
    #         ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
    #         ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
    #         ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)
    #
    #     u_mse /= replication
    #     ps_mse /= replication
    #     ps_notdwsnotdr_mse /= replication
    #     ps_notdws_mse /= replication
    #     ps_notdr_mse /= replication
    #
    #     print('u=', u_mse)
    #     print('ps=', ps_mse)
    #     print('ps_notdws=', ps_notdws_mse)
    #     print('ps_notdr=', ps_notdr_mse)
    #     print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
    #     print()
    #     print()
    #
    #     print(time.time() - time1)
    #     plt.figure()
    #     index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
    #     value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
    #     plt.bar(index, value)
    #     xlabel = 'level ' + str(level_i)
    #     plt.xlabel(xlabel)
    #     plt.ylabel('MSE')
    #     plt.show()


def run66pr():
    print('run66pr')
    time1 = time.time()
    # data = Data("data/test.txt")
    data = Data("./data/bank-additional-full.csv")
    # data = Data("./data/e-shop clothing 2008.csv")
    print(data.true_p)

    epsilon = 0.1
    xs = [1, 2, 4, 6, 8, 9, 10, 11]
    xn = [3, 5, 7, 12]
    level_epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    print('KRR')
    for level_i in range(1, len(level_epsilon) + 1, 1):
        print('level_i=', level_i)
        u_mse = 0
        ps_mse = 0
        ps_notdwsnotdr_mse = 0
        ps_notdws_mse = 0
        ps_notdr_mse = 0
        # replication = 100
        replication = 1

        for i in range(replication):
            u = UKRR(epsilon, data.domain, data.data, xs, xn)
            u.run()
            u.estimate(u.per_data)

            ps = PSKRR(data.domain, data.data, xs, xn, level_epsilon)
            ps.run(level_i)

            u_mse += get_mse(u.es_data, data.true_p)
            ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
            ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
            ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
            ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)
        u_mse /= replication
        ps_mse /= replication
        ps_notdwsnotdr_mse /= replication
        ps_notdws_mse /= replication
        ps_notdr_mse /= replication

        print('u=', u_mse)
        print('ps=', ps_mse)
        print('ps_notdws=', ps_notdws_mse)
        print('ps_notdr=', ps_notdr_mse)
        print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
        print()
        print()

        print(time.time() - time1)
        plt.figure()
        index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
        value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
        plt.bar(index, value)
        xlabel = 'level ' + str(level_i)
        plt.xlabel(xlabel)
        plt.ylabel('MSE')
        plt.show()
    print('SUE')
    for level_i in range(1, len(level_epsilon) + 1, 1):
        print('level_i=', level_i)
        u_mse = 0
        ps_mse = 0
        ps_notdwsnotdr_mse = 0
        ps_notdws_mse = 0
        ps_notdr_mse = 0
        replication = 100

        for i in range(replication):
            u = USUE(epsilon, data.domain, data.data, xs, xn)
            u.run()
            u.estimate(u.per_data)

            ps = PSSUE(data.domain, data.data, xs, xn, level_epsilon)
            ps.run(level_i)

            u_mse += get_mse(u.es_data, data.true_p)
            ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
            ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
            ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
            ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)
        u_mse /= replication
        ps_mse /= replication
        ps_notdwsnotdr_mse /= replication
        ps_notdws_mse /= replication
        ps_notdr_mse /= replication

        print('u=', u_mse)
        print('ps=', ps_mse)
        print('ps_notdws=', ps_notdws_mse)
        print('ps_notdr=', ps_notdr_mse)
        print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
        print()
        print()

        print(time.time() - time1)
        plt.figure()
        index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
        value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
        plt.bar(index, value)
        xlabel = 'level ' + str(level_i)
        plt.xlabel(xlabel)
        plt.ylabel('MSE')
        plt.show()
    print('oue')
    for level_i in range(1, len(level_epsilon) + 1, 1):
        print('level_i=', level_i)
        u_mse = 0
        ps_mse = 0
        ps_notdwsnotdr_mse = 0
        ps_notdws_mse = 0
        ps_notdr_mse = 0
        replication = 100

        for i in range(replication):
            u = UOUE(epsilon, data.domain, data.data, xs, xn)
            u.run()
            u.estimate(u.per_data)

            ps = PSOUE(data.domain, data.data, xs, xn, level_epsilon)
            ps.run(level_i)

            u_mse += get_mse(u.es_data, data.true_p)
            ps_mse += get_mse(ps.level_es_data[level_i - 1], data.true_p)
            ps_notdwsnotdr_mse += get_mse(ps.notdws_notdr[level_i - 1], data.true_p)
            ps_notdws_mse += get_mse(ps.notdws[level_i - 1], data.true_p)
            ps_notdr_mse += get_mse(ps.notdr[level_i - 1], data.true_p)

        u_mse /= replication
        ps_mse /= replication
        ps_notdwsnotdr_mse /= replication
        ps_notdws_mse /= replication
        ps_notdr_mse /= replication

        print('u=', u_mse)
        print('ps=', ps_mse)
        print('ps_notdws=', ps_notdws_mse)
        print('ps_notdr=', ps_notdr_mse)
        print('ps_notdrnotdws=', ps_notdwsnotdr_mse)
        print()
        print()

        print(time.time() - time1)
        plt.figure()
        index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
        value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
        plt.bar(index, value)
        xlabel = 'level ' + str(level_i)
        plt.xlabel(xlabel)
        plt.ylabel('MSE')
        plt.show()


# 实验1的图
def paint1_krr_job():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.0023422509093327126, 5.533053417262209e-05, 1.4945253877973557e-05, 5.406943774715885e-06,
              2.475261726179745e-06]
    data_level1 = [0.002286425571143383, 5.668019949816767e-05, 1.3620907698225861e-05, 5.074467242769244e-06,
                   2.7002105236647237e-06]
    data_level2 = [0.0006045156022191401, 3.9347905383336006e-05, 1.0933248137855119e-05, 4.667513036325646e-06,
                   2.289186465064035e-06]
    data_level3 = [0.0002984038871054312, 3.2591465448044426e-05, 9.614722584618262e-06, 4.0401828683440495e-06,
                   2.1101352844048818e-06]
    data_level4 = [0.00016178611519301309, 2.5505612473233738e-05, 7.887897952202817e-06, 3.5634048251033982e-06,
                   1.858409675177153e-06]
    data_level5 = [0.00011374469301325469, 2.3043028423384607e-05, 7.034817055100296e-06, 3.174191953001268e-06,
                   1.6016463946562606e-06]
    data_level6 = [8.226250286237597e-05, 1.904781069754124e-05, 6.666371468376148e-06, 3.1489760293833692e-06,
                   1.6998482476444705e-06]
    data_level7 = [6.451213957912885e-05, 1.7509941054802898e-05, 6.547040829378614e-06, 3.0698243619433147e-06,
                   1.6923961231861483e-06]
    data_level8 = [6.0716443019185565e-05, 1.5458673871735106e-05, 6.35351151213298e-06, 3.009428557035201e-06,
                   1.6300662368718726e-06]
    data_level9 = [5.7070017221925045e-05, 1.5239137392704816e-05, 6.294775143535116e-06, 2.8322306994471307e-06,
                   1.6579896801972425e-06]
    data_level10 = [4.943814572192448e-05, 1.4381464742838299e-05, 6.024914809675591e-06, 2.745617504461162e-06,
                    1.5590004987279377e-06]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)

    plt.show()


def paint1_sue_job():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.0033593469381966255, 8.635984128769007e-05, 2.725300595155985e-05, 1.3495931818219374e-05,
              7.3134416400845165e-06]
    data_level1 = [0.0031326182331000356, 9.018937096917744e-05, 2.8601343306452496e-05, 1.3457770476287385e-05,
                   7.193699680272799e-06]
    data_level2 = [0.0009535722324530388, 7.07755433383825e-05, 2.600734786335772e-05, 1.1204746429450716e-05,
                   6.976980173406227e-06]
    data_level3 = [0.0004483529870448389, 5.4447937864740454e-05, 1.966685285524515e-05, 1.019434798733849e-05,
                   6.4431306420674714e-06]
    data_level4 = [0.0002675779130443308, 4.6108591561674916e-05, 1.7686945366019462e-05, 9.703820753338906e-06,
                   5.421685193394805e-06]
    data_level5 = [0.000216299452958213, 4.5256209464030785e-05, 1.641546318633351e-05, 8.661858111325972e-06,
                   5.72989719204774e-06]
    data_level6 = [0.0001469593937768559, 3.8766075706220665e-05, 1.572934632530844e-05, 8.858700204337244e-06,
                   5.3892301731659914e-06]
    data_level7 = [0.00011993226356315722, 3.458864128186746e-05, 1.4568404244189592e-05, 7.76904667095223e-06,
                   5.136324321311793e-06]
    data_level8 = [0.00010129961814842994, 3.251811053334291e-05, 1.4848371297726097e-05, 8.587052703485616e-06,
                   5.037306530838236e-06]
    data_level9 = [9.116424174221113e-05, 3.138475818154371e-05, 1.2700253437969443e-05, 7.859652386454524e-06,
                   5.126202034892867e-06]
    data_level10 = [8.766395935614626e-05, 2.6405271038910705e-05, 1.3174728577720852e-05, 7.950438071717377e-06,
                    5.263456822540065e-06]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint1_oue_job():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.003309147994950575, 9.126498543902117e-05, 2.8115200350105736e-05, 1.3411455910835286e-05,
              7.777448736468148e-06]
    data_level1 = [0.0029559719829777443, 8.891434432682563e-05, 2.7226139910274203e-05, 1.352547056437127e-05,
                   7.849839839742373e-06]
    data_level2 = [0.0009391780570541046, 7.139153813073475e-05, 2.6218504951407312e-05, 1.2281343694301456e-05,
                   6.544701295218073e-06]
    data_level3 = [0.0004428461074878854, 5.682483276520606e-05, 2.024182734255492e-05, 9.95502286019722e-06,
                   6.474086964756883e-06]
    data_level4 = [0.00022400532989836256, 4.967653731114503e-05, 2.025595481731319e-05, 9.2921197967758e-06,
                   6.111643225154144e-06]
    data_level5 = [0.00017975571366087988, 4.077748482723167e-05, 1.7252124812630148e-05, 8.938339426148263e-06,
                   5.561842733643628e-06]
    data_level6 = [0.00014219314446878244, 3.58412912522916e-05, 1.6746997345283717e-05, 7.864256540341406e-06,
                   5.522738648078971e-06]
    data_level7 = [0.0001100323295146877, 3.464241002086205e-05, 1.5285626018138437e-05, 7.253529989161167e-06,
                   5.292419344771878e-06]
    data_level8 = [9.803115431304076e-05, 3.063080270789488e-05, 1.5387137262480587e-05, 7.72941850140058e-06,
                   5.255160482293975e-06]
    data_level9 = [9.049708337252665e-05, 2.8314104505753742e-05, 1.4924319934071182e-05, 7.916564099048827e-06,
                   5.42225953562347e-06]
    data_level10 = [8.737184094042449e-05, 2.757817463517435e-05, 1.3524827647493783e-05, 7.736223925094191e-06,
                    5.258130821044019e-06]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_krr_job():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.002286425571143383, 0.0006045156022191401, 0.0002984038871054312, 0.00016178611519301309,
          0.00011374469301325469, 8.226250286237597e-05, 6.451213957912885e-05, 6.0716443019185565e-05,
          5.7070017221925045e-05, 4.943814572192448e-05]
    ps_notdr = [0.021877733490030048, 0.003970052092907926, 0.0016331176133742573, 0.0006133429354787576,
                0.0003691166288074466, 0.00023273526978700158, 0.0001349276848983235, 0.0001018856723313035,
                6.9887290899514e-05, 4.943814572192448e-05]
    ps_notdws = [0.002286425571143383, 0.0006329072834846679, 0.00031168727350749904, 0.00018538075643087442,
                 0.00014571321350189334, 0.00011396747843307102, 8.966654766186679e-05, 0.00010745213769294545,
                 0.00012584876980431295, 0.00019341670844547976]
    ps_notdrnotdws = [0.021877733490030048, 0.004876808215293408, 0.002374401912522121, 0.0011750327310522156,
                      0.0008164953580416779, 0.0005940062561190403, 0.0003618646321157793, 0.00031298653320338673,
                      0.00023774719511083023, 0.00019341670844547976]

    plt.bar(x1, ps)
    plt.bar(x2, ps_notdr, hatch='\\\\\\')
    plt.bar(x3, ps_notdws, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['PS', 'DWS', 'DR', 'PG'])
    # plt.title('KRR')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_sue_job():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.0031326182331000356, 0.0009535722324530388, 0.0004483529870448389, 0.0002675779130443308,
          0.000216299452958213, 0.0001469593937768559, 0.00011993226356315722, 0.00010129961814842994,
          9.116424174221113e-05, 8.766395935614626e-05]
    ps_notdr = [0.029674092226275876, 0.007054811896862801, 0.0021213400597966327, 0.001056505417968844,
                0.0006627953223781726, 0.00040844025377421615, 0.00022773833052547912, 0.0001638276797660529,
                0.0001153636561401193, 8.766395935614626e-05]
    ps_notdws = [0.0031326182331000356, 0.0009880884722913486, 0.0004661610233928949, 0.00029449402965973074,
                 0.0002541901320619417, 0.00018870894323257708, 0.00016880608923059635, 0.00017108329831047868,
                 0.00020194701121797594, 0.0003742794337551547]
    ps_notdrnotdws = [0.029674092226275876, 0.00924629835346146, 0.0033501383454385475, 0.002083465992739847,
                      0.0014642591328196612, 0.0010346655512176437, 0.0005734251258505148, 0.0005243678111380277,
                      0.00043987008625874405, 0.0003742794337551547]

    plt.bar(x1, ps)
    plt.bar(x2, ps_notdr, hatch='\\\\\\')
    plt.bar(x3, ps_notdws, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['PS', 'DWS', 'DR', 'PG'])
    # plt.title('SUE')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_oue_job():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.0029559719829777443, 0.0009391780570541046, 0.0004428461074878854, 0.00022400532989836256,
          0.00017975571366087988, 0.00014219314446878244, 0.0001100323295146877, 9.803115431304076e-05,
          9.049708337252665e-05, 8.737184094042449e-05]
    ps_notdr = [0.0335659504711691, 0.006263374200178829, 0.0025783719009850646, 0.001191479441698972,
                0.0005919011334058996, 0.00038125042404599783, 0.00023038348023322097, 0.00014962344979231896,
                0.00010781586076982052, 8.737184094042449e-05]
    ps_notdws = [0.0029559719829777443, 0.0009713559724423408, 0.0004698173137831306, 0.0002610482220861994,
                 0.00022553263579657773, 0.00018910374262707895, 0.00016087493972171695, 0.0001840457466830692,
                 0.0002253622883031992, 0.00031817693443142767]
    ps_notdrnotdws = [0.0335659504711691, 0.008108222457747062, 0.0037003652972396025, 0.0022640713040074753,
                      0.0011667996760834419, 0.0009653398919517204, 0.0007392088432037341, 0.000552856850925693,
                      0.0004292827496007888, 0.00031817693443142767]

    plt.bar(x1, ps)
    plt.bar(x2, ps_notdr, hatch='\\\\\\')
    plt.bar(x3, ps_notdws, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['PS', 'DWS', 'DR', 'PG'])
    # plt.title('OUE')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint3_krr_job():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.002286425571143383, 0.0006045156022191401, 0.0002984038871054312, 0.00016178611519301309,
            0.00011374469301325469, 8.226250286237597e-05, 6.451213957912885e-05, 6.0716443019185565e-05,
            5.7070017221925045e-05, 4.943814572192448e-05]
    pr50 = [0.0056312260180316, 0.001502684857359955, 0.0006602069274216378, 0.0003959035977208456,
            0.00023948212548230872, 0.00019345055936080744, 0.00014555525557977987, 0.00012210715641746211,
            0.00010560012864765597, 0.00010118136706474652]
    pr66 = [0.010866523561857617, 0.0026358615371000595, 0.0011479709558510753, 0.000648599106929762,
            0.00045278521752739023, 0.00031554523711868604, 0.00024877324600276133, 0.00022525642127514195,
            0.00018145747565446798, 0.00016404591421489796]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint3_sue_job():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.0031326182331000356, 0.0009535722324530388, 0.0004483529870448389, 0.0002675779130443308,
            0.000216299452958213, 0.0001469593937768559, 0.00011993226356315722, 0.00010129961814842994,
            9.116424174221113e-05, 8.766395935614626e-05]
    pr50 = [0.00506783045768352, 0.001242207545822605, 0.0006257818366532427, 0.0004493208436057471,
            0.00025902613955599863, 0.00020390995380687688, 0.00015811886172136688, 0.00014580799632934874,
            0.0001386795930340004, 0.00012879085826524416]
    pr66 = [0.006455664872935954, 0.001736065915272701, 0.0008841202086409829, 0.0005295509472949363,
            0.00035509931138103684, 0.00030756187271137493, 0.00021877511027108357, 0.00018043864866167724,
            0.00017218303521816501, 0.00016384145329391]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint3_oue_job():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.0029559719829777443, 0.0009391780570541046, 0.0004428461074878854, 0.00022400532989836256,
            0.00017975571366087988, 0.00014219314446878244, 0.0001100323295146877, 9.803115431304076e-05,
            9.049708337252665e-05, 8.737184094042449e-05]
    pr50 = [0.004567358055126684, 0.001244713902020452, 0.000630950243336042, 0.00036258635755222944,
            0.00028336662160482345, 0.0002204030015421841, 0.00014807657338143125, 0.0001468648705746825,
            0.00014529346685917622, 0.00013669588857595584]
    pr66 = [0.006992926824280155, 0.0016173060601752875, 0.0007996321246554485, 0.0005385298147524926,
            0.00033537487163173526, 0.00027515981227403793, 0.0002251947419637968, 0.0002038874986734395,
            0.00017196662428561445, 0.00016277237538593096]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_krr_job():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = [0.002286425571143383, 0.0006045156022191401, 0.0002984038871054312, 0.00016178611519301309,
          0.00011374469301325469, 8.226250286237597e-05, 6.451213957912885e-05, 6.0716443019185565e-05,
          5.7070017221925045e-05, 4.943814572192448e-05]
    truep = [0.002170680674224643, 0.000537419590352423, 0.00030441961429274563, 0.00016843238081666988,
             0.00011868154551946503, 7.937348356176492e-05, 6.61832894603753e-05, 5.803113283070313e-05,
             5.434516529453942e-05, 5.033275415996658e-05]
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_sue_job():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = [0.0031326182331000356, 0.0009535722324530388, 0.0004483529870448389, 0.0002675779130443308,
          0.000216299452958213, 0.0001469593937768559, 0.00011993226356315722, 0.00010129961814842994,
          9.116424174221113e-05, 8.766395935614626e-05]
    truep = [0.0032263484744746085, 0.0008857491608814109, 0.0004297180049114798, 0.00025162415463991273,
             0.00019499585896777958, 0.0001509413284820816, 0.00011067039640376652, 9.599884391258087e-05,
             9.014763921279348e-05, 7.833197749768187e-05]
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_oue_job():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = [0.0029559719829777443, 0.0009391780570541046, 0.0004428461074878854, 0.00022400532989836256,
          0.00017975571366087988, 0.00014219314446878244, 0.0001100323295146877, 9.803115431304076e-05,
          9.049708337252665e-05, 8.737184094042449e-05]
    truep = [0.003342233282876974, 0.00079818799303061, 0.00040841139253816177, 0.00026972565877354733,
             0.0001829966374169415, 0.00014269955660235206, 0.00012645467207772623, 9.414559531239998e-05,
             9.907110048322753e-05, 8.811925661006068e-05]
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


######################################
def paint1_krr_star():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.00026925493153337113, 7.267197939583425e-06, 1.9578435225431157e-06, 7.735384678030323e-07,
              4.044692993767202e-07]
    data_level1 = [0.0002712259441593701, 6.604766991395571e-06, 2.0094624556534786e-06, 7.794929314740965e-07,
                   4.0098666825640087e-07]
    data_level2 = [8.281229497269358e-05, 5.604464786849808e-06, 1.5986653937372676e-06, 7.730857156338259e-07,
                   3.6891172694891137e-07]
    data_level3 = [3.599481252619117e-05, 4.9165613213581554e-06, 1.4398169671095406e-06, 7.165155855397704e-07,
                   3.7631965640976007e-07]
    data_level4 = [1.9028131227250198e-05, 3.743392038801459e-06, 1.3536834965345088e-06, 5.628398898905327e-07,
                   3.0787563952835907e-07]
    data_level5 = [1.6272540212735228e-05, 2.819350185863232e-06, 1.096927711711069e-06, 5.63728432014789e-07,
                   2.655119450190763e-07]
    data_level6 = [1.1843325425442268e-05, 2.7153662307809267e-06, 1.0478274793016587e-06, 5.355721852220874e-07,
                   2.8101451297148354e-07]
    data_level7 = [9.322640058581724e-06, 2.537130584665793e-06, 9.736241102565676e-07, 4.587831468291318e-07,
                   2.691279356004673e-07]
    data_level8 = [7.762373573326134e-06, 2.2034562033875042e-06, 9.178518120588611e-07, 4.6159697187357634e-07,
                   2.571545979921293e-07]
    data_level9 = [7.578238337480316e-06, 2.175417290377339e-06, 9.297740051238565e-07, 4.5415311858539867e-07,
                   2.7373770555231106e-07]
    data_level10 = [7.37473823662628e-06, 2.07691560480044e-06, 9.171366252026728e-07, 4.5557814409287165e-07,
                    2.766592447278825e-07]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()

    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint1_sue_star():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.0006056830420845815, 1.6974897309206993e-05, 5.197659789994419e-06, 2.4851063572412102e-06,
              1.3837711680548579e-06]
    data_level1 = [0.0006049343144219709, 1.7157455206881258e-05, 5.123623791229882e-06, 2.5548319132620433e-06,
                   1.3447142338888388e-06]
    data_level2 = [0.00015247461038627453, 1.2541321248978701e-05, 4.42745372303831e-06, 2.0922708059699172e-06,
                   1.1642554907596993e-06]
    data_level3 = [8.553755814495844e-05, 9.918139672567205e-06, 3.4481832877023342e-06, 1.848950105811416e-06,
                   1.0740728717934799e-06]
    data_level4 = [4.5658393491074565e-05, 8.113827937890679e-06, 3.284741927484662e-06, 1.8629535181925957e-06,
                   1.0356866163443475e-06]
    data_level5 = [2.7190194336230968e-05, 7.5859924762418475e-06, 3.1280686903687095e-06, 1.613331799331347e-06,
                   1.0599100227232085e-06]
    data_level6 = [2.4353129343537764e-05, 7.10643982426579e-06, 2.8122277871569586e-06, 1.6196202476568618e-06,
                   1.027391513238491e-06]
    data_level7 = [2.08606889224545e-05, 6.036889748035417e-06, 2.6352535999380194e-06, 1.6220353029607114e-06,
                   9.135444608614051e-07]
    data_level8 = [1.7083347250206517e-05, 6.037302295776507e-06, 2.401708625383325e-06, 1.5819192619609885e-06,
                   9.233475624677466e-07]
    data_level9 = [1.4955145774252685e-05, 5.274301470623526e-06, 2.461840055644347e-06, 1.4948847243879529e-06,
                   9.129243620993274e-07]
    data_level10 = [1.4977476464044098e-05, 5.088405434881695e-06, 2.4426513172176572e-06, 1.4175163933941679e-06,
                    9.036606996466705e-07]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint1_oue_star():
    epsilon = [0.1, 0.6, 1.1, 1.6, 2.1]
    data_u = [0.000536654767095003, 1.712669291102016e-05, 5.4736189393246065e-06, 2.353468639745215e-06,
              1.6159873633165301e-06]
    data_level1 = [0.0005667174441585008, 1.628131885924724e-05, 5.563751170799065e-06, 2.401793912206726e-06,
                   1.5143044982243054e-06]
    data_level2 = [0.00015075219330465696, 1.263888289715773e-05, 4.340732434917322e-06, 2.1365955115800815e-06,
                   1.3269347345842884e-06]
    data_level3 = [7.71768570753118e-05, 1.0003604856589337e-05, 3.6356820700335e-06, 1.8969537178260142e-06,
                   1.2070977535624147e-06]
    data_level4 = [4.337110617787501e-05, 8.359095810199945e-06, 3.2961940783220464e-06, 1.9018304266211665e-06,
                   1.1721040890154805e-06]
    data_level5 = [3.162163050766287e-05, 7.788476831014895e-06, 3.099985906821496e-06, 1.810899243139156e-06,
                   1.1643357778433304e-06]
    data_level6 = [2.245877379007181e-05, 6.150393296623685e-06, 2.951434162030133e-06, 1.6854920637688263e-06,
                   1.11478344279779e-06]
    data_level7 = [1.989529090646494e-05, 6.142350240458393e-06, 2.7961699680432833e-06, 1.7705938454544315e-06,
                   1.050054909695737e-06]
    data_level8 = [1.8665737264475058e-05, 6.005085366769093e-06, 2.7620634540095956e-06, 1.6340744688092067e-06,
                   1.031048091730337e-06]
    data_level9 = [1.56446230725438e-05, 6.052976162743536e-06, 2.6431905456581843e-06, 1.6469482380171295e-06,
                   1.072406976118912e-06]
    data_level10 = [1.5172190073131789e-05, 5.826282689483569e-06, 2.5797813036513877e-06, 1.6220990562163984e-06,
                    1.0304523888395028e-06]
    plt.plot(epsilon, data_u, '^-', label='ULDP')
    plt.plot(epsilon, data_level1, 'v--', label='level1')
    plt.plot(epsilon, data_level2, 'o-.', label='level2')
    plt.plot(epsilon, data_level3, '<:', label='level3')
    plt.plot(epsilon, data_level4, '>-', label='level4')
    plt.plot(epsilon, data_level5, '1--', label='level5')
    plt.plot(epsilon, data_level6, '2-.', label='level6')
    plt.plot(epsilon, data_level7, '3:', label='level7')
    plt.plot(epsilon, data_level8, '4-', label='level8')
    plt.plot(epsilon, data_level9, '*--', label='level9')
    plt.plot(epsilon, data_level10, 'p-.', label='level10')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_krr_star():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.0002712259441593701, 8.281229497269358e-05, 3.599481252619117e-05, 1.9028131227250198e-05,
          1.6272540212735228e-05, 1.1843325425442268e-05, 9.322640058581724e-06, 7.762373573326134e-06,
          7.578238337480316e-06, 7.37473823662628e-06]
    ps_notdr = [0.0024950237397498532, 0.0006315851278571262, 0.00019079682580264883, 9.042289140271074e-05,
                5.844150027126746e-05, 3.0630895483664586e-05, 1.8590698438990325e-05, 1.244177740804776e-05,
                9.891691306035946e-06, 7.37473823662628e-06]
    ps_notdws = [0.0002712259441593701, 8.521379235792181e-05, 3.80102949130728e-05, 2.026436627217683e-05,
                 1.8786936676835266e-05, 1.7253945179429e-05, 1.3911823227608614e-05, 1.3973346145825643e-05,
                 1.7492273610687473e-05, 2.6600802214328982e-05]
    ps_notdrnotdws = [0.0024950237397498532, 0.000811945722347426, 0.00030507755879491757, 0.0001787220377985601,
                      0.00011442959665773155, 8.160017147052877e-05, 5.935575900427861e-05, 4.18633231383268e-05,
                      3.2496057904630325e-05, 2.6600802214328982e-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_notdr, hatch='\\\\\\')
    plt.bar(x3, ps_notdws, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['PS', 'DWS', 'DR', 'PG'])
    # plt.title('KRR')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_sue_star():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.0006049343144219709, 0.00015247461038627453, 8.553755814495844e-05, 4.5658393491074565e-05,
          2.7190194336230968e-05, 2.4353129343537764e-05, 2.08606889224545e-05, 1.7083347250206517e-05,
          1.4955145774252685e-05, 1.4977476464044098e-05]
    ps_notdr = [0.005860025839436064, 0.0014177590662402414, 0.0004330427743433604, 0.0001718847928671899,
                9.774611302579868e-05, 7.064897304564707e-05, 4.153416662770537e-05, 2.9209255731306033e-05,
                1.8561926895635488e-05, 1.4977476464044098e-05]
    ps_notdws = [0.0006049343144219709, 0.00015439716402859772, 9.428793264867715e-05, 5.245911527455695e-05,
                 3.047373077663876e-05, 3.271432773325549e-05, 3.1362608301944375e-05, 3.176470536185219e-05,
                 4.283990079065152e-05, 5.730443048751228e-05]
    ps_notdrnotdws = [0.005860025839436064, 0.0018281133687233194, 0.0006545729569826583, 0.000322753582238024,
                      0.0002306116298858942, 0.00018563247819935335, 0.00012378451093559358, 9.9349105337524e-05,
                      8.651679275379038e-05, 5.730443048751228e-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_notdr, hatch='\\\\\\')
    plt.bar(x3, ps_notdws, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['PS', 'DWS', 'DR', 'PG'])
    # plt.title('SUE')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint2_oue_star():
    x1 = np.array([i for i in range(0, 50, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.0005667174441585008, 0.00015075219330465696, 7.71768570753118e-05, 4.337110617787501e-05,
          3.162163050766287e-05, 2.245877379007181e-05, 1.989529090646494e-05, 1.8665737264475058e-05,
          1.56446230725438e-05, 1.5172190073131789e-05]
    ps_notdr = [0.006562601640075787, 0.0010533277715431418, 0.00038385169849810364, 0.00018544190287092925,
                9.402836462747717e-05, 6.474603908578832e-05, 4.357976703302791e-05, 2.9074688731823814e-05,
                2.1841187471857902e-05, 1.5172190073131789e-05]
    ps_notdws = [0.0005667174441585008, 0.00015620738532501748, 8.322744061489873e-05, 4.6481283065871033e-05,
                 3.809779011738584e-05, 3.039350966285511e-05, 2.9731846848585675e-05, 3.7028620840556094e-05,
                 3.558449278044437e-05, 7.254766203282905e-05]
    ps_notdrnotdws = [0.006562601640075787, 0.0012595397436408196, 0.0006047286133104708, 0.00032157512257499664,
                      0.00024230054541023443, 0.00017293987996560122, 0.00011818954230169723, 0.00010152927716200038,
                      8.739639232900486e-05, 7.254766203282905e-05]

    plt.bar(x1, ps, label='PS')
    plt.bar(x2, ps_notdr, hatch='\\\\\\', label='DWS')
    plt.bar(x3, ps_notdws, hatch='///', label='DR')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx', label='PG')

    xpos = x1 + 1.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend()
    # plt.title('OUE')
    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'

    plt.savefig(name, dpi=300)
    plt.show()


def paint3_krr_star():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.0002712259441593701, 8.281229497269358e-05, 3.599481252619117e-05, 1.9028131227250198e-05,
            1.6272540212735228e-05, 1.1843325425442268e-05, 9.322640058581724e-06, 7.762373573326134e-06,
            7.578238337480316e-06, 7.37473823662628e-06]
    pr50 = [0.00084345278799684, 0.00022924601009311702, 9.852213454153545e-05, 6.431097564460184e-05,
            4.284362873093019e-05, 3.22240913664544e-05, 2.5352740514152568e-05, 2.0244317800815094e-05,
            1.7091415584305053e-05, 1.8066685950696637e-05]
    pr66 = [0.0018371333511195288, 0.00046990904995612606, 0.00020840926874671675, 0.00011092504451389584,
            7.678557505156895e-05, 5.5587912900985696e-05, 4.806477118338653e-05, 3.538784047016944e-05,
            3.207061170012021e-05, 3.0506843812784425e-05]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint3_sue_star():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.0006049343144219709, 0.00015247461038627453, 8.553755814495844e-05, 4.5658393491074565e-05,
            2.7190194336230968e-05, 2.4353129343537764e-05, 2.08606889224545e-05, 1.7083347250206517e-05,
            1.4955145774252685e-05, 1.4977476464044098e-05]
    pr50 = [0.0009882687401553498, 0.000266932617092142, 0.0001249415066982714, 8.162117793771649e-05,
            5.5127089899955924e-05, 3.8258370737463724e-05, 3.353018179950698e-05, 3.090192396737877e-05,
            2.6199933475148522e-05, 2.3411441617618322e-05]
    pr66 = [0.0013668767098869124, 0.00037248568421901286, 0.00015675056491732978, 0.00011071078573871747,
            7.496220418310302e-05, 5.891308192208175e-05, 4.5979541892519356e-05, 3.9748018276517926e-05,
            3.322838509473911e-05, 3.0761182800959346e-05]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint3_oue_star():
    level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pr33 = [0.0005667174441585008, 0.00015075219330465696, 7.71768570753118e-05, 4.337110617787501e-05,
            3.162163050766287e-05, 2.245877379007181e-05, 1.989529090646494e-05, 1.8665737264475058e-05,
            1.56446230725438e-05, 1.5172190073131789e-05]
    pr50 = [0.000953451578197539, 0.00023911232767187635, 0.0001138252296465341, 7.869865726417664e-05,
            5.267511910582364e-05, 4.339338745632077e-05, 2.9496844403050835e-05, 3.104367210066743e-05,
            2.62613255170578e-05, 2.6047129419718164e-05]
    pr66 = [0.001332062236149945, 0.0003165374010668086, 0.00017216585159897008, 9.669932038837859e-05,
            7.125880030324452e-05, 5.4300981699514016e-05, 4.4374283186740787e-05, 4.185123686179423e-05,
            3.4192828804419925e-05, 3.381085579211158e-05]
    plt.plot(level, pr33, '^-', label='33%')
    plt.plot(level, pr50, 'v--', label='50%')
    plt.plot(level, pr66, 'o-.', label='66%')

    plt.semilogy()
    # plt.semilogx()
    plt.xticks(level)

    plt.xlabel('epsilon')
    plt.ylabel('MSE')
    plt.legend()
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_krr_star():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = []
    truep = []
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('KRR')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_sue_star():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = []
    truep = []
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def paint4_oue_star():
    x1 = np.array([i for i in range(0, 30, 3)])
    x2 = np.array([i for i in range(1, 31, 3)])

    y1 = []
    truep = []
    plt.bar(x1, y1, hatch='///')
    plt.bar(x2, truep, hatch='\\\\\\')

    xpos = x1 + 0.5
    xlabel = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7', 'level8', 'level9', 'level10']
    plt.xticks(xpos, xlabel)
    plt.semilogy()

    plt.legend(['with estimate probability', 'with true probability'])

    plt.xlabel('privacy level')
    plt.ylabel('MSE')
    # plt.title('OUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


# paint1_krr_job()
# paint1_sue_job()
# paint1_oue_job()
# paint1_krr_star()
# paint1_sue_star()
# paint1_oue_star()
#
# paint2_krr_job()
# paint2_sue_job()
# paint2_oue_job()
# paint2_krr_star()
# paint2_sue_star()
# paint2_oue_star()
#
# paint3_krr_job()
# paint3_sue_job()
# paint3_oue_job()
# paint3_krr_star()
# paint3_sue_star()
# paint3_oue_star()
# paint3_oue_star()
#
# run66pr()

# data =Data('./data/kosarak.dat')
# time1 = time.time()
# data=[]
# with open('./data/drugname.csv', 'r') as f:
#     for line in f.readlines():
#         # 移除头尾换行符
#         line = line.strip()
#         data.append(line)
# s = set(data)
# s = list(s)
# print(len(s))
#
# with open('./data/drugnamenumber.csv', 'w') as f:
#     f_csv = csv.writer(f)
#     for x in data:
#         number = s.index(x) + 1
#
#         f_csv.writerow([number])
# print(time.time()-time1)
# exit(0)


# time1 = time.time()
# # data = Data("data/test.txt")
# data = Data('./data/drugnamenumber.csv')
# # data = Data("./data/e-shop clothing 2008.csv")
#
#
#
# print(len(data.domain))
# print(len(data.data))
# xs = list(range(1, 1837))
# xn = list(range(1837, 3673))
# level_epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
# print(data.domain)
# print(xs)
# print(xn)
# print('OLH')
# # for level_i in range(1, len(level_epsilon) + 1, 1):
# for level_i in level_epsilon:
#     print('level_i=', level_i)
#     u_mse = 0
#     replication = 1
#
#     for i in range(replication):
#         u = USUE(level_i, data.domain, data.data,xs,xn)
#         u.run()
#         print(time.time() - time1)
#         u.estimate(u.per_data)
#         u_mse += get_mse(u.es_data, data.true_p)
#     u_mse /= replication
#     print('u_mse=', u_mse)
#     print(time.time() - time1)

#################################
# 密码学报实验图
def olh_exp1_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    ukrr = [0.086692913, 0.016629349, 0.006126493, 0.002708243, 1.43E-03, 7.87E-04, 4.54E-04, 2.85E-04, 1.74E-04,
            1.10E-04]
    usue = [0.000238721, 5.58E-05, 2.60E-05, 1.47E-05, 8.65E-06, 6.32E-06, 4.45E-06, 3.24E-06, 2.63E-06, 1.99E-06]
    uolh = [0.000212328, 5.52E-05, 2.29E-05, 1.20E-05, 8.72E-06, 5.60E-06, 3.91E-06, 2.97E-06, 2.17E-06, 1.77E-06]

    plt.plot(epsilon, ukrr, 'o-.', label='uRR')
    plt.plot(epsilon, usue, 'o--', label='uRAP')
    plt.plot(epsilon, uolh, 'o-', label='uOLH')
    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=20)
    # 避免图片显示不全
    plt.tight_layout()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def olh_exp1_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    ukrr = [0.051684273, 0.012212836, 0.003669188, 0.001731097, 9.35E-04, 4.58E-04, 2.48E-04, 1.84E-04, 1.22E-04,
            6.41E-05]
    usue = [0.000493598, 0.000136757, 5.63E-05, 3.09E-05, 1.92E-05, 1.54E-05, 1.04E-05, 7.69E-06, 6.57E-06, 4.52E-06]
    uolh = [0.000515926, 0.000133609, 5.18E-05, 3.13E-05, 1.35E-05, 1.15E-05, 7.50E-06, 4.63E-06, 3.74E-06, 3.30E-06]

    plt.plot(epsilon, ukrr, 'o-.', label='uRR')
    plt.plot(epsilon, usue, 'o--', label='uRAP')
    plt.plot(epsilon, uolh, 'o-', label='uOLH')
    plt.semilogy()
    # plt.semilogx()
    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=20)
    # plt.title('SUE')
    # 避免图片显示不全
    plt.tight_layout()

    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def olh_exp2_drug():
    x1 = [i for i in range(0, 30, 3)]
    x2 = [i for i in range(1, 31, 3)]

    pg = [0.002236883, 0.000602526, 0.000261092, 0.000124306, 7.29E-05, 5.04E-05, 3.30E-05, 2.49E-05, 1.66E-05,
          1.38E-05]
    personal = [0.002236883, 0.000470381, 0.000173324, 7.53E-05, 3.72E-05, 2.12E-05, 1.30E-05, 8.41E-06, 5.68E-06,
                4.14E-06]

    plt.bar(x1, pg, label='uOLH')
    plt.bar(x2, personal, hatch='///', label='uOLH-DWC')

    xpos = []
    for i in x1:
        xpos.append(i + 0.5)
    print(xpos)
    plt.semilogy()
    plt.xticks(xpos, list(range(1, 11)), fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylabel('MSE', fontsize=20)
    plt.xlabel('level', fontsize=20)
    plt.legend(fontsize=20)
    # 避免图片显示不全
    plt.tight_layout()

    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def olh_exp2_nor():
    x1 = [i for i in range(0, 30, 3)]
    x2 = [i for i in range(1, 31, 3)]

    pg = [0.005700094, 0.001234235, 0.00057077, 0.00024808, 0.000163003, 9.53E-05, 6.94E-05, 6.27E-05, 3.89E-05,
          2.83E-05]
    personal = [0.005700094, 0.001027327, 0.000397796, 0.000158907, 8.20E-05, 4.28E-05, 2.77E-05, 1.95E-05, 1.36E-05,
                9.70E-06]

    plt.bar(x1, pg, label='uOLH')
    plt.bar(x2, personal, hatch='///', label='uOLH-DWC')

    xpos = []
    for i in x1:
        xpos.append(i + 0.5)
    print(xpos)
    plt.semilogy()
    plt.xticks(xpos, list(range(1, 11)), fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylabel('MSE', fontsize=20)
    plt.xlabel('level', fontsize=20)
    plt.legend(fontsize=20)
    # 避免图片显示不全
    plt.tight_layout()

    name = sys._getframe().f_code.co_name
    name = './picture/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


##############################################
# 毕业论文实验图
#  plt.plot(epsilon, data_u, '^-', label='ULDP')
#     plt.plot(epsilon, data_level1, 'v--', label='level1')
#     plt.plot(epsilon, data_level2, 'o-.', label='level2')
#     plt.plot(epsilon, data_level3, '<:', label='level3')
#     plt.plot(epsilon, data_level4, '>-', label='level4')
#     plt.plot(epsilon, data_level5, '1--', label='level5')
#     plt.plot(epsilon, data_level6, '2-.', label='level6')
#     plt.plot(epsilon, data_level7, '3:', label='level7')
#     plt.plot(epsilon, data_level8, '4-', label='level8')
#     plt.plot(epsilon, data_level9, '*--', label='level9')
#     plt.plot(epsilon, data_level10, 'p-.', label='level10')

# 第三章实验，比较多个uldp协议在不同隐私预算之间的差别
def exp1_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    uRR = [0.055162457, 0.010592182, 0.004280698, 0.001934741, 0.000987274, 0.000441978, 0.000285671, 0.000161577,
           0.000103691, 6.41E-05]
    uRAP = [0.00055412, 0.000135874, 5.89E-05, 3.33E-05, 2.12E-05, 1.46E-05, 1.10E-05, 8.57E-06, 6.72E-06, 4.92E-06]
    uOUE = [0.000494492, 0.000129531, 5.41E-05, 3.08E-05, 1.78E-05, 1.29E-05, 9.20E-06, 7.00E-06, 4.93E-06, 3.59E-06]
    uOLH = [0.000531872, 0.000149897, 7.41E-05, 3.62E-05, 2.45E-05, 1.50E-05, 1.17E-05, 8.62E-06, 6.41E-06, 4.95E-06]
    uBLH = [0.000538534, 0.000146536, 7.54E-05, 4.23E-05, 3.17E-05, 2.52E-05, 2.04E-05, 1.75E-05, 1.57E-05, 1.37E-05]

    plt.plot(epsilon, uRR, 'o-.', label='uRR')
    plt.plot(epsilon, uRAP, 'o--', label='uRAP')
    plt.plot(epsilon, uOUE, 'v--', label='uOUE')
    plt.plot(epsilon, uOLH, '>-', label='uOLH')
    plt.plot(epsilon, uBLH, '<:', label='uBLH')
    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=13)
    # 避免图片显示不全
    plt.tight_layout()
    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp1_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    uRR = [1.42E-04, 4.81E-05, 1.42E-05, 1.05E-05, 9.17E-06, 4.38E-06, 2.67E-06, 1.66E-06, 1.26E-06, 8.81E-07]
    uRAP = [0.000261946, 6.16E-05, 3.17E-05, 1.39E-05, 7.45E-06, 7.18E-06, 6.56E-06, 3.61E-06, 3.44E-06, 2.46E-06]
    uOUE = [2.40E-04, 5.20E-05, 3.31E-05, 1.52E-05, 1.02E-05, 7.66E-06, 4.52E-06, 3.35E-06, 3.52E-06, 2.44E-06]
    uOLH = [0.000388884, 0.000252751, 2.32E-04, 6.21E-05, 5.78E-05, 5.19E-05, 1.76E-05, 1.55E-05, 9.23E-06, 1.39E-05]
    uBLH = [0.00048791, 0.000316076, 2.38E-04, 2.22E-04, 2.44E-04, 2.42E-04, 2.19E-04, 2.12E-04, 2.00E-04, 2.15E-04]

    plt.plot(epsilon, uRR, 'o-.', label='uRR')
    plt.plot(epsilon, uRAP, 'o--', label='uRAP')
    plt.plot(epsilon, uOUE, 'v--', label='uOUE')
    plt.plot(epsilon, uOLH, '>-', label='uOLH')
    plt.plot(epsilon, uBLH, '<:', label='uBLH')
    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=13)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


# 第三章，敏感数据比例对mse的影响
def exp2_uRR_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.055162457, 0.010592182, 0.004280698, 0.001934741, 0.000987274, 0.000441978, 0.000285671, 0.000161577,
            0.000103691, 6.41E-05]
    xs33 = [0.024560459, 0.004717572, 1.73E-03, 7.67E-04, 4.08E-04, 2.16E-04, 1.21E-04, 7.16E-05, 4.85E-05, 2.81E-05]
    xs66 = [0.093180181, 0.019573197, 6.79E-03, 3.03E-03, 1.55E-03, 8.69E-04, 5.01E-04, 3.00E-04, 1.86E-04, 1.17E-04]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uRAP_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.00055412, 0.000135874, 5.89E-05, 3.33E-05, 2.12E-05, 1.46E-05, 1.10E-05, 8.57E-06, 6.72E-06, 4.92E-06]
    xs33 = [0.000359164, 9.09E-05, 3.97E-05, 2.18E-05, 1.42E-05, 9.12E-06, 6.69E-06, 4.98E-06, 4.04E-06, 3.39E-06]
    xs66 = [0.000696079, 0.000173259, 7.80E-05, 4.30E-05, 2.72E-05, 1.93E-05, 1.35E-05, 1.04E-05, 8.19E-06, 6.33E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uOUE_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.000494492, 0.000129531, 5.41E-05, 3.08E-05, 1.78E-05, 1.29E-05, 9.20E-06, 7.00E-06, 4.93E-06, 3.59E-06]
    xs33 = [0.000343341, 8.13E-05, 3.95E-05, 1.99E-05, 1.25E-05, 8.47E-06, 6.22E-06, 4.48E-06, 3.42E-06, 2.41E-06]
    xs66 = [0.00067911, 0.000175904, 7.06E-05, 3.86E-05, 2.62E-05, 1.73E-05, 1.20E-05, 8.51E-06, 6.75E-06, 4.56E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uOLH_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.000531872, 0.000149897, 7.41E-05, 3.62E-05, 2.45E-05, 1.50E-05, 1.17E-05, 8.62E-06, 6.41E-06, 4.95E-06]
    xs33 = [0.000311135, 0.000112363, 5.34E-05, 2.80E-05, 1.87E-05, 1.14E-05, 8.59E-06, 6.50E-06, 4.56E-06, 4.21E-06]
    xs66 = [0.000810441, 0.000190214, 9.26E-05, 5.01E-05, 2.68E-05, 1.77E-05, 1.48E-05, 1.08E-05, 7.47E-06, 5.63E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uBLH_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.000538534, 0.000146536, 7.54E-05, 4.23E-05, 3.17E-05, 2.52E-05, 2.04E-05, 1.75E-05, 1.57E-05, 1.37E-05]
    xs33 = [0.000298513, 0.000116093, 5.36E-05, 3.10E-05, 2.40E-05, 1.86E-05, 1.53E-05, 1.34E-05, 1.18E-05, 1.16E-05]
    xs66 = [0.000711596, 0.000212791, 8.02E-05, 5.07E-05, 4.16E-05, 2.88E-05, 2.32E-05, 1.84E-05, 1.57E-05, 1.68E-05]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uRR_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [1.42E-04, 4.81E-05, 1.42E-05, 1.05E-05, 9.17E-06, 4.38E-06, 2.67E-06, 1.66E-06, 1.26E-06, 8.81E-07]
    xs33 = [6.47E-05, 1.65E-05, 7.73E-06, 4.00E-06, 2.68E-06, 1.41E-06, 1.33E-06, 6.15E-07, 6.91E-07, 4.52E-07]
    xs66 = [0.000571582, 9.89E-05, 4.48E-05, 1.39E-05, 1.03E-05, 5.41E-06, 4.48E-06, 3.11E-06, 1.89E-06, 1.70E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uRAP_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.000261946, 6.16E-05, 3.17E-05, 1.39E-05, 7.45E-06, 7.18E-06, 6.56E-06, 3.61E-06, 3.44E-06, 2.46E-06]
    xs33 = [1.28E-04, 2.36E-05, 1.19E-05, 1.03E-05, 6.36E-06, 5.37E-06, 3.86E-06, 2.06E-06, 2.09E-06, 2.00E-06]
    xs66 = [0.000333474, 7.07E-05, 3.70E-05, 2.00E-05, 1.45E-05, 8.50E-06, 8.72E-06, 4.44E-06, 4.03E-06, 3.60E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uOUE_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [2.40E-04, 5.20E-05, 3.31E-05, 1.52E-05, 1.02E-05, 7.66E-06, 4.52E-06, 3.35E-06, 3.52E-06, 2.44E-06]
    xs33 = [1.42E-04, 3.06E-05, 1.02E-05, 9.65E-06, 5.82E-06, 4.40E-06, 3.80E-06, 2.70E-06, 2.07E-06, 1.70E-06]
    xs66 = [0.000297434, 8.27E-05, 4.66E-05, 2.24E-05, 1.40E-05, 9.59E-06, 6.78E-06, 5.30E-06, 3.93E-06, 3.41E-06]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uOLH_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.000388884, 0.000252751, 2.32E-04, 6.21E-05, 5.78E-05, 5.19E-05, 1.76E-05, 1.55E-05, 9.23E-06, 1.39E-05]
    xs33 = [0.00033655, 0.000222913, 1.89E-04, 2.23E-05, 1.49E-05, 5.45E-05, 9.73E-06, 1.10E-05, 5.87E-06, 9.79E-06]
    xs66 = [0.000648326, 0.000311178, 2.86E-04, 1.37E-04, 1.19E-04, 7.20E-05, 1.97E-05, 2.01E-05, 1.41E-05, 2.26E-05]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp2_uBLH_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    xs50 = [0.00048791, 0.000316076, 2.38E-04, 2.22E-04, 2.44E-04, 2.42E-04, 2.19E-04, 2.12E-04, 2.00E-04, 2.15E-04]
    xs33 = [0.000353559, 0.000215196, 2.05E-04, 2.07E-04, 2.00E-04, 1.96E-04, 2.08E-04, 2.04E-04, 1.85E-04, 1.94E-04]
    xs66 = [0.000510307, 0.000351633, 2.58E-04, 2.65E-04, 2.50E-04, 2.58E-04, 2.70E-04, 2.38E-04, 2.58E-04, 2.41E-04]
    plt.plot(epsilon, xs50, 'o-.', label='50%')
    plt.plot(epsilon, xs33, 'v--', label='33%')
    plt.plot(epsilon, xs66, '>-', label='66%')

    plt.semilogy()

    plt.xticks(epsilon, fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = '$\epsilon$'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=18)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


# 第四章中那四个柱状图
def exp3_uRR_nor():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.052060807,
          0.011664218,
          0.004612216,
          0.002422067,
          0.001223311,
          0.000811298,
          0.000538628,
          0.000392639,
          0.0002772,
          0.000253219]
    ps_withdws = [0.505608553,
                  0.088124051,
                  0.026990994,
                  0.00961725,
                  0.004609188,
                  0.002399891,
                  0.001391673,
                  0.000753613,
                  0.000393472,
                  0.000253219]
    ps_withdr = [0.052060807,
                 0.012069806,
                 0.004726867,
                 0.002624746,
                 0.001383112,
                 0.000921843,
                 0.000665689,
                 0.00052124,
                 0.000490892,
                 0.000695108]
    ps_notdrnotdws = [0.505608553,
                      0.105823515,
                      0.036727464,
                      0.016717205,
                      0.008246638,
                      0.004590112,
                      0.003003263,
                      0.001674068,
                      0.001057904,
                      0.000695108]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos=[-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
             '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level',fontsize=20)
    plt.ylabel('MSE',fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'],fontsize=18)


    # 避免图片显示不全
    plt.tight_layout()

    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uRAP_nor():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000475145,
          0.000133523,
          6.89E-05,
          4.01E-05,
          2.91E-05,
          2.07E-05,
          1.90E-05,
          1.60E-05,
          1.29E-05,
          1.29E-05]
    ps_withdws = [0.004963873,
                  0.001063573,
                  0.000359485,
                  0.000177081,
                  9.61E-05,
                  5.61E-05,
                  3.66E-05,
                  2.48E-05,
                  1.73E-05,
                  1.29E-05]
    ps_withdr = [0.000475145,
                 0.000137032,
                 7.46E-05,
                 4.55E-05,
                 3.52E-05,
                 2.82E-05,
                 2.66E-05,
                 2.72E-05,
                 3.00E-05,
                 5.48E-05]
    ps_notdrnotdws = [0.004963873,
                      0.001364121,
                      0.000556496,
                      0.000312444,
                      0.000214397,
                      0.000147829,
                      9.63E-05,
                      7.93E-05,
                      6.24E-05,
                      5.48E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uOUE_nor():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000509227,
          0.000130692,
          7.11E-05,
          4.24E-05,
          2.38E-05,
          1.91E-05,
          1.49E-05,
          1.33E-05,
          1.17E-05,
          1.12E-05]
    ps_withdws = [0.005174606,
                  0.00102556,
                  0.000376523,
                  0.000171876,
                  8.23E-05,
                  5.22E-05,
                  3.50E-05,
                  2.01E-05,
                  1.50E-05,
                  1.12E-05]
    ps_withdr = [0.000509227,
                 0.000132786,
                 7.59E-05,
                 4.61E-05,
                 2.94E-05,
                 2.54E-05,
                 2.10E-05,
                 2.41E-05,
                 2.53E-05,
                 3.82E-05]
    ps_notdrnotdws = [0.005174606,
                      0.001221674,
                      0.000574698,
                      0.000306809,
                      0.000181279,
                      0.000138223,
                      8.42E-05,
                      6.02E-05,
                      4.89E-05,
                      3.82E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uOLH_nor():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000577169,
          0.000131337,
          7.44E-05,
          4.79E-05,
          3.12E-05,
          2.95E-05,
          2.52E-05,
          2.07E-05,
          1.81E-05,
          1.79E-05]
    ps_withdws = [0.005738132,
                  0.001044014,
                  0.000431001,
                  0.000217217,
                  0.000109733,
                  7.80E-05,
                  5.17E-05,
                  3.10E-05,
                  2.42E-05,
                  1.79E-05]
    ps_withdr = [0.000577169,
                 0.000132634,
                 7.96E-05,
                 5.24E-05,
                 3.98E-05,
                 3.36E-05,
                 3.38E-05,
                 3.53E-05,
                 4.19E-05,
                 7.75E-05]
    ps_notdrnotdws = [0.005738132,
                      0.001336066,
                      0.000635298,
                      0.000420065,
                      0.000263956,
                      0.00017483,
                      0.000137673,
                      0.000113272,
                      9.67E-05,
                      7.75E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')

    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uBLH_nor():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000609681,
          0.0001565,
          8.89E-05,
          5.78E-05,
          4.20E-05,
          3.54E-05,
          3.12E-05,
          2.78E-05,
          2.73E-05,
          2.83E-05]
    ps_withdws = [0.005450695,
                  0.001173532,
                  0.000478666,
                  0.000192562,
                  0.000111258,
                  7.56E-05,
                  5.70E-05,
                  4.51E-05,
                  3.34E-05,
                  2.83E-05]
    ps_withdr = [0.000609681,
                 0.00015737,
                 0.000100012,
                 7.02E-05,
                 5.25E-05,
                 4.65E-05,
                 4.57E-05,
                 5.42E-05,
                 6.58E-05,
                 0.000102558]
    ps_notdrnotdws = [0.005450695,
                      0.001556515,
                      0.000772984,
                      0.000409362,
                      0.000261897,
                      0.000209977,
                      0.000151685,
                      0.000192407,
                      0.000116723,
                      0.000102558]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uRR_drug():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000238104,
          4.08E-05,
          2.77E-05,
          1.28E-05,
          7.90E-06,
          5.39E-06,
          4.56E-06,
          3.66E-06,
          3.09E-06,
          3.09E-06]
    ps_withdws = [0.001459066,
                  0.00033326,
                  0.000145876,
                  6.62E-05,
                  3.67E-05,
                  1.25E-05,
                  9.28E-06,
                  6.11E-06,
                  3.78E-06,
                  3.09E-06]
    ps_withdr = [0.000238104,
                 4.36E-05,
                 2.96E-05,
                 1.62E-05,
                 9.45E-06,
                 7.68E-06,
                 6.97E-06,
                 6.57E-06,
                 9.00E-06,
                 1.08E-05]
    ps_notdrnotdws = [0.001459066,
                      0.000475485,
                      0.000179712,
                      0.000146517,
                      8.49E-05,
                      3.96E-05,
                      2.46E-05,
                      2.76E-05,
                      1.54E-05,
                      1.08E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uRAP_drug():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.000225514,
          7.43E-05,
          2.91E-05,
          1.75E-05,
          1.06E-05,
          9.83E-06,
          8.90E-06,
          8.49E-06,
          7.81E-06,
          5.52E-06]
    ps_withdws = [0.00330407,
                  0.000648757,
                  0.000160879,
                  8.36E-05,
                  3.67E-05,
                  3.19E-05,
                  1.64E-05,
                  1.38E-05,
                  9.54E-06,
                  5.52E-06]
    ps_withdr = [0.000225514,
                 8.19E-05,
                 3.06E-05,
                 2.06E-05,
                 1.48E-05,
                 1.15E-05,
                 1.42E-05,
                 1.40E-05,
                 1.35E-05,
                 1.67E-05]
    ps_notdrnotdws = [0.00330407,
                      0.000729995,
                      0.000194997,
                      0.000149332,
                      6.95E-05,
                      6.65E-05,
                      4.53E-05,
                      4.08E-05,
                      3.07E-05,
                      1.67E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uOUE_drug():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.00028675,
          5.00E-05,
          2.80E-05,
          1.46E-05,
          1.29E-05,
          9.43E-06,
          9.09E-06,
          5.99E-06,
          5.84E-06,
          6.46E-06]
    ps_withdws = [0.002055436,
                  0.000466372,
                  0.000169074,
                  7.01E-05,
                  3.49E-05,
                  2.99E-05,
                  1.74E-05,
                  1.07E-05,
                  7.01E-06,
                  6.46E-06]
    ps_withdr = [0.00028675,
                 5.46E-05,
                 3.11E-05,
                 1.77E-05,
                 1.42E-05,
                 1.44E-05,
                 1.54E-05,
                 1.44E-05,
                 1.51E-05,
                 2.69E-05]
    ps_notdrnotdws = [0.002055436,
                      0.000504172,
                      0.000270958,
                      0.000147654,
                      9.06E-05,
                      7.66E-05,
                      4.92E-05,
                      4.12E-05,
                      3.22E-05,
                      2.69E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uOLH_drug():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.00026147,
          0.000128755,
          1.04E-04,
          8.39E-05,
          7.10E-05,
          6.44E-05,
          6.25E-05,
          5.89E-05,
          5.48E-05,
          5.78E-05]
    ps_withdws = [0.002659252,
                  0.000730243,
                  0.00031546,
                  0.000151918,
                  1.15E-04,
                  8.92E-05,
                  7.61E-05,
                  6.21E-05,
                  5.93E-05,
                  5.78E-05]
    ps_withdr = [0.00026147,
                 0.00012883,
                 1.11E-04,
                 9.16E-05,
                 7.53E-05,
                 6.46E-05,
                 6.71E-05,
                 7.16E-05,
                 6.40E-05,
                 8.73E-05]
    ps_notdrnotdws = [0.002659252,
                      0.000826766,
                      0.000566947,
                      0.000280812,
                      0.000190878,
                      0.000122442,
                      0.000127855,
                      0.000105809,
                      9.89E-05,
                      8.73E-05]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


def exp3_uBLH_drug():
    x1 = np.array([i for i in range(1, 51, 5)])
    x2 = x1 + 1
    x3 = x2 + 1
    x4 = x3 + 1

    ps = [0.00039322,
          0.000260486,
          2.29E-04,
          2.27E-04,
          2.34E-04,
          2.19E-04,
          2.20E-04,
          2.08E-04,
          2.22E-04,
          2.22E-04]
    ps_withdws = [0.00374728,
                  0.000658807,
                  0.000373837,
                  0.000292249,
                  0.000250012,
                  2.60E-04,
                  2.35E-04,
                  2.12E-04,
                  2.24E-04,
                  2.22E-04]
    ps_withdr = [0.00039322,
                 0.000267765,
                 0.000243357,
                 2.31E-04,
                 2.46E-04,
                 2.18E-04,
                 2.24E-04,
                 2.32E-04,
                 2.50E-04,
                 0.000274803]
    ps_notdrnotdws = [0.00374728,
                      0.000826807,
                      0.000641334,
                      0.000409083,
                      0.000305356,
                      0.000297665,
                      0.000269726,
                      0.000280203,
                      0.000285221,
                      0.000274803]

    plt.bar(x1, ps)
    plt.bar(x2, ps_withdws, hatch='\\\\\\')
    plt.bar(x3, ps_withdr, hatch='///')
    plt.bar(x4, ps_notdrnotdws, hatch='xxx')
    plt.semilogy()

    xpos = x1 + 1.5
    new_xpos = [-2]
    for x in xpos:
        new_xpos.append(x)

    new_xlabel = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']

    plt.xticks(new_xpos, new_xlabel, fontsize=18)
    plt.yticks(fontsize=18)

    plt.xlabel('privacy level', fontsize=20)
    plt.ylabel('MSE', fontsize=20)

    plt.legend(['PS', 'DWC', 'DR', 'PG'], fontsize=18)

    # 避免图片显示不全
    plt.tight_layout()
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=300)
    plt.show()


# 第四章总体图像
def exp4_drug():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    uRR = [0.000238104,
           4.08E-05,
           2.77E-05,
           1.28E-05,
           7.90E-06,
           5.39E-06,
           4.56E-06,
           3.66E-06,
           3.09E-06,
           3.09E-06]
    uRAP = [0.000225514,
            7.43E-05,
            2.91E-05,
            1.75E-05,
            1.06E-05,
            9.83E-06,
            8.90E-06,
            8.49E-06,
            7.81E-06,
            5.52E-06]
    uOUE = [0.00028675,
            5.00E-05,
            2.80E-05,
            1.46E-05,
            1.29E-05,
            9.43E-06,
            9.09E-06,
            5.99E-06,
            5.84E-06,
            6.46E-06]
    uOLH = [0.00026147,
            0.000128755,
            1.04E-04,
            8.39E-05,
            7.10E-05,
            6.44E-05,
            6.25E-05,
            5.89E-05,
            5.48E-05,
            5.78E-05]
    uBLH = [0.00039322,
            0.000260486,
            2.29E-04,
            2.27E-04,
            2.34E-04,
            2.19E-04,
            2.20E-04,
            2.08E-04,
            2.22E-04,
            2.22E-04]

    plt.plot(epsilon, uRR, 'o-.', label='PSuRR')
    plt.plot(epsilon, uRAP, 'o--', label='PSuRAP')
    plt.plot(epsilon, uOUE, 'v--', label='PSuOUE')
    plt.plot(epsilon, uOLH, '>-', label='PSuOLH')
    plt.plot(epsilon, uBLH, '<:', label='PSuBLH')
    plt.semilogy()

    xtick = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']
    new_epsilon=[0,0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    plt.xticks(new_epsilon, xtick,fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = 'privacy level'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=13)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()


def exp4_nor():
    epsilon = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    uRR = [0.052060807,
           0.011664218,
           0.004612216,
           0.002422067,
           0.001223311,
           0.000811298,
           0.000538628,
           0.000392639,
           0.0002772,
           0.000253219]
    uRAP = [0.000475145,
            0.000133523,
            6.89E-05,
            4.01E-05,
            2.91E-05,
            2.07E-05,
            1.90E-05,
            1.60E-05,
            1.29E-05,
            1.29E-05]
    uOUE = [0.000509227,
            0.000130692,
            7.11E-05,
            4.24E-05,
            2.38E-05,
            1.91E-05,
            1.49E-05,
            1.33E-05,
            1.17E-05,
            1.12E-05]
    uOLH = [0.000577169,
            0.000131337,
            7.44E-05,
            4.79E-05,
            3.12E-05,
            2.95E-05,
            2.52E-05,
            2.07E-05,
            1.81E-05,
            1.79E-05]
    uBLH = [0.000609681,
            0.0001565,
            8.89E-05,
            5.78E-05,
            4.20E-05,
            3.54E-05,
            3.12E-05,
            2.78E-05,
            2.73E-05,
            2.83E-05]

    plt.plot(epsilon, uRR, 'o-.', label='PSuRR')
    plt.plot(epsilon, uRAP, 'o--', label='PSuRAP')
    plt.plot(epsilon, uOUE, 'v--', label='PSuOUE')
    plt.plot(epsilon, uOLH, '>-', label='PSuOLH')
    plt.plot(epsilon, uBLH, '<:', label='PSuBLH')
    plt.semilogy()

    xtick = ['level:\n$\epsilon$:', '1\n0.2', '2\n0.4', '3\n0.6', '4\n0.8', '5\n1.0', '6\n1.2', '7\n1.4', '8\n1.6',
                  '9\n1.8', '10\n2.0']
    new_epsilon=[0,0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    plt.xticks(new_epsilon, xtick,fontsize=18)
    plt.yticks(fontsize=18)

    xlabel = 'privacy level'
    ylabel = 'MSE'
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=13)
    # 避免图片显示不全
    plt.tight_layout()

    # plt.title('SUE')
    name = sys._getframe().f_code.co_name
    name = './picture2/' + name + '.eps'
    plt.savefig(name, dpi=600)
    plt.show()

#陈冰写的函数，我检验一下
def chen_olh():
    # 简单数据集
    # data = np.concatenate(([1] * 80000, [2] * 10000, [3] * 10000, [4] * 5000, [5] * 10000, [6] * 5000, [7] * 2000, [8] * 3000))
    data = np.concatenate(([1000] * 20000, [1001] * 20000, [1002] * 10000, [1003] * 5000, [1004] * 10000, [1005] * 5000,
                           [1006] * 2000, [1007] * 3000))
    # data = np.concatenate(([1000] * 20000, [1001] * 20000, [1002] * 10000, [1003] * 5000, [1004] * 10000, [1005] * 5000, [1006] * 2000, [1007] * 3000, [1008] * 2000, [1009] * 2000))
    # 数据集真实频率
    original_freq = list(Counter(data).values())
    for i in range(len(original_freq)):
        original_freq[i] = original_freq[i] / len(data)
    # print("original_freq", original_freq)

    # 实验参数
    epsilon = 10
    domain = [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007]
    # domain = [1,2,3,4,5,6,7,8]

    # Optimal Local Hashing (OLH)
    run_olh = OLH(epsilon, domain, data)
    # run_uolh = uOLH(epsilon, domain, data)

    # Simulate server-side estimation
    olh_estimates = run_olh.run()
    # uolh_estimates = run_uolh.run()
    # print("olh_estimates", olh_estimates)
    # print("olh_estimates", uolh_estimates)

    # 方差
    mse = 0
    umse = 0

    # ------------------------------ Experiment Output (calculating variance) -------------------------

    for i in range(0, len(domain)):
        mse += (olh_estimates[i] - original_freq[i]) ** 2
    mse = mse / len(domain)

    # for i in range(0, len(domain)):
    #     umse += (uolh_estimates[i] - original_freq[i]) ** 2
    # umse = umse / len(domain)

    print("\n")
    print("Experiment run on a dataset of size", len(data), "with d=", len(domain), "and epsilon=", epsilon, "\n")
    print("Optimised Local Hashing (OLH) Variance: ", mse)
    print("Optimised Local Hashing (uOLH) Variance: ", umse)

    print("\n")
    print("Original Frequencies:", original_freq)
    print("OLH Estimates:", olh_estimates)
    # print("uOLH Estimates:", uolh_estimates)
    print("Note: We round estimates to the nearest integer")

    a1 =0
    a2 = 0
    for x in original_freq:
        a1+=x
    for x in olh_estimates:
        a2+= x
    print(a1,a2)

    print("OLH Estimates:", olh_estimates/a2)
    temp = 0
    for x in olh_estimates/a2:
        temp+=x
    print(temp)

# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus']=False
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.rcParams['axes.unicode_minus']=False

# matplotlib.rcParams.update(
# {
# 'text.usetex': False,
# 'font.family': 'stixgeneral',
# 'mathtext.fontset': 'stix',
# }
# )

# olh_exp1_drug()
# olh_exp1_nor()
# olh_exp2_drug()
# olh_exp2_nor()

# d=3672
# print(np.log2(d))
# print(d)
# print(np.log2(d/2+np.exp(2)+1),np.log2(512))
# print(np.log2(d/2+np.exp(2)+1),np.log2(512),np.log2(10))

# 第三章不同uldp协议的mse表现形式
# exp1_drug()
# exp1_nor()


# 第三章敏感数据比例对mse的影响
# exp2_uRR_nor()
# exp2_uRAP_nor()
# exp2_uOUE_nor()
# exp2_uOLH_nor()
# exp2_uBLH_nor()
# exp2_uRR_drug()
# exp2_uRAP_drug()
# exp2_uOUE_drug()
# exp2_uOLH_drug()
# exp2_uBLH_drug()


# 第四章，每个协议一个柱状图
# exp3_uRR_nor()
# exp3_uRAP_nor()
# exp3_uOUE_nor()
# exp3_uOLH_nor()
# exp3_uBLH_nor()
# exp3_uRR_drug()
# exp3_uRAP_drug()
# exp3_uOUE_drug()
# exp3_uOLH_drug()
# exp3_uBLH_drug()

#第四章，总体情况
# exp4_drug()
# exp4_nor()

#
# g1 = (np.exp(0.2) + 1)
# print(g1)
# g2 = (np.exp(1) + 1)
# print(g2)
# g3 = (np.exp(2) + 1)
# print(g3)
# g4 = 2
#
# print(math.log2(g1+5)+math.log2(512))
# print(math.log2(g2+5)+math.log2(512))
# print(math.log2(g3+5)+math.log2(512))
#
# print(math.log2(g4+5)+math.log2(512))

# run66pr()

chen_olh()