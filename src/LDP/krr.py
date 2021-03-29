import numpy as np
from random import choice
from collections import Counter


class KRR(object):
    def __init__(self, epsilon: float, domain: list, data: list):
        super(KRR, self).__init__()
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
        # 总用户数量
        self.n = len(data)
        # 估计出的频率
        self.es_data = []

        e_epsilon = np.exp(self.epsilon)

        self.p = e_epsilon / (e_epsilon + self.d - 1)
        self.q = 1 / (e_epsilon + self.d - 1)

    def run(self):
        for x in self.data:
            self.per_data.append(self.perturb(self.encode(x)))
        self.estimate(self.per_data)


    # 此时传入的是用户的原始数据，并不是该数据在domain中的位置
    def encode(self, x: int) -> int:
        return x

    # 返回的是扰动后的数据，并不是在domain中的
    def perturb(self, x: int) -> int:
        if np.random.uniform(0, 1) < self.p:
            return x
        else:
            per_x = choice(self.domain)
            while per_x == x:
                per_x = choice(self.domain)
            return per_x

    def estimate(self, per_data: list):
        count = Counter(per_data)
        count_dict = dict(count)

        for x in self.domain:
            x_count = count_dict.get(x, 0)
            self.es_data.append((x_count - self.n * self.q) / (self.n * (self.p - self.q)))
