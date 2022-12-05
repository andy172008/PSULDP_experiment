import time

import numpy as np
from random import choice
import xxhash
from collections import Counter


class OLH(object):
    def __init__(self, epsilon: float, domain: list, data: list):
        super(OLH, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 定义域
        self.domain = domain
        # 定义域的长度
        self.d = len(domain)
        # 哈希之后定义域的长度
        self.g = 0
        # 总体数据
        self.data = data
        # 扰动后数据
        self.per_data = []
        # 总用户数量
        self.n = len(data)
        # 估计出的频率
        self.es_data = []

        self.g = int(np.exp(self.epsilon) + 1)
        # self.g = 4
        e_epsilon = np.exp(self.epsilon)
        self.p = e_epsilon / (e_epsilon + self.g - 1)
        self.q = 1 / (e_epsilon + self.g - 1)

    def run(self):
        for i in range(len(self.data)):
            a = self.encode(self.data[i], i)
            b = self.perturb(a)
            self.per_data.append(b)
        self.estimate(self.per_data)
        return self.es_data

        # self.estimate(self.per_data)

    # x此时传入的是用户的原始数据，并不是该数据在domain中的位置
    # pos为用户原始数据在原始数据集合中的位置，也是哈希函数的种子
    def encode(self, x: int, pos: int) -> int:
        # x被哈希到0到g-1中的一个数字
        rs = xxhash.xxh32(str(x), seed=pos).intdigest() % self.g
        # 返回的值是1到g中的一个
        return (rs + 1)

    # 返回的是扰动后的数据，并不是在domain中的
    def perturb(self, x: int) -> int:
        if np.random.uniform(0, 1) < self.p:
            return x
        else:

            per_x = choice(range(1, self.g + 1))
            while per_x == x:
                per_x = choice(range(1, self.g + 1))
            return per_x

    def estimate(self, per_data: list):
        count = Counter(per_data)
        count_dict = dict(count)

        temp111 = 0
        for x in self.domain:
            # time1 = time.time()
            count = 0
            for i in range(len(self.per_data)):
                temp = xxhash.xxh32(str(x), seed=i).intdigest() % self.g
                temp+=1
                if temp == self.per_data[i]:
                    count+=1
            self.es_data.append((count - self.n * self.q) / (self.n * (self.p - self.q)))
            temp111 += count
            # print('olh',time.time()-time1)
        print('temp111',temp111)