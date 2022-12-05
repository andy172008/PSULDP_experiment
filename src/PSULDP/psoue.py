import copy
from random import choice
import time

from ULDP.uoue import *


class PSOUE(object):
    def __init__(self, domain: list, data: list, xs: list, xn: list, level_epsilon: list):
        super(PSOUE, self).__init__()
        # 定义域
        self.domain = domain
        # 定义域的长度
        self.d = len(domain)
        # 总体数据
        self.data = data
        # 敏感数据定义域
        self.xs = xs
        # 非敏感数据定义域
        self.xn = xn
        # 多个隐私级别对应的隐私预算
        self.level_epsilon = level_epsilon
        # 隐私级别的个数
        self.h = len(level_epsilon)
        # 总用户数量
        self.n = len(data)

        # 不同隐私级别下的用户原始数据
        self.level_data = [[] for _ in range(self.h)]
        # 不同隐私级别下的扰动后数据
        self.level_per_data = []
        # 不同隐私级别下的用户数量
        self.level_n = []
        # 不同隐私级别下估计出的频率
        self.level_es_data = []

        for x in self.data:
            pos = choice(range(self.h))
            self.level_data[pos].append(x)
        for x in self.level_data:
            self.level_n.append(len(x))
        self.uldp = []
        for i in range(self.h):
            self.uldp.append(UOUE(level_epsilon[i], self.domain, self.level_data[i], self.xs, self.xn))

    def run(self, level_i):

        for i in range(self.h):
            # 这一步在不同的level下生成了扰动后数据
            self.uldp[i].run()
            # 将原始的扰动后数据记录下来，以便进行dr
            self.level_per_data.append(copy.deepcopy(self.uldp[i].per_data))

            # 在不同的level下进行估计
            self.uldp[i].estimate(self.uldp[i].per_data)
            self.level_es_data.append(copy.deepcopy(self.uldp[i].es_data))

        # 将没有经过dws和dr的数据储存一下
        self.notdws_notdr = copy.deepcopy(self.level_es_data)

        self.dws(level_i)

        self.notdr = copy.deepcopy(self.level_es_data)

        # 现在进行dr操作

        for level_j in range(level_i + 1, self.h + 1, 1):
            self.dr(level_i, level_j)
        self.level_n = []
        for x in self.level_per_data:
            self.level_n.append(len(x))

        self.level_es_data = []
        for i in range(self.h):
            self.uldp[i].es_data = []
            self.uldp[i].estimate(self.level_per_data[i])
            self.level_es_data.append(copy.deepcopy(self.uldp[i].es_data))
        self.notdws = copy.deepcopy(self.level_es_data)

        self.dws(level_i)


    def dws(self, t):
        omega_list = self.get_omega_list(t)
        for j in range(len(self.domain)):
            temp = 0
            for k in range(t - 1, -1, -1):
                temp += omega_list[k] * self.level_es_data[k][j]
            self.level_es_data[t-1][j] = temp

    # 返回一个长度为t的list
    def get_omega_list(self, t):
        rs = []
        cxs = 0
        for i in range(len(self.domain)):
            if self.domain[i] in self.xs:
                cxs += self.level_es_data[t - 1][i]
        cxs = 0.025735651160532193 + 0.2246770904146839 + 0.024618821015829854 + 0.02124405166553365
        sum = 0
        for j in range(t):
            p_j = self.uldp[j].p
            q_j = self.uldp[j].q
            z_j = self.uldp[j].z
            n_j = self.level_n[j]
            temp = cxs * ((1 - p_j - q_j) / (n_j * (p_j - q_j))) + len(self.xs) * (
                    (q_j * (1 - q_j)) / (n_j * (p_j - q_j) * (p_j - q_j))) + (1 - cxs) * ((1 - z_j) / (n_j * z_j))
            temp = 1 / temp
            rs.append(temp)
            sum += temp
        for j in range(t):
            rs[j] = rs[j] / sum
        return rs

    # 这里的level_i是指的隐私级别，从1开始计数的，所以在使用的时候要减1才能对应上list中的实际位置
    def dr(self, level_i, level_j):
        p_i = self.uldp[level_i - 1].p
        q_i = self.uldp[level_i - 1].q
        z_i = self.uldp[level_i - 1].z
        p_j = self.uldp[level_j - 1].p
        q_j = self.uldp[level_j - 1].q
        z_j = self.uldp[level_j - 1].z

        p = (p_i * (1 - q_j) - q_i * (1 - p_j)) / (p_j - q_j)
        q = (p_j * q_i - p_i * q_j) / (p_j - q_j)
        z = z_i / z_j

        for x in self.level_per_data[level_j - 1]:
            for i in range(self.d):
                if self.uldp[level_j - 1].isXs(i):
                    if x[i] == 1:
                        if np.random.uniform(0, 1) < p:
                            x[i] = 1
                        else:
                            x[i] = 0
                    else:
                        if np.random.uniform(0, 1) < q:
                            x[i] = 1
                        else:
                            x[i] = 0
                else:
                    if x[i] == 1:
                        if np.random.uniform(0, 1) < z:
                            x[i] = 1
                        else:
                            x[i] = 0
                    else:
                        x[i] = 0
            self.level_per_data[level_i - 1].append(x)
