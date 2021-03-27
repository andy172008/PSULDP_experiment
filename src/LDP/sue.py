from typing import List
import math
import numpy as np
from data_processing import Data


class SUE(object):
    def __init__(self, data: Data, epsilon: float):
        super(SUE, self).__init__()

        self.data = data
        self.epsilon = epsilon

        e_x2 = math.exp(self.epsilon / 2)
        self.p = e_x2 / (e_x2 + 1)
        self.q = 1 / (e_x2 + 1)
        self.z = (e_x2 - 1) / e_x2

    # 将x编码
    def encode(self, x: int) -> List:
        rs = [0 for _ in range(len(self.data.domain))]
        xpos = self.data.domain.index(x)
        rs[xpos] = 1
        return rs

    # 将编码之后的数据进行扰动
    def perturb(self, encode_x: List) -> List:
        for i in range(len(encode_x)):
            if encode_x[i] == 1:
                if np.random.uniform(0, 1) < self.p:
                    encode_x[i] = 1
                else:
                    encode_x[i] = 0
            else:
                if np.random.uniform(0, 1) < self.q:
                    encode_x[i] = 1
                else:
                    encode_x[i] = 0
        return encode_x

    # 以扰动之后的结果，对原始数据的频率分布进行估算
    # 请注意，这里输入的List中，存放的不是扰动后的频率值，而是扰动后的数量
    # n为当前隐私级别中数据大小
    def estimation(self, count_list: List, n: int) -> List:
        rs = [0 for _ in range(len(count_list))]
        e_x2 = math.exp(self.epsilon / 2)
        for i in range(len(count_list)):
            rs[i] = ((e_x2 + 1) * count_list[i] - n) / (n * (e_x2 - 1))
        return rs


class ULDPSUE(object):
    def __init__(self, data: Data, epsilon: float, xs: List, xn: List):
        super(ULDPSUE, self).__init__()
        self.data = data
        self.epsilon = epsilon

        e_x2 = math.exp(self.epsilon / 2)
        self.p = e_x2 / (e_x2 + 1)
        self.q = 1 / (e_x2 + 1)
        self.z = (e_x2 - 1) / e_x2
        self.xs = xs
        self.xn = xn

    def encode(self, x: int) -> List:
        rs = [0 for _ in range(len(self.data.domain))]
        xpos = self.data.domain.index(x)
        rs[xpos] = 1
        return rs

    def isXs(self, i: int):
        if self.data.domain[i] in self.xs:
            return True
        else:
            return False

    # 将编码之后的数据进行扰动
    def perturb(self, encode_x: List) -> List:
        for i in range(len(encode_x)):
            if self.isXs(i):
                if encode_x[i] == 1:
                    if np.random.uniform(0, 1) < self.p:
                        # encode_x[i] = 1
                        pass
                    else:
                        encode_x[i] = 0
                else:
                    if np.random.uniform(0, 1) < self.q:
                        encode_x[i] = 1
                    else:
                        # encode_x[i] = 0
                        pass
            # 当前元素属于Xn
            else:
                if encode_x[i] == 1:
                    if np.random.uniform(0, 1) < self.z:
                        # encode_x[i] = 1
                        pass
                    else:
                        encode_x[i] = 0
                else:
                    # encode_x[i] = 0
                    pass
        return encode_x

    # 以扰动之后的结果，对原始数据的频率分布进行估算
    # 请注意，这里输入的List中，存放的不是扰动后的频率值，而是扰动后的数量
    # n为当前隐私级别中数据大小
    def estimation(self, count_list: List, n: int) -> List:
        rs = [0 for _ in range(len(count_list))]

        e_x2 = math.exp(self.epsilon / 2)
        for i in range(len(count_list)):
            if self.isXs(i):
                rs[i] = ((e_x2 + 1) * count_list[i] - n) / (n * (e_x2 - 1))
            else:
                rs[i] = (e_x2 * count_list[i]) / (n * (e_x2 - 1))
        return rs
