import numpy as np
import time
from typing import List

from data_processing import Data
from LDP.krr import *
from LDP.sue import *
from LDP.oue import *
from ULDP.ukrr import *
from ULDP.usue import *
from ULDP.uoue import *
from PSULDP.pskrr import *
from PSULDP.pssue import *
from PSULDP.psoue import *
import matplotlib.pyplot as plt


# def run_sue():
#     # url = 'data/kosarak.dat'
#     url = 'data/bank-additional-full.csv'
#     data = Data(url)
#     print('time1', time.time() - time_start)
#     # data.show_data_information()
#
#     # # 计算真实概率
#     # get_true(data, url)
#
#     # 假定有h个隐私级别
#     h = 5
#     epsilon_list = [1.0, 2.0, 3.0, 4.0, 5.0]
#     xs = [1, 2, 3, 4, 5, 6]
#     xn = [7, 8, 9, 10, 11, 12]
#
#     usue1 = ULDPSUE(data, epsilon_list[0], xs, xn)
#     usue2 = ULDPSUE(data, epsilon_list[1], xs, xn)
#     usue3 = ULDPSUE(data, epsilon_list[2], xs, xn)
#     usue4 = ULDPSUE(data, epsilon_list[3], xs, xn)
#     usue5 = ULDPSUE(data, epsilon_list[4], xs, xn)
#
#     rs1 = [0 for _ in range(len(data.domain))]
#     rs2 = [0 for _ in range(len(data.domain))]
#     rs3 = [0 for _ in range(len(data.domain))]
#     rs4 = [0 for _ in range(len(data.domain))]
#     rs5 = [0 for _ in range(len(data.domain))]
#
#     print('time2', time.time() - time_start)
#     #  记录每个隐私级别下有多少人数
#     n_list = [0 for _ in range(h)]
#     with open(url, 'r') as f:
#         for line in f.readlines():
#             # 移除头尾换行符
#             line = line.strip()
#             # 将一行中的数字划分开
#             linelist = line.split(' ')
#             x = int(linelist[0])
#
#             # 用户随机选择隐私级别
#             level = np.random.randint(1, 6)
#             if level == 1:
#                 encode_x = usue1.encode(x)
#                 per_x = usue1.perturb(encode_x)
#                 for i in range(len(data.domain)):
#                     rs1[i] += per_x[i]
#                 n_list[level - 1] += 1
#             elif level == 2:
#                 encode_x = usue2.encode(x)
#                 per_x = usue2.perturb(encode_x)
#                 for i in range(len(data.domain)):
#                     rs2[i] += per_x[i]
#                 n_list[level - 1] += 1
#             elif level == 3:
#                 encode_x = usue3.encode(x)
#                 per_x = usue3.perturb(encode_x)
#                 for i in range(len(data.domain)):
#                     rs3[i] += per_x[i]
#                 n_list[level - 1] += 1
#             elif level == 4:
#                 encode_x = usue4.encode(x)
#                 per_x = usue4.perturb(encode_x)
#                 for i in range(len(data.domain)):
#                     rs4[i] += per_x[i]
#                 n_list[level - 1] += 1
#             elif level == 5:
#                 encode_x = usue5.encode(x)
#                 per_x = usue5.perturb(encode_x)
#                 for i in range(len(data.domain)):
#                     rs5[i] += per_x[i]
#                 n_list[level - 1] += 1
#             else:
#                 print('怎么会执行到这一步呢1')
#     print('time3', time.time() - time_start)
#     rs1 = usue1.estimation(rs1, n_list[0])
#     rs2 = usue2.estimation(rs2, n_list[1])
#     rs3 = usue3.estimation(rs3, n_list[2])
#     rs4 = usue4.estimation(rs4, n_list[3])
#     rs5 = usue5.estimation(rs5, n_list[4])
#     # print(get_mse(rs1, true_p_bank))
#     # print(get_mse(rs2, true_p_bank))
#     # print(get_mse(rs3, true_p_bank))
#     # print(get_mse(rs4, true_p_bank))
#     # print(get_mse(rs5, true_p_bank))
#     print('time4', time.time() - time_start)
#     fxn = \
#         0.07099155093716616 + 0.024618821015829854 + 0.03450033990482665 + \
#         0.02124405166553365 + 0.008012042342429833 + 0.03535010197144799
#     fxn1 = 0
#     for i in range(6, 12):
#         fxn1 += rs5[i]
#     dws = DWS(data, h, epsilon_list, xs, xn, n_list, fxn)
#     dws.getw()
#     rs = dws.weighted_sum([rs1, rs2, rs3, rs4, rs5])
#     # print(get_mse(rs, true_p_bank))
#     # print(rs)
#     print('time5', time.time() - time_start)
#     return [get_mse(rs1, true_p_bank), get_mse(rs2, true_p_bank), get_mse(rs3, true_p_bank), get_mse(rs4, true_p_bank),
#             get_mse(rs5, true_p_bank), get_mse(rs, true_p_bank)]
#
#     # 专利 百分数误差
#     # return [get_percentage(rs1, true_p_bank), get_percentage(rs2, true_p_bank), get_percentage(rs3, true_p_bank),
#     #         get_percentage(rs4, true_p_bank), get_percentage(rs5, true_p_bank), get_percentage(rs, true_p_bank)]


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


# 计算百分数化的误差
def get_percentage(estimation: List, true_p: List):
    length = len(estimation)
    rs = [0 for _ in range(length)]
    for i in range(len(rs)):
        rs[i] = abs(estimation[i] - true_p[i]) / true_p[i]
    return rs


# 计算mse
def get_mse(list1: List, list2: List):
    length = len(list1)
    mse = 0
    for i in range(length):
        mse += (list1[i] - list2[i]) * (list1[i] - list2[i])
    mse /= length
    return mse


if __name__ == '__main__':
    time1 = time.time()
    # data = Data("data/test.txt")
    # data = Data("./data/bank-additional-full.csv")
    data = Data("./data/e-shop clothing 2008.csv")


    print(data.true_p)
    data.show_data_information()
    # epsilon = 1
    # xn = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # xs = [10, 11, 12]
    # sue = SUE(epsilon, data.domain, data.data)
    # usue = USUE(epsilon, data.domain, data.data, xs, xn)
    # sue_mse = 0
    # usue_mse = 0
    # sue.run()
    # usue.run()
    # usue.estimate(usue.per_data)
    # for _ in range(100):
    #     sue_mse += get_mse(sue.es_data, data.true_p)
    #     usue_mse += get_mse(usue.es_data, data.true_p)
    # print(sue_mse, usue_mse)
    # if usue_mse < sue_mse:
    #     print('usue比较小')
    #     print(usue_mse/sue_mse)
    # exit()

    epsilon = 1
    xn = [1, 2, 3]
    xs = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    level_epsilon = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # krr = KRR(epsilon, data.domain, data.data)
    # krr.run()
    u_mse = 0
    ps_mse = 0
    ps_notdwsnotdr_mse = 0
    ps_notdws_mse = 0
    ps_notdr_mse = 0
    replication = 50

    # 这个参数表示输出哪个隐私级别的结果
    level_i =2
    for i in range(replication):
        u = UKRR(epsilon, data.domain, data.data, xs, xn)
        u.run()
        u.estimate(u.per_data)
        print(time.time()-time1)
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

    # print(ps_notdwsnotdr_mse, ps_mse, u_mse)
    print('u', u_mse)
    print('ps', ps_mse)
    print('ps_notdws', ps_notdws_mse)
    print('ps_notdr', ps_notdr_mse)
    print('ps_notdrnotdws', ps_notdwsnotdr_mse)

    print(time.time() - time1)

    plt.figure()
    # plt.plot(2, 1, color="firebrick", linestyle="-", marker='o', markerfacecolor='none', label="SR")
    # plt.plot(epsilon, 2, color="dodgerblue", linestyle="-", marker='*', label="PM")
    # plt.plot(epsilon, 3, color="orange", linestyle="--", marker='o', markerfacecolor='none', label="NCU-SR")
    # plt.plot(epsilon, 4, color="forestgreen", linestyle="--", marker='*', label="NCU-PM")
    # plt.plot(epsilon, MSE_sample, color="black", linestyle="-.", label="non-privacy")
    index = ['u', 'ps', 'ps_notdws', 'ps_notdr', 'ps_notdrnotdws']
    value = [u_mse, ps_mse, ps_notdws_mse, ps_notdr_mse, ps_notdwsnotdr_mse]
    plt.bar(index, value)
    xlabel = 'level ' + str(level_i)
    plt.xlabel(xlabel)
    plt.ylabel('MSE')
    plt.legend(loc="upper right")

    plt.show()
    ############################################################################################################################
    # time_start = time.time()
    # # bank数据集中的真实概率
    # true_p_bank = [0.025735651160532193, 0.09636301835486064, 0.25303486452364765, 0.2246770904146839,
    #                0.1637127318636496, 0.04175973584539186, 0.07099155093716616, 0.024618821015829854,
    #                0.03450033990482665, 0.02124405166553365, 0.008012042342429833, 0.03535010197144799]

    # # 计算mse
    # t = [0.0 for _ in range(6)]
    # for _ in range(10):
    #     temp = run_sue()
    #
    #     for i_main in range(len(temp)):
    #         t[i_main] += temp[i_main]
    # for i_main in range(len(t)):
    #     t[i_main] /= 10
    # print(t)

    # 计算百分数误差，用于专利
    # t = [[0 for _ in range(12)] for _ in range(6)]
    # for _ in range(10):
    #     temp = run_sue()
    #     for a in range(6):
    #         for b in range(12):
    #             t[a][b] += temp[a][b]
    # print(time.time() - time_start)
    # for a in range(6):
    #     for b in range(12):
    #         t[a][b] /= 10
    # print(time.time() - time_start)
    # for a in range(5):
    #     for b in range(12):
    #         if t[a][b] < t[a + 1][b]:
    #             print(a, b)
    #         if t[a][b] < t[5][b]:
    #             print('rs出错了', a, b)
    # print(time.time() - time_start)
    # for a in t:
    #     print(a)
