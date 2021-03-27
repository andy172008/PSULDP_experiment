# 这个文件负责数据加权组合算法，
from numpy import *
from typing import List
from data_processing import Data


class DWS(object):
    def __init__(self, data: Data, h: int, epsilon_list: List, xs: List, xn: List, n_list: List, fxn: float):
        super(DWS, self).__init__()
        self.data = data
        # h为隐私级别数目，h>=1
        self.h = h
        self.epsilon_list = epsilon_list
        self.n_list = n_list
        self.xs = xs
        self.xn = xn
        self.w_list = [0 for _ in range(h)]
        self.fxn = fxn

    # 计算w，t为当前隐私级别
    def getw(self):
        num = 0
        for i in range(self.h):
            e_x2 = math.exp(self.epsilon_list[i] / 2)
            self.w_list[i] = (self.n_list[i] * (e_x2 - 1) * (e_x2 - 1)) / (len(self.xs) * e_x2 + self.fxn * (e_x2 - 1))
            num += self.w_list[i]
        for i in range(self.h):
            self.w_list[i] /= num

    # 依照算出的w，对结果进行加权组合
    def weighted_sum(self, estimation_p: List):
        if len(estimation_p) != self.h:
            print('出现错误，数目不等于h')
        rs = [0 for _ in range(len(self.data.domain))]
        for t in range(self.h):
            for i in range(len(rs)):
                rs[i] += self.w_list[t]*estimation_p[t][i]

        return rs
