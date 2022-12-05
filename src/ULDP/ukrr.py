import numpy as np
from random import choice
from collections import Counter
import xxhash



class UKRR(object):
    def __init__(self, epsilon: float, domain: list, data: list, xs: list, xn: list):
        super(UKRR, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
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
        # 扰动后数据
        self.per_data = []
        # 总用户数量
        self.n = len(data)
        # 估计出的频率
        self.es_data = []

        e_epsilon = np.exp(self.epsilon)
        xs_len = len(self.xs)

        self.p = e_epsilon / (e_epsilon + xs_len - 1)
        self.q = 1 / (e_epsilon + xs_len - 1)
        self.z = (e_epsilon - 1) / (e_epsilon + xs_len - 1)

    # 为了与psuldp结合，这里的run不包含估计过程
    def run(self):
        for x in self.data:
            self.per_data.append(self.perturb(self.encode(x)))

    # 此时传入的是用户的原始数据，并不是该数据在domain中的位置
    def encode(self, x: int) -> int:
        return x

    # 返回的是扰动后的数据，并不是在domain中的
    def perturb(self, x: int) -> int:
        if x in self.xs:
            if np.random.uniform() < self.p:
                return x
            else:
                per_x = choice(self.xs)
                while per_x == x:
                    per_x = choice(self.xs)
                return per_x
        else:
            if np.random.uniform() < self.z:
                return x
            else:
                per_x = choice(self.xs)
                return per_x

    def estimate(self, per_data: list):
        count = Counter(per_data)
        count_dict = dict(count)
        self.n = len(per_data)

        for x in self.domain:
            if x in self.xs:
                x_count = count_dict.get(x, 0)
                self.es_data.append((x_count - self.n * self.q) / (self.n * (self.p - self.q)))
            else:
                x_count = count_dict.get(x, 0)
                self.es_data.append(x_count / (self.n * self.z))
