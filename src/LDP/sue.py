from typing import List
import numpy as np
from data_processing import Data


class SUE(object):
    def __init__(self, epsilon: float, domain: list, data: list ):
        super(SUE, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 定义域
        self.domain = domain
        # 定义域的长度
        self.d = len(domain)
        # 总体数据
        self.data = data
        # 扰动后数据
        self.per_data = []
        # 总用户数据
        self.n = len(data)
        # 估计出的频率
        self.es_data = []

        e_x2 = np.exp(self.epsilon / 2)
        self.p = e_x2 / (e_x2 + 1)
        self.q = 1 / (e_x2 + 1)

    def run(self):
        for x in self.data:
            self.per_data.append(self.perturb(self.encode(x)))
        self.estimation(self.per_data)

    # 将x编码
    def encode(self, x: int) -> List:
        rs = [0 for _ in range(self.d)]
        xpos = self.domain.index(x)
        rs[xpos] = 1
        return rs

    # 将编码之后的数据进行扰动
    def perturb(self, x: list) -> List:
        for i in range(self.d):
            if x[i] == 1:
                if np.random.uniform(0, 1) < self.p:
                    x[i] = 1
                else:
                    x[i] = 0
            else:
                if np.random.uniform(0, 1) < self.q:
                    x[i] = 1
                else:
                    x[i] = 0
        return x

    # 以扰动之后的结果，对原始数据的频率分布进行估算
    # 请注意，这里输入的List中，存放的不是扰动后的频率值，而是扰动后的数量
    # 这里的per_data,是将所有的用户扰动数据对位相加得到的
    def estimation(self, per_data: List):
        count = [0 for _ in range(self.d)]
        for x in per_data:
            count = np.sum([x,count],axis=0)

        for i in range(self.d):
            self.es_data.append((count[i] - self.n * self.q) / (self.n * (self.p - self.q)))


