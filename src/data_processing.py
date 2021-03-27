# @AUTHOR : SX1916085 贺星宇
# @TIME   : 2020.11.4
import time
from collections import Counter


class Data(object):

    def __init__(self, url_address):
        super(Data, self).__init__()
        time1 = time.time()
        # 储存文件地址
        self.urlAddress = ''
        # 储存所有特征，即定义域D
        self.domain = []
        # 储存数据的真实频率
        self.true_p = []
        # 记录共有多少条数据
        self.dataNum = 0
        # 储存所有数据
        self.data = []

        self.urlAddress = url_address

        self.data_statistics()
        time2 = time.time()
        print('数据已载入内存，共用时：')
        print(time2 - time1)
        print()
        # self.show_data_information()

    # 对所有数据做一个简要的统计
    def data_statistics(self):
        with open(self.urlAddress, 'r') as f:

            for line in f.readlines():

                # 移除头尾换行符
                line = line.strip()
                # 将一行中的数字划分开
                linelist = line.split(' ')

                # 检查字符串是否由数字构成
                # for i in linelist:
                #     if not i.isnumeric():
                #         print('error:Non-digital data appears in the data')
                #         print(num, line)
                linelist = [int(x) for x in linelist]
                for x in linelist:
                    self.data.append(x)
        count = Counter(self.data)
        count_dict = dict(count)
        for x in count_dict:
            self.domain.append(x)
        self.domain.sort()

        self.dataNum = len(self.data)

        for x in self.domain:
            self.true_p.append(count_dict.get(x, 0) / self.dataNum)

    # 展示统计出的信息
    def show_data_information(self):
        feature_type = len(self.domain)
        print('共有数据%d条' % self.dataNum)
        print('属性种类共有%d个' % feature_type)
        for i in range(feature_type):
            print('第%d种属性，为%d' % (i + 1, self.domain[i]))
