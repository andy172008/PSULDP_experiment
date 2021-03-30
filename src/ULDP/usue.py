from typing import List
import numpy as np


class USUE(object):
    def __init__(self, epsilon: float, domain: list, data: list, xs: list, xn: list):
        super(USUE, self).__init__()
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
        # 敏感数据定义域
        self.xs = xs
        # 非敏感数据定义域
        self.xn = xn

        e_x2 = np.exp(self.epsilon / 2)
        self.p = e_x2 / (e_x2 + 1)
        self.q = 1 / (e_x2 + 1)
        self.z = (e_x2 - 1) / e_x2

    def run(self):
        for x in self.data:
            self.per_data.append(self.perturb(self.encode(x)))

    def encode(self, x: int) -> List:
        rs = [0 for _ in range(self.d)]
        xpos = self.domain.index(x)
        rs[xpos] = 1
        return rs

    def isXs(self, i: int):
        if self.domain[i] in self.xs:
            return True
        else:
            return False

    # 将编码之后的数据进行扰动
    def perturb(self, x: list) -> List:
        for i in range(self.d):
            # 当前元素属于XS
            if self.isXs(i):
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
            # 当前元素属于XN
            else:
                if x[i] == 1:
                    if np.random.uniform(0, 1) < self.z:
                        x[i] = 1
                    else:
                        x[i] = 0
                else:
                    x[i] = 0
                    pass
        return x

    # 以扰动之后的结果，对原始数据的频率分布进行估算
    # 请注意，这里输入的List中，存放的不是扰动后的频率值，而是扰动后的数量
    # n为当前隐私级别中数据大小
    def estimate(self, per_data: list):
        count = [0 for _ in range(self.d)]
        count = np.array(count)
        for x in per_data:
            x_arr = np.array(x)
            count = count + x_arr
        count = count.tolist()
        # 这是因为使用DR之后，数据总量可能会发生变化
        self.n = len(per_data)
        for i in range(self.d):
            if self.isXs(i):
                self.es_data.append((count[i] - self.n * self.q) / (self.n * (self.p - self.q)))
            else:
                self.es_data.append(count[i] / (self.n * self.z))
